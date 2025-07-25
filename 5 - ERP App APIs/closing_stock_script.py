from db_erp import fetch, update
from datetime import date

def update_closing_stock_from_stock_details():
    try:
        stock_items = fetch("stock_details")
        if not stock_items:
            return {"status": "failed", "message": "No data found in stock_details."}

        today = date.today()
        updated_count = 0

        for product_id, product_name, quantity_available, unit, last_updated in stock_items:
            inventory_records = fetch("inventory_details", product_id=product_id)
            if not inventory_records:
                continue

            for record in inventory_records:
                record_datetime = record[0]
                if hasattr(record_datetime, "date"):
                    record_date = record_datetime.date()
                else:
                    continue

                if record_date == today:
                    filters = {
                        "product_id": product_id,
                        "date": record_datetime
                    }
                    status = update("inventory_details", filters, closing_stock=quantity_available)
                    if status and status[0][0] == 1:
                        updated_count += 1
                    break

        return {"status": "success", "message": f"Updated closing_stock for {updated_count} records."}

    except Exception as e:
        return {"status": "failed", "message": str(e)}


if __name__ == "__main__":
    import json
    result = update_closing_stock_from_stock_details()
    print(json.dumps(result, indent=4))
