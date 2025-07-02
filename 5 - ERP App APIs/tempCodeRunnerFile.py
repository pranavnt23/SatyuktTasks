import pymysql
import json
import numpy as np
import reverse_geocoder as rg
from collections import defaultdict
import csv  # NEW: for writing CSV

def get_odisha_farm_referral_users():
    db = pymysql.connect(
        host="3.14.103.172",
        user="readuser",
        password="Secret@123",
        db="dummy_api"
    )
    cursor = db.cursor()

    print("🚀 Fetching farm_ids and polygon data...")
    cursor.execute("""
        SELECT id, polyinfo, clientID
        FROM polygonStore
        WHERE id IN (
            SELECT DISTINCT farm_id FROM paymentGateway WHERE farm_id IS NOT NULL
        );
    """)
    rows = cursor.fetchall()

    coords_to_ids = defaultdict(list)
    farm_id_to_client = {}

    for farm_id, polyinfo_str, client_id in rows:
        try:
            if not polyinfo_str or not polyinfo_str.strip().startswith('{'):
                continue
            polyinfo_json = json.loads(polyinfo_str)

            coords = polyinfo_json['geo_json']['geometry']['coordinates']
            if not coords or not coords[0] or not coords[0][0] or len(coords[0][0]) < 2:
                continue

            lat, lng = coords[0][0][1], coords[0][0][0]
            coords_to_ids[(lat, lng)].append(farm_id)
            farm_id_to_client[farm_id] = client_id

        except Exception:
            continue

    print("🔍 Performing batched reverse geocoding...")
    coord_list = list(coords_to_ids.keys())
    locations = rg.search(coord_list)

    odisha_farm_ids = []
    for idx, loc in enumerate(locations):
        state = loc.get('admin1', '').strip().lower()
        if state == "odisha":
            odisha_farm_ids.extend(coords_to_ids[coord_list[idx]])

    print(f"\n🌾 FARM IDs IN ODISHA ({len(odisha_farm_ids)} found)")

    # NEW: Create a list to collect referral user data
    referral_data = []

    for farm_id in odisha_farm_ids:
        try:
            client_id = farm_id_to_client.get(farm_id)
            if not client_id:
                continue

            cursor.execute("SELECT user_name,user_id FROM user_credentials WHERE user_id = %s", (client_id,))
            user_row = cursor.fetchone()
            if not user_row:
                continue
            user_name = user_row[0]

            cursor.execute("SELECT referal_code FROM user_details WHERE mobile_no = %s", (user_name,))
            ref_row = cursor.fetchone()
            if not ref_row:
                continue

            referal_code = ref_row[0]
            if not referal_code:
                continue

            cursor.execute("""
                SELECT mobile_no, full_name
                FROM user_details
                WHERE referal_code = %s
            """, (referal_code,))
            referred_user = cursor.fetchone()
            if referred_user:
                referred_mobile, referred_name = referred_user

                # Append to referral_data
                referral_data.append([referred_mobile, referred_name])

        except Exception as e:
            print(f"⚠️ Error with farm_id {farm_id}: {e}")
            continue

    db.close()

    # NEW: Write the referral data to a CSV file
    csv_filename = "odisha_referred_users.csv"
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['referred_user_name', 'full_name'])  # Header
        writer.writerows(referral_data)

    print(f"\n✅ Data successfully saved to {csv_filename}")

if __name__ == "__main__":
    get_odisha_farm_referral_users()
