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

employee = APIRouter()
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@employee.get("/employee")
async def get_employees(token: str, db: Session = Depends(get_db)):
    try:
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return db.query(Employee).all()

@employee.post("/employee")
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
    name = employee.name
    jwt = await create_token(name)
    response = {
        "employee_code": employee.employee_code,
        "name": name,
        "mobile": employee.mobile,
        "email": employee.email,
        "type": employee.type,
        "jwt": jwt,
    }
    return {"message": response}
    

async def create_token(name: OAuth2PasswordRequestForm = Depends()):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = create_access_token(
        data={"sub": name}, expires_delta=access_token_expires
    )
    return access_token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@employee.get("/departments")
async def get_departments(token: str, db: Session = Depends(get_db)):
    try:
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    departments = db.query(Department).all()
    response = []
    for department in departments:
        response.append({"id": department.id, "name": department.name})
    return response