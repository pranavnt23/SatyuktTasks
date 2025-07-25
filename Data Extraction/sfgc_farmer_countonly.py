import csv  
import os
from datetime import datetime
from db_pro import fetch

def export_sf_gc_farmer_stats_optimized():
    user_id_rows = fetch("userID_to_accountID", columns=["user_id"], account_id=6004)
    user_ids = {str(row[0]) for row in user_id_rows if row and row[0]}

    credentials = fetch("user_credentials", columns=["user_id", "user_name"])
    cred_map = {str(row[0]): row[1] for row in credentials if row and row[0] and str(row[0]) in user_ids}

    user_details = fetch("user_details", columns=["mobile_no", "registration_date", "full_name"])
    details_map = {row[0]: (row[1], row[2]) for row in user_details}

    polygon_rows = fetch("polygonStore", columns=["id", "area", "clientID"])
    farms_by_client = {}
    for pid, area, client_id in polygon_rows:
        client_id_str = str(client_id)
        farms_by_client.setdefault(client_id_str, []).append(pid)

    paid_farm_rows = fetch("paymentGateway", columns=["farm_id"])
    paid_farm_ids = {row[0] for row in paid_farm_rows if row and row[0]}

    csv_data = [["Date of Registration", "Farmer Name", "Mobile Number", "Farms Added", "Paid Farms", "Unpaid Farms"]]

    for uid_str, mobile_no in cred_map.items():
        reg_date, full_name = details_map.get(mobile_no, ("N/A", "N/A"))
        farm_ids = farms_by_client.get(uid_str, [])

        paid_count = sum(1 for fid in farm_ids if fid in paid_farm_ids)
        unpaid_count = len(farm_ids) - paid_count

        csv_data.append([reg_date, full_name, mobile_no, len(farm_ids), paid_count, unpaid_count])

    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = os.path.join(downloads_dir, f"SFGC_Farmer_Stats_CountOnly_{timestamp}.csv")

    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

    print(f"CSV exported to: {file_path}")

if __name__ == "__main__":
    export_sf_gc_farmer_stats_optimized()
