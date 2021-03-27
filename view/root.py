import os
from tkinter import Tk,Text,Scrollbar,Button,END,Entry,Frame,filedialog,Label,messagebox,\
                    Listbox,Menubutton,Menu,Checkbutton, \
                    StringVar, IntVar, BooleanVar

class Root(Tk):
   _frames = {}
   _working_directory=''
   _queue='menu'
   Frame = ''
   def __init__(self,context):
      super().__init__()
      self.context = context
      self._initialize()
      context.add_observer(self)
      
      self.build()

   def _initialize(self):
      self.id='root'
      self.title("업무지원툴 v1.1 2020.06.28")
      self.geometry("360x300+%d+%d"%(self.centering()))
      self.config(bg='dark sea green')

   def controller(self, controller):
      self.controller = controller
   
   def centering(self):
      self.update_idletasks()
      x = (self.winfo_screenwidth() - self.winfo_width())/3
      y = (self.winfo_screenheight() - self.winfo_height())/3
      return x,y

   def add(self,frame):
      self._frames[frame.id] = frame

   def active(self):
      self._frames[self._queue].pack(fill='both',expand=True)

   def deactive(self):
      self._frames[self._queue].pack_forget()

   def activate(self):
      self.context.notify_all({'id':'task', 'gid':1})
   
   def build(self):
      menubar = self.menubar()
      statusbar = self.statusbar()
      content = Frame(self,bg='LightCyan4', pady=1,padx=3)
      
      menubar.pack(side='top',fill='x')
      content.pack(side='top',fill='both',expand=True)
      statusbar.pack(side='bottom', anchor='sw', fill='x')
      
      self.Frame = content

   def menubar(self):
      menubar = Frame(self)
      mb1 = Menubutton(menubar,text='setup', width='10', relief='raised')
      mb1.menu = Menu(mb1,tearoff=0)
      mb1['menu'] = mb1.menu
      mb1.menu.add_command(label='directory',command=self.context.directory)
      mb1.menu.add_command(label='menu',command=self.menu)
      mb1.menu.add_command(label='exit',command=self.destroy)
      mb1.pack(side='left')
      
      c = BooleanVar()
      ckl1 = Label(menubar,text='html',relief='flat')
      ckb1 = Checkbutton(menubar, variable=c, relief='flat',command=lambda: self.context.put(html=c.get()))
      ckb1.pack(side='right')
      ckl1.pack(side='right')

      return menubar

   def menu(self):
      msg = self._createMsg(id='task')
      self.context.notify_all(msg)
   
   def _createMsg(self,id, gid=None):
      msg = dict()
      msg['id'] = id
      msg['gid'] = gid
      return msg

   def statusbar(self):
      fr_bot = Frame(self)
      self.info = StringVar()
      lb1 = Label(fr_bot,textvariable=self.info, height='2')
      lb1.pack(fill='x', expand=True, anchor='w')
   
      return fr_bot

   def clear_statusbar(self):
      self.info.set('')

   #change task page
   def update(self,msg):
      caller = msg['id']
      self._queue = caller
      self.deactive()

      _receivers = [f for f in self._frames.keys() if f!=caller]
      self._queue = _receivers[0]
      # self._queue = 'task' sif self._queue=='menu' else 'menu'
      self.active()

      self.clear_statusbar()
   
   def call(self, func, msg):
      if func=='info':
         self.info.set(msg)