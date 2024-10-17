from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
from bidi.algorithm import get_display
class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+400+200")
        self.root.resizable(False,False)
        self.root.iconbitmap('images/logo.ico')
        self.root.title("Inventory Management System | Database")
        self.root.config(bg="white")
        self.root.focus_force()
        #===============Variables===================
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        self.var_ctyup=StringVar()
        self.var_cnum=StringVar()
        #=================title=====================
        lbl_title=Label(self.root,text="Manage Product Category",font=("times new roman",30),bg="#0B2F3A",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_name=Label(self.root,text="اسم الصنف",font=("times new roman",25),bg="white").place(x=50,y=95)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("times new roman",18),bg="lightyellow").place(x=200,y=100,width=300)

        lbl_ctyup=Label(self.root,text="نوع الصنف",font=("times new roman",25),bg="white").place(x=50,y=165)
        txt_ctyup=Entry(self.root,textvariable=self.var_ctyup,font=("times new roman",18),bg="lightyellow").place(x=200,y=170,width=300)

        lbl_cnum=Label(self.root,text="أرقام الصنف",font=("times new roman",25),bg="white").place(x=50,y=235)
        txt_cnum=Entry(self.root,textvariable=self.var_cnum,font=("times new roman",18),bg="lightyellow").place(x=200,y=240,width=300)

        lbl_cdesc = Label(self.root, text="المواصفات", font=("times new roman",25), bg="white").place(x=50, y=305)
        self.txt_cdesc = Text(self.root, font=("times new roman",15), bg="lightyellow")
        self.txt_cdesc.place(x=200, y=310, width=300,height=90)


        # ======button======
        btn_add= Button(self.root, text="إضافة",command=self.add,font=("times new roman", 15), bg="#2196f3", fg="white",cursor="hand2").place(x=70, y=445, width=110, height=28)
        btn_update= Button(self.root, text="تحديث",command=self.update,font=("times new roman", 15), bg="#4caf50", fg="white",cursor="hand2").place(x=190, y=445, width=110, height=28)
        btn_delete= Button(self.root, text="حذف",command=self.delete,font=("times new roman", 15), bg="#f44336", fg="white",cursor="hand2").place(x=310, y=445, width=110, height=28)
        btn_clear= Button(self.root, text="مسح",command=self.clear,font=("times new roman", 15), bg="#607d8b", fg="white",cursor="hand2").place(x=430, y=445, width=110, height=28)

        #=================category Details=====================


        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=590,y=95,width=500,height=380)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.category_tsble=ttk.Treeview(cat_frame,columns=("cid","name","ctyup","cnum","cdesc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.category_tsble.xview)
        scrolly.config(command=self.category_tsble.yview)

        self.category_tsble.heading("cid",text="C ID")
        self.category_tsble.heading("name",text="الأسم")
        self.category_tsble.heading("ctyup",text="نوع الصنف")
        self.category_tsble.heading("cnum",text="أرقام الصنف")
        self.category_tsble.heading("cdesc",text="المواصفات")

        self.category_tsble["show"]="headings"

        self.category_tsble.column("cid",width=40)
        self.category_tsble.column("name",width=90)
        self.category_tsble.column("ctyup",width=90)
        self.category_tsble.column("cnum",width=110)
        self.category_tsble.column("cdesc",width=150)
        self.category_tsble.pack(fill=BOTH,expand=1)
        self.category_tsble.bind("<ButtonRelease-1>",self.get_data)

        #======================images======================
        # self.im1=Image.open("images/pngwing3.png")
        # self.im1=self.im1.resize((618,250),Image.LANCZOS)
        # self.im1=ImageTk.PhotoImage(self.im1)

        # self.lbl_iml=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        # self.lbl_iml.place(x=50,y=220)

        # self.im2=Image.open("images/pngwing4.png")
        # self.im2=self.im2.resize((500,250),Image.LANCZOS)
        # self.im2=ImageTk.PhotoImage(self.im2)

        # self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        # self.lbl_im2.place(x=580,y=220)

        self.show()
    #=======================Functions======================
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("حدث خطأ","يجب أن يكون اسم الصنف موجودًا",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("حدث خطأ","الصنف موجود بالفعل، حاول استخدام صنف آخر",parent=self.root)
                else:
                    cur.execute("Insert into category (name,ctyup,cnum,cdesc) values(?,?,?,?)",(
                        self.var_name.get(),
                        self.var_ctyup.get(),
                        self.var_cnum.get(),
                        self.txt_cdesc.get('1.0',END),
                        ))
                    con.commit()
                    messagebox.showinfo("نجاح","تمت إضافة النصف بنجاح",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}", parent=self.root)

    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.category_tsble.delete(*self.category_tsble.get_children())
            for row in rows:
                self.category_tsble.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.category_tsble.focus()
        content=(self.category_tsble.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])
        self.var_ctyup.set(row[2])
        self.var_cnum.set(row[3])
        self.txt_cdesc.delete('1.0',END)
        self.txt_cdesc.insert(END,row[4])

    def update(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("حدث خطأ","معرف الموظف مطلوب",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("حدث خطأ","معرف الموظف غير صالح",parent=self.root)
                else:
                    cur.execute("Update category set name=?,ctyup=?,cnum=?,cdesc=? where cid=?",(
                                                    self.var_name.get(),
                                                    self.var_ctyup.get(),
                                                    self.var_cnum.get(),
                                                    self.txt_cdesc.get('1.0',END),
                                                    self.var_cat_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("نجاح","تم تحديث الموظف بنجاح",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("حدث خطأ",f"خطأ بسبب : {str(ex)}",parent=self.root)
    
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("حدث خطأ","يرجى اختيار الصنف من القائمة",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("حدث خطأ","خطأ، يرجى المحاولة مرة أخرى",parent=self.root)
                else:
                    op=messagebox.askyesno("تأكد","هل تريد حقًا حذف هذا الصنف؟",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("حذف","تم حذف الصنف بنجاح",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
                        self.var_ctyup.set("")
                        self.var_cnum.set("")
                        self.txt_cdesc.delete('1.0',END)
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}",parent=self.root)

    def clear(self):
        self.var_name.set("")
        self.var_ctyup.set("")
        self.var_cnum.set("")
        self.txt_cdesc.delete('1.0',END),

if __name__=="__main__":
    root=Tk()
    ob=categoryClass(root)
    root.mainloop()