from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import RedirectResponse
from typing import List
import random
import string
from models import URLBase, URL, URLCreate, URLInfo
from database import get_connection

router = APIRouter()


CHARACTERS = string.digits + string.ascii_letters
# Remove similarly shaped characters: 0, O, 1, l, I, 5, S, 8, B
for char in "0O1lI5S8B":
    CHARACTERS = CHARACTERS.replace(char, "")


def generate_short_code(length=7):
    """Generate a random short code for URLs."""
    return ''.join(random.choice(CHARACTERS) for _ in range(length))


@router.post("/shorten", response_model=URLInfo)
async def create_short_url(url_create: URLCreate, request: Request):
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:

            await cursor.execute(
                "SELECT id, short_code, original_url, created_at, access_count FROM urls WHERE original_url = %s",
                (str(url_create.original_url),)
            )
            existing_url = await cursor.fetchone()

            if existing_url:

                url = URL(
                    id=existing_url[0],
                    short_code=existing_url[1],
                    original_url=existing_url[2],
                    created_at=existing_url[3],
                    access_count=existing_url[4]
                )
            else:

                short_code = generate_short_code()

                while True:
                    await cursor.execute(
                        "SELECT id FROM urls WHERE short_code = %s", (
                            short_code,)
                    )
                    if not await cursor.fetchone():
                        break
                    short_code = generate_short_code()

                await cursor.execute(
                    "INSERT INTO urls (original_url, short_code) VALUES (%s, %s)",
                    (str(url_create.original_url), short_code)
                )
                url_id = cursor.lastrowid
                url = URL(
                    id=url_id,
                    short_code=short_code,
                    original_url=url_create.original_url,
                    access_count=0
                )

            base_url = str(request.base_url)
            url_info = URLInfo(
                **url.dict(),
                short_url=f"{base_url}{url.short_code}"
            )
            return url_info
    finally:
        conn.close()


@router.get("/{short_code}")
async def redirect_to_url(short_code: str):
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT original_url FROM urls WHERE short_code = %s",
                (short_code,)
            )
            result = await cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="URL not found")

            original_url = result[0]

            await cursor.execute(
                "UPDATE urls SET access_count = access_count + 1 WHERE short_code = %s",
                (short_code,)
            )

            return RedirectResponse(url=original_url)
    finally:
        conn.close()


@router.get("/info/{short_code}", response_model=URL)
async def get_url_info(short_code: str):
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT id, original_url, short_code, created_at, access_count FROM urls WHERE short_code = %s",
                (short_code,)
            )
            result = await cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="URL not found")

            return URL(
                id=result[0],
                original_url=result[1],
                short_code=result[2],
                created_at=result[3],
                access_count=result[4]
            )
    finally:
        conn.close()
