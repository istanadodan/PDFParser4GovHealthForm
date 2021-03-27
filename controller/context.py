from tkinter import filedialog

class Context:
   context={}
   _observers=[]   
   _cache={}

   def __init__(self):
      pass

   def add_observer(self, observer):
      self._observers.append(observer)

   def find(self,id):
      if id not in self._cache: 
        for o in self._observers:
            if o.id == id: 
                self._cache[id] = o
                break
      return self._cache[id]

   def put(self, **data):
      for k,v in data.items():
         self.context[k] = v

   def get(self,key):
      return self.context.get(key,'')

   def notify(self, _to, func, msg):
      observer = self.find(_to)
      observer.call(func, msg)

   def notify_all(self, msg):
      caller_id = msg['id']
      for obj in self._observers:
         if obj.id != caller_id:
            obj.update(msg)

   def directory(self):
      # 유효설정값이 있을때만 맵 변경
      _dir = filedialog.askdirectory()
      if _dir:
         self.put(directory=_dir)
         self.notify('root','info',_dir)