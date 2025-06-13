import os
import sys

sys.path.append(r"D:\Intern\Satyukt\SQL n Spider")

from db_pro import fetch  
    
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
    total = sum(row[0] for row in data if row[0] is not None)
    return total

def get_limit_area(referal_code: int):
    limit_data = fetch("purchase_units", columns=["unit_limit"], clientID=referal_code)
    total=sum(row[0] for row in limit_data if row[0] is not None)
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

def get_active_unlocked_area(referal_code: int):
    user_ids = get_client_user_ids(referal_code)
    if not user_ids:
        return 0
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID", "active"])
    matching_areas = [
        area for pid, area, cid, active in polygons
        if cid in user_ids and active == 1 and pid in paid_farm_ids and area is not None
    ]
    return sum(matching_areas)

def get_active_locked_area(referal_code: int):
    user_ids = get_client_user_ids(referal_code)
    if not user_ids:
        return 0
    paid_farms = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = set(row[0] for row in paid_farms if row[0] is not None)
    polygons = fetch("polygonStore", columns=["id", "area", "clientID", "active"])
    matching_areas = [
        area for pid, area, cid, active in polygons
        if cid in user_ids and active == 1 and pid not in paid_farm_ids and area is not None
    ]
    return sum(matching_areas)

if __name__ == "__main__":
    referal_code = 73671
    total_area = get_total_area(referal_code)
    print("Total area:", total_area)
    paid_area = get_paid_area(referal_code)
    print("Paid area:", paid_area)
    unpaid_area = get_unpaid_area(referal_code)
    print("Unpaid area:", unpaid_area)
    limit_area = get_limit_area(referal_code)
    print("Limit area:", limit_area)
    used_area = get_used_area(referal_code)
    print("Used area:", used_area)
    available_area = get_available_area(referal_code)
    print("Available area:", available_area)
    print("Inactive Unlocked Area:", get_inactive_unlocked_area(referal_code))
    print("Inactive Locked Area:", get_inactive_locked_area(referal_code))
    print("Active Unlocked Area:", get_active_unlocked_area(referal_code))
    print("Active Locked Area:", get_active_locked_area(referal_code))
