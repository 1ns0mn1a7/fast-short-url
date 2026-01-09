import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from app.schemas import ShortenRequest, ShortenResponse

app = FastAPI()

url_storage = {}


""" Generate a random short URL string of given length."""
def generate_short_url(length: int = 6) -> str:
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    result = []

    for _ in range(length):
        result.append(random.choice(characters))

    return "".join(result)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/shorten", response_model=ShortenResponse)
def shorten_url(request: ShortenRequest) -> dict:
    while True:
        code = generate_short_url()
        if code not in url_storage:
            break

    url_storage[code] = str(request.url)
    return {"short_url": code}


@app.get("/{code}")
def redirect(code: str):
    original_url = url_storage.get(code)
    
    if not original_url:
        raise HTTPException(status_code=404, detail="Short link not found")
    
    return RedirectResponse(original_url)
