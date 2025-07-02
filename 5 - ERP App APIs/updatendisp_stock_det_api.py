from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from db_erp import fetch, update

app = FastAPI(title="Stock Management API")

# 📦 Models
class StockUpdateRequest(BaseModel):
    product_id: int
    quantity: int


class StockDetail(BaseModel):
    product_id: int
    product_name: str
    quantity_available: int
    unit_of_measure: str
    last_updated: str


class StatusMessage(BaseModel):
    status: str
    message: str


class StockListResponse(BaseModel):
    status: str
    data: List[StockDetail]


# 🔁 Update Stock Quantity
@app.put("/stock/update", response_model=StatusMessage)
def update_stock_quantity(request: StockUpdateRequest):
    try:
        if request.quantity < 0:
            return {"status": "failed", "message": "❌ Quantity cannot be negative."}

        product_info = fetch(
            "stock_details",
            columns=["product_name", "quantity_available"],
            product_id=request.product_id
        )

        if not product_info or not product_info[0]:
            return {
                "status": "failed",
                "message": f"❌ No product found with product_id {request.product_id}."
            }

        product_name, existing_quantity = product_info[0]

        result = update(
            table_name="stock_details",
            conditions={"product_id": request.product_id},
            quantity_available=request.quantity
        )

        if result[0][0] == 1:
            return {
                "status": "success",
                "message": f"✅ Stock for '{product_name}' (Product ID: {request.product_id}) updated to {request.quantity} units."
            }
        else:
            return {"status": "failed", "message": f"❌ Update failed: {result[0][1]}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📜 Display All Stock Details
@app.get("/stock", response_model=StockListResponse)
def display_stock_details():
    try:
        details = fetch("stock_details")

        data = [
            {
                "product_id": det[0],
                "product_name": det[1],
                "quantity_available": det[2],
                "unit_of_measure": det[3],
                "last_updated": str(det[4])
            }
            for det in details
        ]

        return {"status": "success", "data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
