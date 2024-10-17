from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk , messagebox
import sqlite3
import time
import os
import tempfile
from bidi.algorithm import get_display
class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+350+150")
        self.root.resizable(False,False)
        self.root.title("Inventory Management System | Database")
        self.root.config(bg="white")
        self.cart_list=[]
        self.cart_length=[]
        self.chk_print=0
        #=============title==============
        root.iconbitmap('images//logo.ico')
        self.icon_title=PhotoImage(file="images//logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#0B2F3A",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #=============logout=============
        btn_logout=Button(self.root,text="تسجيل خروج",command=self.logout,font=("times new roman",15,"bold"),bg="#c30b0b",fg="white",cursor="hand2")
        btn_logout.place(x=1150,y=10,width=150,height=50)

        #=============clock=============
        self.lbl_clock= Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS ",font=("times new roman",15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #==========Product_Frame========

        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        pTitle=Label(ProductFrame1,text="جميع المنتجات",font=("times new roman",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        
        #======Product Search Frame======
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

        lbl_search=Label(ProductFrame2,text="اسم المنتج",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=100,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="بحث",command=self.search,font=("times new roman",15),bg="#2196f3",fg="white",cursor="hand2").place(x=270,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="عرض الكل",command=self.show,font=("times new roman",15),bg="#083531",fg="white",cursor="hand2").place(x=270,y=10,width=100,height=25)
        
        #======Product Details Frame======
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","sale","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid",text="معرف المنتج")
        self.product_Table.heading("name",text="الأسم")
        self.product_Table.heading("price",text="التكلفة")
        self.product_Table.heading("sale",text="البيع")
        self.product_Table.heading("qty",text="الكمية")
        self.product_Table.heading("status",text="حالة")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid",width=90)
        self.product_Table.column("name",width=120)
        self.product_Table.column("price",width=55)
        self.product_Table.column("sale",width=55) 
        self.product_Table.column("qty",width=60)
        self.product_Table.column("status",width=60)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)

        lbl_note=Label(ProductFrame1,text="'ملحوظة:'أدخل 0 الكمية لإزالة المنتج من سلة التسوق",font=("times new roman",13),bg="white",fg="red").pack(side=BOTTOM,fill=X)
        
        # ======Customer Frame======
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,text="تفاصيل العميل",font=("times new roman",15),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="الاسم",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=75,y=35,width=180)
        lbl_content=Label(CustomerFrame,text="رقم المحتوى",font=("times new roman",15),bg="white").place(x=272,y=35)
        txt_content=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=370,y=35,width=140)

        # ======Cal Cart Frame======
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)

        # ======Calculator Frame======
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=340)
        
        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly')
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=6,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=6,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=6,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=6,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=6,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=6,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=6,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=6,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=6,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=6,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=6,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='x',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=6,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=6,cursor="hand2").grid(row=4,column=0)
        btn_lbrace=Button(Cal_Frame,text='(',font=('arial',15,'bold'),command=lambda:self.get_input('('),bd=5,width=4,pady=6,cursor="hand2").grid(row=4,column=1)
        btn_rbrace=Button(Cal_Frame,text=')',font=('arial',15,'bold'),command=lambda:self.get_input(')'),bd=5,width=4,pady=6,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='÷',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=6,cursor="hand2").grid(row=4,column=3)

        btn_deci=Button(Cal_Frame,text='.',font=('arial',15,'bold'),command=lambda:self.get_input('.'),bd=5,width=4,pady=1,cursor="hand2").grid(row=5,column=0)
        btn_C=Button(Cal_Frame,text='C',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=1,cursor="hand2").grid(row=5,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform,bd=5,width=9,pady=1,cursor="hand2").grid(row=5,column=2,columnspan=2)



        # ======Cart Frame======
        cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cart_Frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(cart_Frame,text="[0] :سلة التسوق إجمالي المنتج ",font=("times new roman",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)


        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(cart_Frame,columns=("pid","name","price","sale","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid",text="معرف")
        self.CartTable.heading("name",text="الأسم")
        self.CartTable.heading("price",text="التكلفة")
        self.CartTable.heading("sale",text="البيع")
        self.CartTable.heading("qty",text="الكمية")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=50)
        self.CartTable.column("sale",width=50) 
        self.CartTable.column("qty",width=40)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        # ======ADD Cart Widgets Frame======
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_sale=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        self.var_discount=StringVar()
        
        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=110)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="اسم المنتج",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=140,height=22)
        
        lbl_p_sale=Label(Add_CartWidgetsFrame,text="سعر المنتج",font=("times new roman",15),bg="white").place(x=155,y=5)
        txt_p_sale=Entry(Add_CartWidgetsFrame,textvariable=self.var_sale,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=155,y=35,width=140,height=22)
    
        lbl_discount=Label(Add_CartWidgetsFrame,text="قيمة الخصم",font=("times new roman",15),bg="white").place(x=302,y=5)
        txt_discount=Entry(Add_CartWidgetsFrame,textvariable=self.var_discount,font=("times new roman",15),bg="lightyellow").place(x=302,y=35,width=100,height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame,text="الكمية",font=("times new roman",15),bg="white").place(x=400,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=410,y=35,width=110,height=22)
        
        self.lbl_inStock=Label(Add_CartWidgetsFrame,text="[0] في المخزن",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=385,y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="مسح",command=self.clear_cart,font=("times new roman", 15),bg="#607d8b", fg="white",cursor="hand2").place(x=180, y=70, width=150, height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="إضافة | تحديث",command=self.add_update_cart,font=("times new roman", 15),bg="#4caf50",fg="white",cursor="hand2").place(x=10, y=70, width=160, height=30)

    # ======billing area======
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953, y=110, width=400, height=410)

        BTitle=Label(billFrame,text="فاتورة العميل",font=("times new roman",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

    # ======billing buttons======
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953, y=520, width=400, height=140)

        self.lbl_amnt=Label(billMenuFrame,text='مبلغ الفاتورة\n[0]',font=("times new roman",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2, y=5, width=120, height=70)

        self.lbl_discount=Label(billMenuFrame,text='تخفيض\n[0%]',font=("times new roman",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay=Label(billMenuFrame,text='صافي الربح\n[0]',font=("times new roman",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=146, height=70)

        btn_print=Button(billMenuFrame,text='طباعة',command=self.print_bill,font=("times new roman",15,"bold"),cursor='hand2',bg="lightgreen",fg="white")
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all=Button(billMenuFrame,text='مسح الكل',command=self.clear_all,font=("times new roman",15,"bold"),cursor='hand2',bg="gray",fg="white")
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate=Button(billMenuFrame,text='حفظ الفاتورة',command=self.generate_bill,font=("times new roman",15,"bold"),cursor='hand2',bg="#009688",fg="white")
        btn_generate.place(x=246, y=80, width=146, height=50)

    # ======Footer======
        lbl_footer=Label(self.root,text="IMS-Inventory Management System | Abdelrhaman Diaa طورت بواسطة\n programmers idea & لأي مشكلة فنية فيسبوك : فكرة مبرمجين",font=("times new roman", 11), bg="#4d636d", fg="white")
        lbl_footer.pack(side=BOTTOM,fill=X)

        self.show()
        self.bill_top()
        self.update_data_time()
    # ======All Functions======
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')
    def perform(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,sale,qty,status from product where status='متوفر'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}",parent=self.root)

    def search(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("حدث خطأ","يجب عليك إدخال بيانات البحث المطلوبة",parent=self.root)
            else:
                query = "select pid,name,price,sale,qty,status from product where name  LIKE ?"
                cur.execute(query,('%' + self.var_search.get() +'%',))
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("حدث خطأ","لا يوجد سجلات",parent=self.root)  
                con.close()           
        except Exception as ex:
            messagebox.showerror("حدث خطأ",f"خطأ بسبب : {str(ex)}",parent=self.root)

    def get_data(self, ev):
        f = self.product_Table.focus()
        content = self.product_Table.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_sale.set(row[3])
        self.var_stock.set(row[4])
        self.lbl_inStock.config(text=f"[{str(row[4])}] في المخزن")
        self.var_qty.set('1')
        self.var_discount.set('0')

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = self.CartTable.item(f)
        row = content['values']
        # pid, name, price, sale, qty, status
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_sale.set(row[3])
        self.var_qty.set(row[4])
        # Use quantity from product_Table instead of CartTable
        self.var_stock.set(self.get_quantity_from_product_table(row[0]))  # Assuming row[0] is the product ID
        self.lbl_inStock.config(text=f"[{str(self.var_stock.get())}] في المخزن")
        self.var_discount.set('0')

    def get_quantity_from_product_table(self, product_id):
    
        conn = sqlite3.connect(database='ims.db')
        cur = conn.cursor()

    
        cur.execute("select qty from product where pid = ?", (product_id,))
        result = cur.fetchone()  

        conn.close()

        if result:
            return result[0]
        else:
            return 0
            
    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('حدث خطأ',"الرجاء اختيار المنتج من القائمة",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('حدث خطأ',"الرجاء تحديد الكمية المطلوبة",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('حدث خطأ',"الكمية ليست كافية",parent=self.root)
        else: 
            # price_cal=int(self.var_qty.get())*float(self.var_price.get())
            # price_cal=float(price_cal)
            # sale_cal=int(self.var_qty.get())*float(self.var_sale.get())
            # sale_cal=float(sale_cal)
            sale_cal=self.var_sale.get()
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,sale_cal,self.var_qty.get(),self.var_discount.get()]
            
            # ======update cart======
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('تأكيد',"المنتج موجود بالفعل \n هل تريد التحديث | إزالة من قائمة العربة",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=sale_cal
                        self.cart_list[index_][4]=self.var_qty.get()
            else:
                 self.cart_list.append(cart_data)

            self.show_cart()
            self.calculate_bill_details()

    def calculate_bill_details(self):
        discount = float(self.var_discount.get()) / 100
        bill_amnt = sum(float(row[3]) * int(row[4]) for row in self.cart_list)
        net_price = sum(float(row[2]) * int(row[4]) for row in self.cart_list)

        if discount == 0 :
            self.discount_amount = 0  # حتى لا يتم تعيين القيمة للصفر
        else:
            self.discount_amount = discount * bill_amnt # في حالة وجود تخفيض

        self.billamnt = bill_amnt - self.discount_amount   # مجموع الفاتورة بعد التخفيض
        self.net_pay = self.billamnt  - net_price  # المبلغ الصافي للدفع

        self.bill_update(self.billamnt, self.net_pay, len(self.cart_list)) # تحديث الفاتورة

    def bill_update(self, billamnt , net_pay, cart_length):
        self.lbl_amnt.config(text=f'مبلغ الفاتورة\n{str(billamnt)}')
        self.lbl_discount.config(text=f'تخفيض\n{str(self.discount_amount)}')
        self.lbl_net_pay.config(text=f'صافي الربح\n{str(net_pay)}')
        self.cartTitle.config(text=f"[{str(cart_length)}] :سلة التسوق إجمالي المنتج ")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}",parent=self.root)
    
    def generate_bill(self):
        if self.var_cname.get() == "" and self.var_contact.get() == "":
            messagebox.showerror("حدث خطأ", "لا يجوز ترك حقل الاسم فارغا او رقم الفاتورة")
        elif len(self.cart_list) == 0 :
            messagebox.showerror("حدث خطأ", "\tلم يتم اختيار منتج \n الرجاء إضافة المنتج إلى السلة")
        else:
            #=====Bill Top=====
            self.bill_top()
            #=====Bill Middle=====
            self.bill_middle()
            #=====Bill Bottom=====
            self.bill_bottom()
            
            fp=open(f'bill/{str(self.invoice)}.txt','w',encoding="utf-8")
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('حفظ', "تم إنشاء الفاتورة \n و حفظها على الجهاز",parent=self.root)
            self.chk_print=1


    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\telakhwah - Inventory
\tشركة الأخوة لتجارة قطع الغيار ترحب بكم
\t Phone No. +201********* , Dokki
{str("="*46)}
Customer Name: {self.var_cname.get()}
Phone Number: {self.var_contact.get()}
Bill Number: {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("=")*46}
المشتريات\t\tالعدد\t\tالسعر
{str("=")*46}

           '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)
    
    def bill_bottom(self):
        bill_bottom_temp =f'''
{str("="*46)}
المبلغ الكلي \t\t\tEGP.{self.billamnt}
تخفيض \t\t\tEGP.{self.discount_amount}
{str("="*46)}\n
        '''
        
        self.txt_bill_area.insert(END,bill_bottom_temp)

    

    def bill_middle(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                qty = int(self.var_stock.get()) - int(row[4])
                if int(row[4]) == int(self.var_stock.get()):
                    status = 'نفذت'
                if int(row[4]) != int(self.var_stock.get()):
                    status = 'متوفر'

                sale = float(row[3]) * int(row[4])
                sale = str(sale)
                self.txt_bill_area.insert(END, "\n" + name + "\t\t" + row[4] + "\t\tEGP." + sale + "\n")
                # ==========update qty in product table==========
                cur.execute('Update product set qty=?,status=? where pid=?', (
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_sale.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"[0] في المخزن")
        self.var_stock.set('')
        self.var_discount.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"[0] :سلة التسوق إجمالي المنتج ")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_data_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_data_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('طباعة',"يرجى الانتظار أثناء الطباعة\nاشغل وقتك بذكر الله",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file, 'w',encoding="utf-8").write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('حدث خطأ',"يرجى إنشاء فاتورة لطباعة الإيصال",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__=="__main__":
    root=Tk()
    ob=BillClass(root)
    root.mainloop()
    