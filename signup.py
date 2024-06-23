from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql

def clear():
    emailEntry.delete(0,END)
    userNameEntry.delete(0, END)
    passWordEntry.delete(0, END)
    confirmEntry.delete(0, END)
    check.set(0)

def connect_database():
    if emailEntry.get()=='' or userNameEntry.get()=='' or passWordEntry.get()=='' or confirmEntry.get()=='':
        messagebox.showerror('Error','All fields are required')
    elif passWordEntry.get() != confirmEntry.get():
        messagebox.showerror('Error','Password Mismatch')
    elif check.get()==0:
        messagebox.showerror('Error','Please Accept Terms & Conditions')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='12345')
            mycursor = con.cursor()

            # Check if database exists
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
            email = emailEntry.get()
            username = userNameEntry.get()
            password = passWordEntry.get()

            fetch_query="Select * from data where username=%s"
            mycursor.execute(fetch_query,(userNameEntry.get()))

            row=mycursor.fetchone()
            if row != None:
                messagebox.showerror('Error','User already exist !')
            else:
                insert_query = f"INSERT INTO data (email, username, password) VALUES (%s, %s, %s)"
                mycursor.execute(insert_query, (email, username, password))
                con.commit()
                con.close()
                messagebox.showinfo('Success',' Registration is successfully!')
                clear()
                signup_window.destroy()
                import signin

        except pymysql.err.OperationalError as err:
            messagebox.showerror('Error', f"Database Error: {err}")  # Handle specific errors
            return  # Exit the function on database errors

        except Exception as err:  # Catch other unexpected errors
            messagebox.showerror('Error', f"An unexpected error occurred: {err}")
            return  # Exit the function on other errors


def login_page():
    signup_window.destroy()
    import signin

signup_window=Tk()
signup_window.title("Signup Page")
signup_window.resizable(False,False)
background=ImageTk.PhotoImage(file="landing.jpg")

bgLabel=Label(signup_window,image=background)
bgLabel.grid()

frame=Frame(signup_window,bg='white')
frame.place(x=40,y=70)

heading=Label(frame,text="Create an Account", font=('Microsoft Yahei UI Light',18,'bold'),bg='white',fg='firebrick1')
heading.grid(row=0,column=0,padx=10,pady=10)

emailLabel=Label(frame,text="Email", font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
emailLabel.grid(row=1,column=0,sticky='w', padx=25,pady=(10,0))

emailEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
emailEntry.grid(row=2,column=0,sticky='w', padx=25)

userNameLabel=Label(frame,text='Username', font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
userNameLabel.grid(row=3,column=0,sticky='w', padx=25,pady=(10,0))

userNameEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
userNameEntry.grid(row=4,column=0,sticky='w', padx=25)

passWordLabel=Label(frame,text='Password', font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
passWordLabel.grid(row=5,column=0,sticky='w', padx=25,pady=(10,0))

passWordEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
passWordEntry.grid(row=6,column=0,sticky='w', padx=25)

confirmLabel=Label(frame,text='Confirm Password', font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
confirmLabel.grid(row=7,column=0,sticky='w', padx=25,pady=(10,0))

confirmEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
confirmEntry.grid(row=8,column=0,sticky='w', padx=25)
check=IntVar()
transandconditions=Checkbutton(frame,text='I agree to the Terms & Conditions', font=('Microsoft Yahei UI Light',9,'bold'),bg='white',fg='firebrick1',activebackground='white',activeforeground='firebrick1',cursor='hand2',variable=check)
transandconditions.grid(row=9,column=0,sticky='w', padx=15)

signupBtn=Button(frame,text='Sign Up',width=17,bd=0,font=('Microsoft Yahei UI Light',16,'bold'),bg='firebrick1',fg='white',activebackground='firebrick1',activeforeground='white',command=connect_database)
signupBtn.grid(row=10,column=0,padx=25)

alreadyAccount=Label(frame,text='Dont have an account?', font=('Microsoft Yahei UI Light',9,'bold'),bg='white',fg='firebrick1')
alreadyAccount.grid(row=11,column=0,sticky='w',padx=25,pady=(10))

loginBtn=Button(frame,text='Log In',font=('Open Sans',9,'bold underline'),bg='white',fg='blue',bd=0,cursor='hand2',activebackground='white',activeforeground='blue',command=login_page)
loginBtn.place(x=200,y=370)

signup_window.mainloop()