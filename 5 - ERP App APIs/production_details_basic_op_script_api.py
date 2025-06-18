from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from db_pro import insert, fetch, exists

app = FastAPI(title="Manufacturing Production API")


# 🧱 Models
class ManufactureInput(BaseModel):
    product_id: int
    quantity: int
    status: Optional[str] = "ongoing"


class ProductionEntry(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    start_date: str
    status: str


class StatusMessage(BaseModel):
    status: str
    message: Optional[str] = None


class ProductionListResponse(BaseModel):
    status: str
    data: List[ProductionEntry]


# 🏗️ Add Production Batch
@app.post("/production", response_model=StatusMessage)
def update_manufacture(entry: ManufactureInput):
    try:
        if not exists("product_details", product_id=entry.product_id):
            return {"status": "failed", "message": f"Product ID {entry.product_id} does not exist."}

        product = fetch("product_details", columns=["product_name"], product_id=entry.product_id)
        if not product:
            return {"status": "failed", "message": "Failed to fetch product name."}

        product_name = product[0][0]

        result = insert("production_details",
                        product_id=entry.product_id,
                        product_name=product_name,
                        quantity=entry.quantity,
                        status=entry.status)

        if result[0][0] == 1:
            return {"status": "success", "message": "Production entry added successfully."}
        else:
            return {"status": "failed", "message": result[0][1]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📋 View All Production Entries
@app.get("/production", response_model=ProductionListResponse)
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
        raise HTTPException(status_code=500, detail=str(e))


# 🔎 View Production By Product ID
@app.get("/production/{product_id}", response_model=ProductionListResponse)
def display_by_id(product_id: int):
    try:
        if not exists("production_details", product_id=product_id):
            return {"status": "failed", "data": [], "message": f"No entries for Product ID {product_id}."}

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
        raise HTTPException(status_code=500, detail=str(e))
