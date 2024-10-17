from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import tkinter as tk
import sqlite3
import os
from bidi.algorithm import get_display
class purchasesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+400+200")
        self.root.resizable(False,False)
        self.root.iconbitmap('images/logo.ico')
        self.root.title("Inventory Management System | Database")
        self.root.config(bg="white")
        self.root.focus_force()
        self.purchases_list=[]
        self.var_invoice=StringVar()
        #===============title=================
        lbl_title=Label(self.root,text="View Customer Purchases",font=("times new roman",30),bg="#0B2F3A",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_invoice=Label(self.root,text="رقم الفاتورة",font=("times new roman",15),bg="white").place(x=50,y=100)      
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("times new roman",15),bg="lightyellow").place(x=160,y=100,width=180,height=30)

        btn_search=Button(self.root,text="بحث",command=self.search,font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=30)
        btn_Clear=Button(self.root,text="مسح",command=self.clear,font=("times new roman",15,"bold"),bg="#607d8b",fg="white",cursor="hand2").place(x=490,y=100,width=120,height=30)

        btn_logout=Button(self.root,text="فواتير المشتريات",command=self.buying,font=("times new roman",15,"bold"),bg="#DBA901",cursor="hand2")
        btn_logout.place(x=940,y=100,width=150,height=28)

        #===============purchases List=================
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
        self.Sales_List=Listbox(sales_Frame,font=("times new roman",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

        #===============purchases Area=================
        purchases_Frame=Frame(self.root,bd=3,relief=RIDGE)
        purchases_Frame.place(x=280,y=140,width=490,height=330)

        lbl_title2=Label(purchases_Frame,text="Customer purchasess Area",font=("times new roman",20),bg="orange").pack(side=TOP,fill=X)

        scrolly2=Scrollbar(purchases_Frame,orient=VERTICAL)
        self.purchases_area=Text(purchases_Frame,font=("times new roman",13),bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.purchases_area.yview)
        self.purchases_area.pack(fill=BOTH,expand=1)

        #===============Images=================
        self.purchases_photo=Image.open("images/pngegg5.png")
        self.purchases_photo=self.purchases_photo.resize((310,330),Image.LANCZOS)
        self.purchases_photo=ImageTk.PhotoImage(self.purchases_photo)
        
        lbl_image=Label(self.root,image=self.purchases_photo,bd=0)
        lbl_image.place(x=780,y=140)

        self.show()
    #===========================================
    def show(self):
        del self.purchases_list[:]
        self.Sales_List.delete(0,END)
        #print(os.listdir('../AccountingProject'))
        for i in os.listdir('purchases'):
            #print(i.split('.'),i.split('.')[-1])
            if i.split('.')[-1]=='txt':
                self.Sales_List.insert(END,i)
                self.purchases_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_=self.Sales_List.curselection()
        file_name=self.Sales_List.get(index_)
        #print(file_name)
        self.purchases_area.delete('1.0',END)
        fp=open(f'purchases/{file_name}','r',encoding='utf-8')
        for i in fp:
            self.purchases_area.insert(END,i)
        fp.close()

    

    def search(self):
        invoice_partial_number = self.var_invoice.get()
        if invoice_partial_number == "":
            messagebox.showerror("خطأ", "يجب عليك إدخال جزء من رقم الفاتورة", parent=self.root)
        else:
            # Get all files in the 'purchases' directory
            purchases_files = os.listdir('purchases')
            matched_purchasess_content = ""

            # Check if the entered partial number is in any of the filenames
            for filename in purchases_files:
                if invoice_partial_number in filename:
                    file_path = os.path.join('purchases', filename)
                    # Open the file and read its contents
                    with open(file_path, 'r', encoding='utf-8') as fp:
                        matched_purchasess_content += f"فاتورة: {filename}\n"
                        matched_purchasess_content += fp.read() + "\n\n"

            if matched_purchasess_content:
                # Display the content of matched purchasess
                self.purchases_area.delete('1.0', END)
                self.purchases_area.insert(END, matched_purchasess_content)
            else:
                messagebox.showerror("خطأ", "لا توجد فواتير تحتوي على هذا الجزء من رقم الفاتورة", parent=self.root)

    def clear(self):
        self.show()
        self.purchases_area.delete('1.0',END)
        self.var_invoice.set("")

    def buying(self):
        self.root.destroy()
        os.system("python buying.py")
           


if __name__=="__main__":
    root=tk.Tk()
    ob=purchasesClass(root)
    root.mainloop()