from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    event,
    func,
)
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship

engine = create_engine("sqlite:///db/app.db", connect_args={"check_same_thread": False})
event.listen(
    engine, "connect", lambda conn, rec: conn.execute("PRAGMA foreign_keys=ON")
)


class Base(DeclarativeBase):
    pass


class Run(Base):
    __tablename__ = "runs"
    id = mapped_column(Integer, primary_key=True)
    filename = mapped_column(String, nullable=False)
    run_date = mapped_column(DateTime, nullable=False, index=True)
    result = mapped_column(String, nullable=False)
    checks = mapped_column(Integer)
    overall_coverage = mapped_column(Numeric(5, 2))
    uploaded_at = mapped_column(DateTime, server_default=func.now())
    uploaded_by = mapped_column(String)
    coverpoints = relationship(
        "Coverpoint", back_populates="run", cascade="all, delete-orphan"
    )


class Coverpoint(Base):
    __tablename__ = "coverpoints"
    id = mapped_column(Integer, primary_key=True)
    run_id = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"))
    name = mapped_column(String, nullable=False)
    coverage = mapped_column(Numeric(5, 2))
    run = relationship("Run", back_populates="coverpoints")
    bins = relationship(
        "Bin", back_populates="coverpoint", cascade="all, delete-orphan"
    )


class Bin(Base):
    __tablename__ = "bins"
    id = mapped_column(Integer, primary_key=True)
    coverpoint_id = mapped_column(ForeignKey("coverpoints.id", ondelete="CASCADE"))
    name = mapped_column(String, nullable=False)
    value = mapped_column(String)
    hits = mapped_column(Integer, nullable=False)
    hit = mapped_column(Boolean, nullable=False)
    coverpoint = relationship("Coverpoint", back_populates="bins")
