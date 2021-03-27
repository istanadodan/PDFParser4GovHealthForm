from view import Root, Window1, Window2
from controller import Controller, Context
from model import Model

if __name__== "__main__":  

   context = Context()
   cntl = Controller()
   model = Model()

   root = Root(context)
   root.controller(cntl)

   w1 = Window1(root, context)
   w2 = Window2(root, context)

   root.add(w1)
   root.add(w2)

   cntl.model(model)
   cntl.view(w2)

   root.activate()
   root.mainloop()
