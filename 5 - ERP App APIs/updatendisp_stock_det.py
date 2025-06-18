from db_pro import fetch, update

def update_stock_quantity(product_id: int, quantity: int):
    # Step 1: Validate quantity
    if quantity < 0:
        return {"status": "failed", "message": "❌ Quantity cannot be negative."}

    # Step 2: Check if product exists
    product_info = fetch(
        "stock_details",
        columns=["product_name", "quantity_available"],
        product_id=product_id
    )

    if not product_info or not product_info[0]:
        return {"status": "failed", "message": f"❌ No product found with product_id {product_id}."}

    product_name, existing_quantity = product_info[0]

    # Step 3: Update the stock
    result = update(
        table_name="stock_details",
        conditions={"product_id": product_id},
        quantity_available=quantity
    )

    if result[0][0] == 1:
        return {
            "status": "success",
            "message": f"✅ Stock for '{product_name}' (Product ID: {product_id}) updated to {quantity} units."
        }
    else:
        return {
            "status": "failed",
            "message": f"❌ Update failed: {result[0][1]}"
        }
    
def display_stock_details():
    data =[]

    details=fetch("stock_details")
    for det in details:
        data.append({
            "product_id":det[0],
            "product_name" : det[1],
            "quantity_available": det[2],
            "unit_of_measure": det[3],
            "last_updated": str(det[4])       
        })
    print(data)

# Example usage
if __name__ == "__main__":
    result = update_stock_quantity(1002, 200)
    print(result)
    display_stock_details()