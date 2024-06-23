from tkinter import *
from PIL import ImageTk,Image
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
import profile

def open_customer_details(customer_profile):
    try:
        con = pymysql.connect(host='localhost', user='root', password='12345')
        mycursor = con.cursor()

    except:
        messagebox.showerror('Error, Database connectivity Issue,Please try again')
        return

    query = 'USE Application_data'
    mycursor.execute(query)
    query = 'Select * from customerInfo where id=%s'
    mycursor.execute(query, (customer_profile))
    row = mycursor.fetchone()
    if row != None:
        messagebox.showinfo('Welcome', 'Check Insurance Eligibility')
        profile.profile_summary(customer_profile)

def getProfile(event):
    rowid=table.identify_row(event.y)
    item=table.item(table.focus())
    # Extract customer name from the first element of the row's values
    customer_name = item['values'][0]
    # Call the desired function and pass the customer name
    open_customer_details(customer_name)


main_window=Tk()

main_window.resizable(0,0)
main_window.title('Dashboard')

bgImage=ImageTk.PhotoImage(file='landing.jpg')
bgLabel=Label(main_window,image=bgImage)
bgLabel.grid(row=0,column=0)

#for header
heading=Label(main_window,text='DASHBOARD',font=('Microsoft Yahei UI Light',23,'bold'),bg='white',width=15)
heading.place(x=40,y=120)

# Database connection details (replace with your own)
host = 'localhost'
user = 'root'
password = '12345'
database = 'application_data'

def fetch_data():
    try:
        connection = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()

        # Replace 'your_table_name' with the actual table name
        query = "SELECT ID,UPPER(name), age, birthdate,Salary, UPPER(city),UPPER(Nationality) FROM customerInfo where STATUS IS NULL"

        cursor.execute(query)

        data = cursor.fetchall() # Fetch all rows as a list of tuples

        # Clear existing table data (if any)
        for row in table.get_children():
            table.delete(row)

        # Insert data into the table
        for row in data:
            table.insert('', tk.END, values=row)
        connection.close()

    except pymysql.Error as err:
        messagebox.showerror('Error', f"Database Error: {err}")

# Create a frame for the table
frame = tk.Frame(main_window)
frame.place(x=40,y=100)

# Create the table using ttk.Treeview
table = ttk.Treeview(frame, columns=('ID','Name', 'Age', 'Birthdate','Salary','City','Nationality'), show='headings')


table.heading('ID', text='ID')
table.heading('Name', text='Customer Name')
table.heading('Age', text='Age')
table.heading('Birthdate', text='Birthday')
table.heading('Salary', text='Salary')
table.heading('City', text='City')
table.heading('Nationality', text='Nationality')
table.bind('<Double 1>',getProfile)
table.column('ID', width=50,anchor='center')
table.column('Name', width=170,anchor='center')
table.column('Age', width=50,anchor='center')
table.column('Birthdate', width=100,anchor='center')
table.column('Salary', width=150,anchor='center')
table.column('City', width=150,anchor='center')
table.column('Nationality', width=100,anchor='center')

table.pack()

# Create a button to fetch data
fetch_data_button = tk.Button(frame, text="Fetch Data", command=fetch_data,font=('Open Sans',10,'bold'),width=20,bg='red',fg='white')
fetch_data_button.pack(pady=10)
main_window.mainloop()

