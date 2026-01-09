from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from app.schemas import ShortenRequest, ShortenResponse
from app.services import URLShortenerService

app = FastAPI()

url_storage = {}
service = URLShortenerService(url_storage)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/shorten", response_model=ShortenResponse)
def shorten_url(request: ShortenRequest) -> dict:
    code = service.create_short_url(str(request.url))
    return {"short_url": code}


@app.get("/{code}")
def redirect(code: str):
    original_url = service.get_original_url(code)

    if not original_url:
        raise HTTPException(status_code=404, detail="Short link not found")

    return RedirectResponse(original_url)
