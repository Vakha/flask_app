import pytest

from shepherd.exceptions import NegativeValueException
from shepherd.model import Sex, LabYak, StockReport, Order, OrderStatus
from shepherd import service, EmptyOrderException


def __dummy_order() -> Order:
    return Order(
        customer_id='me',
        day=25,
        milk_requested=111.1,
        skins_requested=2,
        milk_allocated=111.1,
        skins_allocated=2,
        status=OrderStatus.failed
    )

def __perform_order_placing(day: int,
                            milk: float,
                            skins: int,
                            produced_stock: StockReport,
                            allocated_stock: StockReport,
                            monkeypatch) -> Order:
    saved = {'order': None}

    def fake_save_order(order):
        saved['order'] = order

    monkeypatch.setattr('shepherd.storage.find_all_labyaks', lambda: [])
    monkeypatch.setattr('shepherd.product_calculator.production_report', lambda h, d: produced_stock)

    monkeypatch.setattr('shepherd.storage.stock_allocated', lambda d: allocated_stock)
    monkeypatch.setattr('shepherd.storage.save_order', fake_save_order)

    order = service.place_order('me', milk, skins, day)

    assert order == saved['order']
    assert order.customer_id == 'me'
    assert order.milk_requested == milk
    assert order.skins_requested == skins
    return order


def test_place_order_successfully(monkeypatch):
    day = 13
    milk = 1100
    skins = 3
    produced_stock = StockReport(day, 1100, 3)
    allocated_stock = StockReport(day, 0, 0)

    order = __perform_order_placing(
        day=day,
        milk=milk,
        skins=skins,
        produced_stock=produced_stock,
        allocated_stock=allocated_stock,
        monkeypatch=monkeypatch
    )

    assert order.milk_allocated == milk
    assert order.skins_allocated == skins
    assert order.status == OrderStatus.succeeded


def test_place_order_successfully_when_zero_milk_is_ordered(monkeypatch):
    day = 13
    milk = 0
    skins = 3
    produced_stock = StockReport(day, 1100, 3)
    allocated_stock = StockReport(day, 0, 0)

    order = __perform_order_placing(
        day=day,
        milk=milk,
        skins=skins,
        produced_stock=produced_stock,
        allocated_stock=allocated_stock,
        monkeypatch=monkeypatch
    )

    assert order.milk_allocated == milk
    assert order.skins_allocated == skins
    assert order.status == OrderStatus.succeeded


def test_place_order_successfully_when_zero_skins_is_ordered(monkeypatch):
    day = 13
    milk = 1100
    skins = 0
    produced_stock = StockReport(day, 1100, 3)
    allocated_stock = StockReport(day, 0, 0)

    order = __perform_order_placing(
        day=day,
        milk=milk,
        skins=skins,
        produced_stock=produced_stock,
        allocated_stock=allocated_stock,
        monkeypatch=monkeypatch
    )

    assert order.milk_allocated == milk
    assert order.skins_allocated == skins
    assert order.status == OrderStatus.succeeded


def test_place_order_successfully_with_previously_allocated_stocks(monkeypatch):
    day = 13
    milk = 1100
    skins = 3
    produced_stock = StockReport(day, 2200, 6)
    allocated_stock = StockReport(day, 1100, 3)

    order = __perform_order_placing(
        day=day,
        milk=milk,
        skins=skins,
        produced_stock=produced_stock,
        allocated_stock=allocated_stock,
        monkeypatch=monkeypatch
    )

    assert order.milk_allocated == milk
    assert order.skins_allocated == skins
    assert order.status == OrderStatus.succeeded


def test_place_order_when_not_enough_milk(monkeypatch):
    day = 13
    milk = 1100.5
    skins = 3
    produced_stock = StockReport(day, 2200, 6)
    allocated_stock = StockReport(day, 1100, 3)

    order = __perform_order_placing(
        day=day,
        milk=milk,
        skins=skins,
        produced_stock=produced_stock,
        allocated_stock=allocated_stock,
        monkeypatch=monkeypatch
    )

    assert order.milk_allocated == 0
    assert order.skins_allocated == skins
    assert order.status == OrderStatus.partially_succeeded


def test_place_order_when_not_enough_skins(monkeypatch):
    day = 13
    milk = 1100
    skins = 4
    produced_stock = StockReport(day, 2200, 6)
    allocated_stock = StockReport(day, 1100, 3)

    order = __perform_order_placing(
        day=day,
        milk=milk,
        skins=skins,
        produced_stock=produced_stock,
        allocated_stock=allocated_stock,
        monkeypatch=monkeypatch
    )

    assert order.milk_allocated == milk
    assert order.skins_allocated == 0
    assert order.status == OrderStatus.partially_succeeded


def test_place_order_unsuccessfully(monkeypatch):
    day = 13
    milk = 1100.5
    skins = 4
    produced_stock = StockReport(day, 2200, 6)
    allocated_stock = StockReport(day, 1100, 3)

    order = __perform_order_placing(
        day=day,
        milk=milk,
        skins=skins,
        produced_stock=produced_stock,
        allocated_stock=allocated_stock,
        monkeypatch=monkeypatch
    )

    assert order.milk_allocated == 0
    assert order.skins_allocated == 0
    assert order.status == OrderStatus.failed


def test_raise_exception_on_empty_order():
    with pytest.raises(EmptyOrderException):
        service.place_order('me', 0, 0,1)


def test_raise_exception_on_negative_milk_amount():
    with pytest.raises(NegativeValueException):
        service.place_order('me', -1, 1, 1)


def test_raise_exception_on_negative_skins_amount():
    with pytest.raises(NegativeValueException):
        service.place_order('me', 1, -1, 1)


def test_find_orders_by_day(monkeypatch):
    day = 32
    expected_orders = [__dummy_order(), __dummy_order()]

    def fake_find_orders_by_day(_day):
        assert _day == day
        return expected_orders

    monkeypatch.setattr('shepherd.storage.find_orders_by_day', fake_find_orders_by_day)

    actual_orders = service.find_orders_by_day(day)
    assert actual_orders == expected_orders


def test_in_stock_report(monkeypatch):
    day = 23
    produced_stock = StockReport(day, 2200, 6)
    allocated_stock = StockReport(day, 1000, 2)

    monkeypatch.setattr('shepherd.storage.find_all_labyaks', lambda: [])
    monkeypatch.setattr('shepherd.product_calculator.production_report', lambda h, d: produced_stock)
    monkeypatch.setattr('shepherd.storage.stock_allocated', lambda d: allocated_stock)

    report = service.in_stock_report(day)
    assert report == StockReport(day, 1200, 4)
