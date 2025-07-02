from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db_erp import fetch
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# Secure your credentials in environment variables or secrets in production
SENDER_GMAIL = "pranavnt239@gmail.com"
SENDER_PASSWORD = "sdgg ohan pozs gtcq"

# Request model
class ForgotPasswordRequest(BaseModel):
    mobile_no: str

# Email function
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

# FastAPI route
@app.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    mobile_no = request.mobile_no

    # Step 1: Fetch user details
    user_info = fetch(
        "user_registration",
        columns=["email", "full_name"],
        mobile_no=mobile_no
    )

    if not user_info or not user_info[0]:
        raise HTTPException(status_code=404, detail="Mobile number not found in the database.")

    email, full_name = user_info[0]

    # Step 2: Fetch password
    password_info = fetch(
        "user_credentials",
        columns=["password"],
        user_name=mobile_no
    )

    if not password_info or not password_info[0]:
        raise HTTPException(status_code=404, detail="Password not found for this user.")

    password = password_info[0][0]

    # Step 3: Send email
    if send_password_email(email, full_name, password):
        return {"status": "success", "message": "Password sent to your registered email."}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email. Try again later.")
