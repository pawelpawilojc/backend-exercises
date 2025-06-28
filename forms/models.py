from pydantic import BaseModel
from typing import Optional, List


class Answer(BaseModel):
    id: Optional[int] = None
    question_id: int
    answer_text: str
    votes: Optional[int] = 0


class Question(BaseModel):
    id: Optional[int] = None
    question_text: str
    answers: Optional[List[Answer]] = None


class Survey(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    questions: List[Question]
