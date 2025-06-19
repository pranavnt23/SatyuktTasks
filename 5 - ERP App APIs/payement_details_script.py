from db_pro import insert
import json

# Function to insert a payment record
def insert_payment(user_id: int, transaction_id: str, mode_of_payment: str, product_name: str, product_id: int, quantity: int):
    try:
        if not all([user_id, transaction_id, mode_of_payment, product_name, product_id, quantity]):
            return {"status": "failed", "message": "All fields are required."}

        status = insert(
            "payment_details",
            user_id=user_id,
            transaction_id=transaction_id,
            mode_of_payment=mode_of_payment,
            product_name=product_name,
            product_id=product_id,
            quantity=quantity
        )

        if status[0][0] == 1:
            return {"status": "success", "message": "Payment record inserted successfully."}
        else:
            return {"status": "failed", "message": status[0][1]}

    except Exception as e:
        return {"status": "failed", "message": str(e)}

if __name__ == "__main__":
    result = insert_payment(
        user_id=1,
        transaction_id="TXN20240612001",
        mode_of_payment="UPI",
        product_name="Neem Pesticide",
        product_id=1001,
        quantity=3
    )
    print(json.dumps(result, indent=4))
