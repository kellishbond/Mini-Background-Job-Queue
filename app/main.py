
import json
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import init_db, get_connection


app = FastAPI(
    title="Mini Background Job Queue",
    description="A learning project for understanding background job processing.",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


class JobCreate(BaseModel):
    task_type: str
    payload: dict


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


@app.post("/jobs")
def create_job(job: JobCreate):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO jobs (task_type, payload)
        VALUES (?, ?)
        """,
        (job.task_type, json.dumps(job.payload))
    )

    connection.commit()

    job_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Job submitted successfully",
        "job_id": job_id,
        "task_type": job.task_type,
        "status": "PENDING"
    }
    
    
@app.get("/jobs")
def get_jobs():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM jobs ORDER BY id DESC"
    ).fetchall()

    connection.close()

    jobs = []

    for row in rows:
        job = dict(row)
        job["payload"] = json.loads(job["payload"])
        jobs.append(job)

    return {
        "total": len(jobs),
        "jobs": jobs
    }


@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM jobs WHERE id = ?",
        (job_id,)
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    job = dict(row)
    job["payload"] = json.loads(job["payload"])

    return job
