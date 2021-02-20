from typing import List

from shepherd.exceptions import EmptyOrderException, NegativeValueException
from shepherd.model import Order
from shepherd import product_calculator
from shepherd.model import LabYak, Sex, StockReport, Order, OrderStatus
from shepherd import storage


def __define_order_status(order: Order):
    not_allocated_milk = order.milk_requested - order.milk_allocated
    not_allocated_skins = order.skins_requested - order.skins_allocated

    if not_allocated_milk == 0 and not_allocated_skins == 0:
        return OrderStatus.succeeded

    if not_allocated_milk > 0 and not_allocated_skins > 0:
        return OrderStatus.failed

    return OrderStatus.partially_succeeded


def place_order(customer_id: str, milk: float, skins: int, day: int) -> Order:
    if milk < 0 or skins < 0:
        raise NegativeValueException()
    if milk <= 0 and skins <= 0:
        raise EmptyOrderException()

    stock_left = in_stock_report(day)
    prepared_order = Order(
        customer_id=customer_id,
        day=day,
        milk_requested=milk,
        skins_requested=skins,
    )

    if stock_left.milk_liters >= prepared_order.milk_requested:
        prepared_order.milk_allocated = prepared_order.milk_requested

    if stock_left.skins >= prepared_order.skins_requested:
        prepared_order.skins_allocated = prepared_order.skins_requested

    prepared_order.status = __define_order_status(prepared_order)

    storage.save_order(prepared_order)

    return prepared_order


def find_orders_by_day(day: int) -> List[Order]:
    return storage.find_orders_by_day(day)


def find_all_labyaks() -> List[LabYak]:
    return storage.find_all_labyaks()


def in_stock_report(day: int) -> StockReport:
    labyaks = storage.find_all_labyaks()
    report = product_calculator.production_report(labyaks, day)
    allocated_already = storage.stock_allocated(day)
    return StockReport(
        day=day,
        milk_liters=report.milk_liters - allocated_already.milk_liters,
        skins=report.skins - allocated_already.skins
    )
