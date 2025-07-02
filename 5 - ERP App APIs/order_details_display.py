from db_erp import fetch
from encryptdecrypt import decrypt_info
import json

def get_user_orders(user_key: str):
    try:
        # Step 1: Decrypt user_key to get user_id
        decrypted = decrypt_info(user_key)
        if not decrypted or len(decrypted) == 0:
            return {"status": "failed", "message": "Invalid user key."}
        
        user_id = decrypted[0]  # Assuming user_id is the first element

        # Step 2: Fetch order details using user_id
        orders = fetch(
            "order_details",
            columns=[
                "order_id", "product_name", "quantity", "amount",
                "order_placed_date", "dispatch_address", "order_status"
            ],
            user_id=user_id
        )

        if not orders:
            return {"status": "success", "data": [], "message": "No orders found."}

        # Step 3: Structure response
        order_list = []
        for order in orders:
            order_dict = {
                "order_id": order[0],
                "product_name": order[1],
                "quantity": order[2],
                "amount": float(order[3]),
                "order_placed_date": str(order[4]),
                "dispatch_address": order[5],
                "order_status": order[6]
            }
            order_list.append(order_dict)

        return {
            "status": "success",
            "data": order_list
        }

    except Exception as e:
        return {"status": "failed", "message": str(e)}

if __name__ == "__main__":
    user_key_input = "6a2Q1oUVEK4UwGm-52coymEo5TBa4MPkkr51W7ykHC8="
    result = get_user_orders(user_key_input)
    print(json.dumps(result, indent=4))
