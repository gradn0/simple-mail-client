import bcrypt
import sqlite3
from crypto import *

conn = sqlite3.connect("mail-client.db") 
cur = conn.cursor()

def initDatabase():
    #init database
    cur.execute("CREATE TABLE IF NOT EXISTS accounts (username TEXT, ctpassword TEXT, salt TEXT, nonce TEXT, smtpserver TEXT, imapserver TEXT)")

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
        password = bytes(input("Password: "), 'utf-8')
        smtpserver = input("SMTP Server: ")
        imapserver= input("IMAP Server: ")
    else:
        print("An account with that username already exists")
        return
    
    #encrypt password
    salt = bytes(os.urandom(16))
    key = deriveKey(salt)
    ctpassword, nonce = encrypt(password, key)
    
    #input to database
    cur = conn.cursor()
    cur.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)",(username, ctpassword, salt, nonce, smtpserver, imapserver))
    conn.commit()    

    print("\nAccount has been added\n")

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

def signIn():
    #get stored values
    username = input("Username: ")
    ctpassword, salt, nonce = cur.execute("SELECT ctpassword, salt, nonce FROM accounts WHERE username = ?", (username, )).fetchone()

    #decrypt
    key = deriveKey(salt)
    password = decrypt(ctpassword, key, nonce)

    #CHECK IF AUTHENTICATION SUCCESSFULL FIRST!!!!!
    #re-encrypt with new nonce
    ctpassword, nonce = encrypt(password, key)
    cur.execute("UPDATE accounts SET  ctpassword = ? WHERE username = ?", (ctpassword, username, ))
    cur.execute("UPDATE accounts SET  nonce = ? WHERE username = ?", (nonce, username, ))