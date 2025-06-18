from db_pro import insert, fetch, exists
import json

# Add a new manufacturing batch for an existing product
def update_manufacture(product_id: int, quantity: int, status: str = "ongoing"):
    try:
        if not exists("product_details", product_id=product_id):
            return {"status": "failed", "message": f"Product ID {product_id} does not exist."}

        product = fetch("product_details", columns=["product_name"], product_id=product_id)
        if not product:
            return {"status": "failed", "message": "Failed to fetch product name."}

        product_name = product[0][0]

        result = insert("production_details",
                        product_id=product_id,
                        product_name=product_name,
                        quantity=quantity,
                        status=status)

        if result[0][0] == 1:
            return {"status": "success", "message": "Production entry added successfully."}
        else:
            return {"status": "failed", "message": result[0][1]}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


# Display all production entries
def disp_all_elements():
    try:
        result = fetch("production_details",
                       columns=["product_id", "product_name", "quantity", "start_date", "status"])
        data = [
            {
                "product_id": row[0],
                "product_name": row[1],
                "quantity": row[2],
                "start_date": str(row[3]),
                "status": row[4]
            }
            for row in result
        ]
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


# Display production entries for a specific product ID
def display_by_id(product_id: int):
    try:
        if not exists("production_details", product_id=product_id):
            return {"status": "failed", "message": f"No entries for Product ID {product_id}."}

        result = fetch("production_details",
                       columns=["product_id", "product_name", "quantity", "start_date", "status"],
                       product_id=product_id)
        data = [
            {
                "product_id": row[0],
                "product_name": row[1],
                "quantity": row[2],
                "start_date": str(row[3]),
                "status": row[4]
            }
            for row in result
        ]
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


# Example usage
if __name__ == "__main__":
    print(json.dumps(update_manufacture(1004, 80), indent=4))     # Adds new production row
    print(json.dumps(disp_all_elements(), indent=4))              # Displays all rows
    print(json.dumps(display_by_id(1004), indent=4))              # Shows only product_id = 1004
