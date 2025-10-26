import json, os
from sqlalchemy.future import select
from app.models.models import Question
from app.core.database import async_session
from app.utils.logger import logger

QUESTION_PATH = "storages/questions"

async def ingest_questions():
    async with async_session() as session:
        existing = await session.execute(select(Question))
        if existing.scalars().first():
            logger.info("Questions already loaded. Skipping ingest.")
            return

        for fname in os.listdir(QUESTION_PATH):
            if fname.endswith(".json"):
                with open(os.path.join(QUESTION_PATH, fname)) as f:
                    data = json.load(f)
                    q = Question(title=data.get("title", fname), content=data, 
                                 startsAt=data.get("startsAt"), size=data.get("problem", {}).get("field", {}).get("size"))
                    session.add(q)
        await session.commit()
        logger.info("Questions ingested successfully.")
