import pymysql
import json
import reverse_geocoder as rg
from collections import defaultdict
import csv

def get_non_india_farms_with_sugarcane():
    db = pymysql.connect(
        host="3.14.103.172",
        user="readuser",
        password="Secret@123",
        db="dummy_api"
    )
    cursor = db.cursor()

    print("🚀 Bulk fetching ALL polygon data (NO paymentGateway filter)...")
    cursor.execute("""
        SELECT id, polyinfo, clientID, croptype
        FROM polygonStore
    """)
    polygon_rows = cursor.fetchall()

    coords = []
    farm_details = {}
    for farm_id, polyinfo_str, client_id, croptype in polygon_rows:
        try:
            if not polyinfo_str or not polyinfo_str.strip().startswith('{'):
                continue
            polyinfo = json.loads(polyinfo_str)
            lat, lng = polyinfo['geo_json']['geometry']['coordinates'][0][0][1], polyinfo['geo_json']['geometry']['coordinates'][0][0][0]
            coords.append((lat, lng))
            farm_details[(lat, lng)] = {
                "farm_id": farm_id,
                "client_id": client_id,
                "croptype": croptype
            }
        except Exception:
            continue

    print("🌍 Performing batched reverse geocoding...")
    locations = rg.search(coords)

    # Bulk fetch user_credentials
    cursor.execute("SELECT user_id, user_name FROM user_credentials")
    user_cred_map = dict(cursor.fetchall())

    # Bulk fetch user_details
    cursor.execute("SELECT mobile_no, full_name, country_code FROM user_details")
    user_detail_map = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

    farm_data = [["Farm ID", "Mobile Number", "Full Name", "Country Code"]]
    sugarcane_data = [["Farm ID", "Mobile Number", "Full Name", "Country Code", "Crop Type"]]

    for idx, loc in enumerate(locations):
        if loc['cc'] == 'IN':
            continue  # Skip India

        coord = coords[idx]
        farm_info = farm_details.get(coord)
        if not farm_info:
            continue

        farm_id = farm_info['farm_id']
        client_id = farm_info['client_id']
        croptype = (farm_info['croptype'] or '').lower()

        mobile_no = user_cred_map.get(client_id)
        if not mobile_no:
            continue

        user_detail = user_detail_map.get(mobile_no)
        if not user_detail:
            continue

        full_name, country_code = user_detail

        farm_data.append([farm_id, mobile_no, full_name, country_code])

        # Include sugarcane, exclude sugarcane_ratoon
        if 'sugarcane' in croptype and 'ratoon' not in croptype:
            sugarcane_data.append([farm_id, mobile_no, full_name, country_code, farm_info['croptype']])

    db.close()

    with open("non_india_farms.csv", mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(farm_data)

    with open("non_india_sugarcane_farms.csv", mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(sugarcane_data)

    print(f"\n✅ All Non-India farms saved to non_india_farms.csv")
    print(f"✅ Non-India sugarcane (excluding ratoon) farms saved to non_india_sugarcane_farms.csv")

if __name__ == "__main__":
    get_non_india_farms_with_sugarcane()
