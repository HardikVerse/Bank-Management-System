import json
import random
from pathlib import Path
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
                with open(self.database) as f:
                    self.data = json.load(f)
            else:
                print("No existing database found. Starting fresh.")
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error loading database: {e}")
            raise 

        
    def create_account(self):
        name = input("Name: ")
        email = input("Email: ")
        while True:
            age = input("Age: ")
            if not age.isdigit():
                print("\nAge must be numeric!\n")
            elif int(age) < 18:
                print("\nYou must be at least 18 to create an account.")
                return            
            else:
                break  
                
        while True:
            pin = input("4-digit PIN: ")
            if not pin.isdigit():    
                print("\nPIN must be numeric!\n")
            elif len(pin) != 4:
                print("\nPIN must be exactly 4 digits!\n")
            else:
                break

        age = int(age)
        pin = int(pin)

        account_details = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account_no": 5435435,
            "balance": 0
        }

        print()
        for key,value in account_details.items():
            print(f"{key} : {value}")
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
