from db_fms import fetch
import json

def view_all_products():
    try:
        product_data = fetch("product_details")

        if not product_data:
            return {"status": "success", "data": [], "message": "No products found."}

        products = []
        for row in product_data:
            products.append({
                "user_id": row[0],
                "product_id": row[1],
                "product_name": row[2],
                "quantity": row[3],
                "price": float(row[4]),
                "timestamp": str(row[5])
            })

        return {"status": "success", "data": products}

    except Exception as e:
        return {"status": "failed", "message": str(e)}

# Run the script directly to print data
if __name__ == "__main__":
    result = view_all_products()
    print(json.dumps(result, indent=4))
