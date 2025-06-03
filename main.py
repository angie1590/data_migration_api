from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.load_data import load_all_data
from app.core.logger import logger

from app.routers.department_router import router as department_router
from app.routers.job_router import router as job_router
from app.routers.hired_employee_router import router as hired_employee_router
from app.routers.reports import router as reports_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    logger.info("System ready to receive new transactions.")
    yield

app = FastAPI(
    title="Data Migration API",
    description="API for managing departments, jobs, and hired employees, including analytical reports.",
    version="1.0.0",
    lifespan=lifespan
)
# Challenge 1: Ingestion APIs
app.include_router(department_router, prefix="/departments", tags=["Departments"])
app.include_router(job_router, prefix="/jobs", tags=["Jobs"])
app.include_router(hired_employee_router, prefix="/hired-employees", tags=["Hired Employees"])

# Challenge 2: Reporting endpoints
app.include_router(reports_router, prefix="/reports", tags=["Reports"])