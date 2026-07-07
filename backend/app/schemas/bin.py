from pydantic.config import ConfigDict
from pydantic.main import BaseModel


class BinOut(BaseModel):
    name: str
    value: str | None
    hits: int
    hit: bool
    model_config = ConfigDict(from_attributes=True)
