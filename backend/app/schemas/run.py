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
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "filename": "96_25_overall_FCOV.txt",
                "run_date": "2026-06-15T10:38:36",
                "result": "PASSED",
                "overall_coverage": "96.25",
            }
        },
    )


class RunDetail(RunSummary):
    checks: int
    uploaded_at: datetime
    uploaded_by: str | None
    total_bins: int
    missed_bins: int
    coverpoints: list[CoverpointOut] = []
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "filename": "96_25_overall_FCOV.txt",
                "run_date": "2026-06-15T10:38:36",
                "result": "PASSED",
                "overall_coverage": "96.25",
                "checks": 37,
                "uploaded_at": "2026-07-08T09:46:27",
                "uploaded_by": None,
                "total_bins": 29,
                "missed_bins": 3,
                "coverpoints": [],
            }
        },
    )


class RunListParams(BaseModel):
    limit: int = 20
    offset: int = 0
    result: str | None = None
    min_coverage: float | None = None
