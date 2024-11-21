import pandas as pd
import os

csv_file = "bank_managment.csv"
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=[
        "TransactionID", "Name", "Age", "Gender", "DOB", "IdentityNumber", "Type", "Amount", "Balance", "Description"
    ])
    df.to_csv(csv_file, index=False)
else:
    df = pd.read_csv(csv_file)
def display_menu():
    print("\n=== Bank Program ===")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Transaction Statement")
    print("4. Exit")
    return input("Select an option (1-4): ")

def get_balance(name, identity_number):
    user_data = df[(df["Name"] == name) & (df["IdentityNumber"] == identity_number)]
    if user_data.empty:
        return 0
    return user_data["Balance"].iloc[-1]

def deposit(name, age, gender, dob, identity_number, amount, description="Deposit"):
    global df
    current_balance = get_balance(name, identity_number)
    new_balance = current_balance + amount
    transaction_id = len(df) + 1
    new_entry = {
        "TransactionID": transaction_id,
        "Name": name,
        "Age": age,
        "Gender": gender,
        "DOB": dob,
        "IdentityNumber": identity_number,
        "Type": "Deposit",
        "Amount": amount,
        "Balance": new_balance,
        "Description": description
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(csv_file, index=False)
    print(f"Deposited {amount}. New Balance: {new_balance}")

def withdraw(name, identity_number, amount, description="Withdrawal"):
    global df
    current_balance = get_balance(name, identity_number)
    if amount > current_balance:
        print("Insufficient funds.")
        return
    new_balance = current_balance - amount
    transaction_id = len(df) + 1
    user_data = df[(df["Name"] == name) & (df["IdentityNumber"] == identity_number)]
    if user_data.empty:
        print("User not found.")
        return
    new_entry = {
        "TransactionID": transaction_id,
        "Name": name,
        "Age": user_data["Age"].iloc[0],
        "Gender": user_data["Gender"].iloc[0],
        "DOB": user_data["DOB"].iloc[0],
        "IdentityNumber": identity_number,
        "Type": "Withdrawal",
        "Amount": amount,
        "Balance": new_balance,
        "Description": description
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(csv_file, index=False)
    print(f"Withdrew {amount}. New Balance: {new_balance}")

def transaction_statement(name, identity_number):
    user_data = df[(df["Name"] == name) & (df["IdentityNumber"] == identity_number)]
    if user_data.empty:
        print("No transactions available for this user.")
    else:
        print("\n=== Transaction Statement ===")
        print(user_data.to_string(index=False))

while True:
    choice = display_menu()
    if choice in ["1", "2"]:
        name = input("Enter your name: ")
        identity_number = input("Enter your identity number: ")
        
        if choice == "1":
            try:
                age = input("Enter your age: ")
                gender = input("Enter your gender: ")
                dob = input("Enter your date of birth (YYYY-MM-DD): ")
                amount = float(input("Enter deposit amount: "))
                if amount <= 0:
                    print("Amount must be greater than zero.")
                else:
                    deposit(name, age, gender, dob, identity_number, amount)
            except ValueError:
                print("Invalid input. Please enter valid details.")
        
        elif choice == "2":
            try:
                amount = float(input("Enter withdrawal amount: "))
                if amount <= 0:
                    print("Amount must be greater than zero.")
                else:
                    withdraw(name, identity_number, amount)
            except ValueError:
                print("Invalid input. Please enter valid details.")

    elif choice == "3":
        name = input("Enter your name: ")
        identity_number = input("Enter your identity number: ")
        transaction_statement(name, identity_number)

    elif choice == "4":
        print("Thank you for using the bank program. Goodbye!")
        break
    else:
        print("Invalid option. Please select a valid choice.")