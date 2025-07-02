from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from db_erp import fetch, insert, delete, exists

app = FastAPI(title="Product Management API")

# 📦 Product Schema
class Product(BaseModel):
    product_id: int
    product_name: str
    unit_of_measure: str
    cost_per_unit: float

class ProductResponse(Product):
    pass

class StatusMessage(BaseModel):
    status: str
    message: str

class ProductListResponse(BaseModel):
    status: str
    data: List[ProductResponse]
    message: Optional[str] = None


# 🧩 Add Product
@app.post("/product", response_model=StatusMessage)
def add_product(product: Product):
    if not product.product_id or not product.product_name or not product.unit_of_measure or product.cost_per_unit <= 0:
        raise HTTPException(status_code=400, detail="Invalid product details.")

    try:
        status = insert("product_details",
                        product_id=product.product_id,
                        product_name=product.product_name,
                        unit_of_measure=product.unit_of_measure,
                        cost_per_unit=product.cost_per_unit)

        if status[0][0] == 1:
            return {"status": "success", "message": "Product added successfully."}
        else:
            return {"status": "failed", "message": status[0][1]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🔍 View Product by ID
@app.get("/product/{product_id}", response_model=ProductListResponse)
def view_product_by_id(product_id: int):
    try:
        if not exists("product_details", product_id=product_id):
            return {"status": "failed", "data": [], "message": "Invalid product ID."}

        pr_details = fetch("product_details",
                           columns=["product_id", "product_name", "unit_of_measure", "cost_per_unit"],
                           product_id=product_id)

        product_list = [{
            "product_id": p[0],
            "product_name": p[1],
            "unit_of_measure": p[2],
            "cost_per_unit": float(p[3])
        } for p in pr_details]

        return {"status": "success", "data": product_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📜 View All Products
@app.get("/products", response_model=ProductListResponse)
def view_all_products():
    try:
        pr_details = fetch("product_details",
                           columns=["product_id", "product_name", "unit_of_measure", "cost_per_unit"])

        if not pr_details:
            return {"status": "success", "data": [], "message": "No products found."}

        product_list = [{
            "product_id": p[0],
            "product_name": p[1],
            "unit_of_measure": p[2],
            "cost_per_unit": float(p[3])
        } for p in pr_details]

        return {"status": "success", "data": product_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ❌ Delete Product
@app.delete("/product/{product_id}", response_model=StatusMessage)
def delete_product(product_id: int):
    try:
        if not exists("product_details", product_id=product_id):
            return {"status": "failed", "message": "Product not found."}

        delete("product_details", product_id=product_id)
        return {"status": "success", "message": "Product deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
