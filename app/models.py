from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ShortLink(Base):
    __tablename__ = "short_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    clicks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
