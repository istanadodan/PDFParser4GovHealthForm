from service import pdf_service, telegram_service
from tkinter import Tk,Text,Scrollbar,Button,END,Entry,Frame,filedialog,Label,messagebox,\
                    Listbox,Menubutton,Menu,\
                    StringVar, IntVar, LabelFrame
from app import appcontext as context, showdir
from .utils import show_info, select_directory
telegram_svc = telegram_service()

class Window(Frame):

   def __init__(self, parent):
      super().__init__(parent.tabControl)      
      self._initialize()
      self._build()
   
   def _initialize(self):
      self.id='원천세신고'
      
   def _build(self):      
      
      lf = LabelFrame(self)
      lf.pack(side='top', fill='both', expand=True)
      
      label = Label(lf,text='파일생성', width=13, relief='flat')
      button = Button(lf, text='원천세신고', width=10, command=self.tax)
      label.grid(row=0, column=0)
      button.grid(row=0, column=1, sticky='w')
      
      lf.focus()
      # self.config(bg='cornflower blue', padx=45,pady=15)

   def tax(self):
      dir_path = select_directory()
      if not dir_path: return
      
      showdir(dir_path)
      
      try:
         cnt = telegram_svc.convert(dir_path)         
         if not cnt:
            show_info("작업대상이 없습니다.")
            return
         show_info('작업이 완료되었습니다')
         
      except Exception as e:
         show_info(e, 'err') 
   