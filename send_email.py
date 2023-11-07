import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

FROM_EMAIL = "@gmail.com"
TO_EMAIL = ""
USER = ""
PASSWD = ""

def sendemail():
    fromaddr = FROM_EMAIL
    toaddr = TO_EMAIL
    toaddrs = [toaddr]

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Honeypot Network Intrusion Logs"
    body = '''Greetings Honeypot User,
    These logs include all the information regarding the intrusions in your home network.
    Regards,
    Nitish
    '''
    msg.attach(MIMEText(body, 'plain'))

    filename = "./deploy-server/honeypotlogs.json"
    f = open(filename)
    attachment = MIMEText(f.read())
    attachment.add_header('Content-Disposition',
                          'attachment', filename="Logs")
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(USER,PASSWD)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddrs, text)
    server.quit()


sendemail()