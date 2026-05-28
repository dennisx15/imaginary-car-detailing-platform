from fastapi import FastAPI # toolkit for creating web servers and APIs
from backend.routes import faq, appointments
from backend.database.connection import engine
from fastapi.middleware.cors import CORSMiddleware # this is a security feature that prevents other websites from making requests to our backend without permission. We will configure it to allow requests from our frontend.
from backend.routes import auth
from backend.database.models import User, Appointment

app = FastAPI() # this is the web application object

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #this means allow requests from any origin. In production, you would want to specify the exact origin of your frontend, like "http://localhost:3000" or "https://myfrontend.com"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/") # this is a decorator. When someone sends a GET request to /, the function below will run
def root():
    return {"message": "Backend is running"}

app.include_router(faq.router) # this tells the app to include the routes defined in faq.py
app.include_router(appointments.router) # this tells the app to include the routes defined in appointments.py
app.include_router(auth.router)