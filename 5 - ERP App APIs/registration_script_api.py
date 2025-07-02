from fastapi import FastAPI, HTTPException
from pydantic import EmailStr
from db_erp import insert, exists, fetch, update
from encryptdecrypt import encrypt
from datetime import datetime

app = FastAPI()

@app.post("/register")
def register_user(
    full_name: str,
    email: EmailStr,        
    mobile_no: str,
    password: str,
    country_code: int = 91,
    category: str = "general"
):
    # 1. Check if mobile or email already exists
    if exists("user_registration", mobile_no=mobile_no):
        raise HTTPException(status_code=400, detail="Mobile number already exists.")
    if exists("user_registration", email=email):
        raise HTTPException(status_code=400, detail="Email already exists.")

    # 2. Insert user registration data
    result = insert(
        "user_registration",
        full_name=full_name,
        email=email,
        mobile_no=mobile_no,
        country_code=country_code,
    )
    if result[0][0] != 1:
        raise HTTPException(status_code=500, detail=result[0][1])

    # 3. Insert into credentials (without api_key)
    cred_result = insert(
        "user_credentials",
        user_name=mobile_no,
        password=password,
    )
    if cred_result[0][0] != 1:
        raise HTTPException(status_code=500, detail="Credentials insertion failed.")

    # 4. Fetch user_id
    user_data = fetch("user_credentials", columns=["user_id"], user_name=mobile_no)
    if not user_data or not user_data[0]:
        raise HTTPException(status_code=500, detail="Could not retrieve user_id.")
    
    user_id = str(user_data[0][0]).zfill(4)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    api_key = encrypt(user_id, str(mobile_no), timestamp)

    # 5. Update credentials with API key
    update_result = update("user_credentials", {"user_id": user_id}, api_key=api_key)

    # 6. Insert category and account info
    category_result = insert(
        "user_category_accountID",
        userID=user_id,
        accountID=1000,
        category=category
    )

    if update_result[0][0] == 1 and category_result[0][0] == 1:
        return {"status": "success", "message": "User fully registered."}
    else:
        raise HTTPException(status_code=500, detail="API key or category insertion failed.")
