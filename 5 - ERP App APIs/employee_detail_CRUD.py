from db_erp import insert, fetch, delete
import json

def display_employee_by_id(employee_id):
    result = fetch(
        "employee_details",
        columns=["employee_id", "full_name", "email", "designation", "date_of_joining"],
        employee_id=employee_id
    )

    if not result or not result[0]:
        return {"status": "failed", "message": "Employee not found"}

    row = result[0]
    employee = {
        "employee_id": row[0],
        "full_name": row[1],            
        "email": row[2],
        "designation": row[3],
        "date_of_joining": str(row[4])
    }

    return {"status": "success", "employee": employee}

# Function to add a new employee
def add_employee(full_name, email, designation):
    data = {
        "full_name": full_name,
        "email": email,
        "designation": designation
    }
    status = insert("employee_details", **data)
    return {"status": "success" if status[0][0] == 1 else "failed", "message": status[0][1]}

# Function to delete an employee by employee_id
def delete_employee(employee_id):
    status = delete("employee_details", employee_id=employee_id)
    return {"status": "success" if status[0][0] == 1 else "failed", "message": status[0][1]}

# Function to display all employees
def display_employees():
    result = fetch("employee_details", columns=["employee_id", "full_name", "email", "designation", "date_of_joining"])
    employees = [
        {
            "employee_id": row[0],
            "full_name": row[1],
            "email": row[2],
            "designation": row[3],
            "date_of_joining": str(row[4])
        }
        for row in result
    ]
    return employees

# Example usage
if __name__ == "__main__":
    # Add an employee
    #print(add_employee("Neha Kapoor", "neha.kapoor@satyukt.com", "Finance Officer"))

    # Delete an employee
    print(delete_employee(106))

    # Display all employees
    print(json.dumps(display_employees(), indent=4))

    print(json.dumps(display_employee_by_id(104), indent=4))
