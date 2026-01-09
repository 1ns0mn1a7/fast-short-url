from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services import URLShortenerService


def run_cleanup():
    db: Session = SessionLocal()
    try:
        service = URLShortenerService(db)
        deleted = service.cleanup_expired_links()
        print(f"Cleanup completed. Deleted {deleted} expired links.")
    finally:
        db.close()


if __name__ == "__main__":
    run_cleanup()
