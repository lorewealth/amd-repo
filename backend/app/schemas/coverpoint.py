from pydantic.config import ConfigDict
from pydantic.main import BaseModel

from app.schemas.bin import BinOut


class CoverpointOut(BaseModel):
    name: str
    coverage: float
    total_bins: int
    missed_bins: int
    bins: list[BinOut] = []
    model_config = ConfigDict(from_attributes=True)
