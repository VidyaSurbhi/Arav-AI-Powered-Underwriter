from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import pymysql

global openeye_image, closeeye_image  # Store both images (optional)
#Functionality Part
def forget_page():
    login_window.destroy()
    import forgetpassword

def clear():
    userName.delete(0,END)
    password.delete(0, END)


def login_user():
    if userName.get()=='' or password.get()=='':
        messagebox.showerror('Error','All fields are required')

    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='12345')
            mycursor=con.cursor()

        except:
            messagebox.showerror('Error, Database connectivity Issue,Please try again')
            return

        query='USE USERDATA'
        mycursor.execute(query)
        query='Select * from data where username=%s and password=%s'
        mycursor.execute(query,(userName.get(),password.get()))
        row=mycursor.fetchone()
        if row==None:
            messagebox.showerror('Error','Invalid Username or password')
            clear()
        else:
            messagebox.showinfo('Welcome','Login is successfull')
            main()

def main():
    login_window.destroy()
    import main

def signup_page():
    login_window.destroy()
    import signup

def user_enter(event):
    if userName.get()=='Username':
        userName.delete(0,END)

def password_enter(event):
    if password.get()=='Password':
        password.config(show='*')
        password.delete(0,END)

def hide():
    # Update the image of the button directly
    eyeButton.config(image=closeeye_photo)
    password.config(show='*')
    eyeButton.config(command=show)

def show():
    eyeButton.config(image=openeye_photo)
    password.config(show='')
    eyeButton.config(command=hide)

login_window=Tk()

login_window.resizable(0,0)
login_window.title('Underwriter Login Page')

bgImage=ImageTk.PhotoImage(file='landing.jpg')
bgLabel=Label(login_window,image=bgImage)
bgLabel.grid(row=0,column=0)

#for header
heading=Label(login_window,text='UNDERWRITER LOGIN PAGE',font=('Microsoft Yahei UI Light',12,'bold'),bg='white',width=25)
heading.place(x=40,y=120)

#for username layout
userName=Entry(login_window,width=25,font=('Microsoft Yahei UI Light',12,'bold'),bd=0,fg='firebrick1')
userName.place(x=40,y=200)
userName.insert(0,'Username')
userName.bind('<FocusIn>',user_enter)

#frameframe1=Frame(login_window,width=250,height=2,bg='firebrick1')
# frame1.place(x=580,y=2 22)

password=Entry(login_window,width=25,font=('Microsoft Yahei UI Light',12,'bold'),bd=0,fg='firebrick1')
password.place(x=40,y=240)
password.insert(0,'Password')
password.bind('<FocusIn>',password_enter)

frame2=Frame(login_window,width=250,height=2,bg='firebrick1')
#frame2.place(x=580,y=222)

# # Load the eye image
eye_image = Image.open("openeye.jpg")
#
# # Resize the eye image to a smaller size suitable for the button
desired_width = 20  # Adjust this value as needed
desired_height = 20  # Adjust this value as needed
eye_image = eye_image.resize((desired_width, desired_height), Image.LANCZOS)  # Resize using Pillow's ANTIALIAS for smoother scaling

# Convert resized image to PhotoImage for Tkinter
eye_photo = ImageTk.PhotoImage(eye_image)

openeye_image = Image.open("openeye.jpg")
closeeye_image = Image.open("closeeye.jpg")

# Resize the images
openeye_image = openeye_image.resize((desired_width, desired_height), Image.LANCZOS)
closeeye_image = closeeye_image.resize((desired_width, desired_height), Image.LANCZOS)

# Convert resized images to PhotoImage for Tkinter
openeye_photo = ImageTk.PhotoImage(eye_image)
closeeye_photo = ImageTk.PhotoImage(closeeye_image)

eyeButton = Button(login_window, image=closeeye_photo, width=desired_width, height=desired_height, bd=0, bg='white', activebackground='white',cursor='hand2', command=hide)
eyeButton.place(x=260, y=240)

#forget password functionality
forgetBtn=Button(login_window,text='Forget Password?',font=('Microsoft Yahei UI Light',8,'bold'), bd=0,bg='white', activebackground='white',cursor='hand2', command=forget_page,fg='firebrick1',activeforeground='firebrick1')
forgetBtn.place(x=180, y=280)
loginBtn=Button(login_window,text='Login',font=('Open Sans',11,'bold'),fg='white',bg='firebrick1',activeforeground='white',activebackground='firebrick1',cursor='hand2',bd=0,width=11,command=login_user)
loginBtn.place(x=40,y=280)

orLabel=Label(login_window,text='------------OR------------',font=('Open Sans',12),width=28,fg='firebrick1',bg='white')
orLabel.place(x=40,y=320)

signupLabel=Label(login_window,text='Don\'t have an account?',font=('Open Sans',9,'bold'),width=20,fg='firebrick1')
signupLabel.place(x=40,y=350)

newAcctBtn=Button(login_window,text='Create new one',font=('Open Sans',9,'bold underline'),fg='firebrick1',bg='white',activeforeground='white',activebackground='blue',cursor='hand2',bd=0,width=13,command=signup_page)
newAcctBtn.place(x=200,y=350)

login_window.mainloop()