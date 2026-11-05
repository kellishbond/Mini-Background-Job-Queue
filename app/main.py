
from fastapi import FastAPI

app = FastAPI(
    title="Mini Background Job Queue",
    description="A learning project for understanding background job processing.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Mini Background Job Queue",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Mini Background Job Queue"
    }
