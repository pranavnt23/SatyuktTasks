from fastapi import FastAPI, Query
from typing import Optional
from db_pro import fetch

app = FastAPI()

def get_client_user_ids(referal_code: int):
    mobile_nos = fetch("user_details", columns=["mobile_no"], referal_code=referal_code)
    mobile_nos = [row[0] for row in mobile_nos if row[0] is not None]
    if not mobile_nos:
        return []
    user_ids_data = fetch("user_credentials", columns=["user_id"], user_name=mobile_nos)
    user_ids = [row[0] for row in user_ids_data if row[0] is not None]
    return user_ids

def get_total_area(referal_code: int):
    user_ids = get_client_user_ids(referal_code)
    if not user_ids:
        return 0
    data = fetch("polygonStore", columns=["area"], clientID=user_ids)
    return sum(row[0] for row in data if row[0] is not None)

def get_limit_area(referal_code: int):
    limit_data = fetch("purchase_units", columns=["unit_limit"], clientID=referal_code)
    total = sum(row[0] for row in limit_data if row[0] is not None)
    return int(total) if total == int(total) else total

def get_paid_area(referal_code: int):
    user_ids = get_client_user_ids(referal_code)
    if not user_ids:
        return 0
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID"])
    matching_areas = [
        area for pid, area, cid in polygons
        if cid in user_ids and pid in paid_farm_ids and area is not None
    ]
    return sum(matching_areas)

def get_unpaid_area(referal_code: int):
    user_ids = get_client_user_ids(referal_code)
    if not user_ids:
        return 0
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID"])
    matching_areas = [
        area for pid, area, cid in polygons
        if cid in user_ids and pid not in paid_farm_ids and area is not None
    ]
    return sum(matching_areas)

def get_used_area(referal_code: int):
    used_data = fetch("purchase_units", columns=["used_area"], clientID=referal_code)
    total = sum(row[0] for row in used_data if row[0] is not None)
    return int(total) if total == int(total) else total

def get_available_area(referal_code: int):
    limit = get_limit_area(referal_code)
    used = get_used_area(referal_code)
    return limit - used

def get_inactive_unlocked_area(referal_code: int):
    user_ids = get_client_user_ids(referal_code)
    if not user_ids:
        return 0
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID", "active"])
    matching_areas = [
        area for pid, area, cid, active in polygons
        if cid in user_ids and active == 0 and pid in paid_farm_ids and area is not None
    ]
    return sum(matching_areas)

def get_inactive_locked_area(referal_code: int):
    user_ids = get_client_user_ids(referal_code)
    if not user_ids:
        return 0
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID", "active"])
    matching_areas = [
        area for pid, area, cid, active in polygons
        if cid in user_ids and active == 0 and pid not in paid_farm_ids and area is not None
    ]
    return sum(matching_areas)

@app.get("/disp_details")
def disp_details(referal_code: Optional[str] = Query(None)):
    if not referal_code :
        return {"data": {}, "status": "Enter the referal code"}
    try:
        user_ids = get_client_user_ids(referal_code)
        if not user_ids:
            return {"data": {}, "status": "Error"}

        total_area = get_total_area(referal_code)
        paid_area = get_paid_area(referal_code)
        unpaid_area = get_unpaid_area(referal_code)
        limit_area = get_limit_area(referal_code)
        used_area = get_used_area(referal_code)
        available_area = get_available_area(referal_code)
        inactive_unlocked_area = get_inactive_unlocked_area(referal_code)
        inactive_locked_area = get_inactive_locked_area(referal_code)

        data = {
            "Total area": total_area,
            "Paid area": paid_area,
            "Unpaid area": unpaid_area,
            "Limit area": limit_area,
            "Used area": used_area,
            "Available area": available_area,
            "Inactive Unlocked Area": inactive_unlocked_area,
            "Inactive Locked Area": inactive_locked_area
        }
        return {"data": data, "status": "Success"}
    except Exception:
        return {"data": {}, "status": "Error"}