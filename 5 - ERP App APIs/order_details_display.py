from db_erp import fetch, insert, update
from encryptdecrypt import decrypt_info
import json
from datetime import datetime

def get_user_orders(user_key: str):
    try:
        decrypted = decrypt_info(user_key)
        if not decrypted or len(decrypted) == 0:
            return {"status": "failed", "message": "Invalid user key."}
        
        user_id = decrypted[0]

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

        order_list = [{
            "order_id": order[0],
            "product_name": order[1],
            "quantity": order[2],
            "amount": float(order[3]),
            "order_placed_date": str(order[4]),
            "dispatch_address": order[5],
            "order_status": order[6]
        } for order in orders]

        return {"status": "success", "data": order_list}

    except Exception as e:
        return {"status": "failed", "message": str(e)}


def insert_order(product_name: str, quantity: int, price: float, user_id: int, dispatch_address: str, status: str = 'dispatched'):
    try:
        product_info = fetch(
            "stock_details",
            columns=["product_id", "quantity_available"],
            product_name=product_name
        )

        if not product_info:
            return {"status": "failed", "message": f"Product '{product_name}' not found."}

        print(product_info)
        product_id, available_qty = product_info[0]
        print(available_qty)
        
        if quantity > available_qty:
            return {"status": "failed", "message": f"Only {available_qty} units available. Cannot place order."}

        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        status_insert = insert(
            "order_details",
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            amount=price,
            user_id=user_id,
            dispatch_address=dispatch_address,
            order_status=status
        )

        if status_insert[0][0] == 1:
            # Reduce the quantity in product_details
            new_qty = available_qty - quantity
            update("stock_details", {"product_id": product_id}, quantity_available=new_qty)

            return {"status": "success", "message": "Order placed successfully."}
        else:
            return {"status": "failed", "message": status_insert[0][1]}

    except Exception as e:
        return {"status": "failed", "message": str(e)}


if __name__ == "__main__":
    result = insert_order(
        product_name="Neem Pesticide",
        quantity=5,
        price=500.0,
        user_id=123,
        dispatch_address="1234 Elm Street, Example City"
    )
    print(json.dumps(result, indent=4))
