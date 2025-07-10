import csv
import os
from db_pro import fetch

# Step 1: Get all user_ids under account_id 6004
user_id_rows = fetch("userID_to_accountID", columns=["user_id"], account_id=6004)
user_ids = [row[0] for row in user_id_rows if isinstance(row, (list, tuple))]

# Step 2: Fetch mobile numbers from user_credentials
user_mobiles = []
for uid in user_ids:
    cred = fetch("user_credentials", columns=["user_name"], user_id=uid)
    if cred and cred[0] and cred[0][0]:
        user_mobiles.append((uid, cred[0][0]))  # (user_id, mobile_no)

# Step 3: Fetch polygon (farm) and payment info
polygon_rows = fetch("polygonStore", columns=["id", "area", "clientID"])
paid_farm_rows = fetch("paymentGateway", columns=["farm_id"])
paid_farm_ids = set(row[0] for row in paid_farm_rows if row[0])

# Step 4: Prepare CSV header
csv_data = [["Date of Registration", "Farmer Name", "Mobile Number", "Farms Added", "Paid Farms", "Unpaid Farms"]]

# Step 5: Loop through each user and populate data
for uid, mobile_no in user_mobiles:
    user_info = fetch("user_details", columns=["registration_date", "full_name", "mobile_no"], mobile_no=mobile_no)
    if user_info and user_info[0]:
        registration_date, full_name, number = user_info[0]
    else:
        registration_date, full_name, number = "N/A", "N/A", "N/A"

    uid_str = str(uid)

    # Filter farms belonging to the user
    farms = [row for row in polygon_rows if str(row[2]) == uid_str]
    farm_ids = [row[0] for row in farms]

    # Count paid and unpaid farms
    paid_count = sum(1 for fid in farm_ids if fid in paid_farm_ids)
    unpaid_count = len(farm_ids) - paid_count

    csv_data.append([registration_date, full_name, number, len(farms), paid_count, unpaid_count])

# Step 6: Write CSV to Downloads
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(downloads_dir, exist_ok=True)
file_path = os.path.join(downloads_dir, "SFGC_Farmer_Stats_CountOnly.csv")

with open(file_path, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

print(f"✅ CSV exported to: {file_path}")
