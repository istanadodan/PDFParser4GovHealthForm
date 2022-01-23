from view import Root, Window1, Window2

if __name__== "__main__":  

   app = Root() 
   # menu_건강/연금
   w1 = Window1(app)
   # menu_원천세
   w2 = Window2(app)
   app.add(w1)
   app.add(w2)
   app.build()
   app.mainloop() 