import json
from db_pro import fetch
from decimal import Decimal

# JSON Encoder to handle Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def get_all_product_details():
    try:
        # Fetch all rows from product_details
        result = fetch("product_details", columns=["product_id", "product_name", "unit_of_measure", "cost_per_unit"])
        return result
    except Exception as e:
        print("Error:", e)
        return []

# Example execution
if __name__ == "__main__":
    data = get_all_product_details()
    print(json.dumps(data, indent=4, cls=DecimalEncoder))  # Output as clean JSON array
