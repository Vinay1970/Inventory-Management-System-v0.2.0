from tkinter import *
from tkinter import messagebox
import os
from functions import size_changer, go_back, clear_content

# Function Search Button

def search(var_invoice, bill_lists,bill_detail):
    if var_invoice.get()=='':
      messagebox.showerror('Error', 'Invoice no.should be required')
    else:
      if var_invoice.get() in bill_lists:
          fp = open(f'bill/{var_invoice.get()}.txt', 'r')
          bill_detail.delete('1.0', END)
          for i in fp:
              bill_detail.insert(END,i)
          fp.close()
            
#  Funciton Clear Button

def clear(bill_list, bill_lists, bill_detail):
   show(bill_list, bill_lists) 
   bill_detail.delete('1.0', END)           

# Function Show

def show(bill_list, bill_lists):
    del bill_lists[:]
    bill_list.delete(0,END)
    for i in os.listdir('bill'):
      if i.split('.')[-1]=='txt':
        bill_list.insert(END,i)
        bill_lists.append(i.split('.')[0])

# Function Get Data

def get_data(event,bill_list, bill_detail):
   index_= bill_list.curselection()
   file_name= bill_list.get(index_)
   bill_detail.delete(1.0, END)
   fp=open(f'bill/{file_name}', 'r')
   for i in fp:
      bill_detail.insert(END, i)
   fp.close()

#  Main Sales Form
  
def sales_form(window,emp_frame, sup_frame, cat_frame, pdc_frame, sale_frame, contentFrame):
  clear_content(contentFrame)
  global img_back, employee_frame, employee_treeview

  emp_frame.place_forget()
  sup_frame.place_forget()
  cat_frame.place_forget()
  pdc_frame.place_forget()
  sale_frame.place_forget()

  sales_frame = Frame(contentFrame,
                        width=1070, 
                        height=600, 
                        bg='white')
  sales_frame.pack(fill='both', expand=True)

  heading_Label = Label(sales_frame,
                         text="View Customer Bill",
                         font=('Arial', 16, 'bold'),
                         bg="#040822",
                         fg='white'
                         )
  heading_Label.pack(pady=18,fill='x')

# Back Button

  img_back = size_changer('image/back.png', .05)
  back_button = Button(sales_frame, 
                         image=img_back, 
                         bg='white',
                         bd=0,
                         cursor='hand2',
                         command=lambda: go_back(sales_frame,
                                                 emp_frame, 
                                                 sup_frame, 
                                                 cat_frame, 
                                                 pdc_frame, 
                                                 sale_frame)
                         )
  back_button.place(x=10, y=50)

# bill List area

  var_invoice = StringVar()
  bill_lists =[]
  lbl_invoice  = Label(sales_frame, 
                        text= 'Invoice No', 
                        font=('Areal', 14,'bold'), 
                        bg='white').place (x=50,y=100)
  txt_invoice  = Entry(sales_frame, 
                        textvariable=var_invoice, 
                        font=('Areal', 14,'bold'), 
                        bg='lightyellow').place (x=160,
                                                y=100, 
                                                width = 180, 
                                                height=28)
  
# Search Button

  btn_search = Button (sales_frame, 
                        text='Search', 
                        font=('Areal', 15,'bold'), 
                        bg='#2196f3', 
                        fg='white', 
                        cursor='hand2', 
                        command=lambda : search(var_invoice, 
                                                bill_lists,
                                                bill_detail) ).place(x=360,
                                                                    y=100,
                                                                    width=120,
                                                                    height=28 )

# Clear Button

  btn_clear = Button (sales_frame, 
                        command=lambda : clear(bill_list, 
                                              bill_lists, 
                                              bill_detail), 
                      text='Clear', 
                      font=('Areal', 15,'bold'), 
                      bg='#2196f3', 
                      fg='white', 
                      cursor='hand2').place(x=500,
                                            y=100,
                                            width=120,
                                            height=28 )

# Bill Frame

  bill_frame = Frame(sales_frame, 
                      bd=3, 
                      relief=RIDGE, 
                      bg='white')
  bill_frame.place(x=50, 
                    y= 140, 
                    width=200, 
                    height=330)

 # Bills List

  scrolly=Scrollbar(bill_frame, orient=VERTICAL)

  bill_list = Listbox(bill_frame, 
                      font=('gody old style',15, 'bold'),
                      bg='white', 
                      yscrollcommand=scrolly.set)
  scrolly.pack(side=RIGHT,fill=Y)
  scrolly.config(command=bill_list.yview)
  bill_list.pack(fill=BOTH, expand=1)  
  bill_list.bind('<ButtonRelease-1>', lambda event:get_data(event,
                                                            bill_list,
                                                            bill_detail))
  


  # billview area
  bill_view = Frame(sales_frame, 
                    bd=3, 
                    relief=RIDGE, 
                    bg='lightyellow')
  bill_view.place(x=280, 
                  y= 140, 
                  width=400, 
                  height=330)

  lbl_title2= Label(bill_view, 
                    text= 'Customer Bill Area', 
                    font=('gody old style',15, 'bold'),
                    bg='orange').pack(side = TOP, fill=X)

  scrolly2 = Scrollbar(bill_view, orient=VERTICAL)
  bill_detail = Text(bill_view, 
                    font=('gody old style',15, 'bold'),
                    bg='lightyellow', 
                    yscrollcommand=scrolly2.set)
  scrolly2.pack(side=RIGHT, fill=Y)
  scrolly2.config(command=bill_detail.yview)
  bill_detail.pack (fill=BOTH, expand=1)

# Image Bill
#   
  bill_image =size_changer('image/bill.png', .7)

  lbl_image=Label(sales_frame, 
                  image=bill_image, 
                  bg='white')
  lbl_image.image=bill_image
  lbl_image.place(x=700, y= 110)

  show(bill_list, bill_lists)
