from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from bidi.algorithm import get_display
import sqlite3
class productClass:
    class AutocompleteCombobox(ttk.Combobox):
        def set_completion_list(self, completion_list):
            self._completion_list = sorted(completion_list)

        def autocomplete(self, event):
            # نحصل على النص المكتوب
            typed = self.get()
            if typed == '':
                self.configure(values=[])
            else:
                # نقوم بتصفية العناصر التي تبدأ بالنص المكتوب
                completions = [s for s in self._completion_list if s.lower().startswith(typed.lower())]
                self.configure(values=completions)
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+400+200")
        self.root.resizable(False,False)
        self.root.iconbitmap('images//logo.ico')
        self.root.title("Inventory Management System | Database")
        self.root.config(bg="white")
        self.root.focus_force()
        #=======================================
        conn = sqlite3.connect('ims.db')
        cursor = conn.cursor()

        # استعلام SQL لاسترداد أسماء العملاء
        sql_query_cat = "SELECT name FROM category"
        cursor.execute(sql_query_cat)
        results_cat = cursor.fetchall()
        category_names = [result[0] for result in results_cat]

        # استعلام SQL لاسترداد أسماء الموردين
        sql_query_sup = "SELECT name FROM supplier"
        cursor.execute(sql_query_sup)
        results_sup = cursor.fetchall()
        supplier_names = [result[0] for result in results_sup]


        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_sale=StringVar()
        self.var_quy=StringVar()
        self.var_status=StringVar()

        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)
        #==================title==================
        title=Label(product_Frame,text="Manage Products Details",font=("times new roman",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        #=============column1==================
        lbl_category=Label(product_Frame,text="اسم الصنف",font=("times new roman",18),bg="white").place(x=30,y=45)
        lbl_supplier=Label(product_Frame,text="المورد",font=("times new roman",18),bg="white").place(x=30,y=95)
        lbl_product_name=Label(product_Frame,text="اسم المنتج",font=("times new roman",18),bg="white").place(x=30,y=145)
        lbl_price=Label(product_Frame,text="التكلفة",font=("times new roman",18),bg="white").place(x=30,y=195)
        lbl_sale=Label(product_Frame,text="بيع",font=("times new roman",18),bg="white").place(x=30,y=245)
        lbl_quantity=Label(product_Frame,text="كمية",font=("times new roman",18),bg="white").place(x=30,y=295)
        lbl_status=Label(product_Frame,text="حالة",font=("times new roman",18),bg="white").place(x=30,y=345)


        #txt_category=Label(product_Frame,text="الصنف اسم",font=("times new roman",18),bg="white").place(x=30,y=60)
        #=============column2==================
        self.cmd_cat=self.AutocompleteCombobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,justify=CENTER,font=("times new roman",15))
        self.cmd_cat.set_completion_list(category_names)  # تعيين قائمة الاكتمال
        self.cmd_cat.place(x=150,y=45,width=200)
        self.cmd_cat.current(0)
        self.cmd_cat.bind('<KeyRelease>', self.cmd_cat.autocomplete)
        self.cmd_cat.bind('<FocusIn>', self.remove_select_text)

        self.cmd_sup=self.AutocompleteCombobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,justify=CENTER,font=("times new roman",15))
        self.cmd_sup.set_completion_list(supplier_names)
        self.cmd_sup.place(x=150,y=95,width=200)
        self.cmd_sup.current(0)
        self.cmd_sup.bind('<KeyRelease>', self.cmd_sup.autocomplete)
        self.cmd_sup.bind('<FocusIn>', self.remove_select_text)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("times new roman",15),bg="lightyellow").place(x=150,y=145,width=200)
        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow").place(x=150,y=195,width=200)
        txt_sale=Entry(product_Frame,textvariable=self.var_sale,font=("times new roman",15),bg="lightyellow").place(x=150,y=245,width=200)
        txt_quy=Entry(product_Frame,textvariable=self.var_quy,font=("times new roman",15),bg="lightyellow").place(x=150,y=295,width=200)

        cmd_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("متوفر","نفذت"),state='readonly',justify=CENTER,font=("times new roman",15))
        cmd_status.place(x=150,y=345,width=200)
        cmd_status.current(0)

        # ======button======
        btn_add= Button(product_Frame,text="إضافة",command=self.add,font=("times new roman", 15), bg="#2196f3", fg="white",cursor="hand2").place(x=10, y=400, width=100, height=40)
        btn_update= Button(product_Frame,text="تحديث",command=self.update,font=("times new roman", 15), bg="#4caf50", fg="white",cursor="hand2").place(x=120, y=400, width=100, height=40)
        btn_delete= Button(product_Frame,text="حذف",command=self.delete,font=("times new roman", 15), bg="#f44336", fg="white",cursor="hand2").place(x=230, y=400, width=100, height=40)
        btn_clear= Button(product_Frame,text="مسح",command=self.clear,font=("times new roman", 15), bg="#607d8b", fg="white",cursor="hand2").place(x=340, y=400, width=100, height=40)

        #=============SearchFrame===============
        SearchFrame=LabelFrame(self.root,text="البحث",font=("times new roman",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        #=============options==================
        cmd_serch=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","PID","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("times new roman",15))
        cmd_serch.place(x=10,y=10,width=180)
        cmd_serch.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("times new roman",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="بحث",command=self.search,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #=============Porduct Detalis==================
        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.product_table=ttk.Treeview(p_frame,columns=("pid","Category","Supplier","name","price","sale","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid",text="P ID")
        self.product_table.heading("Category",text="اسم الصنف")
        self.product_table.heading("Supplier",text="المورد")
        self.product_table.heading("name",text="الأسم")
        self.product_table.heading("price",text="التكلفة")
        self.product_table.heading("sale",text="بيع")
        self.product_table.heading("qty",text="الكمية")
        self.product_table.heading("status",text="حاله")
        

        self.product_table["show"]="headings"

        self.product_table.column("pid",width=90)
        self.product_table.column("Category",width=90)
        self.product_table.column("Supplier",width=100)
        self.product_table.column("name",width=90)
        self.product_table.column("price",width=90)
        self.product_table.column("sale",width=90)
        self.product_table.column("qty",width=100)
        self.product_table.column("status",width=100)
        self.product_table.pack(fill=BOTH,expand=1)
        self.product_table.bind("<ButtonRelease-1>",self.get_data)

        self.show()
#=================================================================

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("Select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("حدث خطأ",f"خطأ بسبب : {str(ex)}",parent=self.root)

    def add(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("حدث خطأ","جميع الحقول مطلوبة",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("حدث خطأ","المنتج موجود بالفعل، جرب منتجًا مختلفًا",parent=self.root)
                else:
                    cur.execute("Insert into product (Category,Supplier,name,price,sale,qty,status) values(?,?,?,?,?,?,?)",(
                                                    self.var_cat.get(),
                                                    self.var_sup.get(),
                                                    self.var_name.get(),
                                                    self.var_price.get(),
                                                    self.var_sale.get(),
                                                    self.var_quy.get(),
                                                    self.var_status.get(),
                                                    ))
                    con.commit()
                    messagebox.showinfo("نجاح","تمت إضافة المنتج بنجاح",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("حدث خطأ",f"خطأ بسبب : {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}",parent=self.root)


    def get_data(self,ev):
        f=self.product_table.focus()
        content=(self.product_table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_sale.set(row[5])
        self.var_quy.set(row[6])
        self.var_status.set(row[7])
    
    def update(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("حدث خطأ","يرجى اختيار المنتج من القائمة",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("حدث خطأ","منتج غير صالح",parent=self.root)
                else:
                    cur.execute("Update product set Category=?,Supplier=?,name=?,price=?,sale=?,qty=?,status=? where pid=?",(
                                                    self.var_cat.get(),
                                                    self.var_sup.get(),
                                                    self.var_name.get(),
                                                    self.var_price.get(),
                                                    self.var_sale.get(),
                                                    self.var_quy.get(),
                                                    self.var_status.get(),
                                                    self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("نجاح","تم تحديث المنتج بنجاح",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("حدث خطأ"f"خطأ بسبب : {str(ex)}",parent=self.root)
    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("حدث خطأ","حدد المنتج من القائمة",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("حدث خطأ","منتج غير صالح",parent=self.root)
                else:
                    op=messagebox.askyesno("تأكد","هل تريد حقا حذف هذا المنتج",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("حذف","تم حذف المنتج بنجاح",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}",parent=self.root)

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_sale.set("")
        self.var_quy.set("")
        self.var_status.set("متوفر")
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def remove_select_text(self, event):
        if self.var_cat.get() == "Select":
            self.var_cat.set("")
        elif self.var_sup.get() == "Select":
            self.var_sup.set("")

    def search(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("حدث خطأ","حدد خيار البحث حسب رغبتك",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("حدث خطأ","يجب عليك إدخال بيانات البحث المطلوبة",parent=self.root)
            else:
                query = "select * from product where "+self.var_searchby.get()+" LIKE ?"
                cur.execute(query,('%' + self.var_searchtxt.get() +'%',))
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('',END,values=row)
                else:
                    messagebox.showerror("حدث خطأ","لا يوجد سجلات",parent=self.root) 
                con.close()            
        except Exception as ex:
            messagebox.showerror("حدث خطأ",f"خطأ بسبب : {str(ex)}",parent=self.root)
    
    



if __name__=="__main__":
    root=Tk()
    ob=productClass(root)
    root.mainloop()