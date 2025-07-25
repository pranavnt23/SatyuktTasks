from db_erp import insert, fetch
from datetime import date

def add_opening_stock_from_stock_details():
    try:
        stock_items = fetch("stock_details")

        if not stock_items:
            return {"status": "failed", "message": "No data found in stock_details."}

        inserted_count = 0

        for item in stock_items:
            product_id = item[0]         
            product_name = item[1]       
            quantity_available = item[2] 

            status = insert(
                "inventory_details",
                product_id=product_id,
                product_name=product_name,
                opening_stock=quantity_available
            )

            if status and status[0][0] == 1:
                inserted_count += 1
            else:
                continue

        return {"status": "success", "message": f"Inserted {inserted_count} records into inventory_details."}

    except Exception as e:
        return {"status": "failed", "message": str(e)}


if __name__ == "__main__":
    import json
    result = add_opening_stock_from_stock_details()
    print(json.dumps(result, indent=4))
