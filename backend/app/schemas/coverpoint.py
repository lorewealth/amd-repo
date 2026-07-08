from pydantic.config import ConfigDict
from pydantic.main import BaseModel

from .bin import BinOut


class CoverpointOut(BaseModel):
    name: str
    coverage: float
    total_bins: int
    missed_bins: int
    bins: list[BinOut] = []
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "cp_vec",
                "coverage": 81.25,
                "total_bins": 16,
                "missed_bins": 3,
                "bins": [],
            }
        },
    )
