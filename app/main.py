import asyncio
from fastapi import FastAPI
from app.database import init_db
from app.routes import auth_routes, task_routes
# Import 'producer' instead of 'kafka_producer'
from app.kafka.producer import producer
from app.kafka.consumer import start_kafka_consumer
from app.utils.logger import logger

app = FastAPI(
    title="Task Management System",
    description="Modular FastAPI backend with JWT, Kafka, and SQLite",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    # 1. Initialize Database
    logger.info("Initializing SQLite database...")
    init_db()
    
    # 2. Kafka Producer connects automatically on import in your current producer.py
    # So we just log its status
    logger.info("Kafka Producer initialized.")
    
    # 3. Start Kafka Consumer (Background Task)
    logger.info("Starting Kafka Consumer background task...")
    asyncio.create_task(start_kafka_consumer())

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Closing Kafka Producer connection...")
    # Use the .close() method defined in your TaskEventProducer class
    producer.close()

# Include Routers
app.include_router(auth_routes.router)
app.include_router(task_routes.router)

@app.get("/")
async def root():
    return {"status": "online", "message": "Task Management API is running"}