import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os

password=os.environ.get('E_PASSWORD')
address=os.environ.get('ADDRESS')
smtp_server=os.environ.get('SMTP_SERVER')

msg = MIMEMultipart()

def send_email(email, otp, firstname):
    msg['Subject'] = 'Welcome to Verba'
    msg.attach(MIMEText(f'''Hello {firstname},\n\nWelcome to Verba.\nPlease confirm your email address using the OTP: {otp}.\n\nThank you. \n\nDon't Fall Off the Wheel of Words \nVerba. ''', 'plain'))
    

    server = smtplib.SMTP(smtp_server, 587)
    server.starttls()
    server.login(address, password)
    server.sendmail(address, email, msg.as_string())
    server.quit()
        