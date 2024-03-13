from smtplib import SMTP
from imaplib import IMAP4_SSL
from email import message, message_from_bytes
from authentication import *
from layout import *
from html.parser import *

import os

def smtpConnect(smtpserver, username, password):
    smtp = SMTP(smtpserver, 587)

    #connection and login
    smtp.starttls()
    smtp.login(username, password)

    return smtp

def sendMail(username):
    heading("Draft")
    #get stored values
    ctpassword, salt, nonce = cur.execute("SELECT ctpassword, salt, nonce FROM accounts WHERE username = ?", (username, )).fetchone()

    #decrypt
    key = deriveKey(salt)
    password = decrypt(ctpassword, key, nonce)

    #send email 
    smtpserver = cur.execute("SELECT smtpserver FROM accounts WHERE username = ?", (username, )).fetchone()[0]
    
    smtp = smtpConnect(smtpserver, username, password.decode('utf-8'))
    
    m = message.Message()
    m['From'] = username
    m['To'] = input("Recipient: ")
    m['Subject'] = input("Subject: ")
    body = input("Body: ")

    m.set_payload(body)
    smtp.sendmail(username, m['To'], m.as_string())

    smtp.quit()

    print("\nEmail has been sent!\n")

    #re-encrypt with new nonce
    ctpassword, nonce = encrypt(password, key)
    cur.execute("UPDATE accounts SET  ctpassword = ? WHERE username = ?", (ctpassword, username, ))
    cur.execute("UPDATE accounts SET  nonce = ? WHERE username = ?", (nonce, username, ))

def parseMail(byte_data):
    message = message_from_bytes(byte_data[0][1]) 

    #print header
    print("="*70 + "\n")
    print(f"\
To: {message.get('To')}\n\
From: {message.get('From')}\n\
Subject: {message.get('Subject')}\n\
        ")
    
    #print body
    if message.is_multipart():
        payload = message.get_payload() #list of message objects
  
        #print each subemail
        for part in payload:
            if part.get_content_charset() != None:
                if part.get_content_type() == "text/plain":
                    print(part.get_payload())
            else:
                continue
    else: 
        print(message.get_payload()) 

def getMail(username):
    #get stored values
    ctpassword, salt, nonce = cur.execute("SELECT ctpassword, salt, nonce FROM accounts WHERE username = ?", (username, )).fetchone()

    #decrypt
    key = deriveKey(salt)
    password = decrypt(ctpassword, key, nonce)

    #retrieve
    imapserver = cur.execute("SELECT imapserver FROM accounts WHERE username = ?", (username, )).fetchone()[0]
    m = IMAP4_SSL(imapserver, 993)

    m.login(username, password.decode('utf-8'))
    m.select()

    ret, bmail_ids = m.search(None, 'ALL') #data is a byte-like list of mail ids
    mail_ids = bmail_ids[0].decode().split(" ")

    #print email previews
    heading("Inbox")
    for id in mail_ids:
        ret, byte_data = m.fetch(id, '(RFC822)')
        message = message_from_bytes(byte_data[0][1]) 
        #print(id + ". " + message.get("Subject") + " ------------------- " + message.get("From") )
        seperator(id + ". " + message.get("Subject"), message.get("From"))
 
    print("\n")

    #print email
    email_id = input("Choose email id to view: ")
    ret, byte_data = m.fetch(email_id, '(RFC822)')
    parseMail(byte_data)

    m.close()
    m.logout()

    #re-encrypt with new nonce
    ctpassword, nonce = encrypt(password, key)
    cur.execute("UPDATE accounts SET  ctpassword = ? WHERE username = ?", (ctpassword, username, ))
    cur.execute("UPDATE accounts SET  nonce = ? WHERE username = ?", (nonce, username, ))
