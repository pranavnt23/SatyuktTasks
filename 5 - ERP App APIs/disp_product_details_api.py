from fastapi import FastAPI
from fastapi.responses import JSONResponse
from db_erp import fetch
from decimal import Decimal
import json

app = FastAPI(title="Product API")

# Custom JSON Encoder to handle Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

# Function to fetch product details
def get_all_product_details():
    try:
        result = fetch("product_details", columns=["product_id", "product_name", "unit_of_measure", "cost_per_unit"])
        return result
    except Exception as e:
        print("Error:", e)
        return []

# FastAPI Endpoint
@app.get("/products", response_class=JSONResponse)
def read_products():
    data = get_all_product_details()
    return JSONResponse(content=json.loads(json.dumps(data, cls=DecimalEncoder)))
