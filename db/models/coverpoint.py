from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..base import Base


class Coverpoint(Base):
    __tablename__ = "coverpoints"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    coverage: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    run = relationship("Run", back_populates="coverpoints")
    bins = relationship(
        "Bin",
        back_populates="coverpoint",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
