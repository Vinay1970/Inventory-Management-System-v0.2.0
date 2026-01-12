from tkinter import *
from functions import size_changer
from datetime import datetime
from tkinter import messagebox
import pymysql
from functions import connect_database
import logging
from employee import employee_form
from supplier import supplier_form
from category import category_form
from product import product_form
from sales import sales_form
from Billing import billing
from Login import login_page, logout, exit_app

window = Tk()

login_page(window)

window.title('Dashboard')
window.geometry('1270x668+0+0')
window.resizable(0,0)
window.config(bg = 'white')

leftFrame = Frame(window)

leftFrame.place(x=0,y=102, 
                width=200, 
                height=570)

contentFrame = Frame(window, 
                     bg="white")
contentFrame.place(x=200, 
                   y=78, 
                   width=1070, 
                   height = 570)

# Tax Window

def tax_window():
    def save_tax():
        value = tax_count.get()
        try:
            tax_val = float(value)
        except Exception:
            messagebox.showerror('Error', 'Invalid tax value', parent=tax_root)
            return

        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS tax_label (id INT primary key AUTO_INCREMENT, tax DECIMAL(5,2))')
            cursor.execute('INSERT INTO tax_label(tax) VALUES(%s)', (tax_val,))
            connection.commit()
            messagebox.showinfo('Success', f'New {tax_val} Tax is saved Successfully', parent=tax_root)
        except Exception as e:
            logging.exception('Failed to save tax value')
            messagebox.showerror('Error', f'Could not save tax: {e}', parent=tax_root)
        finally:
            try:
                cursor.close()
                connection.close()
            except Exception:
                pass

    tax_root = Toplevel()
    tax_root.title('Tax Window')
    tax_root.geometry('300x200')
    tax_root.grab_set()
    tax_percentage = Label(tax_root,text='Enter tax Percentage %', font=('Ariel', 12, 'bold'))
    tax_percentage.pack(pady=10)
    tax_count = Spinbox(tax_root, from_=0, to=100 )
    tax_count.pack(pady=10)
    
    save_button = Button(tax_root,
                        text='Save',
                        font = ('Ariel', 12, 'bold'),
                        fg = '#010c48',
                        bg="#F7E705",
                        width=10, 
                        command=lambda : save_tax())
    save_button.pack(pady=20)
    
# Update Date & Time

now = datetime.now()
def update_time():
    # update emp 
    cursor, connection = connect_database()
    if not cursor or not connection:
        # schedule next attempt
        window.after(1000, update_time)
        return
    try:
        cursor.execute('SELECT COUNT(*) FROM employee_data')
        total_empno_lable.config(text=cursor.fetchone()[0])

        cursor.execute('SELECT COUNT(*) FROM supplier_data')
        total_supno_lable.config(text=cursor.fetchone()[0])

        cursor.execute('SELECT COUNT(*) FROM category_data')
        total_catno_lable.config(text=cursor.fetchone()[0])

        cursor.execute('SELECT COUNT(*) FROM product_data')
        total_pdcno_lable.config(text=cursor.fetchone()[0])
    
        cursor.execute('SELECT COUNT(*) FROM sale_data')
        total_saleno_lable.config(text=cursor.fetchone()[0])

    except Exception as e:
        logging.exception('Error updating counts in dashboard')
    finally:
        try:
            cursor.close()
            connection.close()
        except Exception:
            pass

    # Get current date and time
    current_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Update label text
    subtitlelabel.config(
        text=f'Welcome Admin\t\t Date : {current_date}\t\t Time : {current_time}'
    )
    
    # Call again after 1000ms
    window.after(1000, update_time)

# GUI PART

tk_img = size_changer('image/budget.png', 0.07)  # reduce size by 7%

# Use tk_img in Label

titlelabel = Label(window,
                    image=tk_img,
                    compound='left',
                    text="  Inventory Management System",
                    font=('Times New Roman', 40, 'bold'),
                    bg='#010c48',
                    fg='white',
                    anchor='w',
                    padx=20
)
titlelabel.place(x=0,y=0,relwidth=1)

#  Logout Button

logoutButton = Button(window,
                      text='Logout',
                      font = ('times new roman', 20, 'bold'),
                      fg = '#010c48',
                      command=lambda : logout(window))
logoutButton.place(x=1100, y =10)
titlelabel.pack()

# Create the label first with placeholder text

subtitlelabel = Label(
    window,
    text="Welcome Admin\t\t Date : --/--/----\t\t Time : --:--:--",
    font=('Times New Roman', 15, 'bold'),
    bg='#4d636d',
    fg='white'
)
subtitlelabel.place(x=0, y=70, relwidth=1)

# Start updating
# Left Side Bar

# left side Image

side_mage = size_changer('image/office.png',.4)
imageLable = Label(leftFrame, 
                   image= side_mage)
imageLable.pack()

# Emp Button

Emp_image = size_changer('image/business-team.png',.07)
employee_button=Button(leftFrame,
                       image=Emp_image,
                       compound='left',
                      text=' Employees', 
                      font=('Arial',17,'bold'), 
                      bg="#200096", 
                      fg='White',
                      command= lambda : employee_form(window,
                                                      emp_frame, 
                                                      sup_frame, 
                                                      cat_frame, 
                                                      pdc_frame, 
                                                      sale_frame, 
                                                      contentFrame)
                      )
employee_button.pack(fill='x')

# Supplier Button

sup_image = size_changer('image/supplier.png',.07)
supplier_button=Button(leftFrame,
                       image=sup_image,
                       compound='left',
                      text=' Supplier', 
                      font=('Arial',17,'bold'), 
                      bg="#200096", 
                      fg='White',
                      command= lambda : supplier_form(window,
                                                      emp_frame, 
                                                      sup_frame, 
                                                      cat_frame, 
                                                      pdc_frame, 
                                                      sale_frame, 
                                                      contentFrame)
                      )
supplier_button.pack(fill='x')

# Catergory Button

cat_image = size_changer('image/bars.png',.07)
cat_button=Button(leftFrame,
                       image=cat_image,
                       compound='left',
                      text=' Category', 
                      font=('Arial',17,'bold'), 
                      bg="#200096", 
                      fg='White',
                      command = lambda : category_form(window,
                                                       emp_frame, 
                                                       sup_frame, 
                                                       cat_frame, 
                                                       pdc_frame, 
                                                       sale_frame, 
                                                       contentFrame))
cat_button.pack(fill='x')

# Product Button

prd_image = size_changer('image/products.png',.07)
prd_button=Button(leftFrame,
                       image=prd_image,
                       compound='left',
                      text=' Product', 
                      font=('Arial',17,'bold'), 
                      bg="#200096", 
                      fg='White',
                      command=lambda : product_form(window,
                                                    emp_frame, 
                                                    sup_frame, 
                                                    cat_frame, 
                                                    pdc_frame, 
                                                    sale_frame, 
                                                    contentFrame)
                      )
prd_button.pack(fill='x')

tax_image = size_changer('image/discount.png',.07)
tax_button=Button(leftFrame,
                       image=tax_image,
                       compound='left',
                      text=' Tax', 
                      font=('Arial',17,'bold'), 
                      bg="#200096", 
                      fg='White',
                      command=lambda : tax_window()
                    )
tax_button.pack(fill='x')

# Sales Button

sales_image = size_changer('image/sales.png',.07)
sales_button=Button(leftFrame,
                       image=sales_image,
                       compound='left',
                      text=' Sales', 
                      font=('Arial',17,'bold'), 
                      bg="#200096", 
                      fg='White',
                      command= lambda : sales_form(window,
                                                    emp_frame, 
                                                    sup_frame, 
                                                    cat_frame, 
                                                    pdc_frame, 
                                                    sale_frame, 
                                                    contentFrame)
                        )
sales_button.pack(fill='x')

# Billing 

bill_image = size_changer('image/bill.png',.07)
bill_button=Button(leftFrame,
                       image=bill_image,
                       compound='left',
                      text=' Billing', 
                      font=('Arial',17,'bold'), 
                      bg="#200096", 
                      fg='White',
                      command= lambda : billing(window,
                                                    emp_frame, 
                                                    sup_frame, 
                                                    cat_frame, 
                                                    pdc_frame, 
                                                    sale_frame, 
                                                    contentFrame,
                                                    subtitlelabel)
                        )
bill_button.pack(fill='x')

# Exit Button

exit_image = size_changer('image/exit.png',.07)
exit_button=Button(leftFrame,
                       image=exit_image,
                       compound='left',
                      text=' Exit', 
                      font=('Arial',17,'bold'), 
                      bg="#200096", 
                      fg='White',
                      command= lambda : exit_app(window))
exit_button.pack(fill='x')

# Frame Employee

emp_frame = Frame(window, 
                  bg="#AC9382",
                  bd=3, 
                  relief='ridge')
emp_frame.place(x=400, 
                y=125, 
                height=170, 
                width=280)

empl_image = size_changer('image/business-team.png', .15)
total_emp_icon_lable = Label(emp_frame,
                             image=empl_image,
                             bg="#AC9382")
total_emp_icon_lable.pack()

total_emp_lable = Label(emp_frame,
                             text='Total Employee',
                             font=('Ariel',20,'bold'),
                             fg='white',
                             bg="#AC9382"
                             )
total_emp_lable.pack()

total_empno_lable = Label(emp_frame,
                             text='0',
                             font=('Ariel',30,'bold'),
                             fg='white',
                             bg="#AC9382"
                             )
total_empno_lable.pack()
#  Frame Supplier

sup_frame = Frame(window, 
                  bg="#9BEC9B",
                  bd=3, 
                  relief='ridge')
sup_frame.place(x=800, 
                y=125, 
                height=170, 
                width=280)

supp_image = size_changer('image/supplier.png', .15)
total_sup_icon_lable = Label(sup_frame,
                             image=supp_image,
                             bg="#9BEC9B")
total_sup_icon_lable.pack()

total_sup_lable = Label(sup_frame,
                             text='Total Supplier',
                             font=('Ariel',20,'bold'),
                             fg='white',
                             bg="#9BEC9B"
                             )
total_sup_lable.pack()

total_supno_lable = Label(sup_frame,
                             text='0',
                             font=('Ariel',30,'bold'),
                             fg='white',
                             bg="#9BEC9B"
                             )
total_supno_lable.pack()

# Frame Catergory

cat_frame = Frame(window, 
                  bg="#C80CEA",
                  bd=3, 
                  relief='ridge')
cat_frame.place(x=400, 
                y=310, 
                height=170, 
                width=280)

cate_image = size_changer('image/bars.png', .15)
total_cat_icon_lable = Label(cat_frame,
                             image=cate_image,
                             bg="#C80CEA")
total_cat_icon_lable.pack()

total_cat_lable = Label(cat_frame,
                             text='Catergories',
                             font=('Ariel',20,'bold'),
                             fg='white',
                             bg="#C80CEA"
                             )
total_cat_lable.pack()

total_catno_lable = Label(cat_frame,
                             text='0',
                             font=('Ariel',30,'bold'),
                             fg='white',
                             bg="#C80CEA"
                             )
total_catno_lable.pack()

# Frame Products

pdc_frame = Frame(window, 
                  bg="#EA690C",
                  bd=3, 
                  relief='ridge')
pdc_frame.place(x=800, 
                y=310, 
                height=170, 
                width=280)

pdc_image = size_changer('image/products.png', .15)
total_pdc_icon_lable = Label(pdc_frame,
                             image=pdc_image,
                             bg="#EA690C")
total_pdc_icon_lable.pack()

total_pdc_lable = Label(pdc_frame,
                             text='Total Products',
                             font=('Ariel',20,'bold'),
                             fg='white',
                             bg="#EA690C"
                             )
total_pdc_lable.pack()

total_pdcno_lable = Label(pdc_frame,
                             text='0',
                             font=('Ariel',30,'bold'),
                             fg='white',
                             bg="#EA690C"
                             )
total_pdcno_lable.pack()

# Frame Sales

sale_frame = Frame(window, 
                   bg="#0CEAEA",
                   bd=3, 
                   relief='ridge')
sale_frame.place(x=600, 
                 y=495, 
                 height=170, 
                 width=280)

sale_image = size_changer('image/sales.png', .15)
total_sale_icon_lable = Label(sale_frame,
                             image=sale_image,
                             bg="#0CEAEA")
total_sale_icon_lable.pack()

total_sale_lable = Label(sale_frame,
                             text='Total Sales',
                             font=('Ariel',20,'bold'),
                             fg='white',
                             bg="#0CEAEA"
                             )
total_sale_lable.pack()

total_saleno_lable = Label(sale_frame,
                             text='0',
                             font=('Ariel',30,'bold'),
                             fg='white',
                             bg="#0CEAEA"
                             )
total_saleno_lable.pack()
update_time()

window.mainloop()
