from db_fms import fetch
import smtplib
from email.mime.text import MIMEText

# Sender credentials — store securely in env vars or config
SENDER_GMAIL = "pranavnt239@gmail.com"
SENDER_PASSWORD = "sdgg ohan pozs gtcq"

def send_password_email(to_email, full_name, password):
    subject = "🔐 Password Recovery - FMS App"
    body = f"""
    Hello {full_name},

    As requested, here is your account password:

    🔑 Password: {password}

    Best regards,  
    FMS Support Team
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_GMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_GMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_GMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def forgot_password(mobile_no: str):
    # 1. Fetch email and name using mobile number
    user_info = fetch(
        "user_registration",
        columns=["email", "full_name"],
        mobile_no=mobile_no
    )

    if not user_info or not user_info[0]:
        return {"status": "failed", "message": "Mobile number not found."}

    email, full_name = user_info[0]

    # 2. Fetch password from user_credentials
    cred_info = fetch(
        "user_credentials",
        columns=["password"],
        user_name=mobile_no
    )

    if not cred_info or not cred_info[0]:
        return {"status": "failed", "message": "Password not found for this user."}

    password = cred_info[0][0]

    # 3. Send password via email
    if send_password_email(email, full_name, password):
        return {"status": "success", "message": "Password sent to your registered email."}
    else:
        return {"status": "failed", "message": "Failed to send email. Please try again later."}

# Example usage
if __name__ == "__main__":
    result = forgot_password("9976334382")
    print(result)
