from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import ShortLink
from app.utils import generate_short_url


class URLShortenerService:
    def __init__(self, db: Session):
        self.db = db

    def create_short_url(self, original_url: str, ttl_hours: int = 24) -> str:
        expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)

        while True:
            code = generate_short_url()

            link = ShortLink(
                code=code, url=original_url, clicks=0, expires_at=expires_at
            )
            self.db.add(link)

            try:
                self.db.commit()
                return code
            except IntegrityError:
                self.db.rollback()

    def get_original_url(self, code: str) -> str | None:
        link = self.db.query(ShortLink).filter(ShortLink.code == code).first()

        if not link:
            return None

        if link.expires_at and link.expires_at < datetime.utcnow():
            return None

        link.clicks += 1
        self.db.commit()

        return link.url

    def get_stats(self, code: str) -> dict | None:
        link = self.db.query(ShortLink).filter(ShortLink.code == code).first()

        if not link:
            return None

        if link.expires_at and link.expires_at < datetime.utcnow():
            return None

        return {"clicks": link.clicks}

    def cleanup_expired_links(self) -> int:
        deleted = (
            self.db.query(ShortLink)
            .filter(
                ShortLink.expires_at.is_not(None),
                ShortLink.expires_at < datetime.utcnow(),
            )
            .delete(synchronize_session=False)
        )

        self.db.commit()
        return deleted
