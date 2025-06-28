import aiomysql
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

db_pool = None


async def connect_to_database():
    global db_pool
    db_pool = await aiomysql.create_pool(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", ""),
        password=os.getenv("DB_PASSWORD", ""),
        db=os.getenv("DB_NAME", "weather_db"),
        autocommit=True
    )


async def disconnect_from_database():
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()


async def get_connection():
    if not db_pool:
        raise HTTPException(
            status_code=500, detail="Database connection not initialized")
    return await db_pool.acquire()
