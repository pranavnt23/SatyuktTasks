from datetime import datetime
from db_erp import insert, exists, fetch, update
from encryptdecrypt import encrypt

def register_user(full_name=None, email=None, mobile_no=None, password=None, country_code=91, category="general"):
    # Check for required arguments
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
   

    # 1. Check if mobile or email already exists
    if exists("user_registration", mobile_no=mobile_no):
        return {"status": "failed", "message": "Mobile number already exists."}
    if exists("user_registration", email=email):
        return {"status": "failed", "message": "Email already exists."}

    # 2. Insert into user_registration
    result = insert(
        "user_registration",
        full_name=full_name,
        email=email,
        mobile_no=mobile_no,
        country_code=country_code,
    )
    if result[0][0] != 1:
        return {"status": "failed", "message": result[0][1]}

    # 3. Insert into user_credentials with mobile_no and password only (no api_key yet)
    cred_result = insert(
        "user_credentials",
        user_name=mobile_no,
        password=password,
    )
    if cred_result[0][0] != 1:
        return {"status": "failed", "message": "User created, but credentials insertion failed."}

    # 4. Fetch the user_id of the just-inserted user
    user_data = fetch(
        "user_credentials",
        columns=["user_id"],
        user_name=mobile_no
    )
    if not user_data or not user_data[0]:
        return {"status": "failed", "message": "Could not retrieve user_id after credentials insert."}

    user_id = str(user_data[0][0]).zfill(4)  # <-- Pad to 4 digits
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    api_key = encrypt(user_id, str(mobile_no), timestamp)

    # 5. Update the same user_credentials row with the generated api_key
    update_result = update(
        "user_credentials",
        {"user_id": user_id},  # conditions
        api_key=api_key        # columns to update
    )

    # 6. Insert into user_category_accountID table
    category_result = insert(
        "user_category_accountID",
        userID=user_id,
        accountID=1000,
        category=category
    )

    if update_result[0][0] == 1 and category_result[0][0] == 1:
        return {"status": "success", "message": "User fully registered with API key and category assigned."}
    else:
        return {"status": "failed", "message": "User created, but issue in API key update or category insert."}


# Example usage
if __name__ == "__main__":
    response = register_user(
        full_name="Test User",
        email="g49rac.cit.rid3201@gmail.com",
        mobile_no=9976334382,
        country_code=91,
        password="securepassword123",
        category="farmer"  # You can customize this value
    )
    print(response)
