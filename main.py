from fastapi import FastAPI
from pydantic import BaseModel
from routes import employee_route, login_route, department_route, training_route, question_route, hazard_route, grievance_route
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://main--moonlit-starship-41aec0.netlify.app/",
    "https://kiosk-x1.firebaseapp.com",
    "*"
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
app.include_router(hazard_route)
app.include_router(grievance_route)