from datetime import datetime
from decimal import Decimal

from pydantic.config import ConfigDict
from pydantic.main import BaseModel

from .coverpoint import CoverpointOut


class RunSummary(BaseModel):
    id: int
    filename: str
    run_date: datetime
    result: str
    overall_coverage: Decimal
    model_config = ConfigDict(from_attributes=True)


class RunDetail(RunSummary):
    checks: int
    uploaded_at: datetime
    uploaded_by: str | None
    total_bins: int
    missed_bins: int
    coverpoints: list[CoverpointOut] = []
    model_config = ConfigDict(from_attributes=True)


class RunListParams(BaseModel):
    limit: int = 20
    offset: int = 0
    result: str | None = None
    min_coverage: float | None = None
