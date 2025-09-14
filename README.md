Mehta Bank - Command-Line Banking Application
A simple yet powerful command-line interface (CLI) banking simulation built with Python.

This project simulates a basic banking system where users can create accounts, log in, manage their funds, and view their transaction history. It also includes a suite of financial calculators. The application is designed to be run in a terminal and uses the colorama library for a more engaging and readable user interface.

✨ Features
Account Management: Create a new bank account with a name and a 4-digit PIN.

User Authentication: Secure login system for existing users.

Core Banking Operations:

Check account balance.

Deposit funds into an account.

Withdraw funds, with checks for insufficient balance.

Transaction History: All deposits and withdrawals are logged with a timestamp and can be reviewed at any time.

Financial Calculators:

Loan EMI Calculator: Calculate Equated Monthly Installments for a loan.

Fixed Deposit (FD) Calculator: Project maturity amount for a lump-sum investment.

Recurring Deposit (RD) Calculator: Project maturity amount for monthly investments.

Interactive CLI: A colorful and user-friendly interface for easy navigation.

Data Persistence: Account information is saved in a accounts.csv file, and transaction logs are stored in individual JSON files.

🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
Python 3.6 or higher

pip (Python package installer)

Installation & Setup
Clone the repository:

Bash

git clone https://github.com/mohitmehta03/Bank-Manament_consol-Application.git
cd Bank-Manament_consol-Application
Install dependencies:
This project requires the colorama library for colored terminal text.

Bash

pip install colorama
(Note: The cryptography library is imported but not fully implemented in the current version. You may need to install it if you extend its functionality: pip install cryptography)

Run the application:

Bash

python main.py 
(Assuming you have named your main script main.py)

💻 How to Use
Once the application is running, you will be greeted with the main menu:

_____ Welcome to the Mehta Bank _____

Date:2025-09-15   Time:12:30:00

Please choose an option:
    1. Create Account
    2. Login Account
    3. Financial Calculators 
    4. Exit
Create an Account: Choose option 1 and follow the prompts to enter your full name and create a 4-digit PIN. Your unique 10-digit account number will be displayed. Save this number!

Login: Choose option 2 and enter your account number and PIN to access your account menu.

User Menu: After logging in, you can view your balance, deposit, withdraw, check transaction history, or log out.

Financial Calculators: Choose option 3 from the main menu to access the financial planning tools without logging in.

📁 File Structure
The application will generate the following files and directories as you use it:

main.py: The main Python script containing the application logic.

accounts.csv: A CSV file created to store user account details (account number, name, balance, PIN).

transaction_logs/: A directory created to store transaction histories.

<account_number>_transactions.json: A separate JSON file for each account's transaction log.

🛠️ Future Improvements
This project is a great starting point, and here are some ways it could be improved:

🔒 Enhanced Security: Implement PIN hashing (e.g., using hashlib) instead of storing PINs in plain text in the accounts.csv file.

🗃️ Robust Database: Migrate from a CSV file to a more robust database system like SQLite to better handle data integrity and prevent corruption.

🖥️ Cross-Platform Support: The current PIN masking function (get_masked_input) is Unix-specific. Replace it with a cross-platform solution like the getpass module for wider compatibility.

💡 Object-Oriented Structure: Refactor the code to use classes (e.g., Account, Customer) to create a more organized and scalable object-oriented structure.

Correct the formula in the Recurring Deposit (RD) Calculator for better accuracy.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
