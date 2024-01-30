import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
from dotenv import load_dotenv
load_dotenv()

password=os.environ.get('E_PASSWORD')
address=os.environ.get('ADDRESS')

msg = MIMEMultipart()

def send_email(email, otp):
    msg['Subject'] = 'Welcome to Verba'
    msg['From'] = email
    msg['To'] = email
    msg.attach(MIMEText(f'''Welcome to Verba. Please confirm your email address using the OTP: {otp}''', 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(address, password)
    server.sendmail(address, email, msg.as_string())
    server.quit()
       
        