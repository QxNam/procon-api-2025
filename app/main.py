from app.routers import ranking
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.utils.ingest_questions import ingest_questions
from app.core.database import engine
from app.models import models
from app.routers.v1 import auth, answer, question, ws
from app.routers import ranking, simulation
from app.utils.logger import logger

app = FastAPI(title="Procon 2025 API")
origins = [
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:8000",
    "http://procon.qxdata.engineer",
    "https://procon.qxdata.engineer"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(auth.router)
app.include_router(answer.router)
app.include_router(question.router)
app.include_router(ranking.router)
app.include_router(simulation.router)
app.include_router(ws.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    logger.info("Database initialized.")
    await ingest_questions()


        