from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, Image
from tkinter import messagebox
import pymysql
import logging
from pathlib import Path
import os
import hashlib
import binascii
from contextlib import contextmanager

# Setup basic logging
LOG_PATH = Path(__file__).parent / 'app.log'
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s - %(message)s'
)


def hash_password(password: str) -> str:
    """Hash a password for storage using PBKDF2-HMAC-SHA256."""
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return binascii.hexlify(salt).decode() + '$' + binascii.hexlify(dk).decode()


def verify_password(password: str, stored: str) -> bool:
    """Verify a stored password against one provided by user."""
    try:
        salt_hex, hash_hex = stored.split('$')
        salt = binascii.unhexlify(salt_hex)
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
        return binascii.hexlify(dk).decode() == hash_hex
    except Exception:
        return False


@contextmanager
def db_cursor():
    """Context manager that yields (cursor, connection) and ensures closure."""
    cursor, connection = None, None
    try:
        cursor, connection = connect_database()
        yield cursor, connection
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if connection:
                connection.close()
        except Exception:
            pass

# Part of calculator
def get_input(num, calc_input):
    num=str(num)
    current = calc_input.get()
    # Prevent invalid concatenation like "8math.sqrt("
    if num.startswith("math.sqrt") and current.isdigit():
        xnum = f"math.sqrt({current})"
    else:
        xnum = current + str(num)
    calc_input.set(xnum)
# Part of calculator
def clear_calc(calc_input):
  return calc_input.set('')
# Part of calculator
def perform_calc(calc_input):
  result = calc_input.get()
  return calc_input.set(eval(result))

def size_changer(fileName, reduceby):
    try:
        # Resolve relative paths against the project directory
        base = Path(__file__).parent
        img_path = (base / fileName).resolve()
        bg_Image = Image.open(img_path)
        width, height = bg_Image.size
        new_width = max(1, int(width * reduceby))
        new_height = max(1, int(height * reduceby))
        resized_img = bg_Image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(resized_img)
        return tk_img
    except Exception as e:
        logging.exception('Failed to load or resize image: %s', fileName)
        # Return a tiny transparent placeholder so callers don't fail
        placeholder = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
        return ImageTk.PhotoImage(placeholder)


def go_back(employee_frame,emp_frame,sup_frame,cat_frame,pdc_frame,sale_frame):
    # Hide employee form
    employee_frame.pack_forget()

    # Restore dashboard frames
    emp_frame.place(x=400, y=125, height=170, width=280)
    sup_frame.place(x=800, y=125, height=170, width=280)
    cat_frame.place(x=400, y=310, height=170, width=280)
    pdc_frame.place(x=800, y=310, height=170, width=280)
    sale_frame.place(x=600, y=495, height=170, width=280)

def clear_content(contentFrame):
    for widget in contentFrame.winfo_children():
        widget.destroy()

def treeview_data(treeview, file):
  cursor, connection = connect_database()
  if not cursor or not connection:
      return
  
  try:
        # connect_database already ensures database exists and is selected
    if file=='emp':
            cursor.execute('Select * from employee_data')
    elif file=='supp':
        cursor.execute('Select * from supplier_data')
    elif file=='cate':
        cursor.execute('Select * from category_data')
    elif file == 'prd':
        cursor.execute('Select * from product_data')
    elif file == 'prd1':
        cursor.execute('Select id,name,price, quantity,discount from product_data')
    elif file == 'sale':
        cursor.execute('Select * from sale_data')
    

    records = cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for record in records:
      treeview.insert('', END, values=record)
  except Exception as e :
      logging.exception('Error loading treeview data for %s', file)
      messagebox.showerror('Error', f'Error due to {e}')
  finally:
      cursor.close()
      connection.close()


def connect_database():
    try:
        connection = pymysql.connect(host=os.environ.get('DB_HOST', 'localhost'),
                                     user=os.environ.get('DB_USER', 'root'),
                                     password=os.environ.get('DB_PASSWORD', 'root')
                                     )
        cursor = connection.cursor()
        # Ensure database exists and is selected
        cursor.execute('CREATE DATABASE IF NOT EXISTS invetory_system')
        cursor.execute('USE invetory_system')
        return cursor, connection
    except Exception as e:
        logging.exception('Database connection error')
        messagebox.showerror('Error', f'Database Connection Error: {e}')
        return None, None


def delete(id,treeview, file):
  index = treeview.selection()
  if not index:
    messagebox.showerror('Error', 'No Row is Selected')
    return
  cursor, connection = connect_database()
  if not cursor or not connection:
      return
  try:
    cursor.execute('USE invetory_system')
    if file == 'emp':
                cursor.execute('DELETE from employee_data WHERE id=%s', (id,))
    elif file == 'supp':
                cursor.execute('DELETE from supplier_data WHERE id=%s', (id,))
    elif file == 'cate':
                cursor.execute('DELETE from category_data WHERE id=%s', (id,))
    
    

    connection.commit()
    treeview_data(treeview, file)
    messagebox.showinfo('INFO', 'Record is Deleted')
  except Exception as e :
        logging.exception('Error deleting record %s from %s', id, file)
        messagebox.showerror('Error', f'Error due to {e}')
  finally:
    cursor.close()
    connection.close()

def calculator(calc_cart_frame):
    calcframe = Frame(calc_cart_frame,bd=4, relief=RIDGE, bg='white')
    calcframe.place(x=2, y=2,width=268, height=340)

    calc_input = StringVar()
    
    cal_input =Entry(calcframe, textvariable=calc_input,font=('Arial', 15, 'bold'),width=21, bd=10, relief=GROOVE, state='readonly',justify=RIGHT)
    cal_input.grid(row=0,columnspan=4)
    
    btn7 = Button(calcframe, text=7, font=('Arial', 15, 'bold'),command=lambda : get_input(7, calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btn7.grid(row=1,column=0)

    btn8 = Button(calcframe, text=8, font=('Arial', 15, 'bold'),command=lambda : get_input(8, calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btn8.grid(row=1,column=1)

    btn9 = Button(calcframe, text=9, font=('Arial', 15, 'bold'),command=lambda : get_input(9, calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btn9.grid(row=1,column=2)

    btnSum = Button(calcframe, text='+', font=('Arial', 15, 'bold'),command=lambda : get_input('+', calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btnSum.grid(row=1,column=3)
    
    btn4 = Button(calcframe, text=4, font=('Arial', 15, 'bold'),command=lambda : get_input(4, calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btn4.grid(row=2,column=0)

    btn5 = Button(calcframe, text=5, font=('Arial', 15, 'bold'),command=lambda : get_input(5, calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btn5.grid(row=2,column=1)

    btn6 = Button(calcframe, text=6, font=('Arial', 15, 'bold'),command=lambda : get_input(6, calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btn6.grid(row=2,column=2)

    btnMinus = Button(calcframe, text='-', font=('Arial', 15, 'bold'),command=lambda : get_input('-', calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btnMinus.grid(row=2,column=3)

    btn1 = Button(calcframe, text=1, font=('Arial', 15, 'bold'),command=lambda : get_input(1, calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btn1.grid(row=3,column=0)

    btn2 = Button(calcframe, text=2, font=('Arial', 15, 'bold'),command=lambda : get_input(2, calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btn2.grid(row=3,column=1)

    btn3 = Button(calcframe, text=3, font=('Arial', 15, 'bold'),command=lambda : get_input(3, calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btn3.grid(row=3,column=2)

    btnEqual = Button(calcframe, text='=', font=('Arial', 15, 'bold'),command=lambda : perform_calc(calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btnEqual.grid(row=3,column=3)

    btn0 = Button(calcframe, text=0, font=('Arial', 15, 'bold'),command=lambda : get_input(0, calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btn0.grid(row=4,column=0)

    btnPoint = Button(calcframe, text='.', font=('Arial', 15, 'bold'),command=lambda : get_input('.', calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btnPoint.grid(row=4,column=1)

    btnMulti = Button(calcframe, text='*', font=('Arial', 15, 'bold'),command=lambda : get_input('*', calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btnMulti.grid(row=4,column=2)

    btnDevide = Button(calcframe, text='/', font=('Arial', 15, 'bold'),command=lambda : get_input('/', calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btnDevide.grid(row=4,column=3)

    btnSq = Button(calcframe, text='Sq', font=('Arial', 15, 'bold'),command=lambda :get_input("**",calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btnSq.grid(row=5,column=0)

    btnStRt = Button(calcframe, text='SqRt', font=('Arial', 15, 'bold'),command=lambda :get_input("math.sqrt(", calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btnStRt.grid(row=5,column=1)

    btnPerc = Button(calcframe, text='%', font=('Arial', 15, 'bold'),command=lambda :get_input('/100',calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btnPerc.grid(row=5,column=2)

    btnClear = Button(calcframe, text='C', font=('Arial', 15, 'bold'),command=lambda :clear_calc(calc_input), bd=5, width=4, pady=6,cursor='hand2')
    btnClear.grid(row=5,column=3)
