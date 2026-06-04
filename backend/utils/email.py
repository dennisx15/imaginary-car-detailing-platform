# backend/utils/email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_verification_email(to_email: str, verification_link: str):
    """
    Assembles and transmits a secure registration verification link to a user.
    """
    # DEVELOPMENT MODE FALLBACK: If no live SMTP credentials exist, print to terminal
    if not os.getenv("SMTP_USERNAME") or os.getenv("SMTP_SERVER") == "localhost":
        print("\n" + "="*60)
        print(f"📨 [DEV MAIL] To: {to_email}")
        print("Subject: Verify Your Car Detailing Account 🧼")
        print(f"Click link to activate: {verification_link}")
        print("="*60 + "\n")
        return True

    # Assembling the standard MIME Email Package
    msg = MIMEMultipart()
    msg['From'] = os.getenv("FROM_EMAIL")
    msg['To'] = to_email
    msg['Subject'] = "Verify Your Car Detailing Account 🧼"

    # Write a clean body message
    body = f"""
    Hello!
    
    Thank you for registering an account with our Car Detailing Hub. 
    Please click the link below to verify your email address and activate your profile dashboard:
    
    {verification_link}
    
    This validation link will remain active for the next 24 hours.
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Open the encrypted TLS pipeline connection to your SMTP provider
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT", 587)))
        server.starttls() # Establish the cryptographic socket tunnel
        server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
        
        # Fire the transmission packet
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Mail system failure processing dispatch network logs: {e}")
        return False