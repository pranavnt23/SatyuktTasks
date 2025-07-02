from fastapi import FastAPI, Form
from db_erp import insert

app = FastAPI(title="💳 Payment Details API")

@app.post("/insert-payment/")
def insert_payment(
    user_id: int = Form(...),
    transaction_id: str = Form(...),
    mode_of_payment: str = Form(...),
    product_name: str = Form(...),
    product_id: int = Form(...),
    quantity: int = Form(...)
):
    try:
        # Insert into DB
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
