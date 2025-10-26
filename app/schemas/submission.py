from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Operation(BaseModel):
    x: int
    y: int
    n: int

class ProblemField(BaseModel):
    size: int
    entities: List[List[int]]

class SubmissionCreate(BaseModel):
    problem_id: Optional[int] = Field(None, example=0)
    ops: List[Operation] = Field(None, description="List of operations to be submitted.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "problem_id": 0,
                    "ops": [
                        {"x": 0, "y": 0, "n": 2},
                        {"x": 2, "y": 2, "n": 2}
                    ]
                }
            ]
        }
    }

class SubmissionResponse(BaseModel):
    user_id: int
    problem_id: int
    pair_count: int
    step_count: int
    step_factor: float
    time_running: float
    score: float
    submitted_at: datetime
