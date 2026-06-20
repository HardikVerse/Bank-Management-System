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
            if not any(account["Account No."] == account_no for account in self.data):
                    return account_no
            
            
    def _find_account(self, account_no, pin):
        match_list = [found_info for found_info in self.data if found_info["Account No."] == account_no and found_info["PIN"] ==pin]
        return match_list[0] if match_list else None
    
        
    def _authentication(self):
        while True:
            acc_no_input = input("\nEnter Account No.: ")
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
    

    @staticmethod
    def _show_details(account):
        print("\nYour account details:")

        for key, value in account.items():
            print(f"\t{key} : {value}")


    @staticmethod
    def _name_input():
        return input("Name: ")
    

    @staticmethod
    def _email_input():
        return input("Email: ")
    

    @staticmethod
    def _age_calculator():
        
        age_calculator_output = []
        while True:
            try:
                input_dob = input("Date of Birth (DD/MM/YYYY): ")
                dob = date.strptime(input_dob, "%d/%m/%Y")

                age_calculator_output.append(input_dob)

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
        
        age_calculator_output.append(age)
        return age_calculator_output
    

    @staticmethod
    def _pin_input():
        while True:
            pin = input("4-digit PIN: ")
            if not pin.isdigit():    
                print("\nPIN must be numeric!\n")
            elif len(pin) != 4:
                print("\nPIN must be exactly 4 digits!\n")
            else:
                return pin
                
            
    def create_account(self):
        name = self._name_input()
        email = self._email_input()
        age_calculator_output = self._age_calculator()

        if age_calculator_output is None:
            return
        
        pin = self._pin_input()

        account_details = {
            "Name": name,
            "Date of Birth": age_calculator_output[0],
            "Age": age_calculator_output[1],
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


    def deposit(self):
        account = self._authentication()

        if account is None:
            return
        
        try: 
            amount = float(input("\nEnter deposit amount: "))
            amount = round(amount, 2)
        except ValueError:
            print("Enter Valid Amount.")

        account["Balance"] += amount
        self._save()
        print("Amount deposited successfully.")

        self._show_details(account)       


    def withdraw(self):
        account = self._authentication()

        if account is None:
            return
        
        self._show_details(account)

        
        try:
            amount = float(input("\nEnter withdraw amount: "))
            amount = round(amount, 2)
        except ValueError:
            print("Enter Valid Amount.")

        if amount < 0 :
            print("Amount must be greater than 0.")
            return
        if account["Balance"] < amount:
            print("Insufficient balance.")
            return
        
        account["Balance"] -= amount
        self._save()
        print("Amount withdrawn successfully.")
        
        self._show_details(account)


    def show_details(self):
        account = self._authentication()

        if account is None:
            return
        
        self._show_details(account)


    def update_details(self):
        account = self._authentication()

        if account is None:
            return
        
        self._show_details(account)
        
        print("\n1. Update Name")
        print("2. Update Date of Birth")
        print("3. Update Email")
        print("4. Update PIN")

        while True:
            try:
                choice = int(input("\nEnter choice here: "))
                break
            except ValueError:
                print("Enter number only.")


        name = ["Name", self._name_input]
        email = ["Email", self._email_input]
        age_calculator_output = ["Date of Birth", self._age_calculator, "Age"]
        pin = ["PIN", self._pin_input]

        choice_check = {
        1 : name,
        2 : age_calculator_output,
        3 : email, 
        4 : pin,
        }

        action = choice_check.get(choice)
        if action:
            detail_str = action[0]
            detail_function = action[1]()
            if detail_function is None:
                return
        else:
            print("Invalid choice")
            return
        
        if isinstance(detail_function, list):
            account[detail_str] = detail_function[0]
            account[action[2]] = detail_function[1]
        else:
            account[detail_str] = detail_function
        
        self._save()
        print("Detail updated successfully.")
        self._show_details(account)


    def delete_account(self):
        account = self._authentication()

        if account is None:
            return
        
        self._show_details(account)
        confirm = input("Are you sure? Press y to confirm: ").strip().lower()
        if confirm != "y":
            print("Deletion cancelled.")
            return

        self.data.remove(account)
        self._save()
        print("Account deleted successfully.")


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
        2 : bank.deposit,
        3 : bank.withdraw, 
        4 : bank.show_details, 
        5 : bank.update_details, 
        6 : bank.delete_account, 
        }
    

    action = choice_check.get(choice)
    if action:
        action()
    else:
        print("Invalid choice")
        

if __name__ == "__main__":
    main()
