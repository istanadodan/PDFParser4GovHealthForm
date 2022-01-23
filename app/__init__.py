import datetime
from .config import get_config, get_config2
from .context import Context

context = Context()
#실행모드
run_mode = 'prod'

GROUP1 = get_config('LISTBOX/group1')
GROUP2 = get_config('LISTBOX/group2')

TASK_NAME = get_config('Class_Mapping/task_name')
CLASS_NAME = get_config('Class_Mapping/class_name')

GROUP_LST = get_config2('group')
CLASS_MAP = get_config2('class_map')

def SH_NAME(id):
    return get_config('GROUP/group%d'%id)[0]

def writelog(format, data=None, mode='prod'):
   if run_mode!='dev' and mode!='prod':return
   
   _time = datetime.datetime.now().strftime('%H:%M:%S')
   if data:
      format = format % data
   
   if mode =='dev':
      print("[%s] %s"%(_time, format))
   else:
      context.notify_all('log', "[%s] %s"%(_time, format))

def showinfo(msg=''):
    context.notify_all('info',msg)

def showdir(path=''):
    context.notify_all('dir',path)