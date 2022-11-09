from pydantic import BaseModel

class GrievanceSchema(BaseModel):
    title: str
    description: str
    status: str
    remarks: str
