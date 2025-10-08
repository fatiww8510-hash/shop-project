import sqlite3
import tkinter
import re

cnt=sqlite3.connect('shop.db')
userid=''

def login(txtuser,txtpass,lblmsg,btnlogin,btnshoppanel,btnshopcart,btnsearch):
    global userid
    user=txtuser.get()
    pas=txtpass.get()
    print(user,pas)
    if user=='' or pas=='':
        lblmsg.configure(text="please fill the inputs",fg="red")
        return
    query=f'''
        SELECT * FROM users WHERE username='{user}' and password='{pas}'
            '''
    result=cnt.execute(query)
    data=result.fetchall()
    if len(data)<1:
        lblmsg.configure(text="wrong username or password...",fg="red")
        return
    lblmsg.configure(text="welcome to your account",fg="green")
    query=f'''
            SELECT id FROM users WHERE username='{user}'
            '''
    result=cnt.execute(query)
    data=result.fetchall()
    userid=data[0][0]
    txtpass.delete(0,"end")
    txtuser.delete(0,"end")
    btnlogin.configure(state="disabled")
    btnshoppanel.configure(state="active")
    btnshopcart.configure(state="active")
    btnsearch.configure(state="active")

def validate(user,pas,cpas,addr):
        if user=='' or pas=='' or cpas=='' or addr=='':
            return False,"ERROR:please fill the inputs"
        if pas!=cpas:
            return False,"ERROR:password and confirm mismatch"
        query=f'''
                SELECT * FROM users WHERE username="{user}"
              '''
        result=cnt.execute(query)
        data=result.fetchall()
        if len(data)>0:
            return False,"ERROR:username already exists"

        regular=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        if not re.match(regular , pas):
            return False,"invalid password"

        return True,""


def signup():
    def register():
        user=txtuser.get()
        pas=txtpass.get()
        cpas=txtcpass.get()
        addr=txtaddr.get()
        result,msg=validate(user,pas,cpas,addr)
        if not result:
            lblmsg.configure(text=msg,fg="red")
            return
        query=f'''
            INSERT INTO users(username,password,address,score)
            VALUES("{user}","{pas}","{addr}",0)
            '''
        cnt.execute(query)
        cnt.commit()
        lblmsg.configure(text="your data registered successfuly",fg="green")

        txtuser.delete(0,"end")
        txtpass.delete(0,"end")
        txtaddr.delete(0,"end")

    winsignup=tkinter.Toplevel()
    winsignup.title("signup pannel")
    winsignup.geometry("300x300")

    lbluser=tkinter.Label(winsignup,text="username:")
    lbluser.pack()
    txtuser=tkinter.Entry(winsignup,width=30)
    txtuser.pack()

    lblpass=tkinter.Label(winsignup,text="password:")
    lblpass.pack()
    txtpass=tkinter.Entry(winsignup,width=30)
    txtpass.pack()

    lblcpass=tkinter.Label(winsignup,text="confirm password:")
    lblcpass.pack()
    txtcpass=tkinter.Entry(winsignup,width=30)
    txtcpass.pack()

    lbladdr=tkinter.Label(winsignup,text="address:")
    lbladdr.pack()
    txtaddr=tkinter.Entry(winsignup,width=30)
    txtaddr.pack()

    lblmsg=tkinter.Label(winsignup,text="")
    lblmsg.pack()

    btnregister=tkinter.Button(winsignup,text="register",command=register)
    btnregister.pack()

    winsignup.mainloop()

def shoppanel():
    def add2cart():
        pid=txtid.get()
        pnum=txtnum.get()

        if pid=='' or pnum=='':
            lblmsg3.configure(text="please fill the inputs",fg="red")
            return
        if (not pid.isdigit()) or (not pnum.isdigit()):
            lblmsg3.configure(text="invalid data",fg="red")
        query=f'''
                SELECT * FROM products WHERE id={int(pid)}
              '''
        result=cnt.execute(query)
        data=result.fetchall()
        if len(data)<1:
            lblmsg3.configure(text="invalid id",fg="red")
            return
        query=f'''
                SELECT * FROM products WHERE id={int(pid)} AND numbers>={int(pnum)}
               '''
        result=cnt.execute(query)
        data=result.fetchall()
        if len(data)<1:
            lblmsg3.configure(text="not enough products",fg="red")
            return
        # query=f'''
        #         INSERT INTO cart(uid,pid,numbers)
        #         VALUES ({userid},{int(pid)},{int(pnum)})
        #         '''
        # cnt.execute(query)
        query=f'''
                UPDATE products SET numbers= numbers-{int(pnum)} WHERE id={int(pid)}
              '''
        cnt.execute(query)
        cnt.commit()

        import datetime
        date = str(datetime.date.today())
        query = f'''
                 INSERT INTO cart(uid,pid,numbers,date)  
                 VALUES({userid},{int(pid)},{int(pnum)},'{date}')
                '''
        cnt.execute(query)
        cnt.commit()

        lblmsg3.configure(text="cart added",fg="green")
        lstbox.delete(0,"end")

        txtid.delete(0,"end")
        txtnum.delete(0,"end")


    winshop=tkinter.Toplevel()
    winshop.title("shop pannel")
    winshop.geometry("400x300")

    lstbox=tkinter.Listbox(winshop,width=60)
    lstbox.pack()

    products=getproducts()
    for item in products:
        text=f'Id: {item[0]} ** name: {item[1]} ** price: {item[2]} ** address: {item[3]}'
        lstbox.insert("end",text)



    lblid=tkinter.Label(winshop,text="product id: ")
    lblid.pack()
    txtid=tkinter.Entry(winshop)
    txtid.pack()

    lblnum=tkinter.Label(winshop,text="product number: ")
    lblnum.pack()
    txtnum=tkinter.Entry(winshop)
    txtnum.pack()

    lblmsg3=tkinter.Label(winshop,text="")
    lblmsg3.pack()

    btnshop=tkinter.Button(winshop,text="add2cart",command=add2cart)
    btnshop.pack()

    winshop.mainloop()


def getproducts():
    query=f'''
            SELECT * FROM products
            '''
    result=cnt.execute(query)
    data=result.fetchall()
    return data
def shopcart():
    wincart=tkinter.Toplevel()
    wincart.title("shop cart")
    wincart.geometry("400x300")

    lstbox=tkinter.Listbox(wincart,width=60)
    lstbox.pack()

    query=f'''
            SELECT pid,numbers FROM cart WHERE uid={userid}
           '''
    result=cnt.execute(query)
    data=result.fetchall()

    for pid,numbers in data:
        query=f'''
                SELECT pname,price FROM products WHERE id={pid}
               '''
        result=cnt.execute(query)
        product=result.fetchall()[0]
        pname, price = product
        text = f'product: {pname} ** count: {numbers} ** price: {price} '
        lstbox.insert("end", text)
    wincart.mainloop()

def search():
    winsearch=tkinter.Toplevel()
    winsearch.title("search")
    winsearch.geometry("300x300")

    lblsearch=tkinter.Label(winsearch,text="ENTER DATE: ")
    lblsearch.pack()

    txtsearch=tkinter.Entry(winsearch,width=30)
    txtsearch.pack()

    lblmsg3=tkinter.Label(winsearch,text="")
    lblmsg3.pack()

    lstbox=tkinter.Listbox(winsearch,width=60)
    lstbox.pack()

    def date():
        date=txtsearch.get()
        if date=='':
            lblmsg3.configure(text="invalid date",fg="red")
            return
        query=f'''
                SELECT pid FROM cart WHERE date='{date}' AND uid={userid}
              '''
        result=cnt.execute(query)
        data=result.fetchall()

        lstbox.delete(0,"end")

        if data:
            for item in data:
                pid=item[0]
                lstbox.insert('end',f'your product id: {pid}')
            lblmsg3.configure(text='your product founded!',fg="green",font='bold')
        else:
            lblmsg3.configure(text="invalid date",fg="red",font='bold')

    btnsearchdate = tkinter.Button(winsearch, text="search", width=15, command=date)
    btnsearchdate.pack()

    winsearch.mainloop()

