from pydantic import BaseModel

class EmployeeSchema(BaseModel):
    id: int
    employee_code: str
    name: str
    department_id: int
    mobile: str
    email: str
    password: str
    type: str
    created_at: str
    updated_at: str