from fastapi import APIRouter, Depends
from config.db import get_db
from models import Employee
from schemas import EmployeeSchema, LoginSchema
from sqlmodel import Session
from datetime import date
from passlib.context import CryptContext

employee = APIRouter()
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from jose import JWTError, jwt
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)

@employee.get("/")
async def read_data(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@employee.post("/")
async def write_data(employee: EmployeeSchema, db: Session = Depends(get_db)):
    x = Employee(
        employee_code = employee.employee_code,
        name = employee.name,
        department_id = employee.department_id,
        mobile = employee.mobile,
        email = employee.email,
        password = get_password_hash(employee.password),
        type = employee.type,
        created_at = date.today(),
        updated_at = date.today()
    )
    db.add(x)
    db.commit()
    return {"message": "Employee Created Succesfully"}

@employee.post("/login")
async def login(payload: LoginSchema, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.email==payload.email).first()

    if not employee:
        return {"message": "Employee not found"}

    if not verify_password(payload.password, employee.password):
        return {"message": "invalid credentials!"}

    return {"message": "login successfull!"}
    

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user