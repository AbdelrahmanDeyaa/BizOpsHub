from tkinter import *
import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import webbrowser
class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Inventory Management System | Login")
        self.root.geometry("1350x750+150+150")
        self.root.resizable(False,False)
        self.root.config(bg="#fafafa")
        root.iconbitmap('images/logo.ico')

        #=======images=======
        self.phone_image=ImageTk.PhotoImage(file="images/pngwing13.png")
        self.lbl_Phone_image=Label(self.root,image=self.phone_image,bd=0,bg="#fafafa").place(x=100,y=60)
      
        #=======Login_Farme=======
        self.name=StringVar()
        self.password=StringVar()
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="User Name",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=120)
        txt_username=Entry(login_frame,textvariable=self.name,font=("times new roman",15),bg="#ECECEC").place(x=50,y=170,width=250)

        lbl_pass=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=240)
        txt_pss=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=290,width=250)

        btn_login=Button(login_frame,command=self.login,text="Login",font=("Arial Rounded MT Bold",15,"bold"),bg="#00B0F0",fg="white",activebackground="#00B0F0",activeforeground="white",cursor="hand2").place(x=50,y=370,width=250,height=35)

        # hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        # or_=Label(login_frame,text="OR",bg="white",fg="lightgray",font=("times new roman",15,"bold")).place(x=150,y=355)

        # btn_forget=Button(login_frame,text="Forget Password ?",font=("Arial Rounded MT Bold",13),bg="white",fg="#00759E",bd=0,activebackground="white",activeforeground="#00759E",cursor="hand2").place(x=100,y=390)

        #=======Farme2=======
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=650,y=570,width=350,height=60)

        #lbl_follw=Label(register_frame,text="FOLLOW Me | LIKE | SHARE",font=("times new roman",13),bg="white").place(x=80,y=20)
        btn_follw=Button(register_frame,text="FOLLOW Me | LIKE | SHARE",font=("times new roman",13),command=self.open_facebook,bg="white",fg="black",bd=0,activebackground="white",activeforeground="black",cursor="hand2").place(x=70,y=15)
   

        #=======Animation Images=======
        self.im1=ImageTk.PhotoImage(file="images/im1.png")
        self.im2=ImageTk.PhotoImage(file="images/im2.png")
        self.im3=ImageTk.PhotoImage(file="images/im3.png")
        self.im4=ImageTk.PhotoImage(file="images/im4.png")
        self.im5=ImageTk.PhotoImage(file="images/im5.png")

        self.lbl_change_image=Label(self.root,bg="#fafafa")
        self.lbl_change_image.place(x=180,y=150,width=200,height=400)

        self.animate()
#=====================All Functions=====================

    def open_facebook(self):
        webbrowser.open_new("https://www.facebook.com/programmers.idea")

    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im4
        self.im4=self.im5
        self.im5=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)

    

    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.name.get() =="" or self.password.get() == "":
                messagebox.showerror("حدث خطأ","جميع الحقول مطلوبة",parent=self.root) 
            elif self.name.get() =="abdo" and self.password.get() == "admin":
                self.root.destroy()
                os.system("python dashboard.py")
            else:  
                cur.execute("select utype from employee where name=? AND pass=?",(self.name.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("حدث خطأ","اسم المستخدم أو كلمة السر غير صحيحة \n حاول مرة أخرى باستخدام البيانات الصحيحة",parent=self.root)
                else:
                    if user[0]=="مسؤل":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}", parent=self.root)
                        
if __name__=="__main__":
    root=Tk()
    ob=Login_System(root)
    root.mainloop()
