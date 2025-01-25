import mysql.connector
from tkinter import *
from tkinter import messagebox
import subprocess

root = Tk()
root.geometry("500x300")
root.configure(bg='#58d68d')
root.resizable(False, False)

def empty():
    user.delete(0, END)
    passw.delete(0, END)
    passw2.delete(0, END)
def f():
    file_path="src//code//sign_in.py"
    subprocess.Popen(file_path, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    root.destroy()
def data():
    if user.get() == '' or passw.get() == '' or passw2.get() == '':
        messagebox.showerror('ERROR', 'All fields are required')
    elif passw.get() != passw2.get():
        messagebox.showerror('ERROR', 'Password Mismatch')
    else:
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='MySQL1234'
            )
            c = conn.cursor()
            try:
                c.execute("CREATE DATABASE IF NOT EXISTS userdata")
                c.execute("USE userdata")
                c.execute("""
                    CREATE TABLE IF NOT EXISTS data (
                        USERID INT AUTO_INCREMENT PRIMARY KEY,
                        USERNAME VARCHAR(100) NOT NULL UNIQUE,
                        PASSWORD VARCHAR(10) NOT NULL 
                    );
                """)
            except mysql.connector.Error as err:
                messagebox.showerror('ERROR', f'Database error: {err}')
                conn.close()
                return

            # Check if username exists
            query = "SELECT * FROM data WHERE username=%s"
            c.execute(query, (user.get(),))  # Parameters should be passed as a tuple
            row = c.fetchone()
            if row is not None:
                messagebox.showerror('ERROR', 'Username already exists')
            else:
                insert_query = "INSERT INTO data (username, password) VALUES (%s, %s)"
                val = (user.get(), passw.get())
                c.execute(insert_query, val)
                conn.commit()
                messagebox.showinfo('Success', 'Account created successfully!')
                conn.close()
                empty()
        except mysql.connector.Error as err:
            messagebox.showerror('ERROR', f'Connection error: {err}')
            return

def v1(e):
    user.delete(0,"end")
def v2(e):
    passw.delete(0,"end")
def v3(e):
    passw2.delete(0,"end")
    

heading = Label(root, text='SIGN UP', font=('calibre', 23, 'bold'), fg='#58d68d')
heading.place(x=180, y=5)

# Username
user = Entry(root, width=25, fg='#229954', bg='white', font=('calibre', 11))
user.place(x=130, y=80)
user.insert(0, 'Username')
user.bind("<FocusIn>", v1)
    

# Password
passw = Entry(root, width=25, fg='#229954', bg='white', font=('calibre', 11))
passw.place(x=130, y=120)
passw.insert(0, 'Password')
passw.bind("<FocusIn>", v2)


passw2 = Entry(root, width=25, fg='#229954', bg='white', font=('calibre', 11))
passw2.place(x=130, y=160)
passw2.insert(0, 'Confirm Password')
passw2.bind("<FocusIn>", v3)


Button(root, width=30, pady=7, text='Create', fg='#229954', border=0, cursor='hand2', command=data).place(x=130, y=200)

#sign_in
label=Label(root,text='Have an account?',fg='white',bg='#58d68d',font=('calibre',9))
label.place(x=160,y=240)
btn=Button(root,text='Sign in',fg='#229954',border=0,cursor='hand2',command=f)
btn.place(x=280,y=240)


root.mainloop()

