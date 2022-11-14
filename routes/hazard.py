from fastapi import APIRouter, Depends, HTTPException, status, Header
from config.db import get_db
from models import Hazard
from schemas import HazardSchema
from sqlmodel import Session
from datetime import date
from utils import app_service

hazard_route = APIRouter(
    prefix="/v1/hazards",
    tags=["Hazards"],
    responses={
        403: {"description": "Not Allowed"},
        200: {"description": "Everything is ok"},
        422: {"description": "Unprocessable Entity"},
        409: {"description": "conflict in request params"},
    }
)

@hazard_route.get("/")
async def get_hazards(token: str = Header(None), db: Session = Depends(get_db)):
    app_service.authMiddleware(token)
    return db.query(Hazard).all()


@hazard_route.post("/")
async def create_hazard(hazard: HazardSchema, token: str = Header(None), db: Session = Depends(get_db)):
    employee_id = app_service.authMiddleware(token)
    x = Hazard(
        title = hazard.title,
        description = hazard.description,
        type = hazard.type,
        department_id = hazard.department_id,
        status = hazard.status,
        remarks = hazard.remarks,
        created_by = employee_id,
        created_at = date.today()
    )
    db.add(x)
    db.commit()
    response = {
        "status": 201,
        "message": "Hazard Created Succesfully"
    }
    return response