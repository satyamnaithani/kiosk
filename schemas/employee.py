from pydantic import BaseModel
from typing import List

class EmployeeSchema(BaseModel):
    name: str
    department_id: int
    mobile: str
    employee_code: str
    email: str
    password: str
    type: str
    is_hod: bool

class EmployeeUpdateSchema(BaseModel):
    name: str
    department_id: int
    employee_code: str
    mobile: str
    email: str
    type: str
    is_hod: bool

class AssignTrainingSchema(BaseModel):
    employee_id: int
    trainings: List[int]
