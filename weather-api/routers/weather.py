from fastapi import APIRouter, HTTPException, Depends
import httpx
import os
from typing import List, Optional
from models import WeatherSearch, WeatherData
from database import get_connection
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@router.get("/weather", response_model=WeatherData)
async def get_weather(city: str, country: Optional[str] = None):
    #
    params = {
        "q": city if not country else f"{city},{country}",
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:

        async with httpx.AsyncClient() as client:
            response = await client.get(OPENWEATHER_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        weather_data = WeatherData(
            city=data["name"],
            country=data["sys"]["country"] if "country" in data["sys"] else None,
            temperature=data["main"]["temp"],
            description=data["weather"][0]["description"],
            humidity=data["main"]["humidity"],
            wind_speed=data["wind"]["speed"]
        )

        conn = await get_connection()
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO searches (city, country, temperature, description, humidity, wind_speed)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        weather_data.city,
                        weather_data.country,
                        weather_data.temperature,
                        weather_data.description,
                        weather_data.humidity,
                        weather_data.wind_speed
                    )
                )
                weather_data.id = cursor.lastrowid
        finally:
            conn.close()

        return weather_data

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="City not found")
        else:
            raise HTTPException(
                status_code=500, detail=f"Error fetching weather data: {str(e)}")


@router.get("/history", response_model=List[WeatherData])
async def get_search_history(limit: int = 10):
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                """
                SELECT id, city, country, temperature, description, humidity, wind_speed, searched_at
                FROM searches
                ORDER BY searched_at DESC
                LIMIT %s
                """,
                (limit,)
            )
            rows = await cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            return [dict(zip(column_names, row)) for row in rows]
    finally:
        conn.close()
