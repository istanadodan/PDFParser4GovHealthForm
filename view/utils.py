from tkinter import messagebox, filedialog
from app.appcontext import Appcontext
from app import showinfo
context = Appcontext()

def select_directory():
   _dir = context.get('directory')
   if not _dir:
      _dir = filedialog.askdirectory()      
      context.put(directory=_dir)      
      
   return _dir

def show_info(msg, type='info'):
   showinfo(msg)
   if type=='err':
      messagebox.showerror('오류',message=msg)
   else:    
      messagebox.showinfo("알림",message=msg) 
      