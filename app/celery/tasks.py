import logging
import httpx
import uuid
from celery.exceptions import Ignore
from asgiref.sync import async_to_sync
from typing import Any, Tuple
from app.celery_app import celery_app
from ..config import settings
from ..database import AsyncSessionLocal
from ..models.job import Job


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def update_job_status(job_id: uuid.UUID, status: str, result: Any = None) -> Job:
    async with AsyncSessionLocal() as session:
        job = await session.get(Job, job_id)
        job.status = status
        if result:
            job.result = result
        await session.commit()
        return job
                
def handle_task_exception(job_id: uuid.UUID, exc: Exception) -> None:
    logger.error(f"Job {job_id} failed: {exc}")
    async_to_sync(update_job_status)(job_id, "error", str(exc))
    raise Ignore()


@celery_app.task(bind=True, name="app.celery.tasks.step_a")
def step_a(self, job_id: uuid.UUID) -> Tuple[uuid.UUID, Any]:
    try:
        logger.info(f"Starting step_a with job_id: {job_id}")
        with httpx.Client() as client:
            response = client.get(settings.API_ENDPOINT)
            data = response.json()
        
        logger.info(f"Completed step_a with job_id: {job_id}")
        return (job_id, data)
    except Exception as exc:
        handle_task_exception(job_id, exc)
    


@celery_app.task(bind=True, name="app.celery.tasks.step_b")
def step_b(self, payload: Tuple[uuid.UUID, Any]) -> uuid.UUID:
        try:
            job_id, data = payload
            logger.info(f"Starting step_b with job_id: {job_id}")
            job = async_to_sync(update_job_status)(job_id, "in_progress", data)
            logger.info(f"Completed step_b with job_id: {job_id} and status: {job.status}")
            return job_id
        except Exception as exc:
            handle_task_exception(job_id, exc)


@celery_app.task(bind=True, name="app.celery.tasks.step_c")
def step_c(self, job_id: uuid.UUID) -> Any:
        try:
            logger.info(f"Starting step_c with job_id: {job_id}")
            # Update job status to "completed"
            job = async_to_sync(update_job_status)(job_id, "completed")
            logger.info(f"Completed step_c with job_id: {job_id} and status: {job.status}")
            return job.result
        except Exception as exc:
            handle_task_exception(job_id, exc)
            
