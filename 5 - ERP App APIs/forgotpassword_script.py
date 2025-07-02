from db_erp import fetch
import smtplib
from email.mime.text import MIMEText

# Predeclared sender credentials (keep password secure!)
SENDER_GMAIL = "pranavnt239@gmail.com"
SENDER_PASSWORD = "sdgg ohan pozs gtcq"

def send_password_email(to_email, full_name, password):
    subject = "🔐 Password Recovery - Satyukt App"
    body = f"""
    Hello {full_name},

    As requested, here is your account password:

    🔑 Password: {password}

    Best regards,  
    Satyukt Analytics Team
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
    # Step 1: Check if user exists and fetch email + full name
    user_info = fetch(
        "user_registration",
        columns=["email", "full_name"],
        mobile_no=mobile_no
    )

    if not user_info or not user_info[0]:
        return {"status": "failed", "message": "Mobile number not found in the database."}

    email, full_name = user_info[0]

    # Step 2: Fetch password using mobile_no
    password_info = fetch(
        "user_credentials",
        columns=["password"],
        user_name=mobile_no
    )

    if not password_info or not password_info[0]:
        return {"status": "failed", "message": "Password not found for this user."}

    password = password_info[0][0]

    # Step 3: Send email
    if send_password_email(email, full_name, password):
        return {"status": "success", "message": "Password sent to your email."}
    else:
        return {"status": "failed", "message": "Failed to send email. Try again later."}

# Example usage
if __name__ == "__main__":
    result = forgot_password("9976334382")
    print(result)
