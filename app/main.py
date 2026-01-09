from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.schemas import ShortenRequest, ShortenResponse
from app.db import get_db
from app.services import URLShortenerService


app = FastAPI()


def get_service(db: Session = Depends(get_db)):
    return URLShortenerService(db)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/shorten", response_model=ShortenResponse)
def shorten_url(
    request: ShortenRequest,
    service: URLShortenerService = Depends(get_service),
):
    code = service.create_short_url(str(request.url))
    return {"short_url": code}


@app.get("/{code}")
def redirect(
    code: str,
    service: URLShortenerService = Depends(get_service),
):
    original_url = service.get_original_url(code)

    if not original_url:
        raise HTTPException(status_code=404, detail="Short link not found")

    return RedirectResponse(original_url)


@app.get("/{code}/stats")
def stats(
    code: str,
    service: URLShortenerService = Depends(get_service),
):
    stats = service.get_stats(code)

    if not stats:
        raise HTTPException(status_code=404, detail="Short link not found")

    return {"code": code, **stats}
