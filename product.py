from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functions import size_changer, go_back, clear_content,connect_database, treeview_data,delete, db_cursor

def clear_fields(category,
                                                  supplier, 
                                                  price,
                                                  discount,
                                                  quantity, 
                                                  status, 
                                                  name,  
                                                  treeview, check):
    
    
    category.set('Select')
    supplier.set('Select')
    name.delete(0,END)
    price.delete(0,END)
    discount.delete(0,END)
    quantity.delete(0,END)
    status.set('Select Status')
    
    if check:
        treeview.selection_remove(treeview.selection())

def search_product(search_combobox,search_entry,treeview):
  if search_combobox.get() =='Search By':
    messagebox.showwarning('Warning', 'Please select an option')
  elif search_entry.get()=='':
    messagebox.showwarning('Warning', 'Please enter the Value')
  else:
    try:
      with db_cursor() as (cursor, connection):
        if not cursor:
          return
        cursor.execute(f'Select * from product_data Where {search_combobox.get()}=%s', (search_entry.get(),))
        records = cursor.fetchall()

      if len(records) == 0:
        messagebox.showerror('Erorr', 'No Records found')
        return
      treeview.delete(*treeview.get_children())
      for record in records:
        treeview.insert('',END, values=record)
    except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')

def Show_all(search_combobox, search_entry,treeview):
  treeview_data(treeview,'prd')
  search_combobox.set('Search By')
  search_entry.delete(0,END)


def delete_product(category,
                                                  supplier, 
                                                  price, 
                                                  discount,
                                                  quantity, 
                                                  status, 
                                                  name,treeview):
  index = treeview.selection()
  dict= treeview.item(index)
  content=dict['values']
  id = content[0]
  if not index:
    messagebox.showerror('Error', 'No Row is Selected')
    return
  ans=messagebox.askyesno('Confirm','Do you really want to delete')
  if ans:
    try:
      with db_cursor() as (cursor, connection):
        if not cursor:
          return
        cursor.execute('DELETE from product_data WHERE id=%s', (id,))
        connection.commit()
      treeview_data(treeview, 'prd')
      clear_fields(category,
                                                  supplier, 
                                                  price,
                                                  discount, 
                                                  quantity, 
                                                  status, 
                                                  name,  
                                                  treeview, False)
      messagebox.showinfo('INFO', 'Record is Deleted')
    except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')

def update_product(category,supplier, price,discount, quantity, status ,name, treeview):
  # getting ID 
  
  index = treeview.selection()
  dict= treeview.item(index)
  content=dict['values']
  id = content[0]

  if not index:
    messagebox.showerror('Error', 'No Row is Selected')
    return
  try:
    with db_cursor() as (cursor, connection):
      if not cursor:
        return
      cursor.execute('SELECT * from product_data WHERE id= %s', (id,))
      currnt_data = cursor.fetchone()
    currnt_data= currnt_data[1:]
    # converting INT TO STR
    currnt_data=list(currnt_data)
    currnt_data[4]=str(currnt_data[4])
    currnt_data=tuple(currnt_data)


    quantity=int(quantity)
    discount=float(discount)
    price = float(price)
    discounted_price = price - (discount*price)/100
    new_data = (category,supplier,name, price,discount,discounted_price, quantity, status)

    if currnt_data == new_data:
      messagebox.showinfo('INFO', 'No changes detected')
      return
      cursor.execute('UPDATE product_data SET category=%s, supplier=%s, name=%s, price=%s,discount=%s, discounted_price=%s,quantity=%s, status=%s WHERE id = %s',
                     (category, supplier, name, price, discount, discounted_price, quantity, status, id))
      connection.commit()
      messagebox.showinfo('INFO', 'Data is updated')
      treeview_data(treeview, 'prd')
  except Exception as e :
    messagebox.showerror('Error', f'Error due to {e}')
  finally:
    pass

def select_data(event,category,supplier,name,price,discount,quantity, status, treeview):
  index=treeview.selection()
  content=treeview.item(index)
  content= content['values']

  name.delete(0,END)
  price.delete(0,END)
  discount.delete(0,END)
  quantity.delete(0,END)

  category.set(content[1])
  supplier.set(content[2])
  name.insert(0,content[3])
  price.insert(0,content[4])
  discount.insert(0,content[5])
  quantity.insert(0,content[7])
  status.set(content[8])


def ftech_supplier_category(category_c, supplier_c):
  category_option = []
  supplier_option = []
  try:
    with db_cursor() as (cursor, connection):
      if not cursor:
        return
      cursor.execute('Select name from category_data')
      names = cursor.fetchall()
      if names:
        category_c.set('Select')
        for name in names:
          category_option.append(name[0])
      category_c.config(values=category_option)

      cursor.execute('Select name from supplier_data')
      names = cursor.fetchall()
      if names:
        supplier_c.set('Select')
        for name in names:
          supplier_option.append(name[0])
      supplier_c.config(values=supplier_option)
  except Exception as e:
    messagebox.showerror('Error', f'Error due to {e}')


def add_product(category,supplier, price, discount, quantity, status ,name, treeview):
  if category == 'Empty':
    messagebox.showerror('ERROR', 'Please Enter The Category')
  elif supplier == 'Empty':
    messagebox.showerror('ERROR', 'Please Enter The Supplier')
  elif category=='Select' or supplier == 'Select' or price == '' or quantity == '' or status == 'Select Status' or name == '':
    messagebox.showerror('ERROR', 'All Fields are required')
  else:
    try:
      with db_cursor() as (cursor, connection):
        if not cursor:
          return
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(50),
            supplier VARCHAR (100),
            name VARCHAR(100),
            price float,
            discount float,
            discounted_price float,
            quantity INT, 
            status VARCHAR(50)
        )
        """)
        cursor.execute('SELECT * from product_data WHERE category=%s AND supplier = %s AND name = %s', (category, supplier, name))
        existing = cursor.fetchone()
        if existing:
          messagebox.showerror('ERROR', 'Product already Exists')
          return
        discount = float(discount)
        price = float(price)
        discounted_price = price - (discount * price) / 100
        cursor.execute('INSERT INTO product_data(category, supplier, name, price,discount,discounted_price, quantity, status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                       (category, supplier, name, price, discount, discounted_price, quantity, status))
        connection.commit()
      messagebox.showinfo('Success', 'The Record is Added')
      treeview_data(treeview, 'prd')
    except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')



def product_form(window,emp_frame, sup_frame, cat_frame, pdc_frame, sale_frame, contentFrame):
  clear_content(contentFrame)
  global img_back, employee_frame, employee_treeview

  emp_frame.place_forget()
  sup_frame.place_forget()
  cat_frame.place_forget()
  pdc_frame.place_forget()
  sale_frame.place_forget()

  product_frame = Frame(contentFrame,
                        width=1070, 
                        height=600, 
                        bg='white')
  product_frame.pack(fill='both', expand=True)

  heading_Label = Label(product_frame,
                         text="Manage Product Details",
                         font=('Arial', 16, 'bold'),
                         bg="#040822",
                         fg='white'
                         )
  heading_Label.pack(pady=18,fill='x')

# Back Button

  img_back = size_changer('image/back.png', .05)
  back_button = Button(product_frame, 
                         image=img_back, 
                         bg='white',
                         bd=0,
                         cursor='hand2',
                         command=lambda: go_back(product_frame,
                                                 emp_frame, 
                                                 sup_frame, 
                                                 cat_frame, 
                                                 pdc_frame, 
                                                 sale_frame)
                         )
  back_button.place(x=10, y=50)

  left_frame = Frame(product_frame, 
                     bg='white',
                     bd=2,
                     relief=RIDGE)
  left_frame.place(x=20,y=80)

  
  category_lable = Label(left_frame, 
                         text='Category', 
                         font=('Arial', 12, 'bold'))
  category_lable.grid(row=0, 
                      column=0, 
                      padx=22, 
                      pady=18)

  category_combobox = ttk.Combobox(left_frame,
                                   values=('Empty'),
                                   width=18, 
                                   state='readonly', 
                                   font=('Arial', 12, 'bold'), 
                                   )
  category_combobox.set('Category')                              
  category_combobox.grid(row=0,
                         column=1, 
                         padx=10, 
                         pady=18)

  supplier_lable = Label(left_frame, 
                         text='Supplier', 
                         font=('Arial', 12, 'bold'))
  supplier_lable.grid(row=1, 
                      column=0, 
                      padx=22, 
                      pady=18)

  supplier_combobox = ttk.Combobox(left_frame,
                                   values=('Empty'),
                                   width=18, 
                                   state='readonly', 
                                   font=('Arial', 12, 'bold'), )
  supplier_combobox.set('Supplier')                              
  supplier_combobox.grid(row=1, 
                         column=1, 
                         padx=10, 
                         pady=18)

  name_lable = Label(left_frame, 
                     text='Name', 
                     font=('Arial', 12, 'bold')
                     )
  name_lable.grid(row=2, 
                  column=0, 
                  padx=22, 
                  pady=18)

  name_entry = Entry(left_frame, 
                     font=('Arial', 12, 'bold'), 
                     bg="#FAF208")
  name_entry.grid(row=2, 
                  column=1, 
                  padx=22, 
                  pady=18)

  price_lable = Label(left_frame, 
                      text='Price', 
                      font=('Arial', 12, 'bold')
                      )
  price_lable.grid(row=3, 
                   column=0, 
                   padx=22, 
                   pady=18)

  price_entry = Entry(left_frame, 
                      font=('Arial', 12, 'bold'), 
                      bg="#FAF208")
  price_entry.grid(row=3, 
                   column=1, 
                   padx=22, 
                   pady=18)

  discount_lable = Label(left_frame, 
                      text='Discount (%)', 
                      font=('Arial', 12, 'bold')
                      )
  discount_lable.grid(row=4, 
                   column=0, 
                   padx=22, 
                   pady=18)

  discount_spinbox = Spinbox(left_frame,
                             from_=0,
                             to=100, 
                            font=('Arial', 12, 'bold'), 
                             width=19
                             )
  discount_spinbox.grid(row=4, 
                   column=1, 
                   padx=22, 
                   pady=18)

  quantity_lable = Label(left_frame, 
                         text='Quantity', 
                         font=('Arial', 12, 'bold'))
  quantity_lable.grid(row=5, 
                      column=0, 
                      padx=22, 
                      pady=18)

  quantity_entry = Entry(left_frame, 
                         font=('Arial', 12, 'bold'), 
                         bg="#FAF208")
  quantity_entry.grid(row=5, 
                      column=1, 
                      padx=22, 
                      pady=18)

  status_lable = Label(left_frame, 
                       text='Status', 
                       font=('Arial', 12, 'bold'))
  status_lable.grid(row=6, 
                    column=0, 
                    padx=22, 
                    pady=18)

  status_combobox = ttk.Combobox(left_frame,
                                 values=('Active',
                                         'Inavtive'),
                                width=18, 
                                state='readonly', 
                                font=('Arial', 12, 'bold'), )
  status_combobox.set('Select Status')                              
  status_combobox.grid(row=6, 
                       column=1, 
                       padx=10, 
                       pady=18)

  button_frame=Frame(left_frame, bg='white')
  button_frame.grid(row=7, 
                    columnspan=2, 
                    pady=(0,20))

  add_button = Button(button_frame, 
                      text='Add', 
                      font=('Arial', 12, 'bold'), 
                      width = 10, 
                      cursor='hand2', 
                      fg='white', 
                      bg='#0f4d7d', 
                      command=lambda :add_product(category_combobox.get(),
                                                  supplier_combobox.get(), 
                                                  price_entry.get(), 
                                                  discount_spinbox.get(),
                                                  quantity_entry.get(), 
                                                  status_combobox.get(), 
                                                  name_entry.get(),  
                                                  treeview)
                      )
  add_button.grid(row=0, 
                  column=0, 
                  padx=(10,0))

  update_button = Button(button_frame, 
                         text='update', 
                         font=('Arial', 12, 'bold'), 
                         width = 10, 
                         cursor='hand2', 
                         fg='white', 
                         bg='#0f4d7d',
                         command=lambda : update_product(category_combobox.get(),
                                                  supplier_combobox.get(), 
                                                  price_entry.get(),
                                                  discount_spinbox.get(), 
                                                  quantity_entry.get(), 
                                                  status_combobox.get(), 
                                                  name_entry.get(),  
                                                  treeview)
                          )
  update_button.grid(row=0, 
                     column=1, 
                     padx=(10,0))

  delete_button = Button(button_frame, 
                         text='Delete', 
                         font=('Arial', 12, 'bold'), 
                         width = 10, 
                         cursor='hand2', 
                         fg='white', 
                         bg='#0f4d7d',
                         command=lambda : delete_product(category_combobox,
                                                  supplier_combobox, 
                                                  price_entry, 
                                                  discount_spinbox,
                                                  quantity_entry, 
                                                  status_combobox, 
                                                  name_entry,
                                                  treeview)
                         )
  delete_button.grid(row=0, 
                     column=2, 
                     padx=(10,0))
  
  clear_button = Button(button_frame, 
                        text='clear', 
                        font=('Arial', 12, 'bold'), 
                        width = 10, 
                        cursor='hand2', 
                        fg='white', 
                        bg='#0f4d7d', 
                        command=lambda : clear_fields(category_combobox,
                                                  supplier_combobox, 
                                                  price_entry, 
                                                  discount_spinbox,
                                                  quantity_entry, 
                                                  status_combobox, 
                                                  name_entry,  
                                                  treeview, True)
                        )
  clear_button.grid(row=0, 
                    column=3,
                    padx=10)

  search_frame= LabelFrame(product_frame,
                           text='Search Product', 
                           font=('Arieal', 14, 'bold'), 
                           bg='white')
  search_frame.place(x=540,y=70)

  
  search_combobox = ttk.Combobox(search_frame,
                                 values=('Category',
                                         'Supplier',
                                         'Name',
                                         'Status'),
                                  width=14, 
                                  state='readonly', 
                                  font=('Arial', 12, 'bold'), 
                                )
  search_combobox.set('Search Product')                              
  search_combobox.grid(row=0, 
                       column=0, 
                       padx=8, 
                       pady=10)

  search_entry = Entry(search_frame, 
                       font=('Arial', 12, 'bold'), 
                       bg="#FAF208", 
                       width=15) 
  search_entry.grid(row=0, column=1)

  search_button = Button(search_frame, 
                         text='Search', 
                         font=('Arial', 12, 'bold'), 
                         width = 8, 
                         cursor='hand2', 
                         fg='white', 
                         bg='#0f4d7d',
                         command=lambda : search_product(search_combobox,
                                                         search_entry,
                                                         treeview)
                        )
  search_button.grid(row=0, 
                     column=2, 
                     padx=8)

  show_all_button = Button(search_frame, 
                             text='Show All', 
                             font=('Arial', 12, 'bold'), 
                             width = 8, 
                             cursor='hand2', 
                             fg='white', 
                             bg='#0f4d7d',
                             command=lambda : Show_all(search_combobox, 
                                                       search_entry,
                                                       treeview)
                            )
  show_all_button.grid(row=0, 
                         column=3, 
                         padx=(0,8))  

  treeview_frame= LabelFrame(product_frame, 
                             font=('Arieal', 14, 'bold'), 
                             bg='white')
  treeview_frame.place(x=540,
                       y=150, 
                       width=520,
                       height=420)

  
  scrolly = Scrollbar(treeview_frame, orient = VERTICAL)
 
  scrollx = Scrollbar(treeview_frame, orient = HORIZONTAL)


  treeview=ttk.Treeview(treeview_frame, 
                        columns=('id',
                                 'category',
                                 'supplier',
                                 'name',
                                 'price',
                                 'discount',
                                 'dis_price',
                                 'quantity',
                                 'status'),
                        show='headings', 
                        yscrollcommand=scrolly.set,
                        xscrollcommand=scrollx.set )

  scrolly.pack(side=RIGHT, fill= 'y')
  scrolly.config(command=treeview.yview)
  scrollx.pack(side=BOTTOM, fill='x')
  scrollx.config(command=treeview.xview)
  treeview.pack(fill=BOTH, expand=1)

  treeview.heading('id', text='ID')
  treeview.heading('category', text='Category')
  treeview.heading('supplier', text='Supplier')
  treeview.heading('name', text='Name')
  treeview.heading('price', text='Price')
  treeview.heading('discount', text='Discount')
  treeview.heading('dis_price', text='Discounted Price')
  treeview.heading('quantity', text='Quantity')
  treeview.heading('status', text='Status')

  treeview.column('id', width= 5)
  treeview.column('category', width= 80)
  treeview.column('supplier', width= 120)
  treeview.column('name', width= 70)
  treeview.column('price', width= 50)
  treeview.column('discount', width= 50)
  treeview.column('dis_price', width= 50)
  treeview.column('quantity', width= 50)
  treeview.column('status', width= 100)

  treeview_data(treeview,'prd')
  treeview.bind('<ButtonRelease-1>', lambda event:select_data(event,category_combobox,supplier_combobox,name_entry,price_entry,discount_spinbox,quantity_entry, status_combobox,treeview))
  ftech_supplier_category(category_combobox,
                          supplier_combobox)