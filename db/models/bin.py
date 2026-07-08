from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..base import Base


class Bin(Base):
    __tablename__ = "bins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    coverpoint_id: Mapped[int] = mapped_column(
        ForeignKey("coverpoints.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(String)
    hits: Mapped[int] = mapped_column(Integer, nullable=False)
    hit: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coverpoint = relationship("Coverpoint", back_populates="bins")
