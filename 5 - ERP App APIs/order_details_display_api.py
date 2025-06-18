from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from db_pro import fetch
from encryptdecrypt import decrypt_info

from datetime import datetime

app = FastAPI(title="Order Details API")

# Response model for order details
class Order(BaseModel):
    order_id: int
    product_name: str
    quantity: int
    amount: float
    order_placed_date: str  # ISO format as string
    dispatch_address: str
    order_status: str

class OrderResponse(BaseModel):
    status: str
    data: List[Order]
    message: str | None = None

@app.get("/user/orders", response_model=OrderResponse)
def get_user_orders(user_key: str):
    try:
        # 🔓 Step 1: Decrypt user key
        decrypted = decrypt_info(user_key)
        if not decrypted or len(decrypted) == 0:
            raise HTTPException(status_code=400, detail="Invalid user key.")

        user_id = decrypted[0]  # Assume user_id is first element

        # 📦 Step 2: Fetch orders
        orders = fetch(
            "order_details",
            columns=[
                "order_id", "product_name", "quantity", "amount",
                "order_placed_date", "dispatch_address", "order_status"
            ],
            user_id=user_id
        )

        # 🪄 Step 3: Structure response
        if not orders:
            return OrderResponse(status="success", data=[], message="No orders found.")

        order_list = []
        for order in orders:
            order_list.append(Order(
                order_id=order[0],
                product_name=order[1],
                quantity=order[2],
                amount=float(order[3]),
                order_placed_date=str(order[4]),
                dispatch_address=order[5],
                order_status=order[6]
            ))

        return OrderResponse(status="success", data=order_list)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")
