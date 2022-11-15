from pydantic import BaseModel

class HazardSchema(BaseModel):
    title: str
    description: str
    type: str
    department_id: int
    status: str
    remarks: str

class HazardCloseSchema(BaseModel):
    status: str
    hazard_feedback: str
