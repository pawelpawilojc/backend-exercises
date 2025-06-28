from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import Survey, Question, Answer
from database import get_connection

router = APIRouter()


@router.post("/surveys", response_model=Survey)
async def create_survey(survey: Survey):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute(
            "INSERT INTO surveys (title, description, created_at) VALUES (%s, %s, NOW())",
            (survey.title, survey.description)
        )
        survey.id = cursor.lastrowid
        for question in survey.questions:
            await cursor.execute(
                "INSERT INTO questions (survey_id, question_text) VALUES (%s, %s)",
                (survey.id, question.question_text)
            )
            question.id = cursor.lastrowid
    conn.close()
    return survey


@router.post("/surveys/{survey_id}/questions")
async def add_questions(survey_id: int, questions: List[Question]):
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT id FROM surveys WHERE id = %s", (survey_id,))
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Survey not found")

            for question in questions:
                await cursor.execute(
                    "INSERT INTO questions (survey_id, question_text) VALUES (%s, %s)",
                    (survey_id, question.question_text)
                )
                question.id = cursor.lastrowid
        return questions
    finally:
        conn.close()


@router.post("/questions/{question_id}/answers")
async def add_question_answers(question_id: int, answers: List[Answer]):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        for answer in answers:
            await cursor.execute(
                "INSERT INTO answers (question_id, answer_text) VALUES (%s, %s)",
                (question_id, answer.answer_text)
            )
    conn.close()
    return {"detail": "Answers added successfully"}


@router.post("/questions/{question_id}/select-answer/{answer_id}")
async def select_answer(question_id: int, answer_id: int):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute(
            "UPDATE answers SET votes = votes + 1 WHERE id = %s AND question_id = %s",
            (answer_id, question_id)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Answer not found")
    conn.close()
    return {"detail": "Answer selected successfully"}


@router.get("/surveys/{survey_id}/basic", response_model=Survey)
async def get_survey_basic(survey_id: int):
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT id, title, description FROM surveys WHERE id = %s",
                (survey_id,)
            )
            survey_row = await cursor.fetchone()
            if not survey_row:
                raise HTTPException(status_code=404, detail="Survey not found")

            survey = Survey(
                id=survey_row[0], title=survey_row[1], description=survey_row[2], questions=[
                ]
            )

            await cursor.execute(
                "SELECT q.id, q.question_text, a.id, a.answer_text "
                "FROM questions q LEFT JOIN answers a ON q.id = a.question_id "
                "WHERE q.survey_id = %s ORDER BY q.id, a.id", (survey_id,)
            )

            rows = await cursor.fetchall()
            questions = {}
            for row in rows:
                question_id, question_text, answer_id, answer_text = row
                if question_id not in questions:
                    questions[question_id] = Question(
                        id=question_id, question_text=question_text)
                    questions[question_id].answers = []
                if answer_id:

                    answer = Answer(
                        id=answer_id,
                        question_id=question_id,
                        answer_text=answer_text
                    )
                    questions[question_id].answers.append(answer)

            survey.questions = list(questions.values())
        return survey
    finally:
        conn.close()


@router.get("/surveys/{survey_id}/results")
async def get_survey_results(survey_id: int):
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT q.id AS question_id, q.question_text, a.id AS answer_id, a.answer_text, a.votes "
                "FROM questions q LEFT JOIN answers a ON q.id = a.question_id "
                "WHERE q.survey_id = %s", (survey_id,)
            )
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            result = {}
            for row in rows:
                row_dict = dict(zip(column_names, row))
                question_id = row_dict["question_id"]

                if question_id not in result:
                    result[question_id] = {
                        "question_id": question_id,
                        "question_text": row_dict["question_text"],
                        "answers": []
                    }

                if row_dict["answer_id"]:
                    result[question_id]["answers"].append({
                        "answer_id": row_dict["answer_id"],
                        "answer_text": row_dict["answer_text"],
                        "votes": row_dict["votes"]
                    })

        return list(result.values())
    finally:
        conn.close()
