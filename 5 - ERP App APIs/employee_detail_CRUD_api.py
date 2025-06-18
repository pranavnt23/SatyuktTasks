from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from db_pro import insert, fetch, delete
from datetime import date

app = FastAPI(title="Employee CRUD API")

# Pydantic Model
class Employee(BaseModel):
    employee_id: int
    full_name: str
    email: str
    designation: str
    date_of_joining: date  # 🛠️ Only DATE, no time

class EmployeeCreate(BaseModel):
    full_name: str
    email: str
    designation: str

# Endpoint: Get employee by ID
@app.get("/employee/{employee_id}", response_model=Employee)
def get_employee_by_id(employee_id: int):
    result = fetch(
        "employee_details",
        columns=["employee_id", "full_name", "email", "designation", "date_of_joining"],
        employee_id=employee_id
    )

    if not result or not result[0]:
        raise HTTPException(status_code=404, detail="Employee not found")

    row = result[0]
    return Employee(
        employee_id=row[0],
        full_name=row[1],
        email=row[2],
        designation=row[3],
        date_of_joining=row[4].date()  # ✨ Fix: Convert datetime to date
    )

# Endpoint: Get all employees
@app.get("/employees", response_model=List[Employee])
def get_all_employees():
    result = fetch("employee_details", columns=["employee_id", "full_name", "email", "designation", "date_of_joining"])
    return [
        Employee(
            employee_id=row[0],
            full_name=row[1],
            email=row[2],
            designation=row[3],
            date_of_joining=row[4].date()  # ✨ Fix: Convert datetime to date
        )
        for row in result
    ]

# Endpoint: Add an employee
@app.post("/employee", status_code=201)
def add_employee(employee: EmployeeCreate):
    data = {
        "full_name": employee.full_name,
        "email": employee.email,
        "designation": employee.designation
    }
    status = insert("employee_details", **data)
    if status[0][0] == 1:
        return {"status": "success", "message": status[0][1]}
    else:
        raise HTTPException(status_code=400, detail=status[0][1])

# Endpoint: Delete an employee
@app.delete("/employee/{employee_id}")
def delete_employee(employee_id: int):
    status = delete("employee_details", employee_id=employee_id)
    if status[0][0] == 1:
        return {"status": "success", "message": status[0][1]}
    else:
        raise HTTPException(status_code=404, detail=status[0][1])
