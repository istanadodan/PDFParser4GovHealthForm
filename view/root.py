from tkinter import LabelFrame, Tk,Text,Scrollbar,Button,END,Entry,Frame,filedialog,Label,messagebox,\
                    Listbox,Menubutton,Menu,Checkbutton, \
                    StringVar, IntVar, BooleanVar, scrolledtext, ttk, WORD
from tkinter.constants import FLAT, INSERT
from app import Context
context = Context()

class Root(Tk):
   _frames={}
   _commands={}
   # _working_directory=''
   # _queue=''
   tabControl=''
   def __init__(self):
      super().__init__()
      context.add_observer(self)
      self._register_commands()
      self._initialize()

   def _initialize(self):
      def _centering():
         self.update_idletasks()
         x = (self.winfo_screenwidth() - 400)/2
         y = (self.winfo_screenheight() - 600)/2
         return x,y
      
      self.id='root'
      self.title("업무지원툴 v1.3 2021.11.27")
      self.geometry("400x600+%d+%d"%(_centering()))
      self.config(bg='silver')
      self.resizable(True, True)
       
      self.tabControl = ttk.Notebook(self, height=120, width=50)      
      # self.tabControl.configure(width=30)
      '''
      nw => above (north) and toe the left (west)
      ne => above and to the right (east)
      en => to the right (east), at the top
      es => to the right (east), at the bottom
      se => below (south) and to the right (east)
      sw => below (south) and to the left (west)
      ws => to the left (west) and to the bottom (south)
      wn => to the left (west) and at top
      '''
      style = ttk.Style()
      style.configure('Tab', focuscolor=style.configure('.')['background'])  
      style.configure('TNotebook', tabposition='wn') 
      style.configure('TNotebook.Tab', padding=[4,4])
      style.configure('.', relief='flat')       

   def add(self,frame):
      self._frames[frame.id] = frame

   # # 위젯 표시하기
   # def active(self):
   #    self._frames[self._queue].pack(fill='both',expand=True)

   # # 위젯 감추기
   # def deactive(self):
   #    if self._queue:
   #       self._frames[self._queue].pack_forget()

   def build(self):
      menubar = self.menubar()      
      menubar.pack(side='top',pady=2, fill='x')
      
      statusbar = self.statusbar()      
      statusbar.pack(side='bottom', pady=1, anchor='sw', fill='x')
      
      #탭에 등록된 윈도우 객체들을 삽입한다.
      for id, mnu in self._frames.items():         
         self.tabControl.add(mnu, text=id)
         
      self.tabControl.pack(side='top', pady=0, fill='both')
      self.tabControl.configure(width=60)
      
      #작업디렉토리 표시라인
      lfworkingdir = LabelFrame(self, text='작업디렉토리', relief=FLAT)
      # ttk.Label(lfworkingdir, text='<위치> ').pack(side='top') 
      self.dir_ = StringVar()
      lb_dir = ttk.Label(lfworkingdir, textvariable=self.dir_)
      lb_dir.pack(side='top', expand=1, fill='both') 
      lfworkingdir.pack(side='top', expand=1, fill='both')
      
      #작업로그 프레임
      lf = ttk.LabelFrame(self, text='')
      lf.pack(side='top', expand=1, fill='both')
      
      #작업로그제목
      log_lb_frame = LabelFrame(lf, text='', relief=FLAT)
      ttk.Label(log_lb_frame, text='작업로그').pack(side='left', expand=1, fill='x') 
      ttk.Button(log_lb_frame, text='clear', command=lambda:self.scr.delete(1.0, END)).pack(side='right')
      log_lb_frame.pack(side='top', fill='x')
      
      #로그내용출력
      self.scr = scrolledtext.ScrolledText(lf, wrap=WORD)
      self.scr.pack(side='top', expand=1, fill='both')
   
   def menubar(self):
      menubar = Frame(self)
      mb1 = Menubutton(menubar,text='setup', width='10', relief='raised')
      mb1.menu = Menu(mb1,tearoff=0)
      mb1['menu'] = mb1.menu
      mb1.menu.add_command(label='directory',command=self.select_directory)
      mb1.menu.add_command(label='exit',command=self.destroy)
      mb1.pack(side='left')
      return menubar

   def select_directory(self):
      _dir = filedialog.askdirectory()
      self.dir_.set(_dir)      
      
      context.put(directory=_dir)
      return _dir

   # self.info 상태바정보 갱신용 변수
   def statusbar(self):
      fr_bot = Frame(self)
      self.info = StringVar()
      lb1 = Label(fr_bot,textvariable=self.info, height='2')
      lb1.pack(fill='x', expand=True, anchor='w')
      
      context.put(statusbar=self.info)
      return fr_bot

   # def show_info(self, msg):
   #    self.info.set(msg)
   
   # def show_workdir(self, msg):
   #    self.dir_.set(msg)
      
   #observer변경사항을 root인터페이스(regmapper에 등록됨)로 연결.
   # message: func, message
   def update(self, message):
          #등록된 명령목록에서 해당 명령문을 찾아 실행한다.
      if message[0] in self._commands:
         func = self._commands[message[0]]
         func(message[1])

   #외부인터페이스와 내부 메소드를 연결
   def _register_commands(self):          
      def writelog(log):         
         self.scr.insert(INSERT, log+'\n')
         self.scr.update()
         self.scr.see(END)
      
      self._commands.update(dict(log=writelog))
      self._commands.update(dict(dir=lambda _path: self.dir_.set(_path)))
      self._commands.update(dict(info=lambda msg: self.info.set(msg)))