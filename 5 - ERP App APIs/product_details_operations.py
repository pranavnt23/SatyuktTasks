from db_pro import exists, fetch, insert, delete
from encryptdecrypt import decrypt_info
import json

def view_product_details_for_user(id:int):
    try:
        if not id or not exists("product_details", product_id=id):
            return {"status": "failed", "message": "Invalid product ID."}  
        pr_details=fetch("product_details",
                         columns=["product_id", "product_name", "unit_of_measure", "cost_per_unit"],
                         product_id=id)
        return {"status": "success", "data": pr_details}
    except Exception as e:
        return {"status": "failed", "message": str(e)}
    
def view_all_products():
    try:
        pr_details = fetch("product_details",
                           columns=["product_id", "product_name", "unit_of_measure", "cost_per_unit"])
        if not pr_details:
            return {"status": "success", "data": [], "message": "No products found."}
        
        product_list = []
        for product in pr_details:
            product_dict = {
                "product_id": product[0],
                "product_name": product[1],
                "unit_of_measure": product[2],
                "cost_per_unit": float(product[3])
            }
            product_list.append(product_dict)
        
        return {"status": "success", "data": product_list}
    
    except Exception as e:
        return {"status": "failed", "message": str(e)}
    
def delete_product(id:int):
    try:
        ex=exists("product_details",product_id=id)
        if not ex:
            return {"status": "failed", "message": "Product not found."}
        delete("product_details", product_id=id)
        return {"status": "success", "message": "Product deleted successfully."}
    except Exception as e:
        return {"status": "failed", "message": str(e)}
    
def add_product(product_id:int, product_name: str, unit_of_measure: str, cost_per_unit: float):
    try:
        if not product_id or not product_name or not unit_of_measure or cost_per_unit <= 0:
            return {"status": "failed", "message": "Invalid product details."}

        status = insert("product_details", product_id=product_id, product_name=product_name,
                        unit_of_measure=unit_of_measure,
                        cost_per_unit=cost_per_unit)

        if status[0][0] == 1:
            return {"status": "success", "message": "Product added successfully."}
        else:
            return {"status": "failed", "message": status[0][1]}
    except Exception as e:
        return {"status": "failed", "message": str(e)}
    
if __name__ == "__main__":
    result = view_product_details_for_user(1002)
    print(json.dumps(result, indent=4))
    
    all_products = view_all_products()
    print(json.dumps(all_products, indent=4))
    
    """delete_result = delete_product(1)
    print(json.dumps(delete_result, indent=4))"""
    
    add_result = add_product(1010, "Product_demonstration", "kg", 100.0)
    print(json.dumps(add_result, indent=4))