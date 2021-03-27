import io, re
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import HTMLConverter
from bs4 import BeautifulSoup as soup, NavigableString, Tag

class Model:

   def __init__(self):
      self.initialize()
   
   def initialize(self):
        self.body=''
        self.html=''

   def to_html(self, pdf_path):
      rsrcmgr = PDFResourceManager()
      retstr = io.BytesIO()
      codec = 'utf-8'
      laparams = LAParams()
      device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
      interpreter = PDFPageInterpreter(rsrcmgr, device)
      password = ""
      maxpages = 0 #is for all
      caching = True
      pagenos=set()
      try:
         with open(pdf_path, 'rb') as fp:
               for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
                  interpreter.process_page(page)
      except Exception:
         print("[ERR] file path=",pdf_path)

      device.close()
      report = retstr.getvalue()
      retstr.close()
      self.html = report.decode('utf-8')
      chtml = self._replace(self.html)
      self.body = soup(chtml, 'html.parser')
   
   def find_all(self,tag,text,recursive):
      return self.body.find_all(tag,text=text,recursive=recursive)

   def _replace(self, info):
      pattern = '(style=".*?")|(\\n)'
      t1 = re.sub(pattern,'',info)
      t2 = re.sub('\<br\/?\>',';',t1)
      return t2
   
   def extract(self, tags, keyword, nth):
      ct = 0
      _basket = ''

      _tag = [tag for tag in tags if keyword in tag.text][0]
      
      while True:
         
         if _tag and \
               not isinstance(_tag, NavigableString) and \
               ct == nth:
               rst =''
               for e in _tag.contents:
                  r = e.text if isinstance(e,Tag) else e
                  if r:
                     rst += r + ';'
                     
               _basket = rst[:-1].split(';')
               break
         
         _tag = _tag.next_sibling
         # print(_tag)
         # print(type(_tag))
         ct += 1

      return _basket
         
      
