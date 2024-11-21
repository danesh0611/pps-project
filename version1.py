import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Function for login validation
def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "admin":
        messagebox.showinfo("Login Success", "Login Successful!")
        login_window.destroy()
        main_menu()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password!")

# Function for the main menu
def main_menu():
    def open_existing_account():
        messagebox.showinfo("Existing Account", "Feature to manage existing accounts will go here!")
    
    def create_new_account():
        messagebox.showinfo("New Account", "Feature to create a new account will go here!")
    
    def exit_system():
        main_menu_window.destroy()

    # Create main menu window
    main_menu_window = tk.Tk()
    main_menu_window.title("Bank Management System - Main Menu")
    main_menu_window.attributes('-fullscreen', True)  # Full-screen mode
    
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
    tk.Button(main_menu_window, text="Existing Account", font=("Arial", 20, "bold"), command=open_existing_account, width=20, bg="#000080", fg="white").pack(pady=20)
    tk.Button(main_menu_window, text="New Account", font=("Arial", 20, "bold"), command=create_new_account, width=20, bg="#006400", fg="white").pack(pady=20)
    tk.Button(main_menu_window, text="Exit", font=("Arial", 20, "bold"), command=exit_system, width=20, bg="#800000", fg="white").pack(pady=20)
    
    main_menu_window.mainloop()

# Creating the login screen
login_window = tk.Tk()
login_window.title("Bank Management System - Login")
login_window.attributes('-fullscreen', True)  # Full-screen mode

# Bind Esc key to exit full-screen
login_window.bind("<Escape>", lambda event: login_window.attributes('-fullscreen', False))

# Background setup
bg_image = Image.open("1.png")  # Replace with your background image path
bg_image = bg_image.resize((login_window.winfo_screenwidth(), login_window.winfo_screenheight()), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(login_window, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Login screen components
tk.Label(login_window, text="Bank Management Login", font=("Arial", 36, "bold"), bg="#ffffff", fg="#000000").pack(pady=30)

tk.Label(login_window, text="Username:", font=("Arial", 20, "bold"), bg="#ffffff", fg="#000000").pack(pady=10)
username_entry = tk.Entry(login_window, font=("Arial", 20), width=30)
username_entry.pack(pady=10)

tk.Label(login_window, text="Password:", font=("Arial", 20, "bold"), bg="#ffffff", fg="#000000").pack(pady=10)
password_entry = tk.Entry(login_window, show="*", font=("Arial", 20), width=30)
password_entry.pack(pady=10)

tk.Button(login_window, text="Login", font=("Arial", 20, "bold"), command=validate_login, bg="#4682B4", fg="white", width=15).pack(pady=30)

login_window.mainloop()
