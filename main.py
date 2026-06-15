from pathlib import Path
from datetime import date, datetime
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
         
    @staticmethod
    def _generate_account_no():
        return "".join(random.choices(string.digits, k = 11))

    def create_account(self):
        name = input("Name: ")
        email = input("Email: ")

        while True:
            try:
                input_dob = input("Date of Birth (DD/MM/YYYY): ")
                dob = date.strptime(input_dob, "%d/%m/%Y")
                break
            except Exception as e:
                print(f"Please try again : {e}")
                
            
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

            pin = int(pin)

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
