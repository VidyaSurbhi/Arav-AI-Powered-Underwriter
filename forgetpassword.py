from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import pymysql
def clear():
    userNameEntry.delete(0,END)
    passWordEntry.delete(0, END)
    confirmEntry.delete(0, END)

def connect_database():
    if userNameEntry.get()=='' or confirmEntry.get()=='' or passWordEntry.get()=='':
        messagebox.showerror('Error','All fields are required')
    elif passWordEntry.get() != confirmEntry.get():
        messagebox.showerror('Error','Password Mismatch')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='12345')
            mycursor = con.cursor()

            check_db_query = "SHOW DATABASES LIKE 'userdata'"
            mycursor.execute(check_db_query)
            db_exists = mycursor.fetchone()  # If a row is returned, the database exists

            if not db_exists:
                # Create database only if it doesn't exist
                query = "CREATE DATABASE USERDATA"
                mycursor.execute(query)

            # Use the database (assuming it exists or was created)
            query = "USE USERDATA"
            mycursor.execute(query)

            # Insert data into the table
            username = userNameEntry.get()
            password = passWordEntry.get()

            fetch_query="Select * from data where username=%s"
            mycursor.execute(fetch_query,(userNameEntry.get()))

            row=mycursor.fetchone()
            if row == None:
                 messagebox.showerror('Error','Incorrect Username!')
            else:
                update_query = "Update data set password=%s where username=%s"
                mycursor.execute(update_query, (username, password))
                con.commit()
                con.close()
                messagebox.showinfo('Success', ' Password updated successfully!')
                clear()
                login_page()

        except pymysql.err.OperationalError as err:
            messagebox.showerror('Error', f"Database Error: {err}")  # Handle specific errors
            return  # Exit the function on database errors

        except Exception as err:  # Catch other unexpected errors
            messagebox.showerror('Error', f"An unexpected error occurred: {err}")
            return  # Exit the function on other errors

def login_page():
    forget_window.destroy()
    import signin

forget_window=Tk()

forget_window.resizable(0,0)
forget_window.title('Forget Password')

bgImage=ImageTk.PhotoImage(file='landing.jpg')
bgLabel=Label(forget_window,image=bgImage)
bgLabel.grid(row=0,column=0)

frame=Frame(forget_window,bg='white', height=300)
frame.place(x=40,y=100)

#for header
heading=Label(forget_window,text='Reset Password',font=('Microsoft Yahei UI Light',23,'bold'),bg='white',width=15)
heading.place(x=40,y=30)

userNameLabel=Label(frame,text='Username', font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
userNameLabel.grid(row=0,column=0,sticky='w', padx=25, pady=(0,5))

userNameEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
userNameEntry.grid(row=1,column=0,sticky='w', padx=25,pady=(5,10))

passWordLabel=Label(frame,text='Password', font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
passWordLabel.grid(row=2,column=0,sticky='w', padx=25,pady=(0,5))

passWordEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
passWordEntry.grid(row=3,column=0,sticky='w', padx=25,pady=(5,10))

confirmLabel=Label(frame,text='New Password', font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
confirmLabel.grid(row=4,column=0,sticky='w', padx=25,pady=(0,5))

confirmEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
confirmEntry.grid(row=5,column=0,sticky='w', padx=25,pady=(5,10))

submtiBtn=Button(frame,text='Submit',width=17,bd=0, font=('Open Sans',15,'bold'),bg='firebrick1',fg='white',activebackground='firebrick1',activeforeground='white',command=connect_database)
submtiBtn.grid(row=6,column=0,padx=25,pady=(20,25))

forget_window.mainloop()