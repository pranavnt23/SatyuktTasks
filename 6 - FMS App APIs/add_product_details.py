from db_fms import insert
import json

def add_product(user_id: int, product_name: str, quantity: int, price: float):
    try:
        if not user_id or not product_name or quantity <= 0 or price <= 0:
            return {"status": "failed", "message": "All fields are required and must be valid."}

        result = insert(
            "product_details",
            user_id=user_id,
            product_name=product_name,
            quantity=quantity,
            price=price
        )

        if result[0][0] == 1:
            return {"status": "success", "message": "Product added successfully."}
        else:
            return {"status": "failed", "message": result[0][1]}
    
    except Exception as e:
        return {"status": "failed", "message": str(e)}

# Example
if __name__ == "__main__":
    response = add_product(
        user_id=2,
        product_name="Drip Kit",
        quantity=50,
        price=600.00
    )
    print(json.dumps(response, indent=4))
