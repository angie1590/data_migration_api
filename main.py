from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.load_data import load_all_data
from app.core.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    logger.info("Loading historic data into the database...")
    load_all_data()

    logger.info("System ready to receive new transactions.")
    yield

app = FastAPI(
    title="Data Migration API",
    description="""
        The Data Migration API is a Proof of Concept (PoC) built to support a large-scale data migration project.

        This API allows you to:

        1. Load historic data from CSV files into a SQL database.
        2. Receive and validate new data via REST endpoints.
        - Supports single and batch transactions (1 to 1000 rows).
        - Validates data against business rules and schema definitions.
        3. Export backups of each table in AVRO format.
        4. Restore tables from AVRO backups.

        All endpoints are designed to be secure, versioned, and easily integrable in automated pipelines.
        """,
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "API is running successfully"}