import os 
import json
import datetime
import random
from colorama import init, Fore, Back, Style
import time
import sys
import termios
import tty
from cryptography.fernet import Fernet

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def loading_animation(): #loading animation
    animation = "|/-\\"
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write("\r" + "Loading " + animation[i % len(animation)])
        sys.stdout.flush()
    sys.stdout.write("\r" + " " * 20 + "\r")  # Clear the line after loading
TRANSACTION_LOG_DIR = "transaction_logs"
Logging_DIR = "logs"
ACCOUNTS_FILE = 'accounts.csv'

def get_masked_input(prompt="Enter your PIN: "):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        pin_chars = []
        while True:
            char = sys.stdin.read(1)
            if char == '\r' or char == '\n':  # Enter key
                break
            elif char == '\x7f':  # Backspace
                if pin_chars:
                    pin_chars.pop()
                    sys.stdout.write('\b \b')  # Erase the asterisk
                    sys.stdout.flush()
            else:
                pin_chars.append(char)
                sys.stdout.write('*')
                sys.stdout.flush()
        sys.stdout.write('\n')
        return "".join(pin_chars)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def generate_account_number():
    return random.randint(1000000000, 9999999999) # Generate a random 10-digit number

def get_all_accounts(): # Load data from the CSV file
    if not os.path.exists(ACCOUNTS_FILE):
        return {} 
    
    with open(ACCOUNTS_FILE, 'r') as file:
        lines = file.readlines()
        accounts = {}
        for line in lines[1:]: 
            acc_num, name, balance, password = line.strip().split(',')
            accounts[acc_num] = {"name": name, "balance": float(balance), "password": password}
        return accounts

def save_all_accounts(accounts): # Save data to the CSV file
    with open(ACCOUNTS_FILE, 'w') as file:
        file.write("account_number,name,balance,password\n")
        for acc_num, details in accounts.items():
            line = f"{acc_num},{details['name']},{details['balance']},{details['password']}\n"
            file.write(line)
def create_account(): # Create a new account
    print("\n--- Create New Account ---")
    name = input("Enter your full name: ")
    while True:
        pin = get_masked_input("Create a 4-digit PIN: ")
        if len(pin) == 4 and pin.isdigit():
            break
        else:
            print("Invalid PIN. Please enter exactly 4 digits.")
    
    account_number = generate_account_number()
    accounts = get_all_accounts()
    accounts[account_number] = {"password": pin, "name": name, "balance": 0.0}
    save_all_accounts(accounts)
    loading_animation()
    print(Style.BRIGHT+Fore.MAGENTA +"\n✅ Account created successfully!")
    print(Style.BRIGHT+"Your new account number is: "+Fore.MAGENTA+f"{account_number}")
    print(Fore.RED+ Style.BRIGHT+"Please keep it safe and do not share it.")
    input("Press Enter to return to the main menu...")
    clear_screen()

def login_account(): # Login to an existing account
    print("\n--- Login to Your Account ---")
    account_number = input("Enter your account number: ")
    accounts = get_all_accounts()
    while True:
        pin = get_masked_input("Enter your 4-digit PIN: ")
        if account_number in accounts and accounts[account_number]['password'] == pin:
            loading_animation()
            print(Fore.GREEN + Style.BRIGHT + "\n✅ Login successful!")
            user_menu(account_number)
            clear_screen()
            loading_animation()
            return
        else:
            print(Fore.RED + "❌ Invalid account number or PIN.")
            
def user_menu(account_number): # Log-in menu after successful login
    while True:
        init(autoreset=True)
        print(Style.BRIGHT +Back.LIGHTMAGENTA_EX +"\n--- User Menu ---")
        print(Style.BRIGHT + "\t1. View Balance\n\t2. Deposit Funds\n\t3. Withdraw Funds\n\t4. View Transaction History\n\t5. Logout")
        choice = input(Style.BRIGHT + Fore.CYAN + "Enter your choice (1-5): ")
        
        if choice == '1':
            view_balance(account_number)
        elif choice == '2':
            deposit_funds(account_number)
        elif choice == '3':
            withdraw_funds(account_number)
        elif choice == '4':
            view_transaction_history(account_number)
        elif choice == '5':
            print(Fore.MAGENTA + Style.BRIGHT + "Logging out...")
            clear_screen()
            return False
        else:
            print(Fore.RED + "Invalid choice. Please try again.")
    clear_screen()
def view_balance(account_number):
    accounts = get_all_accounts()
    balance = accounts[account_number]['balance']
    loading_animation()
    print(Fore.YELLOW + Style.BRIGHT + f"\nYour current balance is: ₹{balance:.2f}")
    input("Press Enter to return to the menu...")
    clear_screen()
def deposit_funds(account_number):
    accounts = get_all_accounts()
    while True:
        try:
            amount = float(input("Enter amount to deposit: ₹"))
            loading_animation()
            if amount <= 0:
                print(Fore.RED + "Amount must be positive.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Invalid amount. Please enter a number.")
    
    accounts[account_number]['balance'] += amount
    save_all_accounts(accounts)
    log_transaction(account_number, "Deposit", amount)
    print(Fore.GREEN + Style.BRIGHT + f"\n✅ Successfully deposited ₹{amount:.2f}.")
    input("Press Enter to return to the menu...")
    clear_screen()
def withdraw_funds(account_number):
    accounts = get_all_accounts()
    while True:
        try:
            amount = float(input("Enter amount to withdraw: ₹"))
            loading_animation()
            if amount <= 0:
                print(Fore.RED + "Amount must be positive.")
                continue
            if amount > accounts[account_number]['balance']:
                print(Fore.RED + "Insufficient funds.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Invalid amount. Please enter a number.")
    
    accounts[account_number]['balance'] -= amount
    save_all_accounts(accounts)
    log_transaction(account_number, "Withdrawal", amount)
    print(Fore.GREEN + Style.BRIGHT + f"\n✅ Successfully withdrew ₹{amount:.2f}.")
    input("Press Enter to return to the menu...")
    clear_screen()
def log_transaction(account_number, transaction_type, amount):
    if not os.path.exists(TRANSACTION_LOG_DIR):
        os.makedirs(TRANSACTION_LOG_DIR)
    
    log_file = os.path.join(TRANSACTION_LOG_DIR, f"{account_number}_transactions.json")
    transaction = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": transaction_type,
        "amount": amount
    }
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            transactions = json.load(file)
    else:
        transactions = []
    
    transactions.append(transaction)
    
    with open(log_file, 'w') as file:
        json.dump(transactions, file, indent=4)

def view_transaction_history(account_number):
    loading_animation()
    log_file = os.path.join(TRANSACTION_LOG_DIR, f"{account_number}_transactions.json")
    print(Style.BRIGHT+ Back.LIGHTMAGENTA_EX + "\n--- Transaction History ---")
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            transactions = json.load(file)
            if not transactions:
                print("No transactions found.")
            else:
                for txn in transactions:
                    print(f"{txn['date']} - {txn['type']}: ₹{txn['amount']:.2f}")
    else:
        print(Style.BRIGHT+"!No transactions found.")
    
    input("Press Enter to return to the menu...")
    clear_screen()

def Banking_calculators():
    while True:
        print(Style.BRIGHT + Back.LIGHTMAGENTA_EX + "\n--- Financial Calculators ---")
        print(Style.BRIGHT + "\t1. Loan EMI Calculator\n\t2. Fixed Deposite Calculator\n\t3. Recurring Deposite calculator\n\t4. Return to Main Menu")
        choice = input(Style.BRIGHT + Fore.CYAN + "Enter your choice (1-4): ")
        
        if choice == '1':
            try:
                loan_amount = float(input("Enter the loan amount (₹): "))
                annual_rate = float(input("Enter the annual interest rate (%): "))
                tenure_years = int(input("Enter the tenure (years): "))
                monthly_rate = annual_rate / (12 * 100)
                tenure_months = tenure_years * 12
                emi = (loan_amount * monthly_rate * (1 + monthly_rate)**tenure_months) / ((1 + monthly_rate)**tenure_months - 1)
                loading_animation()
                print(Fore.GREEN + Style.BRIGHT + f"\nYour monthly EMI is: ₹{emi:.2f}")
                print(Fore.GREEN + Style.BRIGHT + f"Total payment over {tenure_years} years: ₹{emi * tenure_months:.2f}")
                print(Fore.GREEN + Style.BRIGHT + f"Total interest paid: ₹{(emi * tenure_months) - loan_amount:.2f}")
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter numeric values.")
            input("Press Enter to return to the calculator menu...")
        
        elif choice == '2':
            try:
                principal = float(input("Enter the principal amount (₹): "))
                annual_rate = float(input("Enter the annual interest rate (%): "))
                tenure_years = int(input("Enter the tenure (years): "))
                n = 4  # Quarterly compounding
                amount = principal * (1 + annual_rate / (n * 100))**(n * tenure_years)
                loading_animation()
                print(Fore.GREEN + Style.BRIGHT + f"\nMaturity amount after {tenure_years} years: ₹{amount:.2f}")
                print(Fore.GREEN + Style.BRIGHT + f"Total interest earned: ₹{amount - principal:.2f}")
                print(Fore.GREEN + Style.BRIGHT + f"Total investment: ₹{principal:.2f}")
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter numeric values.")
            input("Press Enter to return to the calculator menu...")
        elif choice == '3':
            try:
                monthly_investment = float(input("Enter the monthly investment amount (₹): "))
                annual_rate = float(input("Enter the annual interest rate (%): "))
                tenure_years = int(input("Enter the tenure (years): "))
                n = 4  # Quarterly compounding
                total_amount = monthly_investment * (((1 + annual_rate / (n * 100))**(n * tenure_years) - 1) / (1-((1 + annual_rate / (n * 100))**(-1/3))))
                loading_animation()
                print(Fore.GREEN + Style.BRIGHT + f"\nMaturity amount after {tenure_years} years: ₹{total_amount:.2f}")
                print(Fore.GREEN + Style.BRIGHT + f"Total investment: ₹{monthly_investment * tenure_years * 12:.2f}")
                print(Fore.GREEN + Style.BRIGHT + f"Total interest earned: ₹{total_amount - (monthly_investment * tenure_years * 12):.2f}")
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter numeric values.")
            input("Press Enter to return to the calculator menu...")
        elif choice == '4':
            clear_screen()
            return
        else:
            clear_screen()
            print(Fore.RED + "Invalid choice. Returning to calculator menu.")
        clear_screen()
            
    
def main():
    while True:
        init(autoreset=True)
        print(Fore.MAGENTA+Style.BRIGHT + " _____ Welcome to the Mehta Bank _____")
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        print(Style.BRIGHT+ f"\nDate:{now} \tTime:{datetime.datetime.now().strftime('%H:%M:%S')}")
        print(Style.BRIGHT +Fore.LIGHTMAGENTA_EX+ "\nPlease choose an option:")
        print(Style.BRIGHT + "\t1. Create Account\n\t2. Login Account\n\t3. Financial Calculators \n \t4. Exit")
        choice = input(Style.BRIGHT+ Fore.LIGHTMAGENTA_EX + "Enter your choice (1-4): ")
        if choice == '1':
            create_account()
        elif choice == '2':
            login_account()
        elif choice == '3':
            Banking_calculators()
            input("Press Enter to return to the main menu...")
        elif choice == '4':
            print(Fore.MAGENTA+Style.BRIGHT + " Thank you for visiting Mehta Bank. signing off !")
            exit()
        else:
            clear_screen()
            print(Fore.RED + " Invalid choice. Please try again.")
            

if __name__ == "__main__":
    main()