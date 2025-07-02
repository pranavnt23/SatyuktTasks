import pymysql
import json
import numpy as np
import reverse_geocoder as rg
from collections import defaultdict

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

    print("\n🎯 REFERRED USERS OF ODISHA FARM OWNERS:\n")

    for farm_id in odisha_farm_ids:
        try:
            client_id = farm_id_to_client.get(farm_id)
            if not client_id:
                continue

            # Step 1: Get user_name (mobile number) from credentials
            cursor.execute("SELECT user_name,user_id FROM user_credentials WHERE user_id = %s", (client_id,))
            user_row = cursor.fetchone()
            if not user_row:
                continue
            user_name = user_row[0]
            user_id = user_row[1]

            # Step 2: Get referal_code from user_details
            cursor.execute("SELECT referal_code FROM user_details WHERE mobile_no = %s", (user_name,))
            ref_row = cursor.fetchone()
            if not ref_row:
                continue

            referal_code = ref_row[0]
            if not referal_code:
                continue

            # Step 3: Fetch referred user's info using referal_code
            cursor.execute("""
                SELECT mobile_no, full_name, area
                FROM user_details
                WHERE referal_code = %s
            """, (referal_code,))
            referred_user = cursor.fetchone()
            if referred_user:
                referred_mobile, referred_name, referred_area = referred_user

                # 🌟 STRUCTURED OUTPUT
                print(f"farm_id: {farm_id}")
                print(f"→ user_id: {user_id}")
                print(f"→ referred_user_name: {referred_mobile}")
                print(f"→ full_name: {referred_name}")
                print(f"→ area: {referred_area}")
                print("--------------------------------------------------")

        except Exception as e:
            print(f"⚠️ Error with farm_id {farm_id}: {e}")
            continue

    db.close()

if __name__ == "__main__":
    get_odisha_farm_referral_users()
