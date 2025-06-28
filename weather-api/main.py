from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import weather
from database import connect_to_database, disconnect_from_database, get_connection
import os

app = FastAPI(title="Weather API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await connect_to_database()
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            sql_file_path = os.path.join(
                os.path.dirname(__file__), "sql", "init.sql")
            with open(sql_file_path, "r") as sql_file:
                sql_script = sql_file.read()
            for statement in sql_script.split(";"):
                if statement.strip():
                    await cursor.execute(statement)
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()


@app.on_event("shutdown")
async def shutdown():
    await disconnect_from_database()


app.include_router(weather.router)
