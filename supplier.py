from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
from bidi.algorithm import get_display
class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+400+200")
        self.root.resizable(False,False)
        self.root.iconbitmap('images/logo.ico')
        self.root.title("Inventory Management System | Database")
        self.root.config(bg="white")
        self.root.focus_force()
        #=======================================
        # All Variables======
        self.ver_searchby=StringVar()
        self.ver_searchtxt=StringVar()
        self.ver_sup_invoice=StringVar()
        self.ver_name=StringVar()
        self.ver_email=StringVar()
        self.ver_contact=StringVar()



        #=============self.root===============

        #=============options==================
        lbl_serch=Label(self.root,text="Supplier ID",font=("times new roman",15))
        lbl_serch.place(x=700,y=80)

        txt_search=Entry(self.root,textvariable=self.ver_searchtxt,font=("times new roman",15),bg="lightyellow").place(x=810,y=80,width=160)
        btn_search=Button(self.root,text="بحث",command=self.search,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=980,y=79,width=100,height=28)


        #===============title=================
        title=Label(self.root,text="تفاصيل المورد",font=("times new roman",20,"bold"),bg="#0B2F3A",fg="white").place(x=50,y=10,width=1000,height=40)


        #===============content================
        #======row1======
        sup_invoice=Label(self.root, text="Supplier ID", font=("times new roman", 15),bg="white").place(x=50, y=80)
        txt_invoice=Entry(self.root,textvariable=self.ver_sup_invoice,font=("times new roman",15),bg="lightyellow").place(x=180, y=80,width=170)

                                                    
        #======row2======
        lbl_name = Label(self.root, text="اسم", font=("times new roman", 15), bg="white").place(x=400, y=80)
        txt_name= Entry(self.root, textvariable=self.ver_name, font=("times new roman", 15),bg="lightyellow").place(x=480, y=80, width=170)

        #======row3======
        lbl_name = Label(self.root, text="Email", font=("times new roman", 15), bg="white").place(x=400, y=160)
        txt_name= Entry(self.root, textvariable=self.ver_email, font=("times new roman", 15),bg="lightyellow").place(x=480, y=160, width=170)

        # ======row4======
        lbl_contact = Label(self.root, text="رقم الاتصال", font=("times new roman", 15), bg="white").place(x=50, y=160)
        txt_contact = Entry(self.root, textvariable=self.ver_contact, font=("times new roman", 15), bg="lightyellow").place(x=180, y=160, width=170)

        # ======row5======
        lbl_desc = Label(self.root, text="وصف", font=("times new roman", 15), bg="white").place(x=50, y=240)
        self.txt_desc=Text(self.root, font=("times new roman", 15), bg="lightyellow")
        self.txt_desc.place(x=180, y=240, width=470,height=90)

        # ======button======
        btn_add= Button(self.root, text="إضافة",command=self.add,font=("times new roman", 15), bg="#2196f3", fg="white",cursor="hand2").place(x=180, y=370, width=110, height=35)
        btn_update= Button(self.root, text="تحديث",command=self.update,font=("times new roman", 15), bg="#4caf50", fg="white",cursor="hand2").place(x=300, y=370, width=110, height=35)
        btn_delete= Button(self.root, text="حذف",command=self.delete,font=("times new roman", 15), bg="#f44336", fg="white",cursor="hand2").place(x=420, y=370, width=110, height=35)
        btn_clear= Button(self.root, text="مسح",command=self.clear,font=("times new roman", 15), bg="#607d8b", fg="white",cursor="hand2").place(x=540, y=370, width=110, height=35)

        # ======تفاصيل الموظف======
        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=700,y=120,width=380,height=350)

        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(p_frame,columns=("invoice","name","contact","desc","email"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="Supplier ID")
        self.supplierTable.heading("name",text="الأسم")
        self.supplierTable.heading("contact",text="رقم الاتصال")
        self.supplierTable.heading("desc",text="وصف")
        self.supplierTable.heading("email",text="Email")


        self.supplierTable["show"]="headings"

        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=90)
        self.supplierTable.column("contact",width=90)
        self.supplierTable.column("desc",width=100)
        self.supplierTable.column("email",width=90)
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
#============================Functions=====================================
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.ver_sup_invoice.get()=="":
                messagebox.showerror("حدث خطأ","معرف المورد مطلوب",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.ver_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("حدث خطأ","تم تعيين معرف المورد هذا بالفعل، حاول بمعرف مختلف",parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice,name,contact,desc,email) values(?,?,?,?,?)",(
                                                    self.ver_sup_invoice.get(),
                                                    self.ver_name.get(),
                                                    self.ver_contact.get(),
                                                    self.txt_desc.get('1.0',END),
                                                    self.ver_email.get(),

                    ))
                    con.commit()
                    messagebox.showinfo("نجاح","تمت إضافة المورد بنجاح",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}", parent=self.root)

    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        #print(row)
        self.ver_sup_invoice.set(row[0])
        self.ver_name.set(row[1])
        self.ver_contact.set(row[2])
        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END,row[3])
        self.ver_email.set(row[4])

    def update(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.ver_sup_invoice.get()=="":
                messagebox.showerror("حدث خطأ","معرف المورد مطلوب",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.ver_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("حدث خطأ","معرف المورد غير صالح",parent=self.root)
                else:
                    cur.execute("Update supplier set name=?,contact=?,desc=?,email=? where invoice=?",(
                                                    self.ver_name.get(),                                                   
                                                    self.ver_contact.get(),
                                                    self.txt_desc.get('1.0',END),
                                                    self.ver_email.get(),
                                                    self.ver_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("نجاح","تم تحديث المورد بنجاح",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("حدث خطأ",f"خطأ بسبب : {str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.ver_sup_invoice.get()=="":
                messagebox.showerror("حدث خطأ","معرف المورد مطلوب",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.ver_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("حدث خطأ","رقم الفاتورة غير صالح",parent=self.root)
                else:
                    op=messagebox.askyesno("تأكد","هل تريد حقًا حذف هذا المورد؟",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.ver_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("حذف","تم حذف المورد بنجاح",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}",parent=self.root)
    def clear(self):
        self.ver_sup_invoice.set("")
        self.ver_name.set("")       
        self.ver_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.ver_email.set("")
        self.ver_searchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.ver_searchtxt.get()=="":
                messagebox.showerror("حدث خطأ", "معرف المورد مطلوب",parent=self.root)
            else:
                query ="select * from supplier where invoice LIKE ?"
                cur.execute(query,('%' + self.ver_searchtxt.get() +'%',))
                rows = cur.fetchall()
                if rows:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    for row in rows:
                        self.supplierTable.insert('', END, values=row)

                else:
                    messagebox.showerror("حدث خطأ","لا يوجد سجلات",parent=self.root)
                con.close()
        except Exception as ex:
            messagebox.showerror("حدث خطأ",f"خطأ بسبب : {str(ex)}",parent=self.root)

            

if __name__=="__main__":
    root=Tk()
    ob=supplierClass(root)
    root.mainloop()