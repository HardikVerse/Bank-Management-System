from pathlib import Path
from datetime import date
import json
import random
import string


class Bank:
    database = "users_data.json"
    

    def __init__(self):
        self.data = []
        self._load()
        
    def _load(self):
        path = Path(self.database)
        try:
            if path.exists():
                if path.stat().st_size == 0:
                    self.data = []
                    return
                with open(path) as f:
                    self.data = json.load(f)
            else:
                print("No existing database found. Starting fresh.")
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error loading database: {e}")
            raise 

    def _save(self):
        try:
            with open(self.database, "w") as f:
                json.dump(self.data, f, indent= 4)
        except OSError as err:
            print(f"Error saving database: {err}")
         
    
    def _generate_account_no(self):
        while True: 
            account_no = "".join(random.choices(string.digits, k = 11))
            if not any(acc["Account No."] == account_no for acc in self.data):
                    return account_no
            
    def _find_account(self, account_no, pin):
        match_list = [found_info for found_info in self.data if found_info["Account No."] == account_no and found_info["PIN"] ==pin]
        return match_list[0] if match_list else None
        
    def _authentication(self):
        while True:
            acc_no_input = input("Enter Account No.: ")
            if not acc_no_input.isdigit():
                print("Enter Valid Account Number.")
            else:
                break
        while True:
            acc_pin_input = input("Enter PIN: ")
            if not acc_pin_input.isdigit():
                print("Enter Valid PIN.")
            else:
                break
        
        account = self._find_account(acc_no_input, acc_pin_input)
        if account is None: 
            print("Account not found. Check your account number and PIN.")
        return account
        
    def create_account(self):
        name = input("Name: ")
        email = input("Email: ")

        while True:
            try:
                input_dob = input("Date of Birth (DD/MM/YYYY): ")
                dob = date.strptime(input_dob, "%d/%m/%Y")
                break
            except ValueError:
                print("Please enter a vaild date or in given format.")
            
        today = date.today()

        age = today.year - dob.year

        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1
        
        if age < 18:
            print("\nYou must be at least 18 to create an account.")
            return
        
        while True:
            pin = input("4-digit PIN: ")
            if not pin.isdigit():    
                print("\nPIN must be numeric!\n")
            elif len(pin) != 4:
                print("\nPIN must be exactly 4 digits!\n")
            else:
                break

        account_details = {
            "Name": name,
            "Age": age,
            "Email": email,
            "PIN": pin,
            "Account No.": self._generate_account_no(),
            "Balance": 0
        }

        self.data.append(account_details)
        self._save()

        print("\nAccount created successfully!\n")
        for key,value in account_details.items():
            print(f"\t{key} : {value}")
        print()
        print("Please note the account number and PIN.")

def main():

    bank = Bank()


    print("\n1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Show Details")
    print("5. Update Details")
    print("6. Delete Account")

    while True:
        try:
            choice = int(input("\nEnter choice here: "))
            break
        except ValueError:
            print("Enter number only.")
        

    choice_check = {
        1 : bank.create_account,
        2 : None,
        3 : None, 
        4 : None, 
        5 : None, 
        6 : None, 
        }
    

    action = choice_check.get(choice)
    if action:
        action()
    else:
        print("Invalid choice")
        

if __name__ == "__main__":
    main()
