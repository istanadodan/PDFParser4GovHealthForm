from tkinter import Tk,Text,Scrollbar,Button,END,Entry,Frame,filedialog,Label,messagebox,\
                    Listbox,Menubutton,Menu,\
                    StringVar, IntVar

class Window1(Frame):

   def __init__(self, parent, context):
      super().__init__(parent.Frame)
      context.add_observer(self)
      self.controller = parent.controller
      self.parent = parent
      self.context = context
      self._initialize()

      self.show()
   
   def _initialize(self):
      self.id='menu'
      
   def show(self):
      b0 = Button(self, text='자동분류', width=40, height=5, command=self.auto_classify)
      b1 = Button(self, text='건강보험', width=20, height=3, command=lambda:self.menu(1))
      b2 = Button(self, text='국민연금', width=20, height=3, command=lambda:self.menu(2))
      b0.pack(side="top",fill='both', expand=True, pady=15)
      b1.pack(side="left",fill='x')
      b2.pack(side="left",fill='x')
      self.config(bg='cornflower blue', padx=45,pady=15)

   def menu(self, selector):
      msg = self._createMsg(id=self.id, g_id=selector)
      self.context.notify_all(msg)
   
   def _createMsg(self, id, g_id):
      return dict(gid=g_id, id=id)
      
   def auto_classify(self):
      
      working_dir = self.context.get('directory')
      if not working_dir:
         self.context.directory()
         working_dir = self.context.get('directory')
         if not working_dir:
            messagebox.showwarning("경고",'작업디렉토리가 설정되어 있지 않습니다.')
            return
      
      # html변환여부 체크옵션
      _html = self.context.get('html')

      try:
         self.controller.convert(working_dir, _html)
         
         self.context.notify('root','info',"작업완료")   
         messagebox.showinfo("알림",message="작업이 완료되었습니다.")
         
      except Exception as e:
         print(e)
         messagebox.showerror('포맷오류','잘못된 포맷을 적용하였습니다.')
         self.context.notify('root','info',"작업오류")

   def update(self,msg):
      pass