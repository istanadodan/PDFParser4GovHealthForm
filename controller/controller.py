import os, glob,datetime
import pandas as pd
from .unit_manage import Unit_Manage
from app import SH_NAME

class Controller:
   d = {}
   err={}

   def __init__(self):
      self.mng = Unit_Manage()
   
   def _initialize(self):
      # 클래스에러변수 초기화
      self.err.clear()
      
   def view(self, view):
      self.view = view

   def model(self, model):
      self.model = model
      self.mng.model(model)

   def printend(func):
      def wrapper(self,*args,**kwargs):
         self.view.printout("{:^64s}\n".format("-"*64))
         
         r = func(self,*args,**kwargs)
         
         self.view.printout("{:^64s}\n".format("-"*64))
         self.view.printout("{:^64s}\n".format("<<complete>>"))
         return r
      return wrapper

   def get_result(self):
      return self.result

   def _to_html(self, pdf_file):
      _fullpath = os.path.splitext(pdf_file)[0]+'.html'
      with open(_fullpath, 'w',encoding='utf-8') as fs:
         fs.write(self.mng.html())

   def convert(self, _pdf_dir, _html=False, _unit_list=None, _gid=None):
      print(_pdf_dir)
      # 타입체크용으로 인수값 변환
      _type = int(_gid) -1 if _gid is not None else _gid

      # 컨트롤러내 에러변수등을 초기화
      self._initialize()

      # 관리클래스 초기화
      self.mng.init()

      for pdf_file in glob.glob( _pdf_dir+"/*.pdf" ):
         print(os.path.basename(pdf_file))

         self.mng.file(pdf_file)
         self.mng.set_unit_list(_unit_list)
         # group id를 축출하고 인수값과 비교한다.
         # 인수값이 None이면 모든 파일에 대해 축출작업진행
         if not self.mng.check_type(_type):
            continue

         # 선택된 작업을 가져와 변환작업수행, 결과는 클래스변수에 저장
         for id in self.mng.unit_list():
            unit = self.mng.create_unit(id)
            unit.execute()
         
         self.mng.update_result()
         self.mng.clear()

         #html파일작성여부는 옵션
         if _html:
            self._to_html(pdf_file)
      
      self._to_excel(_pdf_dir)
   
   def _to_excel(self, path):

      for gid, _result in self.mng.result.items():
         # 엑셀시트명을 인수에 따라 설정파일에서 가져온다. 
         _sheet_name = SH_NAME(int(gid)+1)      
         _sn = datetime.date.today().strftime('%y-%m-%d')
         # header = pd.MultiIndex(levels=[['건강보험료','장기요양보험료','납부할보험료','사업장'],
         #                                ['산출보험료','정산보험료','가입자보험료','연체금','납부할보험료','고지년월 차수','사업장관리번호']],
         #                        labels=[[0,0,0,0,1,1,1,1,2,3,3],[0,1,2,3,0,1,2,3,4,5,6]],
         #                        names=['item','account'])
         dest_dir = os.path.join(path, "{0}_{1}_.xlsx".format(_sheet_name,_sn))
         reform = {(outerKey, innerKey): values for outerKey, innerDict in _result.items() for innerKey, values in innerDict.items()}
      
         # from collections import OrderedDict
         # t_dict = OrderedDict()
         # keys = list(reform.keys())
         # t_dict[tuple(keys[-1])] = reform[keys[-1]]
         # for k in keys[:-1]:
         #    t_dict[tuple(k)] = reform[k]
      
         try:
            df = pd.DataFrame(reform)
            self._arrange(df)
            df.to_excel(dest_dir, sheet_name=_sheet_name, na_rep='',header=True,startrow=1,startcol=0)

         except Exception as e:
            print('---------error----------')
            print(reform)
            print(e)

   def _arrange(self, df):
         df.index += 1 #인덱스 1부터 시작.
         # cols = df.columns[-1] + df.columns[:-1]
         # df.columns = cols

