from db_erp import insert, fetch
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


# ✅ Function to display all payment details
def display_all_payment_details():
    try:
        payments = fetch("payment_details")
        if not payments:
            return {"status": "success", "data": [], "message": "No payment records found."}

        payment_list = []
        for payment in payments:
            payment_list.append(payment)

        return {"status": "success", "data": payment_list}

    except Exception as e:
        return {"status": "failed", "message": str(e)}


if __name__ == "__main__":
    # Insert a payment record
    """insert_result = insert_payment(
        user_id=1,
        transaction_id="TXN20240612001",
        mode_of_payment="UPI",
        product_name="Neem Pesticide",
        product_id=1001,
        quantity=3
    )
    print("INSERT PAYMENT RESULT:")
    print(json.dumps(insert_result, indent=4))"""

    # Display all payment records
    display_result = display_all_payment_details()
    print("\nALL PAYMENT DETAILS:")
    print(json.dumps(display_result, indent=4))
