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


class financialDTO(BaseModel):
    pair: str
    price: float
    oscillators: list[IndicatorDTO]
    moving_averages: list[IndicatorDTO]
    pivots: list[PivotDTO]
