from fastapi import FastAPI, HTTPException
from db_pro import fetch

app = FastAPI(title="User Login API", version="1.0")

@app.post("/login")
def login_user(mobile_no: str, password: str):
    # 1. Validate required fields
    if not mobile_no:
        raise HTTPException(status_code=400, detail="Mobile number is required.")
    if not password:
        raise HTTPException(status_code=400, detail="Password is required.")

    # 2. Check user credentials
    user_result = fetch(
        "user_credentials",
        columns=["user_id", "api_key"],
        user_name=mobile_no,
        password=password
    )

    if not user_result or not user_result[0]:
        raise HTTPException(status_code=401, detail="Invalid mobile number or password.")

    user_id, api_key = user_result[0]

    # 3. Fetch full name and mobile
    user_info = fetch(
        "user_registration",
        columns=["full_name", "mobile_no"],
        mobile_no=mobile_no
    )

    if not user_info or not user_info[0]:
        raise HTTPException(status_code=404, detail="User registration data not found.")

    full_name, mobile = user_info[0]

    # 4. Fetch category and account ID
    category_info = fetch(
        "user_category_accountID",
        columns=["accountID", "category"],
        userID=str(user_id).zfill(4)
    )

    if not category_info or not category_info[0]:
        raise HTTPException(status_code=404, detail="User category data not found.")

    account_id, category = category_info[0]

    # 5. Final response
    return {
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
