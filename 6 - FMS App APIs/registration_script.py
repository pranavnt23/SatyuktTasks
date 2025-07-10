from datetime import datetime
from db_fms import insert, exists, fetch, update
from encryptdecrypt import encrypt

def register_user(full_name=None, email=None, mobile_no=None, password=None, country_code=91, category="Retailer"):
    if not full_name:
        return {
        "status": "failed",
        "message": "Full name is required."
    }
    if not email:
        return {
        "status": "failed",
        "message": "Email is required."
    }
    if not mobile_no:
        return {
        "status": "failed",
        "message": "Mobile number is required."
    }
    if not password:
        return {
        "status": "failed",
        "message": "Password is required."
    }
   

    if exists("user_registration", mobile_no=mobile_no):
        return {"status": "failed", "message": "Mobile number already exists."}
    if exists("user_registration", email=email):
        return {"status": "failed", "message": "Email already exists."}

    result = insert(
        "user_registration",
        full_name=full_name,
        email=email,
        mobile_no=mobile_no,
        country_code=country_code,
        category=category
    )
    if result[0][0] != 1:
        return {"status": "failed", "message": result[0][1]}

    cred_result = insert(
        "user_credentials",
        user_name=mobile_no,
        password=password,
    )
    if cred_result[0][0] != 1:
        return {"status": "failed", "message": "User created, but credentials insertion failed."}

    user_data = fetch(
        "user_credentials",
        columns=["user_id"],
        user_name=mobile_no
    )
    if not user_data or not user_data[0]:
        return {"status": "failed", "message": "Could not retrieve user_id after credentials insert."}

    user_id = str(user_data[0][0]).zfill(4)  
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    api_key = encrypt(user_id, str(mobile_no), timestamp)

    
    update_result = update(
        "user_credentials",
        {"user_id": user_id},  
        api_key=api_key        
    )

    if update_result[0][0] == 1:
        return {"status": "success", "message": "User fully registered with API key."}
    else:
        return {"status": "failed", "message": "User created, but issue exists in API key update."}


if __name__ == "__main__":
    response = register_user(
        full_name="Test User2",
        email="g49rac.cit.rid3201@gmail.com",
        mobile_no=9976334383,
        country_code=91,
        password="securepassword123",
        category="Seller"  
    )
    print(response)
