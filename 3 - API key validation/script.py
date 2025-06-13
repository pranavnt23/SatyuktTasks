from db_pro import fetch, exists
from encryptdecrypt import decrypt_info

import pymysql

def get_unlocked_area(user_id):
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if isinstance(row, (list, tuple)) and row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID", "active"], clientID=user_id)
    # Defensive: ensure polygons is a list/tuple
    if not isinstance(polygons, (list, tuple)):
        return 0
    unlocked_area = sum(
        area for pid, area, cid, active in polygons
        if pid in paid_farm_ids and area is not None
    )
    return unlocked_area

def get_locked_area(user_id):
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if isinstance(row, (list, tuple)) and row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID", "active"], clientID=user_id)
    if not isinstance(polygons, (list, tuple)):
        return 0
    locked_area = sum(
        area for pid, area, cid, active in polygons
        if active == 1 and pid not in paid_farm_ids and area is not None
    )
    return locked_area

import pymysql

def count_farms_by_user(user_id):
    if not user_id:
        return 0
    try:
        connection = pymysql.connect(
            host="dev.satyukt.com",
            user="dev_read_sat2farm",
            password="Devread@123",
            db="dummy_api"
        )
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM polygonStore WHERE clientID = %s and active = 1"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                if result:
                    return result[0]
    except Exception as e:
        print(f"Error counting farms: {e}")
    return 0


def count_farmers_under_ref(ref_code):
    farmer_count = 0
    try:
        connection = pymysql.connect(
            host="dev.satyukt.com",
            user="dev_read_sat2farm",
            password="Devread@123",
            db="dummy_api"
        )
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM user_details WHERE referal_code = %s"
                cursor.execute(sql, (ref_code,))
                result = cursor.fetchone()
                if result:
                    farmer_count = result[0]
    except Exception as e:
        print(f"Error fetching farmer count: {e}")
        farmer_count = 0

    return farmer_count


def disp_admin_details(userID):
    subad_details = fetch("user_details", ["mobile_no", "full_name"], referal_code=userID)
    data = []

    for mob, name in subad_details:
        
        idd_result = fetch("user_credentials", ["user_id"], user_name=mob)
        subadmin_user_id = idd_result[0][0] if idd_result and isinstance(idd_result[0], tuple) else None

        # Count farmers referred by this subadmin's user_id
        if subadmin_user_id:
            farmer_count = count_farmers_under_ref(subadmin_user_id)
        else:
            farmer_count = 0

        data.append({
            "Mobile_no": mob,
            "Name": name,
            "No of farmers": farmer_count,
            "User_id": subadmin_user_id
        })

    result = {"data": data, "status": "Success"}
    print(result)
    return result


def disp_subadmin_details(userID):
    farm_details = fetch("user_details", ["full_name", "registration_date", "mobile_no", "referal_code"], referal_code=userID)
    data = []

    for name, reg_date, mob, ref_code in farm_details:
        # Get the farmer's user_id from user_credentials using mobile_no
        user_id_result = fetch("user_credentials", ["user_id"], user_name=mob)
        user_id = user_id_result[0][0] if user_id_result and isinstance(user_id_result[0], tuple) else None


        area = get_unlocked_area(user_id) 
        locked_area = get_locked_area(user_id)  
        no_of_farms = count_farms_by_user(user_id)

        data.append({
            "date_of_registration": reg_date,
            "farmer_name": name,
            "lock_area": locked_area,
            "mobile_no": mob,
            "no_of_farms": no_of_farms,
            "referral_code": ref_code,
            "unlock_area": area
        })

    result = {"data": data, "status": "Success"}
    print(result)
    return result


def check_user(api_key: str):
    try:
        chec = exists("user_credentials", api_key=api_key)
    except Exception as e:
        print({"status": 0, "message": f"Invalid API key: {str(e)}"})
        return

    dec_result = decrypt_info(api_key)
    # Check if dec_result is a tuple/list of length 3
    if not isinstance(dec_result, (list, tuple)) or len(dec_result) != 3:
        print({"status": 0, "message": "Decryption failed or invalid key"})
        return

    mobile_no, password, userID = dec_result
    adm = fetch("user_credentials", ["isAdmin", "subAdmin"], user_id=userID)
    if not adm or isinstance(adm[0], int):
        print({"message": "provided key does not correspond to any Admin", "status": "Failure"})
        return

    is_admin = adm[0][0]
    is_subadmin = adm[0][1]
    if is_admin == 1:
        disp_admin_details(userID)
    else:
        disp_subadmin_details(userID)

# Admin
check_user("kxF_3Oy6P4_HVNkCa9Rzot3ZLibWkcJdrRQORJ81GLs=")

# Subadmin
#check_user("jOU6Ky599r8Kb2bF9UFRQ9t4Dlu7gU0UxsUayGoiax0=")