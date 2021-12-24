from service import pdf_service
from tkinter import Tk,Text,Scrollbar,Button,END,Entry,Frame,filedialog,Label,messagebox,\
                    Listbox,Menubutton,Menu,\
                    StringVar, IntVar, BooleanVar, LabelFrame, Checkbutton
from tkinter.constants import FLAT, SUNKEN
from app import writelog, showinfo, showdir, Context
from .utils import show_info, select_directory

pdf_svc = pdf_service()
context = Context()

class Window(LabelFrame):

   def __init__(self, parent):
      super().__init__(parent.tabControl)
      self._initialize()
      self._build()      
      
   def _initialize(self):
      self.id='건강/연금'
      
   def _build(self):
          
      def _click():
         v=c.get()
         c.set(not v)
         context.put(html= not v)
             
      lf = LabelFrame(self, relief='flat')
            
      #1행 작성
      c = BooleanVar()
      label = Label(lf,text='html작성', width=13)
      label.bind('<Button-1>', lambda e: _click())
      checkbutton = Checkbutton(lf, variable=c, relief='flat',command=lambda: context.put(html=c.get()))
      label.grid(row=0, column=0)
      checkbutton.grid(row=0, column=1, sticky='w')
      
      #2행 작성
      label = Label(lf,text='파일생성', width=13)
      button = Button(lf, text='건강/연금', width=10, command=self.care)
      label.grid(row=1, column=0)
      button.grid(row=1, column=1, columnspan=3)
      
      lf.pack(side='top', fill='both', expand=True)
      lf.focus()
      # button.configure(relief=SUNKEN)
      
      # self.config(bg='cornflower blue')
       
   def care(self):
      dir_path = select_directory()
      if not dir_path: return
      
      showdir(dir_path)
      
      # html변환여부 체크옵션
      _html = context.get('html')

      try:
         cnt = pdf_svc.convert(dir_path, _html)
         if not cnt:
            show_info("작업대상이 없습니다.")
            return
         show_info('작업이 완료되었습니다')
         
      except Exception as e:
         show_info(e,'err')
