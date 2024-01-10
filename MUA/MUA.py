from mail import *
from authentication import *
from layout import *

import os

if __name__ == "__main__":
    #initialisation
    initDatabase() 
    heading("Welcome to Simple Mail Server")
    os.environ["MASTER_PASS"] = input("Enter master password: ")
    active_account = " "

    #main menu
    while True:
        heading("Options")
        print("Active Account: (" + active_account + ")")
        useroption = input("1. Send\n2. View Mail\n3. Add account\n4. Select account\n5. Remove account\n6. Exit\n")
        if useroption == "1":
            if active_account != " ":
                sendMail(active_account)
            else:
                print("Please select an account first.")
        elif useroption == "2":
            if active_account != " ":
                getMail(active_account)
            else:
                print("Please select an account first.")
        elif useroption == "3":
            newAccount()
        elif useroption == "4":
            active_account = selectAccount()
        elif useroption == "5":
            account = input("Type the username of the account you wish to remove: ")
            removeAccount(account)
        elif useroption == "6":
            break
