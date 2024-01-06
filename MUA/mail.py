from smtplib import SMTP
from imaplib import IMAP4_SSL
from email import message, message_from_bytes

def smtpConnect(smtpserver, sender, password):
    smtp = SMTP(smtpserver, 587)

    #connection and login
    smtp.starttls()
    smtp.login(sender, password)

    return smtp
    
def sendMail(sender, password, smtpserver, recipient, subject, body):
    smtp = smtpConnect(smtpserver, sender, password)

    #format message
    m = message.Message()
    m['From'] = sender
    m['To'] = recipient
    m['Subject'] = subject
    body = body
    
    #send message
    m.set_payload(body)
    smtp.sendmail(sender, m['To'], m.as_string())

    smtp.quit()
    
def parseMail(byte_data):
    message = message_from_bytes(byte_data[0][1]) 
    
    #print header
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
            print(part.get_payload())
    else: 
        print(message.get_payload())

def getMail(imapserver, reciever, password):
    m = IMAP4_SSL(imapserver, 993)

    m.login(reciever, password)
    m.select()

    ret, data = m.search(None, 'ALL') #data is list of message numbers
    
    for i in data[0].split():
        ret, data = m.fetch(i, '(RFC822)') #byte data
 
    parseMail(data)

    m.close()
    m.logout()