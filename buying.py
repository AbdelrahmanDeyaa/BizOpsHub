from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk , messagebox
import sqlite3
import time
import os
import tempfile
from bidi.algorithm import get_display
class BuyingClass:
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
        self.root.geometry("1350x660")
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
        btn_logout=Button(self.root,text="فواتير المشتريات",command=self.purchase,font=("times new roman",15,"bold"),bg="#DBA901",cursor="hand2")
        btn_logout.place(x=1150,y=10,width=150,height=50)

        #==========Product_Frame========
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=2,y=70,width=397,height=450)

        pTitle=Label(ProductFrame1,text="إضافة المنتجات",font=("times new roman",25,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        
        #==========Product_Frame2========
        conn = sqlite3.connect('ims.db')
        cursor = conn.cursor()

        sql_query_sup = "SELECT name FROM supplier"
        cursor.execute(sql_query_sup)
        results_sup = cursor.fetchall()
        supplier_names = [result[0] for result in results_sup]

        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_sale=StringVar()
        self.var_qty=StringVar()

        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=47,width=385,height=395)

        lbl_p_name=Label(ProductFrame2,text="اسم المنتج",font=("times new roman",20),bg="white").place(x=20,y=40)
        txt_p_name=Entry(ProductFrame2,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow").place(x=140,y=40,width=190,height=30)
        
        lbl_p_price=Label(ProductFrame2,text="التكلفة",font=("times new roman",20),bg="white").place(x=20,y=120)
        txt_p_price=Entry(ProductFrame2,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow").place(x=140,y=120,width=190,height=30)

        lbl_p_qty=Label(ProductFrame2,text="الكمية",font=("times new roman",20),bg="white").place(x=20,y=200)
        txt_p_qty=Entry(ProductFrame2,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=140,y=200,width=190,height=30)

        btn_clear_cart=Button(ProductFrame2,text="مسح",command=self.clear_cart,font=("times new roman", 20),bg="#607d8b", fg="white",cursor="hand2").place(x=205, y=305, width=160, height=35)
        btn_add_cart=Button(ProductFrame2,text="إضافة | تحديث",command=self.add_update_cart,font=("times new roman", 20),bg="#4caf50",fg="white",cursor="hand2").place(x=20, y=305, width=160, height=35)


        # ======Customer Frame======
        self.var_sup=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=400,y=70,width=552,height=90)

        cTitle=Label(CustomerFrame,text="تفاصيل المورد",font=("times new roman",20),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="الاسم",font=("times new roman",15),bg="white").place(x=5,y=45)
        self.cmd_sup=self.AutocompleteCombobox(CustomerFrame,textvariable=self.var_sup,values=supplier_names,justify=CENTER,font=("times new roman",13))
        self.cmd_sup.set_completion_list(supplier_names)
        self.cmd_sup.place(x=75,y=45,width=140,height=30)
        # self.cmd_sup.current(0)
        self.cmd_sup.bind('<KeyRelease>', self.cmd_sup.autocomplete)
        self.cmd_sup.bind('<FocusIn>', self.remove_select_text)
        lbl_content=Label(CustomerFrame,text="رقم المحتوى",font=("times new roman",15),bg="white").place(x=245,y=45)
        txt_content=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=370,y=45,width=140,height=30)

        # ======Cal Cart Frame======
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=400,y=160,width=552,height=360)
        

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
        cart_Frame.place(x=275,y=8,width=270,height=340)
        self.cartTitle=Label(cart_Frame,text="[0] :سلة التسوق إجمالي المنتج ",font=("times new roman",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)


        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(cart_Frame,columns=("name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("name",text="الأسم")
        self.CartTable.heading("price",text="التكلفة")
        self.CartTable.heading("qty",text="الكمية")
        self.CartTable["show"]="headings"
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=60)
        self.CartTable.column("qty",width=40)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        # ======Lower Cal Cart Frame======
        lCal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        lCal_Cart_Frame.place(x=2,y=520,width=950,height=137)

        self.buying_photo=Image.open("images/buying2.png")
        self.buying_photo=self.buying_photo.resize((945,133),Image.LANCZOS)
        self.buying_photo=ImageTk.PhotoImage(self.buying_photo)

        lbl_image=Label(lCal_Cart_Frame,image=self.buying_photo,bd=0)
        lbl_image.place(x=0,y=0)

        # ======billing area======
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953, y=70, width=400, height=450)

        BTitle=Label(billFrame,text="فاتورة الشراء",font=("times new roman",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # ======billing buttons======
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953, y=520, width=400, height=137)

        self.lbl_amnt=Label(billMenuFrame,text='مبلغ الفاتورة\n[0]',font=("times new roman",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2, y=5, width=390, height=70)

        btn_print=Button(billMenuFrame,text='طباعة',command=self.print_bill,font=("times new roman",15,"bold"),cursor='hand2',bg="lightgreen",fg="white")
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all=Button(billMenuFrame,text='مسح الكل',command=self.clear_all,font=("times new roman",15,"bold"),cursor='hand2',bg="gray",fg="white")
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate=Button(billMenuFrame,text='حفظ الفاتورة',command=self.generate_bill,font=("times new roman",15,"bold"),cursor='hand2',bg="#009688",fg="white")
        btn_generate.place(x=246, y=80, width=146, height=50)

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

    def remove_select_text(self, event):
        if self.var_sup.get() == "Select":
            self.var_sup.set("")

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

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = self.CartTable.item(f)
        row = content['values']
        # name, price, sale, qty
        self.var_pname.set(row[0])
        self.var_price.set(row[1])
        self.var_qty.set(row[2])
    def fetch_cat_sup(self):
        self.sup_list.append("Empty")
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("حدث خطأ",f"خطأ بسبب : {str(ex)}",parent=self.root)
 
    def add_update_cart(self):
        if self.var_pname.get()=='':
            messagebox.showerror('حدث خطأ',"الرجاء اختيار المنتج من القائمة",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('حدث خطأ',"الرجاء تحديد الكمية المطلوبة",parent=self.root)
        else: 
            # price_cal=int(self.var_qty.get())*float(self.var_price.get())
            # price_cal=float(price_cal)
            # sale_cal=int(self.var_qty.get())*float(self.var_sale.get())
            # sale_cal=float(sale_cal)
            cart_data=[self.var_pname.get(),self.var_price.get(),self.var_qty.get()]
            
            # ======update cart======
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pname.get()==row[0]:
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
                        self.cart_list[index_][2]=self.var_qty.get()
            else:
                 self.cart_list.append(cart_data)

            self.show_cart()
            self.calculate_bill_details()

    def calculate_bill_details(self):
        self.billamnt = sum(float(row[1]) * int(row[2]) for row in self.cart_list)

        self.bill_update(self.billamnt,len(self.cart_list)) # تحديث الفاتورة

    def bill_update(self, billamnt , cart_length):
        self.lbl_amnt.config(text=f'مبلغ الفاتورة\n{str(billamnt)}')
        self.cartTitle.config(text=f"[{str(cart_length)}] :سلة التسوق إجمالي المنتج ")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}",parent=self.root)
    
    def generate_bill(self):
        if self.var_sup.get() == "" and self.var_contact.get() == "":
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
            
            fp=open(f'purchases/{str(self.invoice)}.txt','w',encoding="utf-8")
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('حفظ', "تم إنشاء الفاتورة \n و حفظها على الجهاز",parent=self.root)
            self.chk_print=1


    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tBizOpsHub - Inventory
\t\t  فاتورة شراء
\t   شركة الأخوة لتجارة قطع الغيار  
\t  Phone No. +201********* , Dokki
{str("="*46)}
Supplier Name: {self.var_sup.get()}
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
{str("="*46)}\n
        '''
        
        self.txt_bill_area.insert(END,bill_bottom_temp)

    

    def bill_middle(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                name = row[0]
                price = float(row[1]) * int(row[2])
                price = str(price)
                self.txt_bill_area.insert(END, "\n" + name + "\t\t" + row[2] + "\t\tEGP." + price + "\n")
                # ==========update qty in product table==========
            #     cur.execute('Update product set qty=?,status=? where pid=?', (
            #         qty,
            #         status,
            #         pid
            #     ))
            #     con.commit()
            # con.close()
            # self.show()
        except Exception as ex:
            messagebox.showerror("حدث خطأ", f"خطأ بسبب : {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_sup.set("Select")
        self.var_contact.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_sale.set('')
        self.var_qty.set('')


    def clear_all(self):
        del self.cart_list[:]
        self.var_sup.set('')
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

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('طباعة',"يرجى الانتظار أثناء الطباعة\nاشغل وقتك بذكر الله",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file, 'w',encoding="utf-8").write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('حدث خطأ',"يرجى إنشاء فاتورة لطباعة الإيصال",parent=self.root)

    def purchase(self):
        self.root.destroy()
        os.system("python purchases.py")


if __name__=="__main__":
    root=Tk()
    ob=BuyingClass(root)
    root.mainloop()
    
