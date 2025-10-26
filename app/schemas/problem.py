from pydantic import BaseModel, Field
from typing import List, Optional

class ListQuestionSchema(BaseModel):
    '''Schema for querying multiple questions with pagination.'''
    id: Optional[int] = Field(None, example=0)
    size: Optional[int] = Field(None, example=4)


class FieldData(BaseModel):
    '''Schema for the field data of a problem.'''
    size: Optional[int] = Field(None, example=4)
    entities: Optional[List[List[int]]] = Field(
        None,
        example=[
            [6, 3, 4, 0],
            [1, 3, 3, 3],
            [2, 7, 0, 6],
            [1, 2, 7, 4]
        ]
    )

class QuestionSchema(BaseModel):
    '''Schema for a single problem question.'''
    startsAt: Optional[int] = Field(None, example=0)
    problem: Optional[FieldData] = Field(None, description="The field data for the problem.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "startsAt": 0,
                    "problem": {
                        "size": 4,
                        "entities": [
                            [6, 3, 4, 0],
                            [1, 3, 3, 3],
                            [2, 7, 0, 6],
                            [1, 2, 7, 4]
                        ]
                    }
                }
            ]
        }
    }
