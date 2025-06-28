# Backend Exercises

This repository contains backend projects built with FastAPI and MySQL.

## To-Do List Application

### Environment Variables
Create a `.env` file in `todo-list` with the following variables:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=<your_mysql_username>
DB_PASSWORD=<your_mysql_password>
DB_NAME=todo_db
```

### Installation
   ```bash
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

