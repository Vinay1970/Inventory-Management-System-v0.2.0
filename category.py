from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functions import size_changer, go_back, clear_content,connect_database, treeview_data, delete, db_cursor


def clear(id,name,description, treeview):
  id.delete(0,END)
  name.delete(0,END)
  description.delete(1.0,END)
  treeview.selection_remove(treeview.selection())

def select_data(event,id,name,description, treeview):
  index=treeview.selection()
  content=treeview.item(index)
  content= content['values']

  id.delete(0,END)
  name.delete(0,END)
  description.delete(1.0,END)

  id.insert(0,content[0])
  name.insert(0,content[1])
  description.insert(1.0,content[2])


def add_categoery(id, name,description, treeview):
  if id=='' or name == '' or description.strip() == '':
    messagebox.showerror('Error', 'All Fields Requireds')
  else:
    try:
      with db_cursor() as (cursor, connection):
        if not cursor:
          return
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS category_data (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            description TEXT
          )
        ''')
        cursor.execute('Select * from category_data WHERE id=%s', (id,))
        if cursor.fetchone():
          messagebox.showerror('Error', 'Id No. already Exists')
          return
        cursor.execute('''
        INSERT INTO category_data (id, name, description)
        VALUES (%s, %s, %s)
    ''', (id, name, description.strip() if description else None))
        connection.commit()
      messagebox.showinfo('INFO', 'Data is inserted')
      treeview_data(treeview, 'cate')
    except Exception as e:
      messagebox.showerror('Error', f'Error due to {e}')



def category_form(window,emp_frame, sup_frame, cat_frame, pdc_frame, sale_frame, contentFrame):
  global back_image, cat_img  
  clear_content(contentFrame)
  global img_back, employee_frame, employee_treeview

  emp_frame.place_forget()
  sup_frame.place_forget()
  cat_frame.place_forget()
  pdc_frame.place_forget()
  sale_frame.place_forget()

  category_frame = Frame(contentFrame,
                         width=1070, 
                         height=600, 
                         bg='white')
  category_frame.pack(fill='both', expand=True)

  heading_Label = Label(category_frame,
                         text="Manage Category Details",
                         font=('Arial', 16, 'bold'),
                         bg="#040822",
                         fg='white'
                         )
  heading_Label.pack(pady=20,fill='x')

# Back Button

  img_back = size_changer('image/back.png', .05)
  back_button = Button(category_frame, 
                         image=img_back, 
                         bg='white',
                         bd=0,
                         cursor='hand2',
                         command=lambda: go_back(category_frame,
                                                 emp_frame, 
                                                 sup_frame, 
                                                 cat_frame, 
                                                 pdc_frame, 
                                                 sale_frame)
                         )
  back_button.place(x=10, y=50)

  cat_img = size_changer('image/budget.png', .75)
  lable=Label(category_frame,image=cat_img, bg='white')
  lable.place(x=10 ,y=100)

  details_frame = Frame(category_frame, bg='white')
  details_frame.place(x=500, y = 60)

  id_lable=Label(details_frame, 
                 text='id. : ', 
                 font=('Ariel', 14, 'bold'))
  id_lable.grid(row=0, 
                column=0, 
                padx=(0,20), 
                sticky='w')
  id_entry =Entry(details_frame, 
                  font=('Ariel', 14, 'bold'),
                  bg = "#F9F294")
  id_entry.grid(row=0, column=1)

  name_lable=Label(details_frame, 
                   text='Category Name : ', 
                   font=('Ariel', 14, 'bold'))
  name_lable.grid(row=1, 
                  column=0, 
                  padx=(0,20), 
                  pady=20, 
                  sticky='w')
  name_entry =Entry(details_frame, 
                    font=('Ariel', 14, 'bold'),
                    bg = "#F9F294")
  name_entry.grid(row=1, column=1)
 
  description_lable=Label(details_frame, 
                          text='Description : ', 
                          font=('Ariel', 14, 'bold')
                          )
  description_lable.grid(row=2, 
                         column=0,
                           pady=20, 
                           sticky='nw')
  description_text =Text(details_frame, 
                         font=('Ariel', 14, 'bold'),
                         bg = "#F9F294", 
                         width= 20, 
                         height=4, 
                         bd=2)
  description_text.grid(row=2, column=1)

  button_frame = Frame(category_frame, bg='white')
  button_frame.place(x=550, y = 300)

  add_button = Button(button_frame, 
                      text='Add', 
                      font = ('Arial', 14, 'bold'), 
                      width=8, cursor='hand2',
                      bg= "#F7EF56", 
                      fg="#56CAAF",
                      command = lambda : add_categoery(id_entry.get(), 
                                                       name_entry.get(), 
                                                       description_text.get(1.0,END), 
                                                       treeview)
                      )
  add_button.grid(row=0, 
                  column=0, 
                  padx=20)
  

  delete_button = Button(button_frame, 
                         text='Delete', 
                         font = ('Arial', 14, 'bold'), 
                         width=8, 
                         cursor='hand2',
                         bg='#F7EF56', 
                         fg='#56CAAF', 
                         command= lambda :delete(id_entry.get(), 
                                                 treeview,'cate')
                        )
  delete_button.grid(row=0, 
                     column=1, 
                     padx=20)

  clear_button = Button(button_frame, 
                        text='Clear', 
                        font=('Arial', 12, 'bold'), 
                        width = 10, 
                        cursor='hand2', 
                        bg='#F7EF56', 
                        fg='#56CAAF', 
                        command=lambda : clear(id_entry, 
                                               name_entry, 
                                               description_text, 
                                               treeview)
                        )
  clear_button.grid(row=0, column=2)

  treeview_frame = Frame(category_frame, bg='white')
  treeview_frame.place(x=530, 
                       y = 340, 
                       height=200, 
                       width=500)

  ttk.Treeview
  scrolly = Scrollbar(treeview_frame, orient = VERTICAL)
 
  scrollx = Scrollbar(treeview_frame, orient = HORIZONTAL)


  treeview=ttk.Treeview(treeview_frame, 
                        columns=('id', 
                                 'name', 
                                 'description'),
                        show='headings', 
                        yscrollcommand=scrolly.set,
                        xscrollcommand=scrollx.set )

  scrolly.pack(side=RIGHT, fill= 'y')
  scrolly.config(command=treeview.yview)
  scrollx.pack(side=BOTTOM, fill='x')
  scrollx.config(command=treeview.xview)

  treeview.pack(fill=BOTH, expand=1)

  treeview.heading('id', text='Id.')
  treeview.heading('name', text='Category Name')
  treeview.heading('description', text='Description')

  treeview.column('id', width= 60)
  treeview.column('name', width= 140)
  treeview.column('description', width= 200)

  treeview_data(treeview,'cate')
  treeview.bind('<ButtonRelease-1>', lambda event:select_data(event,
                                                              id_entry,
                                                              name_entry,
                                                              description_text, 
                                                              treeview))