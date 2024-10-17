from tkinter import *
from PIL import Image,ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from buying import BuyingClass
import sqlite3
from tkinter import messagebox
import os
import time
from bidi.algorithm import get_display
class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1450x760")
        self.root.resizable(False,False)
        self.root.title("Inventory Management System | Database")
        self.root.config(bg="white")

        #=============title==============
        root.iconbitmap('images/logo.ico')
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#0B2F3A",fg="white",anchor="w",padx=20)
        title.place(x=0,y=0,relwidth=1,height=70)

        #=============logout=============
        btn_logout=Button(self.root,text="تسجيل خروج",command=self.logout,font=("times new roman",15,"bold"),bg="#c30b0b",fg="white",cursor="hand2")
        btn_logout.place(x=1260,y=10,width=150,height=50)

        #=============clock=============
        self.lbl_clock= Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS ",font=("times new roman",15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # =============القائمة اليسري=============
        self.MenuLogo=Image.open("images/pngegg.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.ADAPTIVE)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=615)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        self.icon_pngegg2 = PhotoImage(file="images/pngegg2.png")

        lbl_menu=Label(LeftMenu, text="القوائم", font=("times new roman",20), bg="#009688")
        lbl_menu.pack(side=TOP,fill=X)

        btn_employee=Button(LeftMenu, text="  الموظفين",command=self.employee,image=self.icon_pngegg2,compound=LEFT,padx=5,anchor="w",font=("times new roman", 20,"bold"), bg="#DBA901",fg='black',bd=3,cursor="hand2")
        btn_employee.pack(side=TOP, fill=X)
        btn_supplier = Button(LeftMenu, text="  المورد",command=self.supplier,image=self.icon_pngegg2, compound=LEFT, padx=5, anchor="w",font=("times new roman", 20, "bold"), bg="#DBA901", fg='black', bd=3, cursor="hand2")
        btn_supplier.pack(side=TOP, fill=X)
        btn_categor = Button(LeftMenu, text="  الصنف",command=self.category,image=self.icon_pngegg2, compound=LEFT, padx=5, anchor="w",font=("times new roman", 20, "bold"), bg="#DBA901", fg='black', bd=3, cursor="hand2")
        btn_categor.pack(side=TOP, fill=X)
        btn_product = Button(LeftMenu, text="  المنتج",command=self.product,image=self.icon_pngegg2, compound=LEFT, padx=5, anchor="w",font=("times new roman", 20, "bold"), bg="#DBA901", fg='black', bd=3, cursor="hand2")
        btn_product.pack(side=TOP, fill=X)
        btn_buying = Button(LeftMenu, text="  المشتريات",command=self.buying,image=self.icon_pngegg2, compound=LEFT, padx=5, anchor="w",font=("times new roman", 20, "bold"), bg="#DBA901", fg='black', bd=3, cursor="hand2")
        btn_buying.pack(side=TOP, fill=X)
        btn_sales = Button(LeftMenu, text="  المبيعات",command=self.sales,image=self.icon_pngegg2, compound=LEFT, padx=5, anchor="w",font=("times new roman", 20, "bold"), bg="#DBA901", fg='black', bd=3, cursor="hand2")
        btn_sales.pack(side=TOP, fill=X)
        btn_exit = Button(LeftMenu, text="تسجيل خروج",command=self.logout, image=self.icon_pngegg2, compound=LEFT, padx=5, anchor="w",font=("times new roman", 20, "bold"), bg="#DBA901", fg='black', bd=3, cursor="hand2")
        btn_exit.pack(side=TOP, fill=X)
        # ===========content==============

        self.lbl_employee=Label(self.root,text="عدد الموظفين\n[ 0 ]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("times new roman",20,"bold"))
        self.lbl_employee.place(x=300,y=120,width=300,height=150)

        self.lbl_supplier = Label(self.root, text="عدد الموردين\n[ 0 ]", bd=5, relief=RIDGE, bg="#ff5722", fg="white",font=("times new roman", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, width=300, height=150)

        self.lbl_category = Label(self.root, text="عدد الأصناف\n[ 0 ]", bd=5, relief=RIDGE, bg="#009688", fg="white",font=("times new roman", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, width=300, height=150)

        self.lbl_product = Label(self.root, text="عدد المنتجات\n[ 0 ]", bd=5, relief=RIDGE, bg="#607d8b", fg="white",font=("times new roman", 20, "bold"))
        self.lbl_product.place(x=300, y=300, width=300, height=150)

        self.lbl_buying = Label(self.root, text="عدد المشتريات\n[ 0 ]", bd=5, relief=RIDGE, bg="#23680e", fg="white",font=("times new roman", 20, "bold"))
        self.lbl_buying.place(x=650, y=300, width=300, height=150)

        self.lbl_sales = Label(self.root, text="عدد المبيعات\n[ 0 ]", bd=5, relief=RIDGE, bg="#ffc107", fg="white",font=("times new roman", 20, "bold"))
        self.lbl_sales.place(x=1000, y=300, width=300, height=150)


        #===========footer===============
        lbl_footer=Label(self.root,text="IMS-Inventory Management System | Abdelrhaman Diaa طورت بواسطة\n programmers idea & لأي مشكلة فنية فيسبوك : فكرة مبرمجين",font=("times new roman", 11), bg="#4d636d", fg="white").pack(side=BOTTOM,fill=X)
        self.update_content()
#==============================================================================

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_ob=employeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_ob=supplierClass(self.new_win)
    
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_ob=categoryClass(self.new_win)

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_ob=productClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_ob=salesClass(self.new_win) 
    def buying(self):
        self.new_win=Toplevel(self.root)
        self.new_ob=BuyingClass(self.new_win)  

    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'عدد المنتجات\n[ {str(len(product))} ]')

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'عدد الموردين\n[ {str(len(supplier))} ]')

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'عدد الأصناف\n[ {str(len(category))} ]')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'عدد الموظفين\n[ {str(len(employee))} ]')

            buying=len(os.listdir('purchases'))
            self.lbl_buying.config(text=f'عدد المبيعات\n[ {str(buying)} ]')
            
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'عدد المبيعات\n[ {str(bill)} ]')

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)

        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}", parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

   
            



if __name__=="__main__":
    root=Tk()
    ob=IMS(root)
    root.mainloop()