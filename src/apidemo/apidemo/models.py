from pydantic import BaseModel
from enum import Enum


class TimeInterval(str, Enum):
    m1 = "1m"
    m5 = "5m"
    min15 = "15m"
    min30 = "30m"
    h1 = "1h"
    h2 = "2h"
    h4 = "4h"
    d1 = "1D"
    w1 = "1W"
    M1 = "1M"


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


class PairRequest(BaseModel):
    pairs: list[str]
    intervals: list[TimeInterval]


# ["1m" "5m", "15m", "30m", "1h", "2h", "4h", "1D", "1W", "1M"]
