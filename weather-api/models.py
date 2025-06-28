from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WeatherSearch(BaseModel):
    city: str
    country: Optional[str] = None


class WeatherData(BaseModel):
    city: str
    country: Optional[str] = None
    temperature: float
    description: str
    humidity: Optional[int] = None
    wind_speed: Optional[float] = None
    searched_at: Optional[datetime] = None
    id: Optional[int] = None
