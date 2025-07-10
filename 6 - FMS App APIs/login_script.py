from db_fms import fetch
import json

def login_user(mobile_no, password):
    # 1. Input validation
    if not mobile_no:
        return {"status": "failed", "message": "Mobile number is required."}
    if not password:
        return {"status": "failed", "message": "Password is required."}

    # 2. Validate credentials
    user_result = fetch(
        "user_credentials",
        columns=["user_id", "api_key"],
        user_name=mobile_no,
        password=password
    )

    if not user_result or not user_result[0]:
        return {"status": "failed", "message": "Invalid mobile number or password."}

    user_id, api_key = user_result[0]

    # 3. Fetch user details from registration table
    user_info = fetch(
        "user_registration",
        columns=["full_name", "mobile_no", "category"],
        mobile_no=mobile_no
    )

    if not user_info or not user_info[0]:
        return {"status": "failed", "message": "User registration details not found."}

    full_name, mobile, category = user_info[0]

    # 4. Final response
    response = {
        "status": "success",
        "data": {
            "client_id": str(user_id).zfill(4),
            "full_name": full_name,
            "mobile_no": mobile,
            "category": category,
            "user_key": api_key
        }
    }

    return response


# Example usage
if __name__ == "__main__":
    result = login_user(mobile_no="9976334382", password="securepassword123")
    print(json.dumps(result, indent=4))
