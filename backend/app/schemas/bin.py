from pydantic.config import ConfigDict
from pydantic.main import BaseModel


class BinOut(BaseModel):
    name: str
    value: str | None
    hits: int
    hit: bool
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "vec[ 9]",
                "value": "1001",
                "hits": 0,
                "hit": False,
            }
        },
    )
