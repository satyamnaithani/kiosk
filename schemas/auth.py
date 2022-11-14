from pydantic import BaseModel

class LoginSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "satyam@gmail.com",
                "password": "hell"
            }
        }