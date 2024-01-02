import sys

from PySide6 import QtCore, QtWidgets, QtGui

import smtplib
import imaplib
import mailbox
import email.message

#Define the Qt window class
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        #Create ui features
        #...

def smtpConnect():
    #Connection and login
    smtp.set_debuglevel(1)
    smtp.starttls()
    smtp.login(address, password)
    
def outbound():
    #Format message
    m = email.message.Message()
    m['From'] = address
    m['To'] = input("Recipient: ")
    m['Subject'] = input("Subject: ")
    body = input("Body: ")
    
    #send message
    m.set_payload(body)
    smtp.sendmail(address, m['To'], m.as_string())

if __name__ == "__main__":
    #Initialise Qt window 
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    #Initialise SMTP
    servername = input("Enter SMTP Server: ")
    address = input("Email Address: ")
    password = input("Password: ")

    smtp = smtplib.SMTP(servername, 587)

    #Body
    smtpConnect()
    outbound()
    smtp.quit()

    #Exit
    sys.exit(app.exec())