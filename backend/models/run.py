from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database import (
    Base,
)


class Run(Base):
    __tablename__ = "runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    run_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    result: Mapped[str] = mapped_column(String, nullable=False)
    checks: Mapped[int] = mapped_column(Integer)
    overall_coverage: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    uploaded_by: Mapped[str] = mapped_column(String)
    coverpoints = relationship(
        "Coverpoint",
        back_populates="run",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
