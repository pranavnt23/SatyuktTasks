from db_erp import exists, fetch, insert, update
import json

# Function to view all raw material records
def view_raw_materials():
    try:
        raw_data = fetch("raw_materials", columns=["material_id", "material_name", "entry_date", "quantity"])
        if not raw_data:
            return {"status": "failed", "message": "No raw materials found."}
        
        raw_materials = []
        for row in raw_data:
            raw_materials.append({
                "material_id": row[0],
                "material_name": row[1],
                "entry_date": str(row[2]),
                "quantity": row[3]
            })
        return {"status": "success", "data": raw_materials}
    except Exception as e:
        return {"status": "failed", "message": str(e)}

# Function to view raw material by ID
def view_raw_materials_by_id(material_id: str):
    try:
        raw_data = fetch("raw_materials", columns=["material_id", "material_name", "entry_date", "quantity"], material_id=material_id)
        if not raw_data:
            return {"status": "failed", "message": "No raw material found for the given ID."}
        
        raw_materials = []
        for row in raw_data:
            raw_materials.append({
                "material_id": row[0],
                "material_name": row[1],
                "entry_date": str(row[2]),
                "quantity": row[3]
            })
        return {"status": "success", "data": raw_materials}
    except Exception as e:
        return {"status": "failed", "message": str(e)}

# Function to add a new raw material
def add_raw_material(material_name: str, material_id: str, quantity: int):
    try:
        if not all([material_name, material_id, quantity]):
            return {"status": "failed", "message": "All fields are required."}

        if exists("raw_materials", material_id=material_id):
            return {"status": "failed", "message": "Raw material with this ID already exists."}

        status = insert(
            "raw_materials",
            material_id=material_id,
            material_name=material_name,
            quantity=quantity
        )

        if status[0][0] == 1:
            return {"status": "success", "message": "Raw material added successfully."}
        else:
            return {"status": "failed", "message": status[0][1]}
    except Exception as e:
        return {"status": "failed", "message": str(e)}

# Function to update raw material quantity
def update_raw_material(material_id: str, quantity: int):
    try:
        if not all([material_id, quantity]):
            return {"status": "failed", "message": "All fields are required."}

        if not exists("raw_materials", material_id=material_id):
            return {"status": "failed", "message": "Raw material with this ID does not exist."}

        status = update("raw_materials", {"material_id": material_id}, quantity=quantity)
        if status[0][0] == 1:
            return {"status": "success", "message": "Raw material updated successfully."}
        else:
            return {"status": "failed", "message": status[0][1]}
    except Exception as e:
        return {"status": "failed", "message": str(e)}

# Function to delete a raw material
def delete_raw_material(material_id: str):
    try:
        if not material_id:
            return {"status": "failed", "message": "Material ID is required."}

        if not exists("raw_materials", material_id=material_id):
            return {"status": "failed", "message": "Raw material with this ID does not exist."}

        from db_erp import delete 

        status = delete("raw_materials", material_id=material_id)
        if status[0][0] == 1:
            return {"status": "success", "message": "Raw material deleted successfully."}
        else:
            return {"status": "failed", "message": status[0][1]}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


if __name__ == "__main__":
    
    #print(json.dumps(view_raw_materials(), indent=4))
    #print(json.dumps(view_raw_materials_by_id("RM001"), indent=4))
    #print(json.dumps(add_raw_material("Neem Oil", "RM004", 50), indent=4))
    #print(json.dumps(update_raw_material("RM004", 60), indent=4))
    print(json.dumps(delete_raw_material("RM009"), indent=4))