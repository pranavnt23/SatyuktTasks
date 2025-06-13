from db_pro import fetch
import smtplib
from email.mime.text import MIMEText
from pydantic import EmailStr

# Predeclared sender credentials (keep password secure!)
SENDER_GMAIL = "pranavnt239@gmail.com"
SENDER_PASSWORD = "sdgg ohan pozs gtcq"

def send_password_email(to_email, full_name, password):
    subject = "🔐 Password Recovery - Satyukt App"
    body = f"""
    Dear {full_name},

    As requested, here is your account password:

    🔑 Password: {password}

    Please log in and consider changing your password for better security.

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

def forgot_password(user_email: EmailStr):
    # Step 1: Check if user email exists
    user_info = fetch(
        "user_registration",
        columns=["mobile_no", "full_name"],
        email=user_email
    )

    if not user_info or not user_info[0]:
        return {"status": "failed", "message": "Email not found in the database."}

    mobile_no, full_name = user_info[0]

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
    if send_password_email(user_email, full_name, password):
        return {"status": "success", "message": "Password sent to your email."}
    else:
        return {"status": "failed", "message": "Failed to send email. Try again later."}


# Example usage
if __name__ == "__main__":
    result = forgot_password("g49rac.cit.rid3201@gmail.com")
    print(result)
