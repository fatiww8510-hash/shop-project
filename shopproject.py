import sqlite3
import tkinter
import json
from fusers import*

win=tkinter.Tk()
win.title("login panel")
win.geometry("250x250")

lbluser=tkinter.Label(win,text="username:")
lbluser.pack()
txtuser=tkinter.Entry(win,width=30)
txtuser.pack()

lblpass=tkinter.Label(win,text="password:")
lblpass.pack()
txtpass=tkinter.Entry(win,width=30)
txtpass.pack()

lblmsg=tkinter.Label(win,text="")
lblmsg.pack()

btnlogin=tkinter.Button(win,text="login",width=15,command=lambda :login(txtuser,txtpass,lblmsg,btnlogin,btnshoppanel,btnshopcart,btnsearch))
btnlogin.pack()
btnsignup=tkinter.Button(win,text="signup",width=15,command=signup)
btnsignup.pack()

lblmsg3=tkinter.Label(win,text="")
lblmsg3.pack()

btnshoppanel=tkinter.Button(win,text="shop panel",width=15,command=shoppanel,state='disabled')
btnshoppanel.pack()

btnshopcart=tkinter.Button(win,text="shop cart",width=15,command=shopcart,state='disabled')
btnshopcart.pack()

btnsearch=tkinter.Button(win,text="search",width=15,command=search,state='disabled')
btnsearch.pack()

win.mainloop()
