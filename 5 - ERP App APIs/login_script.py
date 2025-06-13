from db_pro import fetch
import json

def login_user(mobile_no, password):
    # 1. Check if both inputs are present
    if not mobile_no:
        return {"status": "failed", "message": "Mobile number is required."}
    if not password:
        return {"status": "failed", "message": "Password is required."}

    # 2. Validate user credentials
    user_result = fetch(
        "user_credentials",
        columns=["user_id", "api_key"],
        user_name=mobile_no,
        password=password
    )

    if not user_result or not user_result[0]:
        return {"status": "failed", "message": "Invalid mobile number or password."}

    user_id, api_key = user_result[0]

    # 3. Fetch user details from user_registration
    user_info = fetch(
        "user_registration",
        columns=["full_name", "mobile_no"],
        mobile_no=mobile_no
    )

    if not user_info or not user_info[0]:
        return {"status": "failed", "message": "User registration data not found."}

    full_name, mobile = user_info[0]

    # 4. Fetch user category and account ID
    category_info = fetch(
        "user_category_accountID",
        columns=["accountID", "category"],
        userID=str(user_id).zfill(4)
    )

    if not category_info or not category_info[0]:
        return {"status": "failed", "message": "User category data not found."}

    account_id, category = category_info[0]

    # 5. Structure the response
    response = {
        "data": {
            "client_id": str(user_id).zfill(4),
            "acc_id": account_id,
            "full_name": full_name,
            "mobile_no": mobile,
            "category": category,
            "user_key": api_key
        },
        "status": "success"
    }

    return response

# Example usage
if __name__ == "__main__":
    result = login_user(mobile_no="9976334384", password="securepassword123")
    print(json.dumps(result, indent=4))
