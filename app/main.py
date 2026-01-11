from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.schemas import ShortenRequest, ShortenResponse
from app.db import get_db
from app.services import URLShortenerService


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_service(db: Session = Depends(get_db)):
    return URLShortenerService(db)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/shorten", response_model=ShortenResponse)
def shorten_url(
    request: ShortenRequest,
    background_tasks: BackgroundTasks,
    service: URLShortenerService = Depends(get_service),
):
    code = service.create_short_url(
        str(request.url),
        ttl_hours=settings.default_ttl_hours,
    )

    background_tasks.add_task(service.cleanup_expired_links)

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
