import mysql.connector
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # Replace with your MySQL root password
    'database': 'bank_management'
}

def create_new_account():
    def save_account():
        
        name = name_entry.get()
        age = age_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        aadhar = aadhar_entry.get()

        # Generate random account number
        account_number = random.randint(1000000000, 9999999999)

        # Connect to MySQL and insert data
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Create table if not exists
            cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT,
                email VARCHAR(255),
                phone VARCHAR(20),
                aadhar VARCHAR(20),
                account_number VARCHAR(20), 
                balance DECIMAL(10, 2) DEFAULT 0
            )
            """)

            # Insert user data into table
            cursor.execute("""
            INSERT INTO accounts (name, age, email, phone, aadhar, account_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, age, email, phone, aadhar, account_number))
            conn.commit()

            messagebox.showinfo("Success", f"Account created successfully!\nAccount Number: {account_number}")
            new_account_window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # New account window
    new_account_window = tk.Toplevel(main_menu_window)
    new_account_window.title("Create New Account")
    new_account_window.geometry("500x600")
    bg_image = Image.open("4.png")  # Replace with your background image path
    bg_image = bg_image.resize((new_account_window.winfo_screenwidth(), new_account_window.winfo_screenheight()), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Store the image reference to prevent garbage collection
    new_account_window.bg_photo = bg_photo  # This line is important
    bg_label = tk.Label(new_account_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

 

    # Form fields
    tk.Label(new_account_window, text="Name:", font=("Arial", 14)).pack(pady=10)
    name_entry = tk.Entry(new_account_window, font=("Arial", 14))
    name_entry.pack(pady=10)

    tk.Label(new_account_window, text="Age:", font=("Arial", 14)).pack(pady=10)
    age_entry = tk.Entry(new_account_window, font=("Arial", 14))
    age_entry.pack(pady=10)

    tk.Label(new_account_window, text="Email:", font=("Arial", 14)).pack(pady=10)
    email_entry = tk.Entry(new_account_window, font=("Arial", 14))
    email_entry.pack(pady=10)

    tk.Label(new_account_window, text="Phone Number:", font=("Arial", 14)).pack(pady=10)
    phone_entry = tk.Entry(new_account_window, font=("Arial", 14))
    phone_entry.pack(pady=10)

    tk.Label(new_account_window, text="Aadhar Number:", font=("Arial", 14)).pack(pady=10)
    aadhar_entry = tk.Entry(new_account_window, font=("Arial", 14))
    aadhar_entry.pack(pady=10)

    tk.Button(new_account_window, text="Save Account", font=("Arial", 14), command=save_account).pack(pady=20)


def deposit_money(account_number_entry, deposit_amount_entry):
    account_number = account_number_entry.get()
    amount = float(deposit_amount_entry.get())

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the account exists
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
        account = cursor.fetchone()

        if account:
            # Update the balance
            new_balance = float(account[7]) + amount  # account[7] is the balance column
            cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
            conn.commit()
            messagebox.showinfo("Deposit Success", f"Deposited {amount} into account number {account_number}. New balance: {new_balance}")
        else:
            messagebox.showerror("Account Not Found", "Account number not found.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def withdraw_money(account_number_entry, withdraw_amount_entry):
    account_number = account_number_entry.get()
    amount = float(withdraw_amount_entry.get())

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the account exists
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
        account = cursor.fetchone()

        if account:
            # Check if sufficient balance is available
            if account[7] >= amount:
                new_balance = account[7] - amount
                cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
                conn.commit()
                messagebox.showinfo("Withdraw Success", f"Withdrew {amount} from account number {account_number}. New balance: {new_balance}")
            else:
                messagebox.showerror("Insufficient Balance", "Insufficient balance for this withdrawal.")
        else:
            messagebox.showerror("Account Not Found", "Account number not found.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Function for viewing the statement of the account
def view_statement(account_number_entry):
    account_number = account_number_entry.get()

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the account exists
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
        account = cursor.fetchone()

        if account:
            statement = f"Account Number: {account_number}\nName: {account[1]}\nBalance: {account[7]}"
            messagebox.showinfo("Account Statement", statement)
        else:
            messagebox.showerror("Account Not Found", "Account number not found.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Function for account window (deposit, withdraw, statement)
def account_window():
    account_window = tk.Toplevel(main_menu_window)
    account_window.title("Manage Existing Account")
    account_window.geometry("500x600")

    bg_image = Image.open("3.png")  # Replace with your background image path
    bg_image = bg_image.resize((account_window.winfo_screenwidth(), account_window.winfo_screenheight()), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Store the image reference to prevent garbage collection
    account_window.bg_photo = bg_photo  # This line is important
    bg_label = tk.Label(account_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # Form fields
    tk.Label(account_window, text="Account Number:", font=("Arial", 14)).pack(pady=10)
    account_number_entry = tk.Entry(account_window, font=("Arial", 14))
    account_number_entry.pack(pady=10)

    tk.Label(account_window, text="Deposit Amount:", font=("Arial", 14)).pack(pady=10)
    deposit_amount_entry = tk.Entry(account_window, font=("Arial", 14))
    deposit_amount_entry.pack(pady=10)
    tk.Button(account_window, text="Deposit", font=("Arial", 14), command=lambda: deposit_money(account_number_entry, deposit_amount_entry)).pack(pady=10)

    tk.Label(account_window, text="Withdraw Amount:", font=("Arial", 14)).pack(pady=10)
    withdraw_amount_entry = tk.Entry(account_window, font=("Arial", 14))
    withdraw_amount_entry.pack(pady=10)
    tk.Button(account_window, text="Withdraw", font=("Arial", 14), command=lambda: withdraw_money(account_number_entry, withdraw_amount_entry)).pack(pady=10)

    tk.Button(account_window, text="View Statement", font=("Arial", 14), command=lambda: view_statement(account_number_entry)).pack(pady=20)

def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "admin":
        messagebox.showinfo("Login Success", "Login Successful!")
        login_window.destroy()  # Close the login window
        main_menu()  # Open the main menu after login
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password!")
# Function to create new account

# Function for the main menu
def main_menu():
    def open_existing_account():
        messagebox.showinfo("Existing Account", "Feature to manage existing accounts will go here!")

    def exit_system():
        main_menu_window.destroy()

    # Main menu window
    global main_menu_window
    main_menu_window = tk.Tk()
    main_menu_window.title("Bank Management System - Main Menu")
    main_menu_window.attributes('-fullscreen', True)

    # Bind Esc key to exit full-screen
    main_menu_window.bind("<Escape>", lambda event: main_menu_window.attributes('-fullscreen', False))

    # Background setup
    bg_image = Image.open("2.png")  # Replace with your background image path
    bg_image = bg_image.resize((main_menu_window.winfo_screenwidth(), main_menu_window.winfo_screenheight()), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(main_menu_window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # Main menu components
    tk.Label(main_menu_window, text="Bank Management System", font=("Arial", 36, "bold"), bg="#ffffff", fg="#000000").pack(pady=30)
    tk.Button(main_menu_window, text="Existing Account", font=("Arial", 20, "bold"), command=account_window, width=20, bg="#000080", fg="white").pack(pady=20)
    tk.Button(main_menu_window, text="New Account", font=("Arial", 20, "bold"), command=create_new_account, width=20, bg="#006400", fg="white").pack(pady=20)
    tk.Button(main_menu_window, text="Exit", font=("Arial", 20, "bold"), command=exit_system, width=20, bg="#800000", fg="white").pack(pady=20)

    main_menu_window.mainloop()

# Login screen
login_window = tk.Tk()
login_window.title("Bank Management System - Login")
login_window.attributes('-fullscreen', True)

# Bind Esc key to exit full-screen
login_window.bind("<Escape>", lambda event: login_window.attributes('-fullscreen', False))

# Background setup
bg_image = Image.open("1.png")  # Replace with your background image path
bg_image = bg_image.resize((login_window.winfo_screenwidth(), login_window.winfo_screenheight()), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(login_window, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Login components
tk.Label(login_window, text="Bank Management Login", font=("Arial", 36, "bold"), bg="#ffffff", fg="#000000").pack(pady=30)

tk.Label(login_window, text="Username:", font=("Arial", 20, "bold"), bg="#ffffff", fg="#000000").pack(pady=10)
username_entry = tk.Entry(login_window, font=("Arial", 20), width=30)
username_entry.pack(pady=10)

tk.Label(login_window, text="Password:", font=("Arial", 20, "bold"), bg="#ffffff", fg="#000000").pack(pady=10)
password_entry = tk.Entry(login_window, show="*", font=("Arial", 20), width=30)
password_entry.pack(pady=10)

tk.Button(login_window, text="Login", font=("Arial", 20, "bold"), command=validate_login, bg="#4682B4", fg="white", width=15).pack(pady=30)

login_window.mainloop()
