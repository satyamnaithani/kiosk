from pydantic import BaseModel
from typing import List

class EmployeeSchema(BaseModel):
    name: str
    department_id: int
    mobile: str
    email: str
    password: str
    type: str
    is_hod: bool

class EmployeeUpdateSchema(BaseModel):
    name: str
    department_id: int
    mobile: str
    email: str
    type: str
    is_hod: bool

class AssignTraining(BaseModel):
    employee_id: int
    trainings: List[int]
