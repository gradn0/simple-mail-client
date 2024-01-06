import bcrypt
import sqlite3

conn = sqlite3.connect("mail-client.db") 
cur = conn.cursor()

def initDatabase():
    #initialise the accounts database
    cur.execute("CREATE TABLE IF NOT EXISTS accounts (username TEXT, hash TEXT, smtpserver TEXT, imapserver TEXT)")

    conn.commit()

def usernameExists(username):
    #check if username is in the database
    x = cur.execute("SELECT rowid FROM accounts WHERE username = ?", (username, )).fetchone()
    if x is None:
        return False
    else:
        return True

def newAccount():
    #get account details
    username = input("Username: ")
    if(usernameExists(username) == False):
        password = bytes(input("Password: "), "ascii")
        smtpserver = input("SMTP Server: ")
        imapserver= input("IMAP Server: ")
    else:
        print("An account with that username already exists")
        return

    #generate hash and salt
    salt = bcrypt.gensalt()  
    hash = bcrypt.hashpw(password, salt)

    #input to database
    cur = conn.cursor()
    cur.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)",(username, hash, smtpserver, imapserver))
    conn.commit()    

    print("\nAccount has been added\n")

def signIn():
    #input credentials
    username = input("Username: ")
    userpassword = bytes(input("Password: "), 'utf-8')

    if(usernameExists(username)):
        #retrieve hash from database
        hash = cur.execute("SELECT hash FROM accounts WHERE username = ?", (username, )).fetchone()[0]

        #check hash against input
        valid = bcrypt.checkpw(userpassword, hash)
        if(valid):
            print("Signing in...")
        else:
            print("Incorrect username or password")
    else:
        print("Incorrect username or password")

def listAccounts():
    #return a list of usernames in the database
    accounts = cur.execute("SELECT username FROM accounts").fetchall()

    print("\n--------Accounts--------")
    for account in accounts:
        print(account[0])
    print("\n")

def removeAccount(account):
    #deletes an account from the database
    if usernameExists(account):
        cur.execute("DELETE FROM accounts WHERE username = ?", (account, )).fetchone()
        conn.commit()
        print("\nAccount removed.\n")
    else:
        print("\nAccount does not exist\n")
        return