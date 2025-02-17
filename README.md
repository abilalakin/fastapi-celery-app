# FastAPI Celery App

A small FastAPI web application that triggers an asynchronous pipeline of Celery tasks. This project exposes endpoints to create a pipeline job and check its status.

## Features

- **FastAPI**: A lightweight web framework.
- **Celery**: For asynchronous task processing.
- **Postgres**: Persistent storage for job data.
- **Redis**: Message broker for Celery tasks.
- **Docker Compose**: Simplified orchestration for local development.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Environment Variables

Create a `.env` file in the project root with the following content:

```bash
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/pipeline_db
REDIS_URL=redis://redis:6379/0
API_ENDPOINT=https://jsonplaceholder.typicode.com/todos/1
```

### Running the Application

1. **Clone the Repository**

   ```bash
   git clone https://github.com/abilalakin/fastapi-celery-app.git
   cd fastapi-celery-app
   ```

2. **Start Services with Docker Compose**

   ```bash
   docker-compose up -d
   ```

   This command will:

   - Build and run the FastAPI web server.
   - Launch the Celery worker.
   - Set up the Postgres database.
   - Set up the Redis server.

3. **Access the API Documentation**

   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to view the interactive API docs provided by FastAPI.

## API Endpoints

### Create Pipeline

- **URL**: `/pipeline/`
- **Method**: `POST`
- **Description**: Creates a new pipeline job. It initializes a job with a "pending" status, saves it to the database, and then starts a Celery task chain (comprising `step_a`, `step_b`, and `step_c`).
- **Response Example**:
  ```json
  {
    "job_id": "your-generated-job-id"
  }
  ```

### Get Job Status

- **URL**: `/pipeline/{job_id}`
- **Method**: `GET`
- **Description**: Retrieves the status and details of a job using its unique `job_id`. Returns job details including its current status and result data.
- **Response Example**:
  ```json
  {
    "job_id": "your-generated-job-id",
    "status": "pending",
    "result": null,
    "created_at": "2024-02-17T12:00:00Z",
    "updated_at": "2024-02-17T12:30:00Z"
  }
  ```
  If the job is not found, a 404 error is returned.


