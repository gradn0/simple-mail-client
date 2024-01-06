from mail import *
from authentication import *

if __name__ == "__main__":
    #initialisation
    initDatabase() 

    #main menu
    print("--------Simple Mail Server--------")
    while True:
        print("Options: ")
        useroption = input("1. Send\n2. View Mail\n3. Add account\n4. List accounts\n5. Remove account\n6. Exit\n")
        if useroption == "3":
            newAccount()
        elif useroption == "4":
            listAccounts()
        elif useroption == "5":
            account = input("Type the username of the account you wish to remove: ")
            removeAccount(account)
        elif useroption == "6":
            break