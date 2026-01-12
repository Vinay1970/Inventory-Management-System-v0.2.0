from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import math
from functions import size_changer, go_back, clear_content,connect_database, treeview_data, delete, calculator, db_cursor
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

global InvoiceNo

def billPrnt():
    billNoWin = Toplevel()
    billNoWin.title('Bill No')
    billNoWin.geometry('200x100')
    billNoWin.grab_set()

    global InvoiceNo

    invoiceNo = Label(billNoWin, text='Enter the Bill No.', font=('Ariel', 12, 'bold'))
    invoiceNo.pack(pady=10)

    Invoice = Entry(billNoWin)
    Invoice.pack(pady=10)

    def submit_bill():
        InvoiceNo = Invoice.get().strip()
        print("Bill No entered:", InvoiceNo)
        create_bill_pdf(InvoiceNo)
        billNoWin.destroy()   # close popup after submit

    submitBtn = Button(billNoWin, text="Submit", command=submit_bill)
    submitBtn.pack(pady=5)

def create_bill_pdf(billNo):
    filename = f'Bill_{billNo}.pdf'
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Supermarket Bill")
    with db_cursor() as (cursor, connection):
      if not cursor:
        return
      cursor.execute("SELECT * FROM sale_data WHERE billNo = %s", (billNo,))
      rows = cursor.fetchall()
    # Bill details
    if not rows:
        print("No data found for Bill No:", billNo)
        return

    # Extract header info from first row
    id,name,price,quantity,client,phno,crdate,billno,gtotal, discountamt = rows[0]

    # Bill details
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Bill No: {billNo}")
    c.drawString(50, height - 120, f"Client: {client}")
    c.drawString(50, height - 140, f"Date: {crdate}")

    # Table header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 180, "Item")
    c.drawString(200, height - 180, "Price")
    c.drawString(300, height - 180, "Qty")
    c.drawString(400, height - 180, "Amount")

    # Items
    y = height - 200
    c.setFont("Helvetica", 12)
    for id,name,price,quantity,client,phno,crdate,billno,gtotal, discountamt in rows:
        c.drawString(50, y, str(name))
        c.drawString(200, y, f"{price:.2f}")
        c.drawString(300, y, str(quantity))
        c.drawString(400, y, f"{gtotal:.2f}")
        y -= 20

    # Totals (query DB separately)
    with db_cursor() as (cursor, connection):
      if cursor:
        cursor.execute("SELECT SUM(gtotal) FROM sale_data WHERE billNo = %s", (billNo,))
        result = cursor.fetchone()[0]
        grtotal = 0 if result is None else round(result, 2)
        cursor.execute("SELECT SUM(discountamt) FROM sale_data WHERE billNo = %s", (billNo,))
        discountResult = cursor.fetchone()[0]
        discountAmount = 0 if discountResult is None else round(discountResult, 2)
        net_payable = round(grtotal - discountAmount, 2)
      else:
        grtotal = 0
        discountAmount = 0
        net_payable = 0
   
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 20, f"Total Price: {grtotal:.2f}")
    c.drawString(50, y - 40, f"Total Discount: {discountAmount:.2f}")
    c.drawString(50, y - 60, f"Net Payable: {net_payable:.2f}")

    c.save()
    print(f"Bill saved as {filename}")

    # cursor/connection closed by context manager




def clearFields(lbl_amt,lbl_disc,lbl_net_pay,saleTreeview):
   
    lbl_amt.config(text='Bill Amt[0]')
    lbl_disc.config(text='Discount[0]')
    lbl_net_pay.config(text='Net Pay[0]')
    saleTreeview.delete(*saleTreeview.get_children())


def show_sale_data(saleTreeview, billNo, lbl_amt,lbl_disc,lbl_net_pay):
    # Clear existing rows in Treeview
    saleTreeview.delete(*saleTreeview.get_children())
    try:
      with db_cursor() as (cursor, connection):
        if not cursor:
          return
        cursor.execute("SELECT billno,name, price, quantity, gtotal FROM sale_data WHERE billNo = %s", (billNo,))
        rows = cursor.fetchall()
        for row in rows:
          saleTreeview.insert("", "end", values=row)
        cursor.execute("SELECT SUM(gtotal) FROM sale_data WHERE billNo = %s", (billNo,))
        result = cursor.fetchone()[0]
        grtotal = 0 if result is None else round(result, 2)
        lbl_amt.config(text=f'Bill Amt[{grtotal}]')
        cursor.execute("SELECT SUM(discountamt) FROM sale_data WHERE billNo = %s", (billNo,))
        discountResult = cursor.fetchone()[0]
        discountAmount = 0 if discountResult is None else round(discountResult, 2)
        lbl_disc.config(text=f'Discount[{discountAmount}]')
        net_payable = round(grtotal - discountAmount, 2)
        lbl_net_pay.config(text=f'Net Pay[{net_payable}]')
    except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')

def billGen(billFrame, saleTreeview, lbl_amt,lbl_disc,lbl_net_pay):
    billNoWin = Toplevel()
    billNoWin.title('Bill No')
    billNoWin.geometry('200x100')
    billNoWin.grab_set()

    global InvoiceNo

    invoiceNo = Label(billNoWin, text='Enter the Bill No.', font=('Ariel', 12, 'bold'))
    invoiceNo.pack(pady=10)

    Invoice = Entry(billNoWin)
    Invoice.pack(pady=10)

    def submit_bill():
        InvoiceNo = Invoice.get().strip()
        print("Bill No entered:", InvoiceNo)
        show_sale_data(saleTreeview, InvoiceNo,lbl_amt,lbl_disc,lbl_net_pay)
        billNoWin.destroy()   # close popup after submit

    submitBtn = Button(billNoWin, text="Submit", command=submit_bill)
    submitBtn.pack(pady=5)

def show_bill_data(cartTreeview, billNo):
  # Clear existing rows in Treeview
  cartTreeview.delete(*cartTreeview.get_children())
  try:
    with db_cursor() as (cursor, connection):
      if not cursor:
        return
      cursor.execute("SELECT billno,name, price, quantity FROM sale_data WHERE billNo = %s", (billNo,))
      rows = cursor.fetchall()
      for row in rows:
        cartTreeview.insert("", "end", values=row)
  except Exception as e:
    messagebox.showerror('Error', f'Error due to {e}')

def clearCart(prdEntry, priceEntry, qtyEntry,billno, cartTitle, treeview):
    global total, gtotal
    total = 0
    gtotal =0
    # Clear all Entry fields
    prdEntry.delete(0, END)
    priceEntry.delete(0, END)
    qtyEntry.delete(0, END)
    billno.delete(0, END)
    # Reset cart label
    cartTitle.config(text=f'Cart \t Total Product :[{total}]')

    # Clear all rows in Treeview
    treeview.delete(*treeview.get_children())
    

def addProduct(client, phno, crdate, billno,name, price, quantity, Treeview, cartTitle, total, discount):
    if billno == None:
      messagebox.showerror('Error', 'Enter Bill No')
      return
    elif client =='':
      messagebox.showerror('Error', 'Enter Client Name')
      return
    elif phno == '':
      messagebox.showerror('Error', 'Enter Bill No')
      return
    
    gtotal = float(price)*int(quantity)
    discountamt = (float(gtotal) * float(discount))/100
    try:
      with db_cursor() as (cursor, connection):
        if not cursor:
          return
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_data (
          id INT AUTO_INCREMENT PRIMARY KEY,
          name VARCHAR(100),
          price float,
          quantity INT,
          client VARCHAR(100),
          phno VARCHAR(100),
          crdate DATE,
          billno INT,
          gtotal float,
          discountamt float
        )
        ''')
        price = float(price)
        cursor.execute('INSERT INTO sale_data(name, price, quantity,client, phno, crdate, billno, gtotal,discountamt) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (name,price,quantity,client, phno, crdate, billno,gtotal,discountamt))
        connection.commit()
        messagebox.showinfo('Success','The Record is Added')
        cursor.execute("SELECT SUM(quantity) FROM sale_data WHERE billNo = %s", (billno,))
        result = cursor.fetchone()[0]
        total = 0 if result is None else result
        cartTitle.config(text=f'Cart \t Total Product :[{total}]')
        show_bill_data(Treeview,billno)
    except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')

def select_data(event,name,price,qty,discount,treeview, stockLable):
  selected=treeview.selection()
  index = selected[0]
  content=treeview.item(index)['values']

  name.delete(0,END)
  price.delete(0,END)
  qty.delete(0,END) 
  discount.delete(0,END) 

  name.insert(0,content[1])
  price.insert(0,content[2])
  qty.insert(0,content[3])

  discount.insert(0,content[4])

  stockLable.config(text=f'In Stock [{content[3]}]')


def search_product(search_entry,treeview):
  if search_entry=='':
    messagebox.showwarning('Warning', 'Please enter the Value')
  else:
    try:
      with db_cursor() as (cursor, connection):
        if not cursor:
          return
        cursor.execute("SELECT * FROM product_data WHERE name LIKE %s", (f"%{search_entry}%",))
        records = cursor.fetchall()

      if len(records) == 0:
        messagebox.showerror('Erorr', 'No Records found')
        return
      treeview.delete(*treeview.get_children())
      for record in records:
        treeview.insert('',END, values=record)
    except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')

def Show_all(treeview):
  treeview_data(treeview,'prd')

def billing(window,emp_frame, sup_frame, cat_frame, pdc_frame, sale_frame, contentFrame,  subtitlelabel):
  global back_image, cat_img  
  clear_content(contentFrame)
  global img_back, employee_frame, employee_treeview

  emp_frame.place_forget()
  sup_frame.place_forget()
  cat_frame.place_forget()
  pdc_frame.place_forget()
  sale_frame.place_forget()

  billing_frame = Frame(window,
                         width=1270, 
                         height=600, 
                         bg='white')
  billing_frame.pack(fill='both', expand=True)

  

  heading_Label = Label(billing_frame,
                         text="Manage Billing Details",
                         font=('Arial', 16, 'bold'),
                         bg="#040822",
                         fg='white'
                         )
  heading_Label.pack(pady=20,fill='x')

# Back Button

  img_back = size_changer('image/back.png', .05)
  back_button = Button(billing_frame, 
                         image=img_back, 
                         bg='white',
                         bd=0,
                         cursor='hand2',
                         command=lambda: go_back(billing_frame,
                                                 emp_frame, 
                                                 sup_frame, 
                                                 cat_frame, 
                                                 pdc_frame, 
                                                 sale_frame)
                         )
  back_button.place(x=10, y=50)

# product Frame
#  

  productFrame = Frame(billing_frame, 
                       bd=4, 
                       relief= RIDGE, 
                       bg='white')
  productFrame.place(x=6, 
                     y=80, 
                     width= 410, 
                     height= 500)

  pTitle = Label(productFrame, 
                 text='All Products', 
                 font=('gody old style', 20,'bold'),
                 bg='#262626', 
                 fg='white').pack(side=TOP, fill='x')

  searchFrame = Frame(productFrame, 
                      bd=4, 
                      relief= RIDGE, 
                      bg='white')
  searchFrame.place(x=2, 
                    y=42, 
                    width= 400, 
                    height= 90)

  sTitle = Label(searchFrame, 
                 text='Search by Name', 
                 font=('Arial', 15,'bold'),
                 bg='white', 
                 fg='green').grid(row=0, columnspan= 2)

  nameTitle = Label(searchFrame, 
                    text='Name', 
                    font=('Arial', 15,'bold'),
                    bg='white').grid(row=1, column=0)
  
  var_search = Entry(searchFrame, 
                     font=('Arial', 15,'bold'),
                     bg='lightyellow')
  var_search.grid(row=1,column=1)

  btnSearch = Button(searchFrame, 
                     text='Search', 
                     font=('gody old style', 15,'bold'), 
                     bg='#262626', fg='lightyellow',command= lambda : search_product(var_search.get(),productTreeview)).grid(row=1,
                                                          column=2)

  dispFrame = Frame(productFrame, bd=3, relief=RIDGE)
  dispFrame.place(x=2, y=135, width=400,height=320)

  
  scrolly=Scrollbar(dispFrame, orient=VERTICAL)
  
  scrollx=Scrollbar(dispFrame, orient=HORIZONTAL)

  productTreeview = ttk.Treeview(dispFrame, 
                                 columns=('invoice', 
                                         'name', 
                                         'price',
                                         'quantity',
                                         'discount'),
                                  show='headings', 
                                  yscrollcommand=scrolly.set,
                                  xscrollcommand=scrollx.set)
  
  scrollx.pack(side=BOTTOM, fill=X)
  scrolly.pack(side=RIGHT, fill=Y)
  scrollx.config(command=productTreeview.xview)
  scrolly.config(command= productTreeview.yview)
  productTreeview.pack(fill=BOTH, expand=1)

  productTreeview.heading('invoice', text='Invoice')
  productTreeview.heading('name', text='Name')
  productTreeview.heading('price', text='Price')
  productTreeview.heading('quantity', text='Quantity')
  productTreeview.heading('discount', text='Discount')

  productTreeview.column('invoice', width= 5)
  productTreeview.column('name', width= 80)
  productTreeview.column('price', width= 120)
  productTreeview.column('quantity', width= 70)
  productTreeview.column('discount', width= 10)


  treeview_data(productTreeview,'prd1')

  lblNote = Label(productFrame, 
                  text='Enter 0 quantity to remove product from the cart', 
                  font=('Arial', 10,'bold'), 
                  bg='white', 
                  fg='red').pack(side=BOTTOM, fill='x')
  
  
  btnShow = Button(searchFrame, 
                   text='Show All', 
                   font=('gody old style', 15,'bold'), 
                   bg='#262626', 
                   fg='lightyellow', command=lambda : Show_all(productTreeview)).grid(row=0,
                                           column=2)


  custFrame = Frame(billing_frame,bd=4, relief=RIDGE, bg='white')
  custFrame.place(x=420, y=80,width=500, height=70)

  cTitle = Label(custFrame, 
                 text='Custormer Detail', 
                 font=('gody old style', 15,'bold'),
                 bg='#262626', 
                 fg='white').pack(side=TOP, fill='x')
  
  nameTitle = Label(custFrame, 
                    text='Name :', 
                    font=('Arial', 15,'bold'),
                    bg='white').place(x=2, y= 35)
  
  nameEntery = Entry(custFrame, 
                     font=('Arial', 15,'bold'),
                     bg='lightyellow')
  nameEntery.place(x=80, y= 35, width=150)
  
  phoneTitle = Label(custFrame, 
                    text='Phone No. :', 
                    font=('Arial', 15,'bold'),
                    bg='white').place(x=232, y= 35)
  
  phoneEntery = Entry(custFrame, 
                     font=('Arial', 15,'bold'),
                     bg='lightyellow')
  phoneEntery.place(x=350, y= 35, width=140)

  calc_cart_frame = Frame(billing_frame,bd=4, relief=RIDGE, bg='white')
  calc_cart_frame.place(x=420, y=152,width=500, height=350)

# Calculator

  calculator(calc_cart_frame)

# Cart Frame

  cartframe = Frame(calc_cart_frame,bd=4, relief=RIDGE, bg='white')
  cartframe.place(x=272, y=2,width=218, height=340)
  
  cartTitle = Label(cartframe, 
                 text='Cart \t Total Product :[0]', 
                 font=('gody old style', 10,'bold'),
                 bg='#262626', 
                 fg='white')
  
  cartTitle.pack(side=TOP, fill='x')

  scrolly=Scrollbar(cartframe, orient=VERTICAL)
  
  scrollx=Scrollbar(cartframe, orient=HORIZONTAL)

  cartTreeview = ttk.Treeview(cartframe, 
                                 columns=('billno', 
                                         'name', 
                                         'price',
                                         'quantity'),
                                  show='headings', 
                                  yscrollcommand=scrolly.set,
                                  xscrollcommand=scrollx.set)
  
  scrollx.pack(side=BOTTOM, fill=X)
  scrolly.pack(side=RIGHT, fill=Y)
  scrollx.config(command=cartTreeview.xview)
  scrolly.config(command= cartTreeview.yview)
  cartTreeview.pack(fill=BOTH, expand=1)

  cartTreeview.heading('billno', text='Invoice')
  cartTreeview.heading('name', text='Name')
  cartTreeview.heading('price', text='Price')
  cartTreeview.heading('quantity', text='Quantity')
 
  cartTreeview.column('billno', width= 5)
  cartTreeview.column('name', width= 80)
  cartTreeview.column('price', width= 120)
  cartTreeview.column('quantity', width= 70)

  

 
# cart Buttons frame
  buttonsFrame = Frame(billing_frame,bd=4, relief=RIDGE, bg='white')
  buttonsFrame.place(x=420, y=504,width=500, height=77)

  prdName = Label(buttonsFrame, 
                    text='Product Name :', 
                    font=('Arial', 10,'bold'),
                    bg='white').place(x=2, y= 2)
  
  prdEntry = Entry(buttonsFrame, 
                     font=('Arial', 10,'bold'),
                     bg='lightyellow')
  prdEntry.place(x=2, 
                                             y= 25, 
                                             width=75)
  
  prdPrice = Label(buttonsFrame, 
                    text='Price :', 
                    font=('Arial', 10,'bold'),
                    bg='white').place(x=100, y= 2)
  
  priceEntry = Entry(buttonsFrame, 
                     font=('Arial', 10,'bold'),
                     bg='lightyellow')
  priceEntry.place(x=100, 
                                             y= 25, 
                                             width=75)
  
  billNoLable = Label(buttonsFrame, 
                    text='Bill No :', 
                    font=('Arial', 10,'bold'),
                    bg='white').place(x=200, y= 2)
  
  billNo = Entry(buttonsFrame, 
                     font=('Arial', 10,'bold'),
                     bg='lightyellow')
  billNo.place(x=200, 
                                             y= 25, 
                                             width=75)
  
  discountLable = Label(buttonsFrame, 
                    text='Discount :', 
                    font=('Arial', 10,'bold'),
                    bg='white').place(x=280, y= 2)
  
  discount = Entry(buttonsFrame, 
                     font=('Arial', 10,'bold'),
                     bg='lightyellow')
  discount.place(x=280, 
                                             y= 25, 
                                             width=75)

  prdQty = Label(buttonsFrame, 
                    text='Quantity :', 
                    font=('Arial', 10,'bold'),
                    bg='white').place(x=360, y= 2)
  
  qtyEntry = Entry(buttonsFrame, 
                     font=('Arial', 10,'bold'),
                     bg='lightyellow')
  qtyEntry.place(x=360, 
                                             y= 25, 
                                             width=75)

  # getCart(qtyEntry, cartTitle)

  quantity = Entry()
  inStockLable = Label(buttonsFrame, 
                    text=f'In Stock [0000]', 
                    font=('Arial', 10,'bold'),
                    bg='white')
  inStockLable.place(x=2, y= 45)

  
  btnAddPrd = Button(buttonsFrame, 
                   text='Add Product', 
                   font=('gody old style', 10,'bold'), 
                   bg='#262626', 
                   fg='lightyellow', command= lambda: addProduct(nameEntery.get(),
                                                                  phoneEntery.get, 
                                                                  date.today(), 
                                                                  billNo.get(),
                                                                  prdEntry.get(), 
                                                                  priceEntry.get(), 
                                                                  qtyEntry.get(), cartTreeview, 
                                                                  cartTitle, 
                                                                  total, 
                                                                  discount.get()))
  
  btnAddPrd.place(x=180,
                                           y=47, 
                                           height=20)

  btnClrPrd = Button(buttonsFrame, 
                     text='Clear Prod', 
                     font=('gody old style', 10,'bold'), 
                     bg='#262626', fg='lightyellow', command=lambda : clearCart(prdEntry, priceEntry, qtyEntry,billNo, cartTitle, cartTreeview))
  
  btnClrPrd.place(x=360,
                                                           y=47, 
                                                           height=20)
  
# Bill Area
  billFrame = Frame(billing_frame, bd=2, relief=RIDGE, bg='white')
  billFrame.place(x=925, y=80, width=335, height=410)
  BTitle = Label(billFrame, 
                 text='Bill', 
                 font=('gody old style', 20,'bold'),
                 bg='#262626', 
                 fg='white').pack(side=TOP, fill='x')
  
  scrolly=Scrollbar(billFrame, orient=VERTICAL)
  
  scrollx=Scrollbar(billFrame, orient=HORIZONTAL)

  saleTreeview = ttk.Treeview(billFrame, 
                                 columns=('billno', 
                                         'name', 
                                         'price',
                                         'quantity',
                                         'grtotal'),
                                  show='headings', 
                                  yscrollcommand=scrolly.set,
                                  xscrollcommand=scrollx.set)
  
  scrollx.pack(side=BOTTOM, fill=X)
  scrolly.pack(side=RIGHT, fill=Y)
  scrollx.config(command=saleTreeview.xview)
  scrolly.config(command= saleTreeview.yview)
  saleTreeview.pack(fill=BOTH, expand=1)

  saleTreeview.heading('billno', text='Invoice')
  saleTreeview.heading('name', text='Name')
  saleTreeview.heading('price', text='Price')
  saleTreeview.heading('quantity', text='Quantity')
  saleTreeview.heading('grtotal', text = 'Total')
 
  saleTreeview.column('billno', width= 5)
  saleTreeview.column('name', width= 80)
  saleTreeview.column('quantity', width= 70)
  saleTreeview.column('price', width= 120)
  saleTreeview.column('grtotal', width= 120)


# Bill Buttons
  billBtnFrame=Frame(billing_frame, bd=2, relief=RIDGE, bg='white')
  billBtnFrame.place(x=925, y=492,width=335, height=90)

  lbl_amt = Label(billBtnFrame, text='Bill Amt[0]', font=('goudy old style', 12, 'bold'), bg='#3f51b5', fg='white')
  lbl_amt.place(x=2, y=2, width=108, height=40)
 
  lbl_disc = Label(billBtnFrame, text='Discount[0]', font=('goudy old style', 12, 'bold'), bg='#3f51b5', fg='white')
  lbl_disc.place(x=112, y=2, width=108, height=40)

  lbl_net_pay = Label(billBtnFrame, text='Net Pay[0]', font=('goudy old style', 12, 'bold'), bg='#3f51b5', fg='white')
  lbl_net_pay.place(x=224, y=2, width=108, height=40) 

  
  btnPrint = Button(billBtnFrame, text='Print',cursor='hand2', font=('goudy old style', 12, 'bold'), bg="#e75218", fg='white', command= lambda :billPrnt())
  btnPrint.place(x=2, y=44, width=108, height=40)
 
  btnClear = Button(billBtnFrame, text='Clear',cursor='hand2', font=('goudy old style', 12, 'bold'), bg="#e75218", fg='white',command= lambda : clearFields(lbl_amt,lbl_disc,lbl_net_pay,saleTreeview))
  btnClear.place(x=112, y=44, width=108, height=40)

  btnGnrt = Button(billBtnFrame, text='Bill Genrate',cursor='hand2', font=('goudy old style', 12, 'bold'), bg="#e75218", fg='white', command= lambda : billGen(billFrame, saleTreeview,lbl_amt,lbl_disc,lbl_net_pay))
  btnGnrt.place(x=224, y=44, width=108, height=40) 

  productTreeview.bind('<ButtonRelease-1>', lambda event:select_data(event,prdEntry,priceEntry,quantity,discount,productTreeview, inStockLable))
  