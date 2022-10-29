from fastapi import APIRouter, Depends
from config.db import get_db
from models import Employee
from schemas import EmployeeSchema
from sqlmodel import Session

employee = APIRouter()

@employee.get("/")
async def read_data(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@employee.post("/")
async def write_data(employee: EmployeeSchema, db: Session = Depends(get_db)):
    print(employee)
    return db.add({
        id: employee.id,
        employee_code: employee.employee_code,
        name: employee.name,
    })