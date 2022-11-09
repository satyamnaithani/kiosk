from fastapi import APIRouter, Depends, HTTPException, status
from config.db import get_db
from models import Employee, Department
from schemas import EmployeeSchema, LoginSchema, Token
from sqlmodel import Session
from datetime import date
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union
from datetime import datetime, timedelta
from utils import app_service

login_route = APIRouter(
    prefix="/v1/login",
    tags=["Login"],
    responses={
        403: {"description": "Not Allowed"},
        200: {"description": "Everything is ok"},
        422: {"description": "Unprocessable Entity"},
        409: {"description": "conflict in request params"},
    }
)

@login_route.post("/")
async def login(payload: LoginSchema, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.email==payload.email).first()

    if not employee:
        return {
            "status": 404,
            "message": "Employee not found"
        }

    if not app_service.verify_password(payload.password, employee.password):
        return {
            "status": 401,
            "message": "invalid credentials!"
        }
    employee_id = employee.id
    jwt = await app_service.create_token(employee_id)
    response = {
        "employee_code": employee.employee_code,
        "employee_id": employee.id,
        "name": employee.name,
        "mobile": employee.mobile,
        "email": employee.email,
        "type": employee.type,
        "jwt": jwt,
    }
    return {"message": response}