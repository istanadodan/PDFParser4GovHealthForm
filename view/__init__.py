from .root import Root
from .menu1 import Window as Window1
from .menu2 import Window as Window2

app = Root()
app.add(Window1(app))
app.add(Window2(app))
    
def start():
    app.build()
    app.mainloop()

