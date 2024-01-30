import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os

password=os.environ.get('E_PASSWORD')
address=os.environ.get('ADDRESS')
smtp_server=os.environ.get('SMTP_SERVER')

msg = MIMEMultipart()

def send_email(email, otp):
    msg['Subject'] = 'Welcome to Verba'
    msg['From'] = email
    msg['To'] = email
    msg.attach(MIMEText(f'''Welcome to Verba. Please confirm your email address using the OTP: {otp}''', 'plain'))
    
    server = smtplib.SMTP(smtp_server, 587)  
    try:
        server.starttls()
        server.login(address, password)
        server.sendmail(address, email, msg.as_string())
    finally:
        server.quit()
        