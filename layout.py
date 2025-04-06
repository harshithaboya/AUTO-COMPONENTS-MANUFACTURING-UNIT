
from tkinter import messagebox
from tkinter.tix import *
from tkcalendar import *
from PIL import ImageTk as ITk,Image
import mysql.connector
import re
from tkinter import ttk



try:
    mydb=mysql.connector.connect(user='root', password='kavya',host='127.0.0.1',database='ManufacturingUnit',autocommit=True)
    mycursor=mydb.cursor(buffered=True)

    mycursor.execute("USE ManufacturingUnit")
    mycursor.fetchone()
except:
    messagebox.showwarning("No Connection.","Error in connecting to database.")
global sum,total

class Base():
    def __init__(self,root):
        self.root = root
        self.root.title("AUTO COMPONENTS MANUFACTURING UNIT")
        self.root.geometry("1350x759")
        self.root.resizable(width=FALSE, height=FALSE)
        self.bg_icon = ITk.PhotoImage(file="background.jpg")

        bg_lbl = Label(self.root, image=self.bg_icon).pack()
        title = Label(self.root, text="AUTO COMPONENTS MANUFACTURING UNIT", font=("times new roman", 40, "bold"),
                      fg="red", bg="white", relief=GROOVE)
        title.place(x=0, y=30, relwidth=1)
        self.ul_icon = ITk.PhotoImage(file="userlogin.jpg")
        buyer = IntVar()


        drop = Frame(self.root, bg="grey", width=300, height=300)
        drop.place(x=10, y=100)
        drophere=Label(drop, text="DROP HERE", font=("arial",14, "bold", "underline"), fg="white", bg="grey")
        drophere.place(x=0,y=0)
        buy = Label(drop, text="Buyer:", font=("arial",10, "bold", "italic"), fg="white", bg="grey")
        buy.place(x=0, y=30)

        self.choices1 = ('Yes', 'No')
        self.tkvar1 = StringVar(drop)
        self.tkvar1.set(self.choices1[0])
        notcust = ttk.OptionMenu(drop, self.tkvar1, *self.choices1)
        notcust.place(x=50, y=30)
        id = Label(drop, text="ID(IF NOT BUYER):", font=("arial", 8, "bold", "italic"), fg="white", bg="grey")
        id.place(x=0, y=60)
        entid = Entry(drop, bg="white", bd=2, width=25, font=("",8))
        entid.place(x=110, y=60)
        msg=Label(drop, text="Message:", font=("arial", 8, "bold", "italic"), fg="white", bg="grey")
        msg.place(x=0, y=90)
        scrollbar = Scrollbar(root)
        scrollbar.pack(side=RIGHT, fill=Y)
        textbox = Text(drop,width=25,height=10,bd=5)
        textbox.place(x=60,y=90)


        textbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=textbox.yview)
        def addmsg():
            t=textbox.get("1.0", "end-1c")
            print(t)
            print(self.tkvar1.get())
            if len(t)==0:

                messagebox.showwarning("Give feedback", "Enter your message")
            else:
                if self.tkvar1.get()=="Yes":
                    inssql="INSERT INTO feedback(fmsg) values(\"%s\");"%(t)
                    mycursor.execute(inssql)
                elif self.tkvar1.get()=="No":
                    print(entid.get())
                    i = "SELECT * FROM worker where workerid=\"%s\";" % (entid.get())
                    print(i)
                    mycursor.execute(i)
                    wor=mycursor.rowcount
                    print(wor)
                    if wor==0:
                        messagebox.showwarning("ID NOT FOUND", "Enter valid ID")

                    else:
                        inssql = "INSERT INTO message(mid,msg) values(\"%s\",\"%s\");" % (entid.get(), t)
                        print(inssql)
                        mycursor.execute(inssql)
                entid.delete(0, 'end')
                textbox.delete("1.0", "end")


        def backg():
            for widget in self.root.winfo_children():
               widget.destroy()
            Login(root)

        send=Button(drop, text="Send", command=addmsg, font=("arial", 8, "bold"), bd=5, relief=GROOVE)
        send.place(x=200, y=270)
        bac= Button(self.root, text="Back", command=backg, font=("arial", 8, "bold"), bd=5, relief=GROOVE)
        bac.place(x=50, y=700)






class Login(Base):
    def __init__(self,root):
        super().__init__(root)
        Login_Frame = Frame(self.root, bg="grey", width=100, height=500)
        Login_Frame.place(x=800, y=150, relwidth=1)
        log_lbl = Label(Login_Frame, image=self.ul_icon)
        log_lbl.place(x=-450, y=0, relwidth=1)
        l = Label(Login_Frame, text="USER   LOGIN", font=("arial", 30, "bold", "underline"), fg="white", bg="grey")
        l.place(x=-450, y=70, relwidth=1)
        l1 = Label(Login_Frame, text="USER ID     :", font=("arial", 20, "bold", "italic"), fg="white", bg="grey")
        l1.place(x=-590, y=150, relwidth=1)
        userid = Entry(Login_Frame, bg="white", bd=2, width=25, font=("", 18))
        userid.place(x=170, y=150)

        l2 = Label(Login_Frame, text="PASSWORD:", font=("arial", 20, "bold", "italic"), fg="white", bg="grey")
        l2.place(x=-590, y=200, relwidth=1)
        pw = Entry(Login_Frame, bg="white", bd=2, width=25, font=("", 18), show="*")
        pw.place(x=170, y=200)

        def verify():
            global uid
            uid= int(userid.get())
            pwd = pw.get()
            print(uid)
            print(pwd)

            sql = "SELECT * FROM BUYER WHERE BUYER_CONTACT=%d;" % (uid)
            mycursor.execute(sql)
            mycursor.fetchall()
            u = mycursor.rowcount
            sql = "SELECT BUYER_PASSWORD FROM BUYER WHERE BUYER_CONTACT=%d" % (uid)
            mycursor.execute(sql)
            res = mycursor.fetchall()

            if u == 0:
                messagebox.showwarning("SIGN UP", "Not registered")
            elif res[0][0] != pwd:
                messagebox.showinfo("Retry", "Password error")
            else:
                messagebox.showinfo("Login Successful", "User Verified")
                view(root,0,uid)
            userid.delete(0,len(userid.get()))

            pw.delete(0,len(pw.get()))

        def create():
            New_user(root)

        def forgot():
            passwd(root)

        def not_cust():
            memlogin(root)




        B1 = Button(Login_Frame, text="Sign in", command=verify, font=("arial", 18, "bold"), bd=5, relief=GROOVE)
        B1.place(x=150, y=250)
        B2 = Button(Login_Frame, text="Sign up", command=create, font=("arial", 18, "bold"), bd=5, relief=GROOVE)
        B2.place(x=300, y=250)
        B3 = Button(Login_Frame, text="Forgot password", command=forgot, font=("arial", 18, "italic", "underline"),
                    bd=0, bg="grey", relief=GROOVE)
        B3.place(x=300, y=350)
        B4 = Button(Login_Frame, text="Not a customer", command=not_cust, font=("arial", 18, "italic", "underline"), bd=0,
                    bg="grey", relief=GROOVE)
        B4.place(x=300, y=400)


class New_user(Base):
    def __init__(self, root):
        super().__init__(root)

        New_Frame = Frame(self.root, bg="grey", width=100, height=500)
        New_Frame.place(x=800, y=150, relwidth=1)

        self.ul_icon = ITk.PhotoImage(file="userlogin.jpg")
        log_lbl = Label(New_Frame,image=self.ul_icon)
        log_lbl.place(x=-450, y=0, relwidth=1)

        l1 = Label(New_Frame, text="REGISTER", font=("arial", 30, "bold", "underline"), fg="white", bg="grey")
        l1.place(x=-450, y=70, relwidth=1)
        l1 = Label(New_Frame, text="NAME:", font=("arial", 16, "bold", "italic"), fg="white", bg="grey")
        l1.place(x=-590, y=150, relwidth=1)
        l1 = Label(New_Frame, text="CONTACT:", font=("arial", 16, "bold", "italic"), fg="white", bg="grey")
        l1.place(x=-590, y=200, relwidth=1)
        l1 = Label(New_Frame, text="SET PASSWORD:", font=("arial", 16, "bold", "italic"), fg="white", bg="grey")
        l1.place(x=-570, y=250, relwidth=1)
        l1 = Label(New_Frame, text="PASSWORD HINT:", font=("arial", 16, "bold", "italic"), fg="white", bg="grey")
        l1.place(x=-570, y=300, relwidth=1)
        name=Entry(New_Frame, bg="white", bd=2, width=25, font=("", 16))
        name.place(x=200, y=150)


        contact= Entry(New_Frame, bg="white", bd=2, width=25, font=("", 16))
        contact.place(x=200, y=200)
        a = Label(New_Frame, text="(enter 10 digit mobile no.)", font=("arial", 10, "italic"), fg="white", bg="grey")
        a.place(x=250, y=230)
        passwd = Entry(New_Frame, bg="white", bd=2, width=25, font=("", 16))
        passwd.place(x=200, y=250)
        a = Label(New_Frame, text="(maximum length 10)", font=("arial", 10, "italic"), fg="white", bg="grey")
        a.place(x=250, y=280)

        hint = Entry(New_Frame, bg="white", bd=2, width=25, font=("", 16))
        hint.place(x=200, y=300)
        a = Label(New_Frame, text="(Which is your first school?)", font=("arial", 10, "italic"), fg="white", bg="grey")
        a.place(x=250, y=330)


        def back():
            Base(root)

        def register():
            bname=name.get()
            print(bname)
            bcontact=int(contact.get())
            pattern = re.compile("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]")

            bpwd=passwd.get()
            bhint=hint.get()
            if bname=="" or bpwd=="" or bhint=="":
                messagebox.showwarning("PLEASE CHECK", "Enter ALL DETAILS")
                New_user(root)
            else:
                if not pattern.match(str(bcontact)):
                    messagebox.showwarning("NOT VALID", "Enter proper mobile number")
                    return
                sql = "SELECT * FROM BUYER WHERE BUYER_CONTACT=%d;"%(bcontact)
                mycursor.execute(sql)
                print(mycursor)
                mycursor.fetchall()
                u = mycursor.rowcount
                if u != 0:
                    messagebox.showinfo("Sign in", "Account existing")
                    name.delete(0, len(name.get()))

                    contact.delete(0, len(contact.get()))

                    passwd.delete(0, len(passwd.get()))
                    hint.delete(0, len(hint.get()))

                else:
                    sql =("INSERT INTO BUYER(BUYER_NAME,BUYER_CONTACT,BUYER_PASSWORD,BUYER_HINT)""VALUES(%s,%s,%s,%s)")
                    vals=(bname, bcontact, bpwd, bhint)
                    mycursor.execute(sql,vals)
                    mydb.commit()
                    messagebox.showinfo("Account created","Your user id is {}".format(bcontact))
                    name.delete(0, len(name.get()))

                    contact.delete(0, len(contact.get()))

                    passwd.delete(0, len(passwd.get()))
                    hint.delete(0, len(hint.get()))








        B1 = Button(New_Frame, text="BACK", command=back, font=("arial", 18, "bold"), bd=5, relief=GROOVE)
        B1.place(x=150, y=400)
        B2 = Button(New_Frame, text="SIGN IN", command=register, font=("arial", 18, "bold"), bd=5, relief=GROOVE)
        B2.place(x=300, y=400)

class passwd(Base):
    def __init__(self, root):
        super().__init__(root)

        Pass_Frame = Frame(self.root, bg="grey", width=100, height=500)
        Pass_Frame.place(x=800, y=150, relwidth=1)
        log_lbl = Label(Pass_Frame, image=self.ul_icon)
        log_lbl.place(x=-450, y=0, relwidth=1)
        l1 = Label(Pass_Frame, text="CHANGE PASSWORD", font=("arial", 30, "bold", "underline"), fg="white", bg="grey")
        l1.place(x=-450, y=70, relwidth=1)
        l2 = Label(Pass_Frame, text="USER ID     :", font=("arial", 18, "bold", "italic"), fg="white", bg="grey")
        l2.place(x=-590, y=150, relwidth=1)
        userid = Entry(Pass_Frame, bg="white", bd=2, width=25, font=("", 16))
        userid.place(x=200, y=150)

        l3 = Label(Pass_Frame, text="RESET PASSWORD:", font=("arial", 14, "bold", "italic"), fg="white", bg="grey")
        l3.place(x=-570, y=200, relwidth=1)
        pw = Entry(Pass_Frame, bg="white", bd=2, width=25, font=("", 16), show="*")
        pw.place(x=200, y=200)
        a = Label(Pass_Frame, text="(maximum length 10)", font=("arial", 10, "italic"), fg="white", bg="grey")
        a.place(x=250, y=230)

        l4 = Label(Pass_Frame, text="HINT    :", font=("arial", 18, "bold", "italic"), fg="white", bg="grey")
        l4.place(x=-590, y=250, relwidth=1)
        hint= Entry(Pass_Frame, bg="white", bd=2, width=25, font=("", 18))
        hint.place(x=200, y=250)
        a = Label(Pass_Frame, text="(Which is your first school?)", font=("arial", 10, "italic"), fg="white", bg="grey")
        a.place(x=250, y=290)
        def reset():
            u=userid.get()
            p=pw.get()
            h=hint.get()
            if u=="" or p=="" or h=="":
                messagebox.showwarning("PLEASE CHECK", "Enter ALL DETAILS")
                passwd(root)
            else:
                u=int(u)
                sql = "SELECT * FROM BUYER WHERE BUYER_CONTACT=%d;" % (u)
                mycursor.execute(sql)
                print(mycursor)
                mycursor.fetchall()
                m= mycursor.rowcount
                if m== 0:
                    messagebox.showwarning("Sign up", "Register as user")
                    Login(root)
                else:

                    sql = "SELECT * FROM BUYER WHERE BUYER_CONTACT=%s AND BUYER_HINT=%s"
                    vals=(u,h)
                    mycursor.execute(sql,vals)

                    mycursor.fetchall()
                    m = mycursor.rowcount
                    if m==0:
                        messagebox.showwarning("Not verified", "Buyer is not verified to reset password")
                        Login(root)
                    else:
                        sql='UPDATE BUYER SET BUYER_PASSWORD="{}" WHERE BUYER_CONTACT={} AND BUYER_HINT="{}";'.format(p,u,h)
                        print(sql)

                        print(sql)
                        mycursor.execute(sql)
                        mydb.commit()
                        messagebox.showinfo("Password changed", "Sign in using new password")

                        Login(root)







        def back():
            Base(root)
        B1 = Button(Pass_Frame, text="Reset", command=reset, font=("arial", 18, "bold"), bd=5, relief=GROOVE)
        B1.place(x=300, y=350)
        B2 = Button(Pass_Frame, text="Back", command=back, font=("arial", 18, "bold"), bd=5, relief=GROOVE)
        B2.place(x=150, y=350)

class memlogin(Base):
    def __init__(self,root):
        super().__init__(root)
        L_Frame = Frame(self.root, bg="grey", width=100, height=500)
        L_Frame.place(x=800, y=150, relwidth=1)
        ll1 = Label(L_Frame, text="MEMBER  LOGIN", font=("arial", 30, "bold", "underline"), fg="white", bg="grey")
        ll1.place(x=-450, y=70, relwidth=1)
        ll2 = Label(L_Frame, text="LOGIN ID     :", font=("arial", 20, "bold", "italic"), fg="white", bg="grey")
        ll2.place(x=-590, y=150, relwidth=1)
        userid = Entry(L_Frame, bg="white", bd=2, width=25, font=("", 18))
        userid.place(x=170, y=150)

        l2 = Label(L_Frame, text="PASSWORD:", font=("arial", 20, "bold", "italic"), fg="white", bg="grey")
        l2.place(x=-590, y=200, relwidth=1)
        pw = Entry(L_Frame, bg="white",fg="black", bd=2, width=25, font=("", 18), show="*")
        pw.place(x=170, y=200)



        def setDate():
            pw.delete(0, 'end')
            d=myCal.get_date()
            pw.insert(0,d)

            choose.destroy()
            myCal.destroy()

        def getDate():
            global myCal
            myCal = Calendar(L_Frame, setmode='day', date_pattern='yyyy-mm-dd')
            myCal.place(x=200,y=270)
            global choose
            choose=Button(L_Frame, text="Choose", command=setDate, font=("arial", 10, "bold"), bd=5, relief=GROOVE)
            choose.place(x=450, y=230)

        b=Button(L_Frame, text="calendar",command=getDate, font=("arial",6), bd=1, relief=GROOVE)
        b.place(x=450,y=230)

        a = Label(L_Frame, text="(DATE OF JOINING)", font=("arial", 10, "italic"), fg="white", bg="grey")
        a.place(x=300, y=240)
        l3 = Label(L_Frame, text="ROLE:", font=("arial", 20, "bold", "italic"), fg="white", bg="grey")
        l3.place(x=-590, y=270, relwidth=1)
        self.choices1 =('Not a Customer','Main admin','Stock Manager','Shift Manager', 'Employee')
        self.tkvar1 = StringVar(L_Frame)
        self.tkvar1.set("Not a customer")
        notcust =ttk.OptionMenu(L_Frame,self.tkvar1,*self.choices1)
        notcust.place(x=200, y=290)

        def portal():
            if userid.get()=="" or pw.get()=="":
                messagebox.showwarning("FILL!", "Enter all details")

            else:
                if self.tkvar1.get()=="Not a Customer":
                    messagebox.showwarning("Make Choice!", "Choose your role")

                elif self.tkvar1.get()=="Main admin":

                    if userid.get()=="ACMU" and pw.get()=="2020-11-01":
                        L_Frame = Frame(self.root, bg="white", width=100, height=500)
                        L_Frame.place(x=800, y=150, relwidth=1)
                        admin(root)
                    else:
                        messagebox.showwarning("Admin", "No matching records found")
                elif self.tkvar1.get()=="Input Supplier":
                        pass
                elif self.tkvar1.get()=="Stock Manager":
                    msql="select doj from worker where workerid=\"%s\" and position=\"STOCK MANAGER\";"%(userid.get())
                    mycursor.execute(msql)

                    doj=mycursor.fetchall()
                    m = mycursor.rowcount
                    if(m==0):
                        messagebox.showwarning("Stock Manager", "No matching records found")
                        memlogin(root)
                    else:
                        print(doj[0][0])
                        print(pw.get())
                        if(str(doj[0][0])==str(pw.get())):
                            stock(root, userid.get())
                        else:
                            messagebox.showwarning("Stock Manager", "Password error!")
                            memlogin(root)



                elif self.tkvar1.get()=="Shift Manager":
                    msql = "select doj from worker where workerid=\"%s\";" % (userid.get())
                    mycursor.execute(msql)

                    doj = mycursor.fetchall()
                    m = mycursor.rowcount
                    if (m == 0):
                        messagebox.showwarning("Shift Manager", "No matching records found")
                        memlogin(root)
                    else:
                        if (str(doj[0][0])==str(pw.get())):
                            shift(root, userid.get())
                        else:
                            messagebox.showwarning("Shift Manager", "Password error!")
                            memlogin(root)

                elif self.tkvar1.get()=="Employee":
                    msql = "select doj from worker where workerid=\"%s\";" % (userid.get())
                    mycursor.execute(msql)

                    doj = mycursor.fetchall()
                    m = mycursor.rowcount
                    if (m == 0):
                        messagebox.showwarning("Employee", "No matching records found")
                        memlogin(root)
                    else:
                        if (str(doj[0][0]) ==str(pw.get())):
                            employee(root, userid.get())
                        else:
                            messagebox.showwarning("Employee", "Password error!")
                            memlogin(root)




        def back():
            Login(root)
        B1 = Button(L_Frame, text="Sign in", command=portal, font=("arial", 18, "bold"), bd=5, relief=GROOVE)
        B1.place(x=150, y=400)
        B2 = Button(L_Frame, text="Back", command=back, font=("arial", 18, "bold"), bd=5, relief=GROOVE)
        B2.place(x=300, y=400)
class view(Base):
    def __init__(self,root,p,uid):
        super().__init__(root)
        Page_Frame= Frame(self.root, bg="grey", width=2000, height=1000)
        Page_Frame.place(x=400, y=100)
        sql = "SELECT * FROM product"
        mycursor.execute(sql)
        f = mycursor.fetchall()
        r = mycursor.rowcount
        global quanti, e,pri
        def bill(uid,r_set,sum,pri,billstr,filestr,r_rows,total):
            a1="SELECT BUYER_NAME,BUYER_CONTACT FROM BUYER WHERE BUYER_CONTACT=\"%s\""%(uid)
            mycursor.execute(a1)
            f1= mycursor.fetchall()


            outF = open(filestr, "w")
            outF.write("AUTO COMPONENTS MANUFACTURING UNIT")
            outF.write("\n")
            outF.write("----------------------------------------------------------------------------------------------------------\n")
            outF.write("Transaction ID:"+billstr)
            outF.write("\n")
            outF.write("Name:"+str(f1[0][0]))
            outF.write("\n")
            outF.write("Contact:"+str(f1[0][1]))
            outF.write( "----------------------------------------------------------------------------------------------------------\n")
            outF.write("|%6s|%15s|%7s|%5s|%8s|\n"%("CODE","NAME","MRP(Rs)","Quantity","TotalCost(Rs)"))
            outF.write("----------------------------------------------------------------------------------------------------------\n")

            for i in range(r_rows):
                outF.write("|%6s|%15s|%7d|%5d|%8d|\n"%(r_set[i][0],r_set[i][1],r_set[i][2],r_set[i][3],r_set[i][4]))
            outF.write("----------------------------------------------------------------------------------------------------------\n")
            outF.write("Total:Rs."+str(sum))
            outF.write("\n")
            outF.write("Printing Price:Rs."+str(pri))
            outF.write("\n")
            outF.write("Printing name:"+str(pr.get()))
            outF.write("\n")
            outF.write( "----------------------------------------------------------------------------------------------------------\n")
            outF.write("Total amount paid:Rs."+str(total))
            outF.close()





        def confirm():
            msql = "SELECT prodid,prodname,mrp,quantity,totalcost FROM CART WHERE buyerid=\"%s\" and billed=\"no\";" % (uid)
            print(msql)
            mycursor.execute(msql)

            y = mycursor.rowcount
            print(y)
            if y == -1:
                messagebox.showwarning("Error", "ADD TO CART")
                return
            gsql="select sum(totalcost),sum(quantity) from cart where buyerid=%d and billed=\"no\";"%(int(uid))
            mycursor.execute(gsql)
            k=mycursor.fetchall()
            res= messagebox.askyesnocancel("Confirm", "Do you want to be packed in your name(additional charges applicable)?")
            print(res)
            if res==True:
                if pr.get()=="":
                    messagebox.showwarning("Error", "Enter printing name")
                    return

                last=messagebox.askyesno("Confirm", "Would you like to pay Rs. %d ?"%(int(k[0][0])+int(k[0][1])*2))
                if last==True:
                    asql = "SELECT * FROM transaction;"
                    pri=int(k[0][1])*2
                    total=int(k[0][0])+pri

                    mycursor.execute(asql)
                    a = mycursor.fetchall()
                    ar = mycursor.rowcount
                    billstr="T"+str(ar+1)
                    filestr=("bills/"+billstr+".txt")
                    osql = "SELECT prodid as CODE,prodname as NAME,mrp as RsPerpiece,quantity as QUANTITY,totalcost as TOTAL_COSTinRs from cart where buyerid=%d and billed=\"no\";" % (uid)

                    mycursor.execute(osql)
                    r_set = mycursor.fetchall()
                    r_rows= mycursor.rowcount
                    bill(uid,r_set,sum,pri,billstr,filestr,r_rows,total)
                    bsql="INSERT INTO transaction values(\"%s\",%d,%d,\"%s\",\"%s\",%d,now());"%(billstr,int(k[0][0]),pri,uid,filestr,total)
                    mycursor.execute(bsql)
                    osql = "SELECT distinct(prodid) from cart where buyerid=%d and billed=\"no\";" % (uid)

                    mycursor.execute(osql)
                    o = mycursor.fetchall()
                    oc = mycursor.rowcount
                    makestr = ""

                    for i in range(oc):

                        makestr = makestr + "\"" + o[i][0] + "\""
                        if i != oc - 1:
                            makestr = makestr + ","
                    print(makestr)
                    csql="UPDATE cart set billed=\"yes\" where prodid in(%s) and buyerid=\"%s\""%(makestr,uid)
                    mycursor.execute(csql)
                    messagebox.showinfo("Payment Done", "Bill generated")
                    for widget in self.root.winfo_children():
                        widget.destroy()
                    Login(root)
                else:
                    last = messagebox.askyesno("Confirm", "Would you like to pay %d?;"%(int(k[0][0])))
                    if last == True:
                        asql = "SELECT * FROM transaction;"
                        pri = 0
                        total = int(k[0][0])+ pri

                        mycursor.execute(asql)
                        a = mycursor.fetchall()
                        ar = mycursor.rowcount
                        billstr = "T" + str(ar + 1)
                        filestr = ("bills/" + billstr + ".txt")
                        osql = "SELECT prodid as CODE,prodname as NAME,mrp as RsPerpiece,quantity as QUANTITY,totalcost as TOTAL_COSTinRs from cart where buyerid=%d and billed=\"no\";" % (
                            uid)

                        mycursor.execute(osql)
                        r_set = mycursor.fetchall()
                        r_rows = mycursor.rowcount

                        bill(uid, r_set, sum, pri, billstr, filestr, r_rows, total)
                        bsql = "INSERT INTO transaction values(\"%s\",%d,%d,\"%s\",\"%s\",%d,now());" % (
                        billstr, int(k[0][0]), pri, uid, filestr, total)
                        mycursor.execute(bsql)
                        osql = "SELECT distinct(prodid) from cart where buyerid=%d and billed=\"no\";" % (uid)

                        mycursor.execute(osql)
                        o = mycursor.fetchall()
                        oc = mycursor.rowcount
                        makestr = ""

                        for i in range(oc):

                            makestr = makestr + "\"" + o[i][0] + "\""
                            if i != oc - 1:
                                makestr = makestr + ","
                        print(makestr)
                        csql = "UPDATE cart set billed=\"yes\" where prodid in(%s) and buyerid=\"%s\"" % (makestr, uid)
                        mycursor.execute(csql)
                        messagebox.showinfo("Payment Done","Bill generated")
                        for widget in self.root.winfo_children():
                            widget.destroy()
                        Login(root)




            elif res==False:
                last = messagebox.askyesno("Confirm","Would you like to pay %d ?" %(int(k[0][0])))
                if last==True:
                    asql = "SELECT * FROM transaction;"
                    pri=0
                    total=int(k[0][0])+pri

                    mycursor.execute(asql)
                    a = mycursor.fetchall()
                    ar = mycursor.rowcount
                    billstr="T"+str(ar+1)
                    filestr=("bills/"+billstr+".txt")
                    osql = "SELECT prodid as CODE,prodname as NAME,mrp as RsPerpiece,quantity as QUANTITY,totalcost as TOTAL_COSTinRs from cart where buyerid=%d and billed=\"no\";" % (
                        uid)

                    mycursor.execute(osql)
                    r_set = mycursor.fetchall()
                    r_rows = mycursor.rowcount
                    bill(uid,r_set,int(k[0][0]),pri,billstr,filestr,r_rows,total)
                    bsql="INSERT INTO transaction values(\"%s\",%d,%d,\"%s\",\"%s\",%d,now());"%(billstr,int(k[0][0]),pri,uid,filestr,total)
                    mycursor.execute(bsql)
                    osql = "SELECT distinct(prodid) from cart where buyerid=%d and billed=\"no\";" % (uid)

                    mycursor.execute(osql)
                    o = mycursor.fetchall()
                    oc = mycursor.rowcount
                    makestr = ""

                    for i in range(oc):

                        makestr = makestr + "\"" + o[i][0] + "\""
                        if i != oc - 1:
                            makestr = makestr + ","
                    print(makestr)
                    csql="UPDATE cart set billed=\"yes\" where prodid in(%s) and buyerid=\"%s\""%(makestr,uid)
                    mycursor.execute(csql)
                    messagebox.showinfo("Payment Done", "Bill generated")
                    for widget in self.root.winfo_children():
                        widget.destroy()
                    Login(root)
            elif res==None:
                return

        def add():
            if (quan.get() == "" or int(quan.get()) < 1):
                messagebox.showwarning("Error", "Enter proper quantity")
                return
            sql = "SELECT * FROM CART;"
            mycursor.execute(sql)
            d = mycursor.fetchall()
            c = mycursor.rowcount
            c = "C" + str(c + 1)
            print(c)
            quantity = int(quan.get())

            xsql = "SELECT * FROM CART where prodid=\"%s\" and buyerid=%d and billed=\"no\";"%(f[p][0],uid)
            mycursor.execute(xsql)
            ch = mycursor.fetchall()
            cht= mycursor.rowcount
            if cht==1:
                xsql = "UPDATE CART SET QUANTITY=QUANTITY+%d where prodid=\"%s\" and buyerid=%d and billed=\"no\";" % (quantity, f[p][0], uid)
                mycursor.execute(xsql)
                lsql = "UPDATE CART SET totalcost=mrp*quantity where prodid=\"%s\" and buyerid=%d and billed=\"no\";" % (f[p][0], uid)
                mycursor.execute(lsql)

            else:

                sql = "INSERT INTO CART VALUES (\"%s\",\"%s\",\"%s\",\"%s\",%d,%d,%d,'no');" % (
                c, uid, f[p][0], f[p][1], f[p][4], quantity, quantity * f[p][4])
                print(sql)
                mycursor.execute(sql)
            usql = "UPDATE product SET quantity=quantity-%d WHERE pid=\"%s\";" % (int(quantity), f[p][0])
            print(usql)

            mycursor.execute(usql)
            usql = "UPDATE department SET quantity=quantity-%d WHERE prodid=\"%s\";" % (int(quantity), f[p][0])
            mycursor.execute(usql)
            quan.delete(0, 'end')
            Red = Frame(Page_Frame, bg="red", width=400, height=500)
            Red.place(x=500, y=50)
            urcart = Label(Red, text="YOUR CART", font=("times new roman", 12, "bold", "italic", "underline"), fg="red",
                           bg="white")
            urcart.place(x=10, y=10)
            Red2 = Frame(Red, bg="red", width=400, height=300)
            Red2.place(x=0, y=50)

            b2 = Button(Page_Frame, text="Next", command=incr,
                        font=("times new roman", 8, "bold", "italic", "underline"),
                        bd=2, relief=GROOVE, bg="yellow", fg="black")
            b2.place(x=350, y=550)
            msql = "SELECT prodid as CODE,prodname as NAME,mrp as RsPerpiece,quantity as QUANTITY,totalcost as TOTAL_COSTinRs FROM CART WHERE buyerid=\"%s\" and billed=\"no\";" % (
                uid)

            mycursor.execute(msql)
            r_set = mycursor.fetchall()

            r_rows = mycursor.rowcount
            pd = mycursor.description

            quanti = 0
            sum = 0

            # ball=list()
            for j in range(5):
                e = Entry(Red2, width=12, bg="white", fg='black',
                          font=('Arial', 6, 'bold'))

                e.grid(row=0, column=j + 1)
                e.insert(END, pd[j][0])
            for i in range(r_rows):
                r_set[i] = list(r_set[i])
                sum = sum + int(r_set[i][4])
                quanti = quanti + r_set[i][3]
                for j in range(5):
                    e = Entry(Red2, width=12, bg="white", fg='black',
                              font=('Arial', 8, 'bold'))

                    e.grid(row=i + 1, column=j + 1)
                    e.insert(END, r_set[i][j])
            lb1 = Label(Red, text="PrintingName:", font=("times new roman", 12, "bold", "italic", "underline"),
                        fg="red", bg="white")
            lb1.place(x=10, y=380)
            global pr
            pr = Entry(Red, bg="white", bd=2, width=25, font=("", 12))
            pr.place(x=150, y=380)
            # lb2 = Label(Red, text="(if necessary, additional charges applicable)",font=("times new roman", 12,"italic"),fg="red", bg="white")
            # lb2(x=20,y=390)
            l = Label(Red, text="Total Price: Rs." + str(sum),
                      font=("times new roman", 12, "bold", "italic", "underline"),
                      fg="red", bg="white")
            l.place(x=100, y=410)

            blk = Button(Red, text="Proceed to pay", command=confirm, font=("arial", 12, "italic", "underline"), bd=2,
                         bg="yellow", relief=GROOVE)
            blk.place(x=100, y=450)







        Red1 = Frame(Page_Frame, bg="red", width=400, height=500)
        Red1.place(x=50, y=50)


        user=Label(Red1, text="UserID:"+str(uid), font=("times new roman", 20, "bold", "italic","underline"), fg="red", bg="white")
        user.place(x=10, y=40)


        bal=Balloon(Red1)

        img = f[p][1] + ".jpg"
        print(img)

        img_icon = ITk.PhotoImage(Image.open(img))
        l1 = Label(Red1, image=img_icon)
        l1.image = img_icon  # <== this is were we anchor the img object
        l1.configure(image=img_icon)
        l1.place(x=50, y=90)

        bal.bind_widget(l1, balloonmsg="Description:" + f[p][2])
        l2 = Label(Red1, text="Product Code:" + f[p][0],
                   font=("times new roman", 10, "bold", "italic", "underline"), fg="red", bg="white")
        l2.place(x=0, y=270)
        l3 = Label(Red1, text="Name:" + f[p][1], font=("times new roman", 10, "bold", "italic", "underline"),
                   fg="red", bg="white")
        l3.place(x=0, y=310)
        l4 = Label(Red1, text="Quantity:" , font=("times new roman", 10, "bold", "italic", "underline"),
                   fg="red", bg="white")
        l4.place(x=50, y=450)
        global quan
        quan=Entry(Red1, bg="white", bd=2, width=5, font=("", 12))
        quan.place(x=150,y=450)

        l5 = Label(Red1, text="Weight:" + f[p][3], font=("times new roman", 10, "bold", "italic", "underline"),
                   fg="red", bg="white")
        l5.place(x=0, y=350)
        l6 = Label(Red1, text="MRP:" + str(f[p][4]), font=("times new roman", 10, "bold", "italic", "underline"),
                   fg="red", bg="white")
        l6.place(x=0, y=390)
        b = Button(Red1, text="Add to cart", command=add,
                   font=("times new roman", 8, "bold", "italic", "underline"),
                   bd=2, relief=GROOVE, bg="yellow", fg="black")
        b.place(x=250, y=450)
        def decr():
            view(root,p-1,uid)
        def incr():
            view(root,p+1,uid)

        if p>0:

            b1 = Button(Page_Frame, text="Previous", command=decr,
                    font=("times new roman", 8, "bold", "italic", "underline"),
                    bd=2, relief=GROOVE, bg="yellow", fg="black")
            b1.place(x=250, y=550)
        if p<=r-1:

            b22= Button(Page_Frame, text="Next", command=incr,
                    font=("times new roman", 8, "bold", "italic", "underline"),
                    bd=2, relief=GROOVE, bg="yellow", fg="black")
            b22.place(x=350, y=550)
            if p==r-1:
                b22.destroy()


        Red = Frame(Page_Frame, bg="red", width=400, height=500)
        Red.place(x=500, y=50)
        urcart = Label(Red, text="YOUR CART", font=("times new roman", 12, "bold", "italic", "underline"), fg="red",
                       bg="white")
        urcart.place(x=10, y=10)
        Red2 = Frame(Red, bg="red", width=400, height=300)
        Red2.place(x=0, y=50)


        msql= "SELECT prodid as CODE,prodname as NAME,mrp as RsPerpiece,quantity as QUANTITY,totalcost as TOTAL_COSTinRs FROM CART WHERE buyerid=\"%s\" and billed=\"no\";" % (uid)
        print(msql)
        mycursor.execute(msql)
        r_set=mycursor.fetchall()

        r_rows = mycursor.rowcount
        pd=mycursor.description
        #b = Button(self.e,text="Remove", command=None, font=("arial", 6, "italic", "underline"),
         #          bd=0,
          #         bg="yellow", relief=GROOVE)
        global sum,quanti
        quanti=0
        sum=0
        global e
        #ball=list()
        for j in range(5):
            e = Entry(Red2, width=12, bg="white", fg='black',
                      font=('Arial', 6, 'bold'))

            e.grid(row=0, column=j + 1)
            e.insert(END, pd[j][0])
        for i in range(r_rows):
            r_set[i]=list(r_set[i])
            sum=sum+int(r_set[i][4])
            quanti=quanti+r_set[i][3]
            for j in range(5):

                e = Entry(Red2, width=12,bg="white" ,fg='black',
                               font=('Arial', 8, 'bold'))


                e.grid(row=i+1, column=j+1)
                e.insert(END, r_set[i][j])
        lb1=Label(Red, text="PrintingName:", font=("times new roman", 12, "bold", "italic", "underline"),
                   fg="red", bg="white")
        lb1.place(x=10,y=380)
        global pr
        pr= Entry(Red, bg="white", bd=2, width=25, font=("", 12))
        pr.place(x=150, y=380)
        #lb2 = Label(Red, text="(if necessary, additional charges applicable)",font=("times new roman", 12,"italic"),fg="red", bg="white")
        #lb2(x=20,y=390)
        l= Label(Red, text="Total Price: Rs." + str(sum), font=("times new roman", 12, "bold", "italic", "underline"),
                   fg="red", bg="white")
        l.place(x=100,y=410)




        blk = Button(Red, text="Proceed to pay", command=confirm, font=("arial", 12, "italic", "underline"),bd=2,bg="yellow", relief=GROOVE)
        blk.place(x=100,y=450)


class admin(Base):
    def __init__(self,root):
        super().__init__(root)

        A_Frame = Frame(self.root, bg="red", width=420, height=420)
        A_Frame.place(x=10, y=100)
        Red1 = Frame(A_Frame, bg="yellow", width=350, height=350)
        Red1.place(x=20, y=20)

        def viewmsg():

            A_Frame = Frame(self.root, bg="red", width=1000, height=1000)
            A_Frame.place(x=600, y=100)
            Red2 = Frame(A_Frame, bg="red", width=1000, height=1000)
            Red2.place(x=0, y=0)
            vsql = "SELECT fmsg from feedback where readmsg=\"no\";"
            print(vsql)
            mycursor.execute(vsql)
            v_set = mycursor.fetchall()

            v_rows = mycursor.rowcount
            p = mycursor.description

            if v_rows==0:
                lab=Label(Red2, text="None" , font=("times new roman", 10, "bold", "italic", "underline"),
                   fg="red", bg="white")
                lab.place(x=100,y=100)
            else:
                for i in range(v_rows):
                    v_set[i] = list(v_set[i])

                    e = Entry(Red2, width=50, bg="white", fg='black',
                                  font=('Arial', 8, 'bold'))

                    e.grid(row=i, column=i)
                    e.insert(END, v_set[i][0])
                vsql = "UPDATE feedback set readmsg=\"yes\";"
                print(vsql)
                mycursor.execute(vsql)
        def commsg():

            A_Frame = Frame(self.root, bg="red", width=1000, height=1000)
            A_Frame.place(x=600, y=100)
            Red2 = Frame(A_Frame, bg="red", width=1000, height=1000)
            Red2.place(x=0, y=0)
            vsql = "SELECT mid,msg from message where readmsg=\"no\";"
            print(vsql)
            mycursor.execute(vsql)
            v_set = mycursor.fetchall()

            v_rows = mycursor.rowcount
            p = mycursor.description
            if v_rows==0:
                lab=Label(Red2, text="None" , font=("times new roman", 10, "bold", "italic", "underline"),
                   fg="red", bg="white")
                lab.place(x=100,y=100)
            else:
                for j in range(2):
                    e = Entry(Red2, width=12, bg="white", fg='black',
                              font=('Arial', 6, 'bold'))

                    e.grid(row=0, column=j + 1)
                    e.insert(END, p[j][0])
                for i in range(v_rows):
                    for j in range(2):
                        e = Entry(Red2, width=20, bg="white", fg='black',
                                  font=('Arial', 8, 'bold'))

                        e.grid(row=i+1, column=j)
                        e.insert(END,v_set[i][j])
                vsql = "UPDATE message set readmsg=\"yes\";"
                print(vsql)
                mycursor.execute(vsql)



        def shop():
            A_Frame = Frame(self.root, bg="red", width=1000, height=1000)
            A_Frame.place(x=600, y=100)
            Red2 = Frame(A_Frame, bg="red", width=1000, height=1000)
            Red2.place(x=0, y=0)

            def setDate1():

                fdate.delete(0, 'end')
                d1 = myCal1.get_date()
                fdate.insert(0, d1)

                choose1.destroy()
                myCal1.destroy()


            def getDate1():
                global myCal1
                myCal1 = Calendar(Red2, setmode='day', date_pattern='yyyy-mm-dd')
                myCal1.place(x=30, y=50)
                global choose1
                choose1= Button(Red2, text="Choose", command=setDate1, font=("arial", 10, "bold"), bd=5,
                                relief=GROOVE)
                choose1.place(x=150, y=250)

            def setDate2():
                tdate.delete(0, 'end')

                d2 = myCal2.get_date()
                tdate.insert(0,d2)
                choose2.destroy()
                myCal2.destroy()


            def getDate2():
                global myCal2
                myCal2 = Calendar(Red2, setmode='day', date_pattern='yyyy-mm-dd')
                myCal2.place(x=110, y=50)
                global choose2
                choose2 = Button(Red2, text="Choose", command=setDate2, font=("arial", 10, "bold"), bd=5,
                                 relief=GROOVE)
                choose2.place(x=300, y=250)

            froml=Label(Red2, text="FROM:", font=("arial", 8, "bold", "italic"), fg="white", bg="grey")
            froml.place(x=20,y=20)
            fdate = Entry(Red2, bg="white",fg="black", bd=2, width=10, font=("", 10))
            fdate.place(x=60, y=20)
            tol= Label(Red2, text="TO:", font=("arial", 8, "bold", "italic"), fg="white", bg="grey")
            tol.place(x=150, y = 20)
            tdate = Entry(Red2, bg="white", fg="black", bd=2, width=10, font=("", 10))
            tdate.place(x=200, y=20)
            cal1= Button(Red2, text="calendar", command=getDate1, font=("arial", 6), bd=1, relief=GROOVE)
            cal1.place(x=80, y=40)
            cal2= Button(Red2, text="calendar", command=getDate2, font=("arial", 6), bd=1, relief=GROOVE)
            cal2.place(x=240, y=40)


            def submit():
                if fdate.get()!="" and tdate.get()!="":
                    vsql = "SELECT transid,buyerid,totalprice,purdate from transaction where purdate between \"%s\" and \"%s\";"%(str(fdate.get()),str(tdate.get()))
                    print(vsql)
                    mycursor.execute(vsql)
                    v_set = mycursor.fetchall()
                    p = mycursor.description
                    v_rows = mycursor.rowcount
                    if v_rows == 0:
                        lab = Label(Red2, text="None", font=("times new roman", 10, "bold", "italic", "underline"),
                                    fg="red", bg="white")
                        lab.place(x=100, y=300)
                    else:

                        for j in range(4):
                            e = Entry(Red2, width=12, bg="white", fg='black',
                                      font=('Arial', 6, 'bold'))

                            e.grid(row=0, column=j + 1)
                            e.insert(END, p[j][0])
                        shopsum=0
                        for i in range(v_rows):
                            shopsum=shopsum+v_set[i][2]
                            for j in range(4):
                                e = Entry(Red2, width=12, bg="white", fg='black',
                                          font=('Arial', 8, 'bold'))

                                e.grid(row=i+1, column=j + 1)
                                e.insert(END, v_set[i][j])
                        messagebox.showinfo("Income","In the given period,amount recieved is Rs." + str(shopsum))

                else:
                    messagebox.showwarning("NOT ENTERED", "FILL DATES")


            sub = Button(Red2, text="SUBMIT", command=submit, font=("arial", 6), bd=1, relief=GROOVE)
            sub.place(x=100, y=100)
        def supply():
            A_Frame = Frame(self.root, bg="red", width=1000, height=1000)
            A_Frame.place(x=600, y=100)
            Red2 = Frame(A_Frame, bg="red", width=1000, height=1000)
            Red2.place(x=0, y=0)

            def setDate1():
                fdate.delete(0, 'end')
                d1 = myCal1.get_date()
                fdate.insert(0, d1)

                choose1.destroy()
                myCal1.destroy()

            def getDate1():
                global myCal1
                myCal1 = Calendar(Red2, setmode='day', date_pattern='yyyy-mm-dd')
                myCal1.place(x=30, y=50)
                global choose1
                choose1 = Button(Red2, text="Choose", command=setDate1, font=("arial", 10, "bold"), bd=5,
                                 relief=GROOVE)
                choose1.place(x=150, y=250)

            def setDate2():
                tdate.delete(0, 'end')

                d2 = myCal2.get_date()
                tdate.insert(0, d2)
                choose2.destroy()
                myCal2.destroy()

            def getDate2():
                global myCal2
                myCal2 = Calendar(Red2, setmode='day', date_pattern='yyyy-mm-dd')
                myCal2.place(x=110, y=50)
                global choose2
                choose2 = Button(Red2, text="Choose", command=setDate2, font=("arial", 10, "bold"), bd=5,
                                 relief=GROOVE)
                choose2.place(x=300, y=250)

            froml = Label(Red2, text="FROM:", font=("arial", 8, "bold", "italic"), fg="white", bg="grey")
            froml.place(x=20, y=20)
            fdate = Entry(Red2, bg="white", fg="black", bd=2, width=10, font=("", 10))
            fdate.place(x=60, y=20)
            tol = Label(Red2, text="TO:", font=("arial", 8, "bold", "italic"), fg="white", bg="grey")
            tol.place(x=150, y=20)
            tdate = Entry(Red2, bg="white", fg="black", bd=2, width=10, font=("", 10))
            tdate.place(x=200, y=20)
            cal1 = Button(Red2, text="calendar", command=getDate1, font=("arial", 6), bd=1, relief=GROOVE)
            cal1.place(x=80, y=40)
            cal2 = Button(Red2, text="calendar", command=getDate2, font=("arial", 6), bd=1, relief=GROOVE)
            cal2.place(x=240, y=40)

            def submit():
                if fdate.get() != "" and tdate.get() != "":
                    vsql = "SELECT * from rawpurchase where purchase between \"%s\" and \"%s\";" % (str(fdate.get()), str(tdate.get()))
                    print(vsql)
                    mycursor.execute(vsql)
                    v_set = mycursor.fetchall()
                    p = mycursor.description
                    v_rows = mycursor.rowcount
                    if v_rows == 0:
                        lab = Label(Red2, text="None", font=("times new roman", 10, "bold", "italic", "underline"),
                                    fg="red", bg="white")
                        lab.place(x=100, y=300)
                    else:
                        for j in range(6):
                            e = Entry(Red2, width=12, bg="white", fg='black',
                                      font=('Arial', 6, 'bold'))

                            e.grid(row=0, column=j + 1)
                            e.insert(END, p[j][0])
                        supplysum=0
                        for i in range(v_rows):
                            supplysum=supplysum+v_set[i][4]
                            for j in range(6):
                                e = Entry(Red2, width=12, bg="white", fg='black',
                                          font=('Arial', 8, 'bold'))

                                e.grid(row=i+1, column=j + 1)
                                e.insert(END, v_set[i][j])
                        messagebox.showinfo("Expenditure","In the given period,Raw inut purchase is made for Rs."+str(supplysum))
                        
                else:
                    messagebox.showwarning("NOT ENTERED", "FILL DATES")

            sub = Button(Red2, text="SUBMIT", command=submit, font=("arial", 6), bd=1, relief=GROOVE)
            sub.place(x=100, y=100)
        def dept():
            A_Frame = Frame(self.root, bg="red", width=1000, height=1000)
            A_Frame.place(x=600, y=100)
            Red2 = Frame(A_Frame, bg="red", width=1000, height=1000)
            Red2.place(x=0, y=0)
            vsql = "select d.deptid,d.deptname,d.prodid,d.quantity,p.weight,p.mrp from department d inner join product p on d.prodid=p.pid;"
            print(vsql)
            mycursor.execute(vsql)
            v_set = mycursor.fetchall()
            p = mycursor.description
            v_rows = mycursor.rowcount
            if v_rows == 0:
                lab = Label(Red2, text="None", font=("times new roman", 10, "bold", "italic", "underline"),
                            fg="red", bg="white")
                lab.place(x=100, y=100)
            else:
                for j in range(6):
                    e = Entry(Red2, width=12, bg="white", fg='black',
                              font=('Arial', 8, 'bold'))

                    e.grid(row=0, column=j + 1)
                    e.insert(END, p[j][0])
                for i in range(v_rows):
                    for j in range(6):
                        e = Entry(Red2, width=12, bg="white", fg='black',
                                  font=('Arial', 8, 'bold'))

                        e.grid(row=i+1, column=j + 1)
                        e.insert(END, v_set[i][j])

        def workers():
            A_Frame = Frame(self.root, bg="red", width=1000, height=1000)
            A_Frame.place(x=600, y=100)
            Red2 = Frame(A_Frame, bg="red", width=1000, height=1000)
            Red2.place(x=0, y=0)
            vsql = "select * from worker;"
            print(vsql)
            mycursor.execute(vsql)
            v_set = mycursor.fetchall()

            v_rows = mycursor.rowcount

            p=mycursor.description
            if v_rows == 0:
                lab = Label(Red2, text="None", font=("times new roman", 10, "bold", "italic", "underline"),
                            fg="red", bg="white")
                lab.place(x=100, y=100)
            else:

                for j in range(14):
                    e = Entry(Red2, width=12, bg="white", fg='black',
                              font=('Arial', 8, 'bold'))

                    e.grid(row=0, column=j + 2)
                    e.insert(END, p[j][0])


                for i in range(v_rows):
                    for j in range(14):
                        e = Entry(Red2, width=12, bg="white", fg='black',
                                  font=('Arial', 8, 'bold'))

                        e.grid(row=i+1, column=j + 2)
                        e.insert(END, v_set[i][j])
        def addbonus():
            A_Frame= Frame(self.root, bg="red", width=1000, height=1000)
            A_Frame.place(x=600, y=100)
            Red2= Frame(A_Frame, bg="red", width=1000, height=1000)
            Red2.place(x=0, y=0)
            quant = Label(Red2, text="BONUS PERCENTAGE:", font=("arial", 8, "bold", "italic"), fg="white", bg="grey")
            quant.place(x=50, y=100)
            inq = Entry(Red2, bg="white", fg="black", bd=2, width=10, font=("", 10))
            inq.place(x=150, y=100)

            def upd():
                vsql = "UPDATE worker set salary=salary+((%d/100)*salary) " % (int(inq.get()))
                print(vsql)
                mycursor.execute(vsql)
                inq.delete(0, 'end')


            B1 = Button(Red2, text="INSERT", command=upd, font=("arial", 12, "italic"), bd=2, bg="yellow",
                        fg="black", relief=GROOVE)
            B1.place(x=100, y=200)

        B1=Button(Red1, text="View Feedback", command=viewmsg, font=("arial", 12, "italic"),bd=2,bg="red",fg="white",relief=GROOVE)
        B1.place(x=50,y=10)
        B2 = Button(Red1, text="View Messages", command=commsg, font=("arial", 12, "italic"), bd=2,
                    bg="red", fg="white", relief=GROOVE)
        B2.place(x=50, y=50)

        B3=Button(Red1, text="ADD BONUS", command=addbonus, font=("arial", 12, "italic"), bd=2,
               bg="red", fg="white", relief=GROOVE)
        B3.place(x=50,y=100)
        B4=Button(Red1, text="View Shopping", command=shop, font=("arial", 12, "italic"), bd=2,
                    bg="red", fg="white", relief=GROOVE)
        B4.place(x=50,y=150)
        B5 = Button(Red1, text="View Supply", command=supply, font=("arial", 12, "italic"), bd=2,
                    bg="red", fg="white", relief=GROOVE)
        B5.place(x=50, y=200)
        B6 = Button(Red1, text="View Department", command=dept, font=("arial", 12, "italic"), bd=2,
                    bg="red", fg="white", relief=GROOVE)
        B6.place(x=50, y=250)

        B7= Button(Red1, text="View Staff", command=workers, font=("arial", 12, "italic"), bd=2,
                    bg="red", fg="white", relief=GROOVE)
        B7.place(x=50, y=300)



class stock(Base):
    def __init__(self,root,wid):
        super().__init__(root)

        A_Frame = Frame(self.root, bg="grey", width=2000, height=1000)
        A_Frame.place(x=400, y=100)
        Red1 = Frame(A_Frame, bg="red", width=400, height=500)
        Red1.place(x=50, y=50)
        vsql = " select w.workerid,w.workername,w.position,w.deptid,d.deptname,w.supervisor,w.salary,d.prodid from worker w inner join department d on d.deptid=w.deptid where workerid =\"%s\";"%(wid)
        print(vsql)
        mycursor.execute(vsql)
        f= mycursor.fetchall()
        print(f)
        v_rows = mycursor.rowcount
        id= Label(Red1, text="ID:" + f[0][0],
                   font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        id.place(x=10, y=10)
        name= Label(Red1, text="Name:" + f[0][1],
                   font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        name.place(x=10, y=30)
        role= Label(Red1, text="Role:" + f[0][2],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        role.place(x=10, y=60)
        did= Label(Red1, text="Dept ID:" + f[0][3],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        did.place(x=10, y=90)
        dname = Label(Red1, text="Dept Name:" + f[0][4],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        dname.place(x=10, y=120)
        sup = Label(Red1, text="Supervisor:" + f[0][5],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        sup.place(x=10, y=150)
        dept=f[0][3]
        sal = Label(Red1, text="Salary:Rs." + str(f[0][6]),
                    font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        sal.place(x=10, y=180)



        def shift():
            Red = Frame(A_Frame, bg="red", width=400, height=500)
            Red.place(x=500, y=50)
            Red2 = Frame(Red, bg="red", width=400, height=500)
            Red2.place(x=0, y=0)
            vsql="SELECT workerid,workername,position FROM worker WHERE position IN (\"SHIFT 1 MANAGER\",\"SHIFT 2 MANAGER\") AND deptid=\"%s\";"%(dept)
            print(vsql)
            mycursor.execute(vsql)
            v_set = mycursor.fetchall()
            p = mycursor.description
            v_rows = mycursor.rowcount
            if v_rows == 0:
                lab = Label(Red2, text="None", font=("times new roman", 10, "bold", "italic", "underline"),
                            fg="red", bg="white")
                lab.place(x=100, y=100)
            else:
                for j in range(3):
                    e = Entry(Red2, width=18, bg="white", fg='black',
                              font=('Arial', 6, 'bold'))

                    e.grid(row=0, column=j + 1)
                    e.insert(END, p[j][0])
                for i in range(v_rows):
                    for j in range(3):
                        e = Entry(Red2, width=18, bg="white", fg='black',
                                  font=('Arial', 8, 'bold'))

                        e.grid(row=i+1, column=j + 1)
                        e.insert(END, v_set[i][j])

        def shift1():
            Red = Frame(A_Frame, bg="red", width=400, height=500)
            Red.place(x=500, y=50)
            Red2 = Frame(Red, bg="red", width=400, height=500)
            Red2.place(x=0, y=0)
            vsql = "SELECT workerid,workername,position FROM worker WHERE position=\"EMPLOYEE\" AND supervisor=\"SHIFT 1 MANAGER\" AND deptid=\"%s\";" % (dept)
            print(vsql)
            mycursor.execute(vsql)
            v_set = mycursor.fetchall()
            p = mycursor.description
            v_rows = mycursor.rowcount
            if v_rows == 0:
                lab = Label(Red2, text="None", font=("times new roman", 10, "bold", "italic", "underline"),
                            fg="red", bg="white")
                lab.place(x=100, y=100)
            else:
                for j in range(3):
                    e = Entry(Red2, width=18, bg="white", fg='black',
                              font=('Arial', 6, 'bold'))

                    e.grid(row=0, column=j + 1)
                    e.insert(END, p[j][0])
                for i in range(v_rows):
                    for j in range(3):
                        e = Entry(Red2, width=18, bg="white", fg='black',
                                  font=('Arial', 8, 'bold'))

                        e.grid(row=i+1, column=j + 1)
                        e.insert(END, v_set[i][j])
        def shift2():
            Red = Frame(A_Frame, bg="red", width=400, height=500)
            Red.place(x=500, y=50)
            Red2 = Frame(Red, bg="red", width=400, height=500)
            Red2.place(x=0, y=0)
            vsql = "SELECT workerid,workername,position FROM worker WHERE position=\"EMPLOYEE\" AND supervisor=\"SHIFT 2 MANAGER\" AND deptid=\"%s\";" % (
                dept)
            print(vsql)
            mycursor.execute(vsql)
            v_set = mycursor.fetchall()
            p = mycursor.description
            v_rows = mycursor.rowcount
            if v_rows == 0:
                lab = Label(Red2, text="None", font=("times new roman", 10, "bold", "italic", "underline"),
                            fg="red", bg="white")
                lab.place(x=100, y=100)
            else:
                for j in range(3):
                    e = Entry(Red2, width=18, bg="white", fg='black',
                              font=('Arial', 6, 'bold'))

                    e.grid(row=0, column=j + 1)
                    e.insert(END, p[j][0])
                for i in range(v_rows):
                    for j in range(3):
                        e = Entry(Red2, width=18, bg="white", fg='black',
                                  font=('Arial', 8, 'bold'))

                        e.grid(row=i+1, column=j + 1)
                        e.insert(END, v_set[i][j])
        def supplies():
            Red = Frame(A_Frame, bg="red", width=400, height=500)
            Red.place(x=500, y=50)
            Red2 = Frame(Red, bg="red", width=400, height=500)
            Red2.place(x=0, y=0)
            vsql = "SELECT supplyid,supplyname,composition,priceperunit FROM rawinput;"
            print(vsql)
            mycursor.execute(vsql)
            v_set = mycursor.fetchall()
            p = mycursor.description
            v_rows = mycursor.rowcount
            if v_rows == 0:
                lab = Label(Red2, text="None", font=("times new roman", 10, "bold", "italic", "underline"),
                            fg="red", bg="white")
                lab.place(x=100, y=100)
            else:
                for j in range(4):
                    e = Entry(Red2, width=18, bg="white", fg='black',
                              font=('Arial', 6, 'bold'))

                    e.grid(row=0, column=j + 1)
                    e.insert(END, p[j][0])
                for i in range(v_rows):
                    for j in range(4):
                        e = Entry(Red2, width=18, bg="white", fg='black',
                                  font=('Arial', 8, 'bold'))

                        e.grid(row=i+1, column=j + 1)
                        e.insert(END, v_set[i][j])
        def purchase():
            Red = Frame(A_Frame, bg="red", width=400, height=500)
            Red.place(x=500, y=50)
            Red2 = Frame(Red, bg="red", width=400, height=500)
            Red2.place(x=0, y=0)
            make= Label(Red2, text="MAKE YOUR PURCHASE", font=("arial", 12, "bold", "italic","underline"), fg="white", bg="grey")
            make.place(x=20, y=20)
            sid = Label(Red2, text="SUPPLY ID:", font=("arial", 8, "bold", "italic"), fg="white",
                         bg="grey")
            sid.place(x=20, y=60)
            supply = Entry(Red2, bg="white", fg="black", bd=2, width=10, font=("", 8))
            supply.place(x=100, y=60)
            qu= Label(Red2, text="ENTER QUANTITY:", font=("arial", 8, "bold", "italic"), fg="white",
                        bg="grey")
            qu.place(x=20, y=90)

            qua = Entry(Red2, bg="white", fg="black", bd=2, width=10, font=("", 8))
            qua.place(x=200, y=90)
            def conf():
                if supply.get()!="" and qua.get()!="":
                    s=supply.get()
                    vsql = "SELECT supplyname,composition,priceperunit from rawinput where supplyid=\"%s\";"%(s)
                    print(vsql)
                    mycursor.execute(vsql)
                    v= mycursor.fetchall()

                    v_rows = mycursor.rowcount
                    if v_rows==0:
                        messagebox.showwarning("Error", "No such supplier")
                    else:
                        last = messagebox.askyesno("Please Confirm", "Purchased %s from %s and paid Rs. %d?" % (v[0][1],v[0][0],int(v[0][2])*int(qua.get())))
                        if last==True:
                            vsql = "INSERT INTO rawpurchase(supplyid,item,quantity,totalcost,purchase,deptid) values(\"%s\",\"%s\",%d,%d,now(),\"%s\");"%(s,v[0][1],int(qua.get()),int(v[0][2])*int(qua.get()),f[0][3])
                            print(vsql)
                            mycursor.execute(vsql)


                        else:
                            return
                    stock(root,wid)
                else:
                    messagebox.showwarning("Error", "Enter all columns")





            B1 = Button(Red2, text="Purchased", command=conf, font=("arial", 12, "italic"), bd=2, bg="yellow",
                        fg="black", relief=GROOVE)
            B1.place(x=100, y=130)


            
        def goods():
            Red = Frame(A_Frame, bg="red", width=400, height=500)
            Red.place(x=500, y=50)
            Red2 = Frame(Red, bg="red", width=400, height=500)
            Red2.place(x=0, y=0)
            vsql = "SELECT * from rawpurchase"
            print(vsql)
            mycursor.execute(vsql)
            v_set = mycursor.fetchall()
            p = mycursor.description
            v_rows = mycursor.rowcount
            if v_rows == 0:
                lab = Label(Red2, text="None", font=("times new roman", 10, "bold", "italic", "underline"),
                            fg="red", bg="white")
                lab.place(x=100, y=100)
            else:
                for j in range(6):
                    e = Entry(Red2, width=8, bg="white", fg='black',
                              font=('Arial', 6, 'bold'))

                    e.grid(row=0, column=j + 1)
                    e.insert(END, p[j][0])

                for i in range(v_rows):
                    for j in range(6):
                        e = Entry(Red2, width=8, bg="white", fg='black',
                                  font=('Arial', 8, 'bold'))

                        e.grid(row=i+1, column=j + 1)
                        e.insert(END, v_set[i][j])

        def addquan():
            Red = Frame(A_Frame, bg="red", width=400, height=500)
            Red.place(x=500, y=50)
            Red2 = Frame(Red, bg="red", width=400, height=500)
            Red2.place(x=0, y=0)
            quant = Label(Red2, text="ENTER QUANTITY:", font=("arial", 8, "bold", "italic"), fg="white", bg="grey")
            quant.place(x=50, y=100)
            inq = Entry(Red2, bg="white", fg="black", bd=2, width=10, font=("", 10))
            inq.place(x=150, y=100)

            def upd():
                vsql = "UPDATE department set quantity=quantity+%d where prodid=\"%s\""%(int(inq.get()),str(f[0][7]))
                print(vsql)
                mycursor.execute(vsql)
                vsql = "UPDATE product set quantity=quantity+%d where pid=\"%s\""%(int(inq.get()),str(f[0][7]))
                print(vsql)
                mycursor.execute(vsql)
                inq.delete(0, 'end')

            B1 = Button(Red2, text="INSERT", command=upd, font=("arial", 12, "italic"), bd=2, bg="yellow",
                        fg="black", relief=GROOVE)
            B1.place(x=200, y=200)


        B1 = Button(Red1, text="View Shift Managers", command=shift, font=("arial", 12, "italic"), bd=2, bg="red",
                    fg="white", relief=GROOVE)
        B1.place(x=50, y=220)
        B2 = Button(Red1, text="View SHIFT1 EMPLOYEES ", command=shift1, font=("arial", 12, "italic"), bd=2,
                    bg="red", fg="white", relief=GROOVE)
        B2.place(x=50, y=260)

        B3 = Button(Red1, text="View SHIFT2 EMPLOYEES ", command=shift2, font=("arial", 12, "italic"), bd=2,
                    bg="red", fg="white", relief=GROOVE)
        B3.place(x=50, y=300)
        B4 = Button(Red1, text="View Supplies", command=supplies, font=("arial", 12, "italic"), bd=2,
                    bg="red", fg="white", relief=GROOVE)
        B4.place(x=50, y=340)
        B5 = Button(Red1, text="ADD Purchases", command=purchase, font=("arial", 12, "italic"), bd=2,
                    bg="red", fg="white", relief=GROOVE)
        B5.place(x=50, y=380)
        B6 = Button(Red1, text="Import Goods", command=goods, font=("arial", 12, "italic"), bd=2,
                    bg="red", fg="white", relief=GROOVE)
        B6.place(x=50, y=420)
        B7 = Button(Red1, text="Add Quantity", command=addquan, font=("arial", 12, "italic"), bd=2,
                    bg="red", fg="white", relief=GROOVE)
        B7.place(x=50, y=460)


class shift(Base):
    def __init__(self,root,wid):
        super().__init__(root)

        A_Frame = Frame(self.root, bg="grey", width=2000, height=1000)
        A_Frame.place(x=400, y=100)
        Red1 = Frame(A_Frame, bg="red", width=400, height=500)
        Red1.place(x=50, y=50)
        vsql = " select w.workerid,w.workername,w.position,w.deptid,d.deptname,w.supervisor,w.salary from worker w inner join department d on d.deptid=w.deptid where workerid =\"%s\";"%(wid)
        print(vsql)
        mycursor.execute(vsql)
        f= mycursor.fetchall()
        print(f)
        v_rows = mycursor.rowcount
        id= Label(Red1, text="ID:" + f[0][0],
                   font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        id.place(x=10, y=10)
        name= Label(Red1, text="Name:" + f[0][1],
                   font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        name.place(x=10, y=40)
        role= Label(Red1, text="Role:" + f[0][2],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        role.place(x=10, y=70)
        did= Label(Red1, text="Dept ID:" + f[0][3],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        did.place(x=10, y=100)
        dname = Label(Red1, text="Dept Name:" + f[0][4],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        dname.place(x=10, y=130)
        sup = Label(Red1, text="Supervisor:" + f[0][5],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        sup.place(x=10, y=160)
        sal = Label(Red1, text="Salary:Rs." +str(f[0][6]),
                    font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        sal.place(x=10, y=190)
        vsql = " select workerid,workername from worker where deptid=\"%s\" and supervisor=\"Main admin\";"%(f[0][3])
        print(vsql)
        mycursor.execute(vsql)
        g = mycursor.fetchall()
        v_rows = mycursor.rowcount
        supid = Label(Red1, text="Supervisor id:" + g[0][0],
                    font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        supid.place(x=10, y=220)
        supname = Label(Red1, text="Supervisor name:" + g[0][1],
                    font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        supname.place(x=10, y=250)
        def emp():
            Red = Frame(A_Frame, bg="red", width=400, height=500)
            Red.place(x=500, y=50)
            Red2 = Frame(Red, bg="red", width=400, height=500)
            Red2.place(x=0, y=0)
            vsql = "SELECT workerid,workername,position FROM worker WHERE position=\"EMPLOYEE\" AND supervisor=\"%s\" AND deptid=\"%s\";" % (str(f[0][2]),str(f[0][3]))
            print(vsql)
            mycursor.execute(vsql)
            v_set = mycursor.fetchall()
            p = mycursor.description
            v_rows = mycursor.rowcount
            if v_rows == 0:
                lab = Label(Red2, text="None", font=("times new roman", 10, "bold", "italic", "underline"),
                            fg="red", bg="white")
                lab.place(x=100, y=100)
            else:
                for j in range(3):
                    e = Entry(Red2, width=18, bg="white", fg='black',
                              font=('Arial', 6, 'bold'))

                    e.grid(row=0, column=j + 1)
                    e.insert(END, p[j][0])
                for i in range(v_rows):
                    for j in range(3):
                        e = Entry(Red2, width=18, bg="white", fg='black',
                                  font=('Arial', 8, 'bold'))

                        e.grid(row=i+1, column=j + 1)
                        e.insert(END, v_set[i][j])


        B1 = Button(Red1, text="View Employees", command=emp, font=("arial", 12, "italic"), bd=2, bg="red",
                    fg="white", relief=GROOVE)
        B1.place(x=10, y=280)

class employee(Base):
    def __init__(self,root,wid):
        super().__init__(root)

        A_Frame = Frame(self.root, bg="grey", width=2000, height=1000)
        A_Frame.place(x=400, y=100)
        Red1 = Frame(A_Frame, bg="red", width=400, height=500)
        Red1.place(x=50, y=50)
        vsql = " select w.workerid,w.workername,w.position,w.deptid,d.deptname,w.supervisor,w.salary from worker w inner join department d on d.deptid=w.deptid where workerid =\"%s\";"%(wid)
        print(vsql)
        mycursor.execute(vsql)
        f= mycursor.fetchall()
        print(f)
        v_rows = mycursor.rowcount
        id= Label(Red1, text="ID:" + f[0][0],
                   font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        id.place(x=10, y=10)
        name= Label(Red1, text="Name:" + f[0][1],
                   font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        name.place(x=10, y=40)
        role= Label(Red1, text="Role:" + f[0][2],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        role.place(x=10, y=70)
        did= Label(Red1, text="Dept ID:" + f[0][3],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        did.place(x=10, y=100)
        dname = Label(Red1, text="Dept Name:" + f[0][4],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        dname.place(x=10, y=130)
        sup = Label(Red1, text="Supervisor:" + f[0][5],
                     font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        sup.place(x=10, y=160)
        sal = Label(Red1, text="Salary:Rs." + str(f[0][6]),
                    font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        sal.place(x=10, y=190)
        vsql = " select workerid,workername from worker where deptid=\"%s\" and supervisor=\"Main admin\";"%(f[0][3])
        print(vsql)
        mycursor.execute(vsql)
        g = mycursor.fetchall()
        v_rows = mycursor.rowcount
        supid = Label(Red1, text="Supervisor id:" + g[0][0],
                    font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        supid.place(x=10, y=220)
        supname = Label(Red1, text="Supervisor name:" + g[0][1],
                    font=("times new roman", 8, "bold", "italic", "underline"), fg="red", bg="white")
        supname.place(x=10, y=250)










root=Tk()
obj=Login(root)
root.mainloop()




#C:\Users\Kavya\OneDrive\Documents\zoom\2020-10-22 16.31.40 1nh18cs118 n kavya's personal meeting room 7744259661

