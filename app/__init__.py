import datetime
from .appcontext import Appcontext
from .config import get_config, load_setting

appcontext = Appcontext()
if not appcontext.get('config'):
   load_setting()

#실행모드
run_mode = 'prod'

def writelog(format, data=None, mode='prod'):
   if run_mode!='dev' and mode!='prod':return
   
   _time = datetime.datetime.now().strftime('%H:%M:%S')
   if data:
      format = format % data
   
   if mode =='dev':
      print("[%s] %s"%(_time, format))
   else:
      appcontext.notify_all('log', "[%s] %s"%(_time, format))

def showinfo(msg=''):
    appcontext.notify_all('info',msg)

def showdir(path=''):
    appcontext.notify_all('dir',path)