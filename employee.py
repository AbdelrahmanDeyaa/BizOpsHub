from tkinter import *
from tkinter import ttk,messagebox
import sqlite3
from bidi.algorithm import get_display
class employeeClass:
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
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj= StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()


        #=============SearchFrame===============
        SearchFrame=LabelFrame(self.root,text=" البحث عن موظف ",font=("times new roman",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #=============options==================
        cmd_serch=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","EID","Email","Name","Contact"),state='readonly',justify=CENTER,font=("times new roman",15))
        cmd_serch.place(x=10,y=10,width=180)
        cmd_serch.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("times new roman",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="بحث",command=self.search,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)


        #===============title=================
        title=Label(self.root,text="تفاصيل الموظف",font=("times new roman",17),bg="#0B2F3A",fg="white").place(x=50,y=100,width=1000)


        #===============content================
        #======row1======
        lbl_empid=Label(self.root, text="Emp ID", font=("times new roman", 15),bg="white").place(x=50, y=150)
        lbl_gender=Label(self.root, text="جنس", font=("times new roman", 15), bg="white").place(x=400, y=150)
        lbl_contact=Label(self.root, text="رقم الاتصال", font=("times new roman", 15), bg="white").place(x=750, y=150)
        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=("times new roman",15),bg="lightyellow").place(x=150, y=150,width=180)
        cmd_gender = ttk.Combobox(self.root,textvariable=self.var_gender,values=("Select","ذكر","أنثى","آخر"), state='readonly', justify=CENTER,font=("times new roman", 15))
        cmd_gender.place(x=500, y=150,width=180)
        cmd_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("times new roman",15),bg="lightyellow").place(x=865, y=150,width=180)
        #======row2======
        lbl_name = Label(self.root, text="اسم", font=("times new roman", 15), bg="white").place(x=50, y=190)
        lbl_dob = Label(self.root, text="D.O.B", font=("times new roman", 15), bg="white").place(x=400, y=190)
        lbl_doj = Label(self.root, text="D.O.J", font=("times new roman", 15), bg="white").place(x=750, y=190)
        txt_name= Entry(self.root, textvariable=self.var_name, font=("times new roman", 15),bg="lightyellow").place(x=150, y=190, width=180)
        txt_dob= Entry(self.root, textvariable=self.var_dob, font=("times new roman", 15),bg="lightyellow").place(x=500, y=190, width=180)
        txt_doj= Entry(self.root, textvariable=self.var_doj, font=("times new roman", 15),bg="lightyellow").place(x=865, y=190, width=180)
        # ======row3======
        lbl_email = Label(self.root, text="Email", font=("times new roman", 15), bg="white").place(x=50, y=230)
        lbl_pass= Label(self.root, text="كلمة المرور", font=("times new roman", 15), bg="white").place(x=400, y=230)
        lbl_utype = Label(self.root, text="نوع المستخدم", font=("times new roman", 15), bg="white").place(x=750, y=230)
        txt_email = Entry(self.root, textvariable=self.var_email, font=("times new roman", 15), bg="lightyellow").place(x=150, y=230, width=180)
        txt_pass = Entry(self.root, textvariable=self.var_pass, font=("times new roman", 15), bg="lightyellow").place(x=500, y=230, width=180)
        cmd_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Select","مسؤل", "موظف"),state='readonly', justify=CENTER, font=("times new roman", 15))
        cmd_utype.place(x=865, y=230, width=180)
        cmd_utype.current(0)
        # ======row4======
        lbl_address = Label(self.root, text="العنوان", font=("times new roman", 15), bg="white").place(x=50, y=270)
        self.txt_address = Text(self.root, font=("times new roman", 15), bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=300,height=60)
        lbl_salary = Label(self.root, text="المرتب", font=("times new roman", 15), bg="white").place(x=500, y=270)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("times new roman", 15), bg="lightyellow").place(x=600, y=270, width=180)
        # ======button======
        btn_add= Button(self.root, text="إضافة",command=self.add,font=("times new roman", 15), bg="#2196f3", fg="white",cursor="hand2").place(x=500, y=305, width=110, height=28)
        btn_update= Button(self.root, text="تحديث",command=self.update,font=("times new roman", 15), bg="#4caf50", fg="white",cursor="hand2").place(x=620, y=305, width=110, height=28)
        btn_delete= Button(self.root, text="حذف",command=self.delete,font=("times new roman", 15), bg="#f44336", fg="white",cursor="hand2").place(x=740, y=305, width=110, height=28)
        btn_clear= Button(self.root, text="مسح",command=self.clear,font=("times new roman", 15), bg="#607d8b", fg="white",cursor="hand2").place(x=860, y=305, width=110, height=28)

        # ======تفاصيل الموظف======
        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.employee_table=ttk.Treeview(p_frame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.employee_table.xview)
        scrolly.config(command=self.employee_table.yview)

        self.employee_table.heading("eid",text="معرف العميل")
        self.employee_table.heading("name",text="الأسم")
        self.employee_table.heading("email",text="بريد إلكتروني")
        self.employee_table.heading("gender",text="جنس")
        self.employee_table.heading("contact",text="رقم الاتصال")
        self.employee_table.heading("dob",text="تاريخ الميلاد")
        self.employee_table.heading("doj",text="تاريخ الالتحاق بالعمل")
        self.employee_table.heading("pass",text="كلمة المرور")
        self.employee_table.heading("utype",text="نوع المستخدم")
        self.employee_table.heading("address", text="العنوان")
        self.employee_table.heading("salary",text="المرتب")

        self.employee_table["show"]="headings"

        self.employee_table.column("eid",width=90)
        self.employee_table.column("name",width=90)
        self.employee_table.column("email",width=100)
        self.employee_table.column("gender",width=90)
        self.employee_table.column("contact",width=90)
        self.employee_table.column("dob",width=100)
        self.employee_table.column("doj",width=110)
        self.employee_table.column("pass",width=100)
        self.employee_table.column("utype",width=100)
        self.employee_table.column("address",width=150)
        self.employee_table.column("salary",width=100)
        self.employee_table.pack(fill=BOTH,expand=1)
        self.employee_table.bind("<ButtonRelease-1>",self.get_data)

        self.show()
#=================================================================
    def add(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("حدث خطأ","معرف الموظف مطلوب",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("حدث خطأ","تم تعيين معرف الموظف هذا بالفعل، حاول بمعرف مختلف",parent=self.root)
                else:
                    cur.execute("Insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                                    self.var_emp_id.get(),
                                                    self.var_name.get(),
                                                    self.var_email.get(),
                                                    self.var_gender.get(),
                                                    self.var_contact.get(),

                                                    self.var_dob.get(),
                                                    self.var_doj.get(),

                                                    self.var_pass.get(),
                                                    self.var_utype.get(),
                                                    self.txt_address.get('1.0',END),
                                                    self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("نجاح","تمت إضافة الموظف بنجاح",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("حدث خطأ",f"خطأ بسبب : {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.employee_table.delete(*self.employee_table.get_children())
            for row in rows:
                self.employee_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}",parent=self.root)


    def get_data(self,ev):
        f=self.employee_table.focus()
        content=(self.employee_table.item(f))
        row=content['values']
        # print(row)
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])

        self.var_dob.set(row[5])
        self.var_doj.set(row[6])

        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])
    def update(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("حدث خطأ","معرف الموظف مطلوب",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("حدث خطأ","معرف الموظف غير صالح",parent=self.root)
                else:
                    cur.execute("Update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                                                    self.var_name.get(),
                                                    self.var_email.get(),
                                                    self.var_gender.get(),
                                                    self.var_contact.get(),

                                                    self.var_dob.get(),
                                                    self.var_doj.get(),

                                                    self.var_pass.get(),
                                                    self.var_utype.get(),
                                                    self.txt_address.get('1.0',END),
                                                    self.var_salary.get(),
                                                    self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("نجاح","تم تحديث الموظف بنجاح",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("حدث خطأ",f"خطأ بسبب : {str(ex)}",parent=self.root)
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("حدث خطأ","معرف الموظف مطلوب",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("حدث خطأ","معرف الموظف غير صالح",parent=self.root)
                else:
                    op=messagebox.askyesno("تأكيد","هل تريد حقًا حذف هذا الموظف؟",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("حذف","تم حذف الموظف بنجاح",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب  : {str(ex)}",parent=self.root)

    def clear(self):
        self.var_emp_id.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_name.set("")
        self.var_dob.set("")

        self.var_doj.set("")
        self.var_email.set("")

        self.var_pass.set("")
        self.var_utype.set("مسؤل")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("حدث خطأ","حدد البحث عن طريق أحد الخيارات",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("حدث خطأ","يجب عليك إدخال بيانات البحث المطلوبة",parent=self.root)
                
            else:
                query = "select * from employee where "+self.var_searchby.get()+" LIKE ?"
                cur.execute(query,('%' + self.var_searchtxt.get() +'%',))
                rows=cur.fetchall()
                if rows:
                    self.employee_table.delete(*self.employee_table.get_children())
                    for row in rows:
                        self.employee_table.insert('',END,values=row)
                else:
                    messagebox.showerror("حدث خطأ","لا يوجد سجلات",parent=self.root)     
                con.close()        
        except Exception as ex:
            messagebox.showerror("حدث خطأ",f"خطأ بسبب : {str(ex)}",parent=self.root)

    
if __name__=="__main__":
    root=Tk()
    ob=employeeClass(root)
    root.mainloop()