class Appcontext:
   context={}
   _observers=[]   
   _cache={}   

   def put(self, **data):
      for k,v in data.items():
         self.context[k] = v

   def get(self,key):
      return self.context.get(key,'')
   
   def add_observer(self, observer):
      self._observers.append(observer)

   def find(self,id):
      if id not in self._cache: 
        for o in self._observers:
            if o.id == id: 
                self._cache[id] = o
                break
      return self._cache[id]
 
   #(id, msg)
   def notify_all(self, *message):      
      for obj in self._observers:         
         obj.update(message)
