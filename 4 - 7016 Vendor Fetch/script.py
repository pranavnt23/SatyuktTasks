from db_pro import fetch, exists
import json

columns = [
    "clientID", "businessType", "agriProductSales", "agricultureServices",
    "PANDetails", "GSTNDetails", "firmName", "firmAddress", "identityProof",
    "bankDetails", "shopPicture", "licence", "license_img", "aadhar_img",
    "country", "state", "district", "locality", "pinCode", "storeNo",
    "profile_status"
]

def row_to_dict(columns, row):
    return {column: value for column, value in zip(columns, row)}

def get_all_vendor_profiles():
    # Step 1: Fetch all vendor registrations
    vendor_rows = fetch("7016_vendor_registration", columns=columns)
    if not vendor_rows:
        return {
            "status": "Failed",
            "detail": "No vendor data found.",
            "status_code": 404
        }

    vendor_profiles = []

    for row in vendor_rows:
        if not isinstance(row, (list, tuple)):
            continue

        vendor_data = row_to_dict(columns, row)
        client_id = vendor_data.get("clientID")

        # STEP 5: Check payment status like you asked
        pay = exists("7016_vendor_payment", clientID=client_id)

        # STEP 6: Get user_name
        user_name_data = fetch("user_credentials", ["user_name"], user_id=client_id)
        user_name = user_name_data[0][0] if user_name_data and isinstance(user_name_data[0], (list, tuple)) else ""

        # STEP 7: Get full_name & email
        full_name = ""
        email = ""
        if user_name:
            user_details_data = fetch("user_details", ["full_name", "email"], mobile_no=user_name)
            if user_details_data and isinstance(user_details_data[0], (list, tuple)):
                full_name = user_details_data[0][0]
                email = user_details_data[0][1]

        # STEP 8: Build full profile
        profile = {
            "GSTNDetails": vendor_data.get("GSTNDetails", ""),
            "PANDetails": vendor_data.get("PANDetails", ""),
            "aadhar_img": f"https://micro.satyukt.com/vendor_profile_img/{client_id}/adhar.png",
            "agriProductSales": vendor_data.get("agriProductSales", ""),
            "agricultureServices": vendor_data.get("agricultureServices", ""),
            "bankDetails": vendor_data.get("bankDetails", ""),
            "businessType": vendor_data.get("businessType", ""),
            "clientID": client_id,
            "country": vendor_data.get("country", ""),
            "district": vendor_data.get("district", ""),
            "email": email,
            "firmAddress": vendor_data.get("firmAddress", ""),
            "firmName": vendor_data.get("firmName", ""),
            "full_name": full_name,
            "identityProof": vendor_data.get("identityProof", ""),
            "licence": vendor_data.get("licence", ""),
            "license_img": f"https://micro.satyukt.com/vendor_profile_img/{client_id}/licence.png",
            "locality": vendor_data.get("locality", ""),
            "payment_status": pay,
            "pinCode": vendor_data.get("pinCode", ""),
            "shopPicture": vendor_data.get("shopPicture", ""),
            "state": vendor_data.get("state", ""),
            "storeNo": vendor_data.get("storeNo", ""),
            "profile_status": vendor_data.get("profile_status", ""),
            "user_name": user_name,
            "vendor_documents": {
                "aadhar": f"https://micro.satyukt.com/vendor_profile_img/{client_id}/adhar.png",
                "license": f"https://micro.satyukt.com/vendor_profile_img/{client_id}/licence.png"
            }
        }

        vendor_profiles.append(profile)

    return {
        "status": "Success",
        "total_vendors": len(vendor_profiles),
        "vendors": vendor_profiles
    }

# TESTING
if __name__ == "__main__":
    result = get_all_vendor_profiles()
    print(json.dumps(result, indent=2))
