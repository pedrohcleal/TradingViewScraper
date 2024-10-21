from pydantic import BaseModel

class IndicatorDTO(BaseModel):
    pair: str
    interval: str
    register_time: str
    name: str
    value: float | None
    action: str | None


class PivotDTO(BaseModel):
    pair: str
    interval: str
    register_time: str
    pivot: str
    classic: float | None
    fibo: float | None
    camarilla: float | None
    woodie: float | None
    dm: float | None