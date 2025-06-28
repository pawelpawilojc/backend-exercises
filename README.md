# Backend Exercises

## Overview

This repository contains a collection of backend API exercises built with **FastAPI** and **MySQL**. The exercises cover: REST API development, database connectivity, CRUD operations, API documentation, environment configuration, and working with relational databases.

These exercises were completed as part of my **Backend** course at **DSW University of Lower Silesia (Uniwersytet Dolnośląski DSW)**.

### Environment Variables
Create a `.env` file in `project-folder` with the following variables:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=<your_mysql_username>
DB_PASSWORD=<your_mysql_password>
DB_NAME=<project_db>
```

### Installation
Installation is similar for each project
   ```bash
   cd project-folder
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
The application will be accessible at `http://127.0.0.1:8000`.

### API Documentation
FastAPI provides interactive API documentation:
- Swagger UI: `http://127.0.0.1:8000/docs`


## To-Do List Application

### Key Endpoints
- `POST /tasks`: Create a new task
- `GET /tasks`: Get tasks with optional filters (status, priority) and sorting
- `PUT /tasks/{task_id}`: Update a task
- `DELETE /tasks/{task_id}`: Delete a task

### Screenshots
#### Database
![Database](/todo-list/screenshots/todo_db.png)

#### Uvicorn
![Uvicorn](/todo-list/screenshots/uvicorn.png)

## Forms/Survey Application

### Key Endpoints
- `POST /surveys`: Create a new survey with questions
- `POST /surveys/{survey_id}/questions`: Add questions to an existing survey
- `POST /questions/{question_id}/answers`: Add answer options to a question
- `POST /questions/{question_id}/select-answer/{answer_id}`: Vote for an answer
- `GET /surveys/{survey_id}/basic`: Get survey details without vote counts
- `GET /surveys/{survey_id}/results`: Get survey results with vote statistics

### Screenshots
#### Database
![Database](/forms/screenshots/database.png)

#### Uvicorn
![Uvicorn](/forms/screenshots/uvicorn.png)

#### Survey result API response
![Survey result](/forms/screenshots/survey_result.png)
