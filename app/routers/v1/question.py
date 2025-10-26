from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.models import Question
from app.schemas.problem import ListQuestionSchema, FieldData, QuestionSchema
from app.utils.logger import logger
from typing import List

router = APIRouter(
    prefix="/question",
    tags=["Questions"],
    # dependencies=[Depends(get_current_active_user)],
)

@router.get(
    "/{id}", 
    response_model=QuestionSchema,
    status_code=200,
    summary="Get question by ID",
    description="Retrieve a specific question by its ID."
)
async def get_question(id: int, db: AsyncSession = Depends(get_db)):
    '''Get a specific question by its ID.'''
    result = await db.execute(select(Question).where(Question.startsAt == id))
    q = result.scalar_one_or_none()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    field = q.content.get("problem", {}).get("field", {})
    logger.info(f"Fetched question ID={q.id} - title='{q.title}'")
    return QuestionSchema(
        startsAt=q.startsAt,
        problem=FieldData(
            **field
        )
    )

@router.get(
    "", 
    response_model=List[ListQuestionSchema],
    status_code=200,
    summary="List all questions",
    description="Retrieve a list of all available questions."
)
async def list_questions(db: AsyncSession = Depends(get_db)):
    '''List all available questions.'''
    result = await db.execute(select(Question))
    questions = result.scalars().all()
    result = [
        ListQuestionSchema(
            id=q.startsAt,
            size=q.size,
        ) for q in questions
    ]
    return sorted(result, key=lambda x: x.id)


