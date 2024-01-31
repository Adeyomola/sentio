import smtplib
import os

password=os.environ.get('E_PASSWORD')
address=os.environ.get('ADDRESS')
smtp_server=os.environ.get('SMTP_SERVER')

def send_email(email, otp, firstname):
    msg = f'''Subject: Welcome to Verba Hello {firstname},\n\nWelcome to Verba.\nPlease confirm your email address using the OTP: {otp}.\n\nThank you. \n\nDon't Fall Off the Wheel of Words \nVerba.'''
    
    server = smtplib.SMTP(smtp_server, 587)
    server.starttls()
    server.login(address, password)
    server.sendmail(address, email, msg)
    server.quit()
        