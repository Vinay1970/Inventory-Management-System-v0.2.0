from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functions import size_changer, go_back, clear_content,connect_database, treeview_data,delete, db_cursor
 
def select_data(event,invoice,name,contact,description, treeview):
  index=treeview.selection()
  content=treeview.item(index)
  content= content['values']
  invoice.delete(0,END)
  name.delete(0,END)
  contact.delete(0,END)
  description.delete(1.0,END)
  invoice.insert(0,content[0])
  name.insert(0,content[1])
  contact.insert(0,content[2])
  description.insert(1.0,content[3])

def search_supplier(invoice, treeview):
  if invoice == '':
    messagebox.showerror('ERROR', 'Please Enter Invoice No.')
    return
  else:
    try:
      with db_cursor() as (cursor, connection):
        if not cursor:
          return
        cursor.execute('SELECT * from supplier_data WHERE invoice=%s', (invoice,))
        record = cursor.fetchone()
        if not record:
          messagebox.showerror('ERROR', 'Wrong Invoice No.')
          return
        treeview.delete(*treeview.get_children())
        treeview.insert('', END, values=record)
    except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')

def show_all(value, treeview):
    treeview_data(treeview,'supp')
    value.delete(0,END)
    # search_option.set('Search By')


def clear(invoice,name,contact,description, treeview):
  invoice.delete(0,END)
  name.delete(0,END)
  contact.delete(0,END) 
  description.delete(1.0,END)
  treeview.selection_remove(treeview.selection())

def update_supplier(invoice,name, contact,description,treeview):
  index = treeview.selection()
  if not index:
    messagebox.showerror('Error', 'No Row is Selected')
    return
  try:
    with db_cursor() as (cursor, connection):
      if not cursor:
        return
      cursor.execute('SELECT * from supplier_data WHERE invoice=%s', (invoice,))
      currnt_data = cursor.fetchone()
      if not currnt_data:
        messagebox.showerror('Error', 'Record not found')
        return
      currnt_data = currnt_data[1:]
      new_data = (name, contact, description)
      if currnt_data == new_data:
        messagebox.showinfo('INFO', 'No changes detected')
        return
      cursor.execute('UPDATE supplier_data SET name=%s, contact=%s, description=%s WHERE invoice = %s',
                     (name, contact, description, invoice))
      connection.commit()
    messagebox.showinfo('INFO', 'Data is updated')
    treeview_data(treeview, 'supp')
  except Exception as e:
    messagebox.showerror('Error', f'Error due to {e}')

def add_supplier(invoice,name, 
                 contact,
                 description,
                 treeview):
  
  if invoice=='' or name == '' or contact == '' or description.strip() == '':
    messagebox.showerror('Error', 'All Fields Requireds')
  else:
    try:
      with db_cursor() as (cursor, connection):
        if not cursor:
          return
        cursor.execute('SELECT * from supplier_data WHERE invoice=%s', (invoice,))
        if cursor.fetchone():
          messagebox.showerror('Error', 'Invoice No. already Exists')
          return
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS supplier_data (
            invoice INT PRIMARY KEY,
            name VARCHAR(100),
            contact VARCHAR(15),
            description TEXT
          )
        ''')
        cursor.execute('''
        INSERT INTO supplier_data (invoice, name, contact, description)
        VALUES (%s, %s, %s, %s)
    ''', (invoice, name, contact, description.strip() if description else None))
        connection.commit()
      messagebox.showinfo('INFO', 'Data is inserted')
      treeview_data(treeview, 'supp')
    except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')


def supplier_form(window,emp_frame, sup_frame, cat_frame, pdc_frame, sale_frame, contentFrame):
  clear_content(contentFrame)
  global img_back, employee_frame, employee_treeview

  emp_frame.place_forget()
  sup_frame.place_forget()
  cat_frame.place_forget()
  pdc_frame.place_forget()
  sale_frame.place_forget()

  supplier_frame = Frame(contentFrame,
                         width=1070, 
                         height=600, 
                         bg='white')
  
  supplier_frame.pack(fill='both', expand=True)

  heading_Label = Label(supplier_frame,
                         text="Manage Supplier Details",
                         font=('Arial', 16, 'bold'),
                         bg="#040822",
                         fg='white'
                         )
  heading_Label.pack(pady=20,fill='x')

# Back Button

  img_back = size_changer('image/back.png', .05)
  back_button = Button(supplier_frame, 
                         image=img_back, 
                         bg='white',
                         bd=0,
                         cursor='hand2',
                         command=lambda: go_back(supplier_frame,
                                                 emp_frame, 
                                                 sup_frame, 
                                                 cat_frame, 
                                                 pdc_frame, 
                                                 sale_frame)
                         )
  back_button.place(x=10, y=50)

  left_frame=Frame(supplier_frame, 
                   bg='white')
  left_frame.place(x=10, y= 100)

  invoice_lable=Label(left_frame, 
                      text='Invoice No. : ', 
                      font=('Ariel', 14, 'bold')
                      )
  
  invoice_lable.grid(row=0, 
                     column=0, 
                     padx=20, 
                     sticky='w'
                     )
  invoice_entry =Entry(left_frame, 
                       font=('Ariel', 14, 'bold'),
                       bg = "#F9F294")
  invoice_entry.grid(row=0, column=1)

  name_lable=Label(left_frame, 
                   text='Supplier Name : ', 
                   font=('Ariel', 14, 'bold')
                   )
  name_lable.grid(row=1, 
                  column=0, 
                  padx=20, 
                  pady=20, 
                  sticky='w'
                  )
  name_entry =Entry(left_frame, 
                    font=('Ariel', 14, 'bold'),
                    bg = "#F9F294"
                    )
  name_entry.grid(row=1, column=1)

  contact_lable=Label(left_frame, 
                      text='Supplier Contact : ', 
                      font=('Ariel', 14, 'bold')
                      )
  contact_lable.grid(row=2, 
                     column=0, 
                     padx=20, 
                     pady=20, 
                     sticky='w')
  contact_entry =Entry(left_frame, 
                       font=('Ariel', 14, 'bold'),
                       bg = "#F9F294"
                       )
  contact_entry.grid(row=2, column=1)

  description_lable=Label(left_frame, 
                          text='description : ', 
                          font=('Ariel', 14, 'bold')
                          )
  description_lable.grid(row=3, 
                         column=0, 
                         padx=20, 
                         pady=20, 
                         sticky='nw'
                         )
  description_text =Text(left_frame, 
                         font=('Ariel', 14, 'bold'),
                         bg = "#F9F294", 
                         width= 20, 
                         height=4, bd=2)
  description_text.grid(row=3, column=1)

  buttonFrame= Frame(left_frame, bg='white')
  buttonFrame.grid(row=4, columnspan=2, pady=40)
  

  save_button = Button(buttonFrame, 
                       text='Save', 
                       font=('Arial', 12, 'bold'), 
                       width = 10, 
                       cursor='hand2', 
                       fg='white', 
                       bg='#0f4d7d', 
                       command=lambda : add_supplier(invoice_entry.get(), 
                                                     name_entry.get(), 
                                                     contact_entry.get(), 
                                                     description_text.get(1.0,END), 
                                                     treeview)
                      )
  save_button.grid(row=0, column=0, padx=20)
  
  update_button = Button(buttonFrame, 
                         text='Update', 
                         font=('Arial', 12, 'bold'), 
                         width = 10, 
                         cursor='hand2', 
                         fg='white', 
                         bg='#0f4d7d', 
                         command=lambda :update_supplier(invoice_entry.get(), 
                                                         name_entry.get(), 
                                                         contact_entry.get(), 
                                                         description_text.get(1.0,END).strip(), treeview)
                        )
  update_button.grid(row=0, column=1)

  delete_button = Button(buttonFrame, 
                         text='Delete', 
                         font=('Arial', 12, 'bold'), 
                         width = 10, 
                         cursor='hand2', 
                         fg='white', 
                         bg='#0f4d7d', 
                         command= lambda :delete(invoice_entry.get(), 
                                                 treeview,'supp')
                        )
  delete_button.grid(row=0, column=2, padx=20)

  clear_button = Button(buttonFrame, 
                        text='Clear', 
                        font=('Arial', 12, 'bold'), 
                        width = 10, 
                        cursor='hand2', 
                        fg='white', 
                        bg='#0f4d7d', 
                        command=lambda : clear(invoice_entry, 
                                               name_entry, 
                                               contact_entry, 
                                               description_text, 
                                               treeview)
                        )
  clear_button.grid(row=0, column=3)

  right_frame=Frame(supplier_frame, bg='white')
  right_frame.place(x=520, y=95,width=500, height=350)

  search_frame = Frame(right_frame, bg='white')
  search_frame.pack(pady=(0,20))


  num_lable=Label(search_frame, 
                  text='Invoice No. : ', 
                  font=('Ariel', 14, 'bold')
                  )
  num_lable.grid(row=0, 
                 column=0, 
                 padx=(0,15), 
                 sticky='w')
  search_entry =Entry(search_frame, 
                      font=('Ariel', 14, 'bold'),
                      bg = "#F9F294", 
                      width=10
                      )
  search_entry.grid(row=0, column=1)

  search_button = Button(search_frame, 
                         text='Search', 
                         font=('Arial', 12, 'bold'), 
                         width = 10, 
                         cursor='hand2', 
                         fg='white', 
                         bg='#0f4d7d', 
                         command= lambda :search_supplier(search_entry.get(), 
                                                          treeview))
  search_button.grid(row=0, 
                     column=2,
                     padx=15)

  show_button = Button(search_frame, 
                       text='Show All', 
                       font=('Arial', 12, 'bold'), 
                       width = 10, 
                       cursor='hand2', 
                       fg='white',
                       bg='#0f4d7d', 
                       command=lambda : show_all(search_entry, 
                                                 treeview)
                      )
  show_button.grid(row=0, column=3)

  scrolly = Scrollbar(right_frame, orient = VERTICAL)
 
  scrollx = Scrollbar(right_frame, orient = HORIZONTAL)


  treeview=ttk.Treeview(right_frame, 
                        columns=('invoice', 'name', 'contact', 'description'),
                        show='headings', 
                        yscrollcommand=scrolly.set,
                        xscrollcommand=scrollx.set 
                      )

  scrolly.pack(side=RIGHT, fill= 'y')
  scrolly.config(command=treeview.yview)
  scrollx.pack(side=BOTTOM, fill='x')
  scrollx.config(command=treeview.xview)
  treeview.pack(fill=BOTH, expand=1)

  treeview.heading('invoice', text='Invoice No.')
  treeview.heading('name', text='Name')
  treeview.heading('contact', text='Contact')
  treeview.heading('description', text='Description')

  treeview.column('invoice', width= 80)
  treeview.column('name', width= 160)
  treeview.column('contact', width= 120)
  treeview.column('description', width= 300)

  treeview_data(treeview,'supp')
  treeview.bind('<ButtonRelease-1>', lambda event:select_data(event,
                                                              invoice_entry,
                                                              name_entry,
                                                              contact_entry,
                                                              description_text, 
                                                              treeview))