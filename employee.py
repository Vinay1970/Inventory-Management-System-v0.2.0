from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from functions import size_changer, go_back, clear_content,connect_database, treeview_data,delete, hash_password, db_cursor

def select_data(event,empid_entry,
        name_entry, 
        email_entry, 
        gender_combobox, 
        dob_entry, 
        contact_entry, 
        empType_combobox, 
        education_combobox, 
        workshift_combobox,
        address_entry, 
        doj_entry, 
        salary_entry, 
        userType_combobox, 
        password_entry):
    
    index = employee_treeview.selection()
    content = employee_treeview.item(index)
    row = content['values']
    clear_fields(empid_entry,
        name_entry, 
        email_entry, 
        gender_combobox, 
        dob_entry, 
        contact_entry, 
        empType_combobox, 
        education_combobox, 
        workshift_combobox,
        address_entry, 
        doj_entry, 
        salary_entry, 
        userType_combobox, 
        password_entry, False)
    
    empid_entry.insert(0,row[0])
    name_entry.insert(0,row[1])
    email_entry.insert(0,row[2])
    gender_combobox.set(row[3])
    dob_entry.set_date(row[4])
    contact_entry.insert(0,row[5])
    empType_combobox.set(row[6])
    education_combobox.set(row[7])
    workshift_combobox.set(row[8])
    address_entry.insert(0,row[9])
    doj_entry.set_date(row[10])
    salary_entry.insert(0,row[11])
    userType_combobox.set(row[12])
    password_entry.insert(0,row[13])


def add_employee(empid,
                 name, 
                 email, 
                 gender, 
                 dob, 
                 contact, 
                 empType, 
                 education, 
                 workshift,
                 address, 
                 doj, 
                 salary, 
                 userType, 
                 password):
    
    if (empid=='' or name =='' or email == '' or gender == 'select gender' or contact =='' or empType == 'Employment Type' or education == 'Education' or workshift == 'Work Shift' or address == '\n' or salary == '' or userType == 'User Type' or password == ''):
        messagebox.showerror('Error','All Fields are required' )
    else:
        try:
            with db_cursor() as (cursor, connection):
                if not cursor:
                    return
                cursor.execute('SELECT empid FROM employee_data WHERE empid=%s', (empid,))
                if cursor.fetchone():
                    messagebox.showerror('Error', 'Id already Exists')
                    return
                address = address.strip()
                pwd_hash = hash_password(password)
                cursor.execute('INSERT INTO employee_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                               (empid, name, email, gender, dob, contact, empType, education, workshift, address, doj, salary, userType, pwd_hash))
                connection.commit()
            treeview_data(employee_treeview, 'emp')
            messagebox.showinfo('Sucess', 'Data is inserted Sucessfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
    
#  Clear Fields Functions

def clear_fields(empid_entry,
        name_entry, 
        email_entry, 
        gender_combobox, 
        dob_entry, 
        contact_entry, 
        empType_combobox, 
        education_combobox, 
        workshift_combobox,
        address_entry, 
        doj_entry, 
        salary_entry, 
        userType_combobox, 
        password_entry, check):
    
    empid_entry.delete(0,END)
    name_entry.delete(0,END)
    email_entry.delete(0,END)
    gender_combobox.set('Select Gender')
    from datetime import date
    dob_entry.set_date(date.today())
    contact_entry.delete(0,END)
    empType_combobox.set('Emplyment Type')
    education_combobox.set('Education')
    workshift_combobox.set('Work Shift')
    address_entry.delete(0,END)
    doj_entry.set_date(date.today())
    salary_entry.delete(0,END)
    userType_combobox.set('User Type')
    password_entry.delete(0,END)

    if check:
        employee_treeview.selection_remove(employee_treeview.selection())

# Updating Employee

def update_employee(empid,name, email, gender, dob, contact, empType, education, workshift,address, doj, salary, userType, password):
    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No Row is Selected')
    else:
        try:
            with db_cursor() as (cursor, connction):
                if not cursor:
                    return
                address = address.strip()
                pwd_hash = hash_password(password)
                cursor.execute('UPDATE employee_data set name = %s, email=%s, gender = %s, dob=%s, contact= %s, employement_type=%s, education=%s, work_shift = %s, address = %s, doj=%s, salary=%s, usertype=%s, password=%s WHERE empid=%s',
                               (name, email, gender, dob, contact, empType, education, workshift, address, doj, salary, userType, pwd_hash, empid,))
                connction.commit()
            treeview_data(employee_treeview,'emp')
            messagebox.showinfo('Success', 'Data is Updated Successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')

# Swarch Employee 
def search_employee(search_option,value):
    if search_option == 'Search By':
        messagebox.showerror('Error', 'No Option is Selected')
    elif value=='':
        messagebox.showerror('Error', 'No Value is Selected')
    else:
        search_option =search_option.replace(' ','_')
        try:
            with db_cursor() as (cursor, connection):
                if not cursor:
                    return
                cursor.execute(f'SELECT * from employee_data WHERE {search_option} LIKE %s', (f'%{value}%',))
                records = cursor.fetchall()
                employee_treeview.delete(*employee_treeview.get_children())
                for record in records:
                    employee_treeview.insert('',END, values=record)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')

# Function Show All Button
def show_all(search_option,value):
    treeview_data(employee_treeview,'emp')
    value.delete(0,END)
    search_option.set('Search By')


def employee_form(window,emp_frame, sup_frame, cat_frame, pdc_frame, sale_frame, contentFrame):
    clear_content(contentFrame)
    global img_back, employee_frame, employee_treeview

    emp_frame.place_forget()
    sup_frame.place_forget()
    cat_frame.place_forget()
    pdc_frame.place_forget()
    sale_frame.place_forget()

    employee_frame = Frame(contentFrame,
                           width=1070, 
                           height=600, 
                           bg='white')
    employee_frame.pack(fill='both', expand=True)

    heading_Label = Label(employee_frame,
                         text="Manage Employee Details",
                         font=('Arial', 16, 'bold'),
                         bg="#040822",
                         fg='white'
                         )
    heading_Label.pack(pady=20,fill='x')

# Back Button

    img_back = size_changer('image/back.png', .05)
    back_button = Button(employee_frame, 
                         image=img_back, 
                         bg='white',
                         bd=0,
                         cursor='hand2',
                         command=lambda: go_back(employee_frame,emp_frame,sup_frame,cat_frame,pdc_frame,sale_frame)
                         )
    back_button.place(x=10, y=50)

# top Frame with Search bar
    topFrame = Frame(employee_frame,
                     bg='white',
                     )
    topFrame.place(x=0, y=80, relwidth=1,height=235)

    # Search Bar
    search_frame = Frame(topFrame)
    search_frame.pack(fill='x')

    # Search box
    search_combobox = ttk.Combobox(search_frame,
                              values=('Empid', 'Name', 'Email','Gender','Dob','Contact','Employement Type', 'Education', 'Work Shift', 'Address', 'Doj', 'Salary','UserType'), 
                              font=('Arial',12), 
                              state='readonly', 
                              justify=CENTER
                              )
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=20)

    # Search Entry
    search_entry = Entry(search_frame, 
                          font=('Arial',12), 
                          bg='lightyellow')
    search_entry.grid(row=0, column=1,padx=20)

    # Search Button
    search_button = Button(search_frame, 
                           text='Search', 
                           font=('Arial', 12),
                           width =10,
                           cursor='hand2',
                           fg='white',
                           bg = '#010c48',
                           command= lambda:search_employee(search_combobox.get(),
                                                           search_entry.get())
                           )
    search_button.grid(row=0, column=2, padx=20)

    # Show all Button
    show_button = Button(search_frame, 
                           text='Show All', 
                           font=('Arial', 12),
                           width =10,
                           cursor='hand2',
                           fg='white',
                           bg = '#010c48',
                           command= lambda :show_all(search_combobox,
                                                     search_entry)
                           )
    show_button.grid(row=0, column=3, padx=20)

# Scroll Bar
# Horizontal Scroll Bar

    horizontal_scrollbar = Scrollbar(topFrame, orient=HORIZONTAL)

# Vertical Scroll bar

    vertical_scrollbar = Scrollbar(topFrame, orient=VERTICAL)

    # Tree View 

    employee_treeview = ttk.Treeview(topFrame,
                                     columns=('empid',
                                              'name',
                                              'email',
                                              'gender', 
                                              'dob',
                                              'contact',
                                              'employee_type', 
                                              'education',
                                              'work_shift',
                                              'address',
                                              'doj', 
                                              'salary', 
                                              'usertype' ),
                                     show='headings',
                                     yscrollcommand=vertical_scrollbar.set,
                                     xscrollcommand=horizontal_scrollbar.set
                                    ) 
    
    horizontal_scrollbar.pack(side=BOTTOM, fill='x')
    vertical_scrollbar.pack(side=RIGHT, fill='y',pady=(10,0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.yview)

    employee_treeview.pack(pady=(10,0))

    employee_treeview.heading('empid',text='EmpId')
    employee_treeview.heading('name',text='Name')
    employee_treeview.heading('email',text='e-Mail')
    employee_treeview.heading('gender',text='Gender')
    employee_treeview.heading('dob',text='Date of Birth')
    employee_treeview.heading('contact',text='Contact')
    employee_treeview.heading('employee_type',text='Employee Type')
    employee_treeview.heading('education',text='Education')
    employee_treeview.heading('work_shift',text='Work Shift')
    employee_treeview.heading('address',text='Address')
    employee_treeview.heading('doj',text='Date of joining')
    employee_treeview.heading('salary',text='Salary')
    employee_treeview.heading('usertype',text='User Type')
   
    employee_treeview.column('empid', width=60)
    employee_treeview.column('name', width='140')
    employee_treeview.column('email', width=180)
    employee_treeview.column('gender', width=80)
    employee_treeview.column('dob', width=100)
    employee_treeview.column('contact', width=100)
    employee_treeview.column('employee_type', width=120)
    employee_treeview.column('education', width=120)
    employee_treeview.column('work_shift', width=100)
    employee_treeview.column('address', width=200)
    employee_treeview.column('doj', width=100)
    employee_treeview.column('salary', width=140)
    employee_treeview.column('usertype', width=120)

    
    treeview_data(employee_treeview, 'emp')
    employee_treeview.bind('<ButtonRelease-1>', lambda event:select_data(event,
                                                                         empid_entry,       name_entry,         email_entry,        gender_combobox,         dob_entry,         contact_entry,         empType_combobox,         education_combobox,       workshift_combobox,        address_entry,         doj_entry,         salary_entry,         userType_combobox,         password_entry))

    # Employee Section
    detail_frame = Frame(employee_frame)
    detail_frame.place(x=0, y=310)


    detail_frame.grid_columnconfigure(0, minsize=100)
    detail_frame.grid_columnconfigure(1, minsize=150)
    detail_frame.grid_columnconfigure(2, minsize=100)
    detail_frame.grid_columnconfigure(3, minsize=150)
    detail_frame.grid_columnconfigure(4, minsize=100)
    detail_frame.grid_columnconfigure(5, minsize=150)

    # Labales
    # Emp id Lable & Entry
    
    row_frame = Frame(detail_frame)
    row_frame.pack(fill='x')

    empid_lable = Label(row_frame, 
                        text='Emp Id', 
                        font=('Arial', 12, 'bold'))
    empid_lable.grid(row=0, 
                     column=0, 
                     padx=20, 
                     pady=10)

    empid_entry = Entry(row_frame,
                        font=('Arial', 12, 'bold'), 
                        bg = "#EBEF6A", 
                        width=20)
    empid_entry.grid(row=0, 
                     column=1, 
                     padx=20, 
                     pady=10)

    # Name Lable & Entry
    
    name_lable = Label(row_frame, 
                       text='Name', 
                       font=('Arial', 12, 'bold'))
    name_lable.grid(row=0, 
                    column=2, 
                    padx=20, 
                    pady=10)

    name_entry = Entry(row_frame,
                       font=('Arial', 12, 'bold'), 
                       bg = "#EBEF6A", 
                       width=20)
    name_entry.grid(row=0, 
                    column=3, 
                    padx=20, 
                    pady=10)

    # E mail Lable & Entry

    email_lable = Label(row_frame, 
                        text='E Mail', 
                        font=('Arial', 12, 'bold'))
    email_lable.grid(row=0, 
                     column=4, 
                     padx=20, 
                     pady=10)

    email_entry = Entry(row_frame,
                        font=('Arial', 12, 'bold'), 
                        bg = "#EBEF6A", 
                        width=20)
    email_entry.grid(row=0, 
                     column=5, 
                     padx=20, 
                     pady=10)

    # Gender Lable & Entry
    row1_frame = Frame(detail_frame)
    row1_frame.pack(fill='x')

    gender_lable = Label(row1_frame, 
                         text='Gender', 
                         font=('Arial', 12, 'bold'))
    gender_lable.grid(row=1, 
                      column=0, 
                      padx=22, 
                      pady=10)

    gender_combobox = ttk.Combobox(row1_frame,
                                   values=('Male', 'Female'),
                                   width=18, 
                                   state='readonly', 
                                   font=('Arial', 12, 'bold'), )
    gender_combobox.set('Selact Gender')                              
    gender_combobox.grid(row=1, 
                         column=1, 
                         padx=10, 
                         pady=10)

    # Contact Lable & Entry

    contact_lable = Label(row1_frame, 
                          text='Contact', 
                          font=('Arial', 12, 'bold'))
    contact_lable.grid(row=1, 
                       column=2, 
                       padx=22, 
                       pady=10)

    contact_entry = Entry(row1_frame,
                          font=('Arial', 12, 'bold'), 
                          bg = "#EBEF6A", 
                          width=20)
    contact_entry.grid(row=1, 
                       column=3, 
                       padx=10,
                         pady=10)

    # Address Lable & Entry

    address_lable = Label(row1_frame, 
                          text='Address', 
                          font=('Arial', 12, 'bold'))
    address_lable.grid(row=1, 
                       column=4, 
                       padx=22, 
                       pady=10)

    address_entry = Entry(row1_frame,
                          font=('Arial', 12, 'bold'), 
                          bg = "#EBEF6A", 
                          width=20)
    address_entry.grid(row=1, 
                       column=5, 
                       padx=10, 
                       pady=10)

    # Date of Birth Lable & Entry

    row2_frame = Frame(detail_frame)
    row2_frame.pack(fill='x')

    dob_lable = Label(row2_frame, 
                      text='Date of Birth', 
                      font=('Arial', 12, 'bold'))
    dob_lable.grid(row=2, 
                   column=0, 
                   padx=10, 
                   pady=10)

    dob_entry = DateEntry(row2_frame, 
                          width = 18, 
                          font = ('Arial', 12, 'bold'), 
                          state = 'readonly', 
                          date_pattern = 'dd/mm/yyyy')
    dob_entry.grid(row=2, 
                   column=1, 
                   padx=10, 
                   pady=10)

    # Education Lable & Entry

    education_lable = Label(row2_frame, 
                            text='Education', 
                            font=('Arial', 12, 'bold'))
    education_lable.grid(row=2, 
                         column=2, 
                         padx=10, 
                         pady=10)

    education_combobox = ttk.Combobox(row2_frame,
                                      values=('B. Tech', 
                                              'B. Com',
                                              'M. Tech', 
                                              'M. Com', 
                                              'B. Sc', 
                                              'M. Sc', 
                                              'BBA', 
                                              "LLB", 
                                              'MBA', 
                                              'LLB', 
                                              'LLM', 
                                              'B. Arch', 
                                              'M. Arch'),
                                        width=18, 
                                        state='readonly', 
                                        font=('Arial', 12, 'bold'))
    education_combobox.set('Education')                              
    education_combobox.grid(row=2, 
                            column=3, 
                            padx=10, 
                            pady=10)

    # Employment Type Lable & Entry

    empType_lable = Label(row2_frame, 
                          text='Emplyment Type', 
                          font=('Arial', 12, 'bold'))
    empType_lable.grid(row=2, 
                       column=4, 
                       padx=10, 
                       pady=10)

    empType_combobox = ttk.Combobox(row2_frame,values=('Full Time', 
                                                         'Part Time', 
                                                         'Casual', 
                                                         'Contact',
                                                         'Intern'),
                                    width=18, 
                                    state='readonly', 
                                    font=('Arial', 12, 'bold')
                                    )
    empType_combobox.set('Employment Type')                              
    empType_combobox.grid(row=2, 
                          column=5, 
                          padx=10, 
                          pady=10)

    # Date of Joining Lable & Entry

    row3_frame = Frame(detail_frame)
    row3_frame.pack(fill='x')

    doj_lable = Label(row3_frame, 
                      text='Date Of Join', 
                      font=('Arial', 12, 'bold'))
    doj_lable.grid(row=3, 
                   column=0, 
                   padx=10, 
                   pady=10)

    doj_entry = DateEntry(row3_frame, 
                          width = 18, 
                          font = ('Arial', 12, 'bold'), 
                          state = 'readonly', 
                          date_pattern = 'dd/mm/yyyy')
    doj_entry.grid(row=3, 
                   column=1, 
                   padx=10, 
                   pady=10)

    # Salary Lable & Entry

    salary_lable = Label(row3_frame, 
                         text='Salary', 
                         font=('Arial', 12, 'bold'))
    salary_lable.grid(row=3, 
                      column=2, 
                      padx=10, 
                      pady=10)

    salary_entry = Entry(row3_frame,
                         font=('Arial', 12, 'bold'), 
                         bg = "#EBEF6A")
    salary_entry.grid(row=3, 
                      column=3, 
                      padx=10, 
                      pady=10)

    # Work Shift Lable & Entry

    workShift_lable = Label(row3_frame, 
                            text='Work Shift', 
                            font=('Arial', 12, 'bold'))
    workShift_lable.grid(row=3, 
                         column=4, 
                         padx=10, 
                         pady=10)

    workshift_combobox = ttk.Combobox(row3_frame,
                                      values=('Genral', 
                                              'Morning', 
                                              'Evening', 
                                              'Night'),
                                        width=18, 
                                        state='readonly', 
                                        font=('Arial', 12, 'bold')
                                        )
    workshift_combobox.set('Work Shift')                              
    workshift_combobox.grid(row=3, 
                            column=5, 
                            padx=10, 
                            pady=10)

    # User Type Lable & Entry

    row4_frame = Frame(detail_frame)
    row4_frame.pack(fill='x')

    userType_lable = Label(row4_frame, 
                           text='User Type', 
                           font=('Arial', 12, 'bold')
                           )
    userType_lable.grid(row=4,
                         column=2, 
                         padx=10, 
                         pady=10)

    userType_combobox = ttk.Combobox(row4_frame,
                                     values=('Admin', 'Employee'),
                                     width=18, 
                                     state='readonly', 
                                     font=('Arial', 12, 'bold')
                                     )
    userType_combobox.set('User Type')                              
    userType_combobox.grid(row=4, 
                           column=3, 
                           padx=10, 
                           pady=10)

    # Password Lable & Entry

    password_lable = Label(row4_frame, 
                           text='PassWord', 
                           font=('Arial', 12, 'bold'))
    password_lable.grid(row=4, 
                        column=4, 
                        padx=10, 
                        pady=10)

    password_entry = Entry(row4_frame,
                           font=('Arial', 12, 'bold'), 
                           bg = "#EBEF6A")
    password_entry.grid(row=4, 
                        column=5, 
                        padx=10, 
                        pady=10)

    #  Button Frame

    button_frame = Frame(detail_frame)
    button_frame.pack(fill='x')

    add_button = Button(button_frame, 
                        text='Add', 
                        font=('Arial', 12, 'bold'), 
                        width = 10, 
                        cursor='hand2', 
                        fg='white', 
                        bg='#0f4d7d', 
                        command=lambda:add_employee(empid_entry.get(),
                                                    name_entry.get(), 
                                                    email_entry.get(), 
                                                    gender_combobox.get(), 
                                                    dob_entry.get(), 
                                                    contact_entry.get(), 
                                                    empType_combobox.get(), 
                                                    education_combobox.get(), 
                                                    workshift_combobox.get(),
                                                    address_entry.get(), 
                                                    doj_entry.get(), 
                                                    salary_entry.get(), 
                                                    userType_combobox.get(), 
                                                    password_entry.get())
                        )

    add_button.grid(row=0, 
                    column=0, 
                    padx=20)

    update_button = Button(button_frame, 
                           text='Update', 
                           font=('Arial', 12, 'bold'), 
                           width = 10,
                            cursor='hand2', 
                            fg='white', 
                            bg='#0f4d7d', 
                            command=lambda :update_employee(empid_entry.get(),
                                                             name_entry.get(), 
                                                             email_entry.get(), 
                                                            gender_combobox.get(), 
                                                            dob_entry.get(), 
                                                            contact_entry.get(), 
                                                            empType_combobox.get(), 
                                                            education_combobox.get(), 
                                                            workshift_combobox.get(),
                                                            address_entry.get(), 
                                                            doj_entry.get(), 
                                                             salary_entry.get(), 
                                                            userType_combobox.get(), 
                                                            password_entry.get())
                                                )
    update_button.grid(row=0, column=1, padx=20)
    
    delete_button = Button(button_frame, 
                           text='Delete', 
                           font=('Arial', 12, 'bold'), 
                           width = 10, 
                           cursor='hand2', 
                           fg='white', 
                           bg='#0f4d7d', 
                           command=lambda :delete(empid_entry.get(),
                                                  employee_treeview,
                                                  'emp')
                            )
    
    delete_button.grid(row=0, column=2, padx=20)
    
    clear_button = Button(button_frame, 
                          text='Clear', 
                          font=('Arial', 12, 'bold'), 
                          width = 10, 
                          cursor='hand2', 
                          fg='white', 
                          bg='#0f4d7d', 
                          command=lambda :clear_fields(empid_entry,
                                                        name_entry, 
                                                        email_entry, 
                                                        gender_combobox, 
                                                        dob_entry, 
                                                        contact_entry, 
                                                        empType_combobox, 
                                                        education_combobox, 
                                                        workshift_combobox,
                                                        address_entry, 
                                                        doj_entry, 
                                                        salary_entry, 
                                                        userType_combobox, 
                                                        password_entry, True)
                            )
    
    clear_button.grid(row=0, column=3, padx=20)
