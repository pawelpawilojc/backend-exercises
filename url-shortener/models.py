from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class URLBase(BaseModel):
    original_url: HttpUrl


class URLCreate(URLBase):
    pass


class URL(URLBase):
    id: int
    short_code: str
    created_at: Optional[datetime] = None
    access_count: int = 0


class URLInfo(URL):
    short_url: str
