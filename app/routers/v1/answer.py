from time import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas import problem
from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.models import Submission
from app.schemas.submission import SubmissionCreate, SubmissionResponse
from app.services.judge import judge, score_evaluation, STEP_FACTOR
from app.utils.logger import logger
from app.models.models import Submission, User, Question

router = APIRouter(
    prefix="/answer",
    tags=["Answer"],
    dependencies=[Depends(get_current_active_user)],
)

@router.post(
    "", 
    response_model=SubmissionResponse, 
    status_code=201, 
    summary="Submit an answer for a problem", 
    description="Submit an answer for a problem and receive the evaluation results."
)
async def submit_answer(
    submission: SubmissionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    """Submit an answer for a problem."""

    try:
        problem_data = await db.execute(select(Question).where(Question.startsAt == submission.problem_id))
        problem_data = problem_data.scalar_one().content.get("problem").get("field")
    except Exception as e:
        logger.error(f"Problem retrieval failed: {str(e)}")
        raise HTTPException(status_code=404, detail="Problem not found")
    
    try:
        start_time = time()
        ops_data = [op.dict() for op in submission.ops]
        pair_count, step_count = judge(problem_data, ops_data, simulate=False)["pair_count"], len(ops_data)
        time_running = time() - start_time
    except Exception as e:
        logger.error(f"Judging failed: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid submission")
    
    score = score_evaluation(submission.problem_id, pair_count, step_count, time_running)
    sub = Submission(
        user_id = user.id,
        problem_id = submission.problem_id,
        ops = [op.dict() for op in submission.ops],
        pair_count = pair_count,
        step_count = step_count,
        step_factor = STEP_FACTOR,
        time_running = time_running,
        score = score
    )
    db.add(sub)
    await db.commit()
    await db.refresh(sub)

    logger.info(f"User {user.username} submitted answer ID={sub.id} with {pair_count} pairs")

    return SubmissionResponse(
        user_id = sub.user_id,
        problem_id = sub.problem_id,
        pair_count = sub.pair_count,
        step_count = sub.step_count,
        step_factor = sub.step_factor,
        time_running = sub.time_running,
        score = sub.score,
        submitted_at = sub.submitted_at
    )

@router.get(
    "/{id}", 
    response_model=SubmissionResponse,
    status_code=200,
    summary="Get submission by ID",
    description="Retrieve a specific submission by its ID."
)
async def get_submission(
    id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user)
):
    '''Get a specific submission by its ID.'''
    result = await db.execute(select(Submission).where(Submission.problem_id == id, Submission.user_id == user.id))
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    return SubmissionResponse(
        user_id = sub.user_id,
        problem_id = sub.problem_id,
        pair_count = sub.pair_count,
        step_count = sub.step_count,
        step_factor = sub.step_factor,
        time_running = sub.time_running,
        score = sub.score,
        submitted_at = sub.submitted_at
    )
