from fastapi import APIRouter, Depends, HTTPException, status, Header
from config.db import get_db
from models import Employee, Department, TrainingAssignee
from schemas import EmployeeSchema, LoginSchema, Token, EmployeeUpdateSchema, AssignTrainingSchema
from sqlmodel import Session
from datetime import date
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union
from datetime import datetime, timedelta
from utils import app_service

employee_route = APIRouter(
    prefix="/v1/employee",
    tags=["Employee"],
    responses={
        403: {"description": "Not Allowed"},
        200: {"description": "Everything is ok"},
        422: {"description": "Unprocessable Entity"},
        409: {"description": "conflict in request params"},
    }
)

@employee_route.get("/")
async def get_employees(token: str = Header(None), db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    return db.query(Employee).all()

@employee_route.get("/{id}")
async def get_employee_details(id: int, token: str = Header(None), db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    return db.query(Employee).get(id)

@employee_route.post("/")
async def create_employee(employee: EmployeeSchema, token: str = Header(None), db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    employee_count = db.query(Employee).count()
    name = employee.name
    employee_code = (name[0] + name[len(name) - 1]).upper() + str(1000 + employee_count)
    x = Employee(
        employee_code = employee_code,
        name = name,
        department_id = employee.department_id,
        mobile = employee.mobile,
        email = employee.email,
        password =app_service.get_password_hash(employee.password),
        type = employee.type,
        is_hod = employee.is_hod,
        created_at = date.today(),
        updated_at = date.today()
    )
    db.add(x)
    if employee.is_hod: 
        db.flush()
        db.query(Department).filter(Department.id == employee.department_id).update({Department.hod: x.id, Department.updated_at: date.today()}, synchronize_session = False)
    db.commit()
    response = {
        "status": 201,
        "message": "Employee Created Succesfully"
    }
    return response
@employee_route.patch("/{employee_id}")
async def update_employee(employee_id: int, employee: EmployeeUpdateSchema, token: str = Header(None), db: Session = Depends(get_db)):
    app_service.authMiddleware((token))
    update_employee = {
        Employee.name: employee.name,
        Employee.department_id: employee.department_id,
        Employee.mobile: employee.mobile,
        Employee.email: employee.email,
        Employee.type: employee.type,
        Employee.is_hod: employee.is_hod,
        Employee.updated_at: date.today()
    }
    db.query(Employee).filter(Employee.id == employee_id).update(update_employee)
    if employee.is_hod: 
        db.query(Department).filter(Department.id == employee.department_id).update({Department.hod: employee_id, Department.updated_at: date.today()}, synchronize_session = False)
    db.commit()
    response = {
        "status": 200,
        "message": "Employee Updated Succesfully"
    }
    return response

@employee_route.delete("/{employee_id}")
async def delete_employee(employee_id: int, token: str = Header(None), db: Session = Depends(get_db)):
    app_service.authMiddleware((token))
    db.query(Employee).filter(Employee.id == employee_id).delete()
    db.commit()
    response = {
        "status": 200,
        "message": "Employee Deleted Succesfully"
    }
    return response

@employee_route.post("/assign_training")
async def assign_training(payload: AssignTrainingSchema, token: str = Header(None), db: Session = Depends(get_db)):
    employee_id = app_service.authMiddleware((token))
    for training_id in payload.trainings:
        assignee = TrainingAssignee(
            employee_id = employee_id,
            training_id = training_id,
            assigned_on = date.today()
        )
    db.add(assignee)
    db.commit()
    response = {
        "status": 200,
        "message": "Training Assigned Succesfully"
    }
    return response