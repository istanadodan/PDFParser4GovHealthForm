from tkinter import Tk,Text,Scrollbar,Button,END,Entry,Frame,filedialog,Label,messagebox,\
                    Listbox,Menubutton,Menu,\
                    StringVar, IntVar
from app import GROUP1, GROUP2

_global_group = [GROUP1, GROUP2]
     
class Window2(Frame):
   
   def __init__(self, parent, context):
      super(Window2,self).__init__(parent.Frame)
      context.add_observer(self)
      self.parent = parent
      self.context = context
      self.controller = parent.controller
      self._initialize()
      
      self.build()

   def _initialize(self):
      self.id='task'
      #画面遷移の順番を示す指示物
      self.unit_name_list = []

   def update(self,msg):
      self._gid = msg['gid'] 
      self.unit_name_list = _global_group[msg['gid'] - 1]
      
      self._update_unit_name_list()
      self.task_lbx.delete(0,END)
      
   def convert(self):

      units = self._task_box.get(0,END)
      if not units:
         self.context.notify('root','info',"처리할 작업이 없습니다.")
         return

      working_dir = self.context.get('directory')
      if not working_dir:
         self.context.directory()
         working_dir = self.context.get('directory')
         if not working_dir:
            messagebox.showwarning("경고",'작업디렉토리가 설정되어 있지 않습니다.')
            return
         
       # html변환여부 체크옵션
      _html = self.context.get('html')
      _gid = self._gid

      try:
         self.controller.convert(working_dir, _html, units, _gid)
         
         self.context.notify('root','info',"작업완료")   
         messagebox.showinfo("알림",message="작업이 완료되었습니다.")
         
      except Exception as e:
         print(e)
         messagebox.showerror('포맷오류','잘못된 포맷을 적용하였습니다.')
         self.context.notify('root','info',"작업오류")

   def build(self):
      componets = self.component_list()
      tasks = self.task_list()

      componets.pack(side="left", fill='y')
      componets.config(bg='steel blue3')
      tasks.pack(side='right', fill='both',expand=True)
      tasks.config(bg='light grey',padx=3)

   def _update_unit_name_list(self):
      self._list.delete(0,END)

      for i, name in enumerate(self.unit_name_list):
         self._list.insert(i, name)
      
   def component_list(self):
      #sandy brown
      fr1 = Frame(self)
      scrollbar = Scrollbar(fr1)
      scrollbar.pack(side="right",fill="y")
      
      self._list = Listbox(fr1, bg="dim grey",fg="white", width=20, yscrollcommand=scrollbar.set)

      mb1 = Menubutton(fr1,text='선택메뉴',relief='flat',bg='steel blue3')
      mb1.menu = Menu(mb1,tearoff=0)
      mb1['menu'] = mb1.menu
      mb1.menu.add_command(label='등록', command=self.choose_all)
      mb1.pack(side='bottom')
      mb1.menu.add_command(label='선택', command=lambda:self._list.select_set(0,END))
      mb1.menu.add_command(label='해제', command=lambda:self._list.selection_clear(0,'end'))      

      self._list.pack(anchor="center",fill="both",expand=True,padx=3,pady=3)
      
      scrollbar.config(command=self._list.yview)
      self._list.config(highlightcolor='green',font=('나눔고딕',10), activestyle='none',selectmode='extended')

      self._list.bind('<<ListboxSelect>>', self.select_item)
      self._list.bind('<Button-3>', self.sub_menu1)
      self._list.exportselection = 0

      return fr1

   def select_item(self,event):
      self.clear_submenu()
      
      widget = event.widget
      #print("select item",widget.curselection())
      # if isinstance(widget,Listbox):
      v = widget.curselection()
      t = [widget.get(i) for i in v]

      self.context.notify('root','info',t)

   def clear_submenu(self):
      if hasattr(self, 'sub_fr'):
         self.sub_fr.destroy()

   def _setActivate(self, obj, index):
      obj.selection_set(index)
      # obj.see(index)
      # obj.activate(index)
      # obj.selection_anchor(index)

   def sub_menu1(self,event):
      self.clear_submenu()
      x, y = event.x, event.y
      
      self._setActivate(self._list, self._list.nearest(y))

      self.sub_fr = Frame(self, height=10)
      b1 = Button(self.sub_fr,text='reg', command=self.choose_task, relief='flat')
      b1.pack(side='top', fill='both')
      self.sub_fr.place(x=x+15,y=y)

   def choose_all(self):
      self.clear_submenu()
      for el in self._list.get(0,END):
         if not self._isduplicate(el):
            self._task_box.insert(END, el)

   def choose_task(self):
      self.clear_submenu()
      ixs = self._list.curselection()
      for ix in ixs:
         el = self._list.get(ix)
         if not self._isduplicate(el):
            self._task_box.insert(END, el)

   def _isduplicate(self, txt):      
      for v in list(self._task_box.get(0,'end')):
         if v == txt: return True
      return False

   def task_list(self):
      fr = Frame(self)
      fr_top = Frame(fr)
      task_lbx = Listbox(fr_top)
      task_lbx.pack(anchor="center",fill="both",expand=True,padx=3,pady=3)
      self._task_box = task_lbx
      
      fr_bot = Frame(fr,height='2')
      b1 = Menubutton(fr_bot,text='실행메뉴')
      b1.menu = Menu(b1,tearoff=0)
      b1['menu'] = b1.menu
      b1.menu.add_command(label='실행',command=self.convert)
      b1.menu.add_command(label='비우기',command=self.delete_task_item)
      b1.pack()

      fr_top.pack(side='top',fill='both', expand=True)
      fr_bot.pack(side='bottom',fill='x')  
      task_lbx.config(highlightcolor='green',font=('굴림체',10), activestyle='none',selectmode='extended')

      self.task_lbx =task_lbx

      return fr

   def delete_task_item(self):
      v=self.task_lbx.curselection()
      #print(v)
      if not v:
         self.task_lbx.delete(0,END)
      elif len(v)==1:
         self.task_lbx.delete(v)
      else:
         self.task_lbx.delete(v[0],v[-1])
