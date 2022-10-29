from fastapi import FastAPI
from pydantic import BaseModel
from routes.employee import employee

app=FastAPI()

app.include_router(employee)