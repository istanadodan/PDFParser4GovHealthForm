import os, glob,datetime
import pandas as pd
from .unit_manage import Unit_Manage
from app import SH_NAME, GROUP1, GROUP2, writelog, showinfo

class Service:

   def __init__(self):
      self.mng = Unit_Manage()

   def get_result(self):
      return self.result

   def _to_html(self, pdf_file):
      _fullpath = os.path.splitext(pdf_file)[0]+'.html'
      with open(_fullpath, 'w',encoding='utf-8') as fs:
         fs.write(self.mng.html())

   # unit목록을 반환한다.
   def _getUnitList(self, _unit_list):          
      if _unit_list:
         return _unit_list

      found_keyword = self.mng.get_check_keyword()
      if '건강' in found_keyword:
         self.mng.doc_type(0)
         return GROUP1
      if '연금' in found_keyword:
         self.mng.doc_type(1)      
         return GROUP2
      
      return None    
         
   def convert(self, _pdf_dir, _html=False, _unit_list=None):
      # 상태바 초기화
      showinfo('')
      
      folder_generator  = glob.glob( _pdf_dir+"/*.pdf" )
      # 1. 대상존재여부 체크
      cnt = sum(1 for x in folder_generator)
      if not cnt:
         return 0          

      # 관리클래스 변수초기화
      self.mng.initialize()

      for no, pdf_file in enumerate(folder_generator):
         writelog("작업개시: [%2d]%s",(no+1,os.path.basename(pdf_file)))
               
         # 2. 파일로드
         self.mng.file(pdf_file)       
         
         # 3. 건강 혹은 연금용 파일인지 체크
         unit_list = self._getUnitList(_unit_list) 
         writelog('선택 유닛: %s', unit_list)
         if unit_list is None: pass
         
         # 4. 가져올 항목취득객체를 받아 실행
         for id in unit_list:
            writelog('항목취득객체ID: %s', id, 'dev')
            unit = self.mng.create_unit(id)            
            unit.execute()
            
         self.mng.update_result()
         self.mng.clear()
         
         #5. html파일작성여부는 옵션
         if _html:
            self._to_html(pdf_file)
         
         writelog("작업완료: [%2d]%s",(no+1,os.path.basename(pdf_file)))

      writelog('[결과] %s', self.mng.result,'dev')

      #6. 엑셀파일작성      
      self._to_excel_(_pdf_dir)
      
      return cnt
   
   def _to_excel_(self, path):
      writelog("<<엑셀파일 작성개시>>")
      
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
      
         df = pd.DataFrame(reform)
         self._arrange(df)
         df.to_excel(dest_dir, sheet_name=_sheet_name, na_rep='',header=True,startrow=1,startcol=0)
            
      writelog("<<엑셀파일 작성완료>>")

   def _arrange(self, df):
         df.index += 1 #인덱스 1부터 시작.
         # cols = df.columns[-1] + df.columns[:-1]
         # df.columns = cols

   def printend(func):
      def wrapper(self,*args,**kwargs):
         writelog("{:^64s}\n".format("-"*64))
         
         r = func(self,*args,**kwargs)
         
         writelog("{:^64s}\n".format("-"*64))
         writelog("{:^64s}\n".format("<<complete>>"))
         return r
      return wrapper