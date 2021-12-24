import os, glob,datetime
import pandas as pd
from model import TextModel
from app import SH_NAME, writelog, showinfo
from .telegram_vo import Body, Header

class Service:
   err={}

   def __init__(self):
      pass
   
   def _initialize(self):
      # 클래스에러변수 초기화
      self.err.clear()
      
   def view(self, view):
      self.view = view

   def get_result(self):  
      return self.result

   def convert(self, _file_dir):
      showinfo('')
      
      folder_generator  = glob.glob( _file_dir+"/*.txt" )
      cnt = sum(1 for x in folder_generator)
      if not cnt:
         return 0
           
      # 컨트롤러내 에러변수등을 초기화
      self._initialize()

      result = {}
      for telegram in folder_generator:
         writelog("%s 개시>>", os.path.basename(telegram))

         #파일명 추가
         _result = {'파일명':{'filename':[os.path.basename(telegram)]}}
         
         with open(telegram, 'r', encoding='euc-kr') as f:
            first_line = f.readline()
            header = Header(first_line)     
            _result.update(header.to_map())
            
            # print(header.to_map())                   
            body = Body(f)
            _result.update(body.to_map())
         
         if not result:
            result = _result
         else:
            for key, sub in result.items():
               for subkey, item in sub.items():
                  result[key][subkey] += _result[key][subkey]
         
         writelog("%s 완료>>", os.path.basename(telegram))
                      
      self._to_excel(result, _file_dir)
      
      return cnt
               
      
   def _to_excel(self, result, path):

      writelog("<<엑셀파일 작성개시>>")
      SHEET_NAME = '원천세신고'
      _sn = datetime.date.today().strftime('%y-%m-%d')

      dest_dir = os.path.join(path, "{0}_{1}_.xlsx".format(SHEET_NAME,_sn))
      reform = {(outerKey, innerKey): item for outerKey, items in result.items() for innerKey, item in items.items()}

      df = pd.DataFrame(reform)
      df.to_excel(dest_dir, sheet_name=SHEET_NAME, na_rep='',header=True,startrow=1,startcol=0)
      
      writelog("<<엑셀파일 작성완료>>")       