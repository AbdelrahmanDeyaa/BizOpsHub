from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import tkinter as tk
import sqlite3
import os
from bidi.algorithm import get_display
class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+400+200")
        self.root.resizable(False,False)
        self.root.iconbitmap('images/logo.ico')
        self.root.title("Inventory Management System | Database")
        self.root.config(bg="white")
        self.root.focus_force()
        self.bill_list=[]
        self.var_invoice=StringVar()
        #===============title=================
        lbl_title=Label(self.root,text="View Customer Bills",font=("times new roman",30),bg="#0B2F3A",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_invoice=Label(self.root,text="رقم الفاتورة",font=("times new roman",15),bg="white").place(x=50,y=100)      
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("times new roman",15),bg="lightyellow").place(x=160,y=100,width=180,height=28)

        btn_search=Button(self.root,text="بحث",command=self.search,font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=28)
        btn_Clear=Button(self.root,text="مسح",command=self.clear,font=("times new roman",15,"bold"),bg="#607d8b",fg="white",cursor="hand2").place(x=490,y=100,width=120,height=28)

        #===============Bill List=================
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
        self.Sales_List=Listbox(sales_Frame,font=("times new roman",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

        #===============Bill Area=================
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=140,width=490,height=330)

        lbl_title2=Label(bill_Frame,text="Customer Bills Area",font=("times new roman",20),bg="orange").pack(side=TOP,fill=X)

        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,font=("times new roman",13),bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        #===============Images=================
        self.bill_photo=Image.open("images/pngegg5.png")
        self.bill_photo=self.bill_photo.resize((310,330),Image.LANCZOS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)
        
        lbl_image=Label(self.root,image=self.bill_photo,bd=0)
        lbl_image.place(x=780,y=140)

        self.show()
    #===========================================
    def show(self):
        del self.bill_list[:]
        self.Sales_List.delete(0,END)
        #print(os.listdir('../AccountingProject'))
        for i in os.listdir('bill'):
            #print(i.split('.'),i.split('.')[-1])
            if i.split('.')[-1]=='txt':
                self.Sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_=self.Sales_List.curselection()
        file_name=self.Sales_List.get(index_)
        #print(file_name)
        self.bill_area.delete('1.0',END)
        fp=open(f'bill/{file_name}','r',encoding='utf-8')
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()

    

    def search(self):
        invoice_partial_number = self.var_invoice.get()
        if invoice_partial_number == "":
            messagebox.showerror("خطأ", "يجب عليك إدخال جزء من رقم الفاتورة", parent=self.root)
        else:
            # Get all files in the 'bill' directory
            bill_files = os.listdir('bill')
            matched_bills_content = ""

            # Check if the entered partial number is in any of the filenames
            for filename in bill_files:
                if invoice_partial_number in filename:
                    file_path = os.path.join('bill', filename)
                    # Open the file and read its contents
                    with open(file_path, 'r', encoding='utf-8') as fp:
                        matched_bills_content += f"فاتورة: {filename}\n"
                        matched_bills_content += fp.read() + "\n\n"

            if matched_bills_content:
                # Display the content of matched bills
                self.bill_area.delete('1.0', END)
                self.bill_area.insert(END, matched_bills_content)
            else:
                messagebox.showerror("خطأ", "لا توجد فواتير تحتوي على هذا الجزء من رقم الفاتورة", parent=self.root)




    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)
        self.var_invoice.set("")
           


if __name__=="__main__":
    root=tk.Tk()
    ob=salesClass(root)
    root.mainloop()