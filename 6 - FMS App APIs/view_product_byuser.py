from db_fms import fetch
import json

def view_products_by_user(user_id: int):
    try:
        if not user_id:
            return {"status": "failed", "message": "User ID is required."}

        product_data = fetch(
            "product_details",
            columns=["product_id", "product_name", "quantity", "price", "timestamp"],
            user_id=user_id
        )

        if not product_data:
            return {"status": "success", "data": [], "message": "No products found for this user."}

        products = []
        for row in product_data:
            products.append({
                "product_id": row[0],
                "product_name": row[1],
                "quantity": row[2],
                "price": float(row[3]),
                "timestamp": str(row[4])
            })

        return {"status": "success", "data": products}
    
    except Exception as e:
        return {"status": "failed", "message": str(e)}

# Example
if __name__ == "__main__":
    result = view_products_by_user(1)
    print(json.dumps(result, indent=4))
