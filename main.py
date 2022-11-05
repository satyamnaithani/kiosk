from fastapi import FastAPI
from pydantic import BaseModel
from routes.employee import employee
from routes.training import training
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee)
app.include_router(training)