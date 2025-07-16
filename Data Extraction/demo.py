import pymysql
import json
import reverse_geocoder as rg
from collections import defaultdict
import csv

def get_guyana_farms_with_sugarcane():
    db = pymysql.connect(
        host="3.14.103.172",
        user="readuser",
        password="Secret@123",
        db="dummy_api"
    )
    cursor = db.cursor()

    print("🚀 Fetching all polygon data (no paymentGateway filter)...")
    cursor.execute("""
        SELECT id, polyinfo, clientID, croptype
        FROM polygonStore
    """)
    rows = cursor.fetchall()

    coords = []
    farm_info_map = {}

    for farm_id, polyinfo_str, client_id, croptype in rows:
        try:
            if not polyinfo_str or not polyinfo_str.strip().startswith('{'):
                continue
            polyinfo_json = json.loads(polyinfo_str)

            coords_raw = polyinfo_json['geo_json']['geometry']['coordinates']
            if not coords_raw or not coords_raw[0][0]:
                continue

            lat, lng = coords_raw[0][0][1], coords_raw[0][0][0]
            coords.append((lat, lng))
            farm_info_map[(lat, lng)] = {
                "farm_id": farm_id,
                "client_id": client_id,
                "croptype": croptype
            }

        except Exception:
            continue

    print("🔍 Performing batched reverse geocoding...")
    locations = rg.search(coords)

    # Bulk fetch user credentials and details
    cursor.execute("SELECT user_id, user_name FROM user_credentials")
    user_cred_map = dict(cursor.fetchall())

    cursor.execute("SELECT mobile_no, full_name, country_code FROM user_details")
    user_detail_map = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

    farm_data = [["Farm ID", "Mobile Number", "Full Name", "Country Code"]]
    sugarcane_data = [["Farm ID", "Mobile Number", "Full Name", "Country Code", "Crop Type"]]

    for idx, loc in enumerate(locations):
        country = loc.get('cc', '').strip().upper()
        if country != "GY":
            continue  # skip non-Guyana

        coord = coords[idx]
        farm_info = farm_info_map.get(coord)
        if not farm_info:
            continue

        farm_id = farm_info["farm_id"]
        client_id = farm_info["client_id"]
        croptype = farm_info["croptype"] or ""

        mobile_no = user_cred_map.get(client_id)
        if not mobile_no:
            continue

        user_detail = user_detail_map.get(mobile_no)
        if not user_detail:
            continue

        full_name, country_code = user_detail

        farm_data.append([farm_id, mobile_no, full_name, country_code])

        if 'sugarcane' in croptype.lower():
            sugarcane_data.append([farm_id, mobile_no, full_name, country_code, croptype])

    db.close()

    # Save CSVs
    with open("guyana_farms.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(farm_data)

    with open("guyana_sugarcane_farms.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(sugarcane_data)

    print("\n✅ All Guyana farms saved to guyana_farms.csv")
    print("✅ Sugarcane farms in Guyana saved to guyana_sugarcane_farms.csv")

if __name__ == "__main__":
    get_guyana_farms_with_sugarcane()
