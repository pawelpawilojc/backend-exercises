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

## URL Shortener Application

### Key Endpoints
- `POST /shorten`: Create a shortened URL from a long URL
- `GET /{short_code}`: Redirect to the original URL
- `GET /info/{short_code}`: Get information about a shortened URL

### Technical Details
- Uses a 7-character short code: letters and digits
- Excludes similarly shaped characters: 0, O, 1, l, I, 5, S, 8, B
- Total possible combinations: 52^7

### Screenshots
#### Database
![Database](/url-shortener/screenshots/database.png)

#### Uvicorn
![Uvicorn](/url-shortener/screenshots/uvicorn.png)

#### Redirect
https://github.com/user-attachments/assets/6a74d375-f926-4b8d-9d48-de325270096e

## Weather API Application

### Key Endpoints
- `GET /weather?city={city}&country={country}`: Get current weather for a city
- `GET /history?limit={limit}`: Get search history (default limit: 10)

### Environment Variables
In addition to database credentials, you need to set:
- `OPENWEATHER_API_KEY`: Your API key from OpenWeatherMap

### Screenshots
#### Database
![Database](/weather-api/screenshots/database.png)

#### Uvicorn
![Uvicorn](/weather-api/screenshots/uvicorn.png)

#### History API response
![weather history](/weather-api/screenshots/history-response.png)