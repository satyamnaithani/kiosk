from fastapi import FastAPI
from pydantic import BaseModel
from routes import employee_route, login_route, department_route, training_route, question_route
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
app.include_router(login_route)
app.include_router(employee_route)
app.include_router(department_route)
app.include_router(training_route)
app.include_router(question_route)