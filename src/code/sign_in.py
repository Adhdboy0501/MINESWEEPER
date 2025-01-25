import mysql.connector
from tkinter import *
from tkinter import messagebox
import subprocess

root=Tk()
root.geometry("500x300")
root.configure(bg='#58d68d')
root.resizable(False,False)

def f():
    file_path="src//code//sign_up.py"
    subprocess.Popen(file_path, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    root.destroy()
def game():
    with open ("text.txt","w")as f:
        f.write(user.get())
    file_path="src//code//level_final.py"
    subprocess.Popen(file_path, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    root.destroy()
def sign_in():
    if user.get() == '' or passw.get() == '':
        messagebox.showerror('ERROR', 'All fields are required')
    else:
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='MySQL1234'
            )
            c = conn.cursor()
            try:
                c.execute("USE userdata")
            
                # Check if username exists for login
                query = "SELECT * FROM data WHERE username=%s"
                c.execute(query, (user.get(),))  # Parameters should be passed as a tuple
                row = c.fetchone()
                if row is None:
                    messagebox.showerror('ERROR', 'Username does not exist')
                else:
                    query = "SELECT PASSWORD FROM data WHERE username=%s"
                    c.execute(query, (user.get(),))
                    row = c.fetchone()
##                    print(type(row))
                    if row[0] != passw.get():
                        messagebox.showerror('ERROR', 'Username and password do not match')
                    else:
                        messagebox.showinfo('','Login successful!')
                        
                        game()

            except mysql.connector.Error as err:
                messagebox.showerror('ERROR', f'Database error: {err}')
            finally:
                conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror('ERROR', f'Connection error: {err}')


def v1(e):
    user.delete(0,"end")
def v2(e):
    passw.delete(0,"end")

heading=Label(root,text='USER LOGIN',font=('calibre',23,'bold'),fg='#58d68d')
heading.place(x=150,y=5)

##username:
user=Entry(root,width=25,fg='#229954',bg='white',font=('calibre',11))
user.place(x=130,y=80)
user.insert(0,'Username')
user.bind("<FocusIn>", v1)


##password:
passw=Entry(root,width=25,fg='#229954',bg='white',font=('calibre',11),show='*')
passw.place(x=130,y=120)
passw.insert(0,'Password')
passw.bind("<FocusIn>", v2)


Button(root,width=30,pady=7,text='Sign in',fg='#229954',border=0,cursor='hand2',command=sign_in).place(x=130,y=180)
label=Label(root,text='Create new account',fg='white',bg='#58d68d',font=('calibre',9))
label.place(x=160,y=220)
btn=Button(root,text='Sign up',fg='#229954',border=0,cursor='hand2',command=f)
btn.place(x=280,y=220)


root.mainloop()
