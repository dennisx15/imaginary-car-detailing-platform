from fastapi import FastAPI # toolkit for creating web servers and APIs
from backend.routes import faq, appointments
from backend.database.connection import engine

app = FastAPI() # this is the web application object

@app.get("/") # this is a decorator. When someone sends a GET request to /, the function below will run
def root():
    return {"message": "Backend is running"}

app.include_router(faq.router) # this tells the app to include the routes defined in faq.py
app.include_router(appointments.router) # this tells the app to include the routes defined in appointments.py