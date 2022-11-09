from pydantic import BaseModel

class EmployeeSchema(BaseModel):
    employee_code: str
    name: str
    department_id: int
    mobile: str
    email: str
    password: str
    type: str
    is_hod: bool