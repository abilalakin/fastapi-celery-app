from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from celery import chain
from app.celery.tasks import step_a, step_b, step_c
from ..database import get_db
from ..models.job import Job
from ..schemas import JobResponse, JobIdResponse


router = APIRouter(prefix="/pipeline")

@router.post("/", response_model=JobIdResponse, status_code=201)
async def create_pipeline(db: AsyncSession = Depends(get_db)):
    job = Job(status="pending")
    db.add(job)
    try:
        await db.commit()
        await db.refresh(job)
        # Start Celery pipeline
        pipeline = chain(
            step_a.s(str(job.job_id)),
            step_b.s(),
            step_c.s()
        ).apply_async()
        
        return {"job_id": job.job_id}
    
    except Exception as e:
        await db.rollback()
        # Update status to "error"
        job.status = "error"
        job.result = str(e)
        db.add(job)
        await db.commit()
        
        raise HTTPException(status_code=500, detail="Failed to create pipeline")

@router.get("/{job_id}", response_model=JobResponse, status_code=200)
async def get_job_status(job_id: str, db: AsyncSession = Depends(get_db)):
    try:
        job = await db.get(Job, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return job
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while retrieving job status")
