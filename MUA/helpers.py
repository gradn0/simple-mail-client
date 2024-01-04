from smtplib import SMTP
from imaplib import IMAP4_SSL
from email import message, message_from_bytes

#Submission Handling-----------------------------------------------------

def smtpConnect(smtpserver, sender, password):
    #SMTP instance
    smtp = SMTP(smtpserver, 587)

    #Connection and login
    #smtp.set_debuglevel(1)
    smtp.starttls()
    smtp.login(sender, password)

    return smtp
    
def sendMail(sender, password, smtpserver, recipient, subject, body):

    smtp = smtpConnect(smtpserver, sender, password)

    #Format message
    m = message.Message()
    m['From'] = sender
    m['To'] = recipient
    m['Subject'] = subject
    body = body
    
    #send message
    m.set_payload(body)
    smtp.sendmail(sender, m['To'], m.as_string())

    smtp.quit()

#Retrieval Handling-----------------------------------------------------
    
def parseMail(byte_data):
    message = message_from_bytes(byte_data[0][1]) #Message object
    
    #Print header
    print(f"\
To: {message.get('To')}\n\
From: {message.get('From')}\n\
Subject: {message.get('Subject')}\n\
        ")
    
    #Print body
    if message.is_multipart():
        payload = message.get_payload() #list of message objects
        for part in payload:
            print(part.get_payload())
    else: 
        print(message.get_payload())


def getMail(imapserver, reciever, password):
    #IMAP instance and connect to inbox
    m = IMAP4_SSL(imapserver, 993)

    #m.debug = 5
    m.login(reciever, password)
    m.select()

    ret, data = m.search(None, 'ALL') #data is list of message numbers
    
    for i in data[0].split():
        ret, data = m.fetch(i, '(RFC822)') #byte data
 
    parseMail(data)

    m.close()
    m.logout()