from sqlalchemy import String, Integer, ForeignKey, Float, UniqueConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.models.base import Base, TimestampMixin


class Recognition(Base, TimestampMixin):
    __tablename__ = "recognitions"
    __table_args__ = (
        UniqueConstraint("image_id", "model", name="uq_image_model"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_id: Mapped[int] = mapped_column(Integer, ForeignKey("images.id", ondelete="CASCADE"))
    label_en: Mapped[str] = mapped_column(String(255))
    label_zh: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default="")
    phonetic: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default="")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    model: Mapped[str] = mapped_column(String(128))
    raw_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")

    image = relationship("Image")