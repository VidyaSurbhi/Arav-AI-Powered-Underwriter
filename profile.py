from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import tkinter as tk
import tkinter.filedialog as fd
import pymysql
from tkinter import ttk
import os
# for pdf reading and summarization-
import os
import openai
import PyPDF2
import re

# id=1

# new code
def profile_summary(passed_id):
    global id
    id=passed_id
    def getApprove():
        con = pymysql.connect(host='localhost', user='root', password='12345')
        mycursor = con.cursor()

        # Use the database (assuming it exists or was created)
        query = "USE LIFEASIADB"
        mycursor.execute(query)
        id = passed_id
        fetch_query = "Select * from customerProfile where id=%s"
        mycursor.execute(fetch_query, (id))

        update_query = "Update customerProfile set status=%s where id=%s"
        mycursor.execute(update_query, ('APPROVE', id))

        query1 = "USE APPLICATION_DATA"
        mycursor.execute(query1)

        # use a trigger to update into Application_data into customerInfo

        # Insert data into the table
        id = passed_id

        fetch_query = "Select * from customerInfo where id=%s"
        mycursor.execute(fetch_query, (id))

        update_query = "Update customerInfo set status=%s where id=%s"
        mycursor.execute(update_query, ('APPROVE', id))
        con.commit()

        con.commit()
        con.close()
        messagebox.showinfo('Success', ' Approve!')
        profile_window.destroy()

    def getReject():
        con = pymysql.connect(host='localhost', user='root', password='12345')
        mycursor = con.cursor()

        # Use the database (assuming it exists or was created)
        query = "USE LIFEASIADB"
        mycursor.execute(query)

        # use a trigger to update into Application_data into customerInfo

        # Insert data into the table
        id = passed_id

        fetch_query = "Select * from customerProfile where id=%s"
        mycursor.execute(fetch_query, (id))

        update_query = "Update customerProfile set status=%s where id=%s"
        mycursor.execute(update_query, ('REJECT', id))

        query1 = "USE APPLICATION_DATA"
        mycursor.execute(query1)

        # use a trigger to update into Application_data into customerInfo

        # Insert data into the table
        id = passed_id

        fetch_query = "Select * from customerInfo where id=%s"
        mycursor.execute(fetch_query, (id))

        update_query = "Update customerInfo set status=%s where id=%s"
        mycursor.execute(update_query, ('REJECT', id))
        con.commit()

        con.commit()
        con.close()
        messagebox.showinfo('Success', ' Reject!')
        profile_window.destroy()

    def user_enter(event):
        if enterquery.get() == 'Enter your query here':
            enterquery.delete(0, END)

    profile_window = tk.Tk()

    # profile_window.resizable(width='1200',height='1200')
    profile_window.geometry('1000x600')  # Set width and height (1200x800 pixels)
    profile_window.resizable(False, False)  # Disable resizing
    profile_window.title('Summary Page')
    wrapper1 = LabelFrame(profile_window, text='Customer Profile')
    wrapper2 = LabelFrame(profile_window, text='Summary')

    wrapper1.pack(fill="both", expand="yes", padx=20, pady=10, side=tk.LEFT)
    wrapper2.pack(fill="both", expand="yes", padx=20, pady=10, side=tk.RIGHT)

    # Create label widgets
    label = tk.Label(wrapper1, text="Id - ", font=('Open Sans', 9, 'bold'), width=25, anchor=tk.W)
    label.pack()

    label1 = tk.Label(wrapper1, text="Name -", font=('Open Sans', 9, 'bold'), width=25, anchor=tk.W)
    label1.pack()

    label2 = tk.Label(wrapper1, text="Age - ", font=('Open Sans', 9, 'bold'), width=25, anchor=tk.W)
    label2.pack()

    label3 = tk.Label(wrapper1, text="Salary -", font=('Open Sans', 9, 'bold'), width=25, anchor=tk.W)
    label3.pack()

    label4 = tk.Label(wrapper1, text="Nationality - ", font=('Open Sans', 9, 'bold'), width=25, anchor=tk.W)
    label4.pack()

    label5 = tk.Label(wrapper1, text="City -", font=('Open Sans', 9, 'bold'), width=25, anchor=tk.W)
    label5.pack()

    label6 = tk.Label(wrapper1, text="CIBIL Score - ", font=('Open Sans', 9, 'bold'), width=25, anchor=tk.W)
    label6.pack()

    label7 = tk.Label(wrapper1, text="Medical(Drink/Smoke) -", font=('Open Sans', 9, 'bold'), width=25, anchor=tk.W)
    label7.pack()

    label8 = tk.Label(wrapper1, text="Nominee -", font=('Open Sans', 9, 'bold'), width=25, anchor=tk.W)
    label8.pack()

    label9 = tk.Label(wrapper1, text="Premium Amount - ", font=('Open Sans', 9, 'bold'), width=25, anchor=tk.W)
    label9.pack()

    label10 = tk.Label(wrapper1, text="DRC Category -", font=('Open Sans', 9, 'bold'), width=25, anchor=tk.W)
    label10.pack()

    ProfileGet = tk.Button(wrapper1, text="Open Financial Doc", command=getProfile, font=('Open Sans', 9, 'bold'),
                           width=25, anchor=tk.W, fg='firebrick1')
    ProfileGet.pack(pady=20)

    header2 = tk.Label(wrapper2, text="Financial Summary", font=("Open Sans", 16, 'bold'))
    header2.pack()

    enterquery = Entry(wrapper2, width=25, font=('Microsoft Yahei UI Light', 10, 'bold'), bd=0, fg='firebrick1')
    enterquery.place(x=20, y=40)
    enterquery.insert(0, 'Enter your query here')
    enterquery.bind('<FocusIn>', user_enter)

    approveGet = tk.Button(wrapper2,text="APPROVE", command=getApprove, font=('Open Sans', 12, 'bold'),
                           width=10, anchor=tk.E, fg='firebrick1')
    approveGet.pack(padx=(150,50),pady=(430,10))
    # approveGet.insert(0, 'Approve')
    # approveGet.bind('<FocusIn>', getApprove)

    rejectGet = tk.Button(wrapper2, text="REJECT", command=getReject, font=('Open Sans',12, 'bold'),
                           width=10, anchor=tk.E, fg='firebrick1')
    rejectGet.pack(padx=(150,50),pady=(10,10))

    con = pymysql.connect(host='localhost', user='root', password='12345')
    mycursor = con.cursor()

    query = 'USE LifeAsiaDB'
    mycursor.execute(query)

    query = "SELECT ID,Name,Age,Salary,Nationality,city,CreditScore,Medical,Nominee,PremAmt,DrcCategory FROM customerprofile WHERE ID = %s"
    id = passed_id
    mycursor.execute(query, (id))  # Parameterized query

    # Fetch name and age as a tuple
    result = mycursor.fetchone()

    if result:  # Check if a record is found
        id, name, age, Salary, Nationality, City, CreditScore, Medical, Nominee, PremAmt, DrcCategory = result
    # Update label text
    label.config(text=f"ID: {id}")
    label1.config(text=f"Name: {name}")
    label2.config(text=f"Age: {age}")
    label3.config(text=f"Salary: {Salary}")
    label4.config(text=f"Nationality: {Nationality}")
    label5.config(text=f"City: {City}")
    label6.config(text=f"CIBIL Score: {CreditScore}")
    label7.config(text=f"Medical(Drink/Smoke): {Medical}")
    label8.config(text=f"Nominee : {Nominee}")
    label9.config(text=f"Premium Amt: {PremAmt}")
    label10.config(text=f"DRC Category: {DrcCategory}")

    con.close()
    profile_window.mainloop()


def getProfile():
    # Open file dialog for PDF selection
    os.system("VidyaSurbhiDS.docx")





