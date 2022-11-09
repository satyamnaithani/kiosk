from pydantic import BaseModel

class EmployeeSchema(BaseModel):
    name: str
    department_id: int
    mobile: str
    email: str
    password: str
    type: str
    is_hod: bool

class EmployeeDeleteSchema(BaseModel):
    employee_id: int