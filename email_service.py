# email_service.py
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

if not EMAIL or not APP_PASSWORD:
    # do not crash — but warn
    print("Warning: EMAIL_ADDRESS or EMAIL_APP_PASSWORD not set in .env")

def send_email(to_email, subject, message):
    """
    Sends a plain-text email via Gmail SMTP using the app password.
    Returns True on success, False on failure.
    """
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Email Error:", e)
        return False
