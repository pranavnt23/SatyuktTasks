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

def parse_referal_code(referal_code: Optional[str]):
    if not referal_code or referal_code.strip() == "":
        return None, {"message": "Please provide the referal code."}
    try:
        return int(referal_code), None
    except ValueError:
        return None, {"message": "Please provide a valid referal code."}

@app.get("/get_total_area")
def get_total_area(referal_code: Optional[str] = Query(None)):
    code, error = parse_referal_code(referal_code)
    if error:
        return error
    user_ids = get_client_user_ids(code)
    if not user_ids:
        return {"message": "Please provide a valid referal code."}
    data = fetch("polygonStore", columns=["area"], clientID=user_ids)
    total = sum(row[0] for row in data if row[0] is not None)
    return {"total_area": total, "message": "Success"}

@app.get("/get_limit_area")
def get_limit_area(referal_code: Optional[str] = Query(None)):
    code, error = parse_referal_code(referal_code)
    if error:
        return error
    limit_data = fetch("purchase_units", columns=["unit_limit"], clientID=code)
    total = sum(row[0] for row in limit_data if row[0] is not None)
    return {"limit_area": int(total) if total == int(total) else total, "message": "Success"}

@app.get("/get_paid_area")
def get_paid_area(referal_code: Optional[str] = Query(None)):
    code, error = parse_referal_code(referal_code)
    if error:
        return error
    user_ids = get_client_user_ids(code)
    if not user_ids:
        return {"message": "Please provide a valid referal code."}
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID"])
    matching_areas = [
        area for pid, area, cid in polygons
        if cid in user_ids and pid in paid_farm_ids and area is not None
    ]
    return {"paid_area": sum(matching_areas), "message": "Success"}

@app.get("/get_unpaid_area")
def get_unpaid_area(referal_code: Optional[str] = Query(None)):
    code, error = parse_referal_code(referal_code)
    if error:
        return error
    user_ids = get_client_user_ids(code)
    if not user_ids:
        return {"message": "Please provide a valid referal code."}
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID"])
    matching_areas = [
        area for pid, area, cid in polygons
        if cid in user_ids and pid not in paid_farm_ids and area is not None
    ]
    return {"unpaid_area": sum(matching_areas), "message": "Success"}

@app.get("/get_used_area")
def get_used_area(referal_code: Optional[str] = Query(None)):
    code, error = parse_referal_code(referal_code)
    if error:
        return error
    used_data = fetch("purchase_units", columns=["used_area"], clientID=code)
    total = sum(row[0] for row in used_data if row[0] is not None)
    return {"used_area": int(total) if total == int(total) else total, "message": "Success"}

@app.get("/get_available_area")
def get_available_area(referal_code: Optional[str] = Query(None)):
    code, error = parse_referal_code(referal_code)
    if error:
        return error
    limit = get_limit_area(referal_code)["limit_area"]
    used = get_used_area(referal_code)["used_area"]
    return {"available_area": limit - used, "message": "Success"}

@app.get("/inactive_unlocked_area")
def get_inactive_unlocked_area(referal_code: Optional[str] = Query(None)):
    code, error = parse_referal_code(referal_code)
    if error:
        return error
    user_ids = get_client_user_ids(code)
    if not user_ids:
        return {"message": "Please provide a valid referal code."}
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID", "active"])
    matching_areas = [
        area for pid, area, cid, active in polygons
        if cid in user_ids and active == 0 and pid in paid_farm_ids and area is not None
    ]
    return {"inactive_unlocked_area": sum(matching_areas), "message": "Success"}

@app.get("/inactive_locked_area")
def get_inactive_locked_area(referal_code: Optional[str] = Query(None)):
    code, error = parse_referal_code(referal_code)
    if error:
        return error
    user_ids = get_client_user_ids(code)
    if not user_ids:
        return {"message": "Please provide a valid referal code."}
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID", "active"])
    matching_areas = [
        area for pid, area, cid, active in polygons
        if cid in user_ids and active == 0 and pid not in paid_farm_ids and area is not None
    ]
    return {"inactive_locked_area": sum(matching_areas), "message": "Success"}

@app.get("/active_unlocked_area")
def get_active_unlocked_area(referal_code: Optional[str] = Query(None)):
    code, error = parse_referal_code(referal_code)
    if error:
        return error
    user_ids = get_client_user_ids(code)
    if not user_ids:
        return {"message": "Please provide a valid referal code."}
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID", "active"])
    matching_areas = [
        area for pid, area, cid, active in polygons
        if cid in user_ids and active == 1 and pid in paid_farm_ids and area is not None
    ]
    return {"active_unlocked_area": sum(matching_areas), "message": "Success"}

@app.get("/active_locked_area")
def get_active_locked_area(referal_code: Optional[str] = Query(None)):
    code, error = parse_referal_code(referal_code)
    if error:
        return error
    user_ids = get_client_user_ids(code)
    if not user_ids:
        return {"message": "Please provide a valid referal code."}
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID", "active"])
    matching_areas = [
        area for pid, area, cid, active in polygons
        if cid in user_ids and active == 1 and pid not in paid_farm_ids and area is not None
    ]
    return {"active_locked_area": sum(matching_areas), "message": "Success"}