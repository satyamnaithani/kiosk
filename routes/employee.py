from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models import Employee, Department, TrainingAssignee, Assesment
from schemas import EmployeeSchema, LoginSchema, Token, EmployeeUpdateSchema, AssignTrainingSchema
from sqlmodel import Session
from datetime import date
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union
from datetime import datetime, timedelta
from utils import app_service
from utils.oauth2 import oauth2_scheme
from sqlalchemy import or_

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
async def get_employees(db: Session = Depends(get_db)):
    # app_service.authMiddleware(token)
    employees = db.query(Employee).order_by(Employee.updated_at.desc()).all()
    arr = []
    for employee in employees:
        print(employee.department)
        arr.append({
            "id": employee.id,
            "employee_code": employee.employee_code,
            "name": employee.name,
            "department_id": employee.department_id,
            "department": employee.department.name,
            "mobile": employee.mobile,
            "email": employee.email,
            "password": employee.password,
            "type": employee.type,
            "is_hod": employee.is_hod,
            "created_at": employee.created_at,
            "updated_at": employee.updated_at,
            
        })
    return arr

@employee_route.get("/{id}")
async def get_employee_details(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    return db.query(Employee).get(id)

@employee_route.post("/")
async def create_employee(employee: EmployeeSchema, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    employee_exist = db.query(Employee).filter(or_(Employee.email == employee.email, Employee.mobile == employee.mobile)).count()
    if employee_exist != 0:
        return {
            "status": 405,
            "message": "Employee with this email or number already exist"
        }

    name = employee.name
    # employee_code = (name[0] + name[len(name) - 1]).upper() + str(1000 + employee_count)
    x = Employee(
        employee_code = employee.employee_code,
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
async def update_employee(employee_id: int, employee: EmployeeUpdateSchema, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    app_service.authMiddleware((token))
    update_employee = {
        Employee.name: employee.name,
        Employee.department_id: employee.department_id,
        Employee.employee_code: employee.employee_code,
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
async def delete_employee(employee_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    app_service.authMiddleware((token))
    db.query(Employee).filter(Employee.id == employee_id).delete()
    db.commit()
    response = {
        "status": 200,
        "message": "Employee Deleted Succesfully"
    }
    return response

@employee_route.post("/assign_training")
async def assign_training(payload: AssignTrainingSchema, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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

@employee_route.get("/assessments/{employee_id}")
async def fetch_assessments(employee_id: int, db: Session = Depends(get_db)):
    assessments = db.query(Assesment).filter(Assesment.employee_id == employee_id).all()
    if assessments == None:
        return {
            "status": 404,
            "message": "assessment not found"
        }
    arr = []
    for assessment in assessments:
        arr.append({
            "id": assessment.id,
            "score": assessment.score,
            "training": assessment.training.title,
            "question_answers": assessment.question_answers
        })
    response = {
        "status": 200,
        "data": arr
    }
    return response