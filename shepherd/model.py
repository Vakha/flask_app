from dataclasses import dataclass
from enum import Enum


class Sex(Enum):
    female = 'f'
    male = 'm'


@dataclass
class LabYak:
    name: str
    age_in_days: int
    sex: Sex


class OrderStatus(Enum):
    succeeded = 'succeeded'
    partially_succeeded = 'partially_succeeded'
    failed = 'failed'


@dataclass
class Order:
    customer_id: str
    day: int
    milk_requested: float
    skins_requested: int
    milk_allocated: float = 0
    skins_allocated: int = 0
    status: OrderStatus = OrderStatus.failed


@dataclass
class StockReport:
    day: int
    milk_liters: float
    skins: int
