from pprint import pprint

from shepherd import EmptyOrderException
from shepherd.exceptions import NegativeValueException
from shepherd.model import Order, OrderStatus, Sex, LabYak
from shepherd.yakshopapi import order_to_view, labyak_to_view

base_url = '/yak-shop'


def __dummy_order() -> Order:
    return Order(
        customer_id='me',
        day=25,
        milk_requested=111.2,
        skins_requested=3,
        milk_allocated=111.1,
        skins_allocated=2,
        status=OrderStatus.failed
    )


def __dummy_labyak() -> LabYak:
    return LabYak("Betty-1", 400, Sex.female)


def __make_body(order: Order) -> dict:
    return {
        "customer": order.customer_id,
        "order": {
            "milk": order.milk_requested,
            "skins": order.skins_requested,
        }
    }


def __mock_place_order(order: Order, requested_day: int, monkeypatch):
    def __fake_place_order(customer_id: str, milk: float, skins: int, day: int) -> Order:
        assert customer_id == order.customer_id
        assert milk == order.milk_requested
        assert skins == order.skins_requested
        assert day == requested_day
        return order

    monkeypatch.setattr('shepherd.service.place_order', __fake_place_order)


def test_place_order_succeed(client, monkeypatch):
    day = 2
    order = __dummy_order()
    order.status = OrderStatus.succeeded
    __mock_place_order(order, day, monkeypatch)

    response = client.post(f'{base_url}/order/{day}', json=__make_body(order))

    assert response.status_code == 201
    assert response.get_json() == {'milk': order.milk_allocated,
                                   'skins': order.skins_allocated}


def test_place_order_partially_succeed(client, monkeypatch):
    day = 2
    order = __dummy_order()
    order.status = OrderStatus.partially_succeeded
    __mock_place_order(order, day, monkeypatch)

    response = client.post(f'{base_url}/order/{day}', json=__make_body(order))

    assert response.status_code == 206
    assert response.get_json() == {'milk': order.milk_allocated,
                                   'skins': order.skins_allocated}


def test_place_order_failed(client, monkeypatch):
    day = 2
    order = __dummy_order()
    order.status = OrderStatus.failed
    __mock_place_order(order, day, monkeypatch)

    response = client.post(f'{base_url}/order/{day}', json=__make_body(order))

    assert response.status_code == 404


def test_place_order_wrong_body(client, monkeypatch):
    day = 2
    order = __dummy_order()
    order.status = OrderStatus.partially_succeeded
    __mock_place_order(order, day, monkeypatch)

    response = client.post(f'{base_url}/order/{day}', json={'bla': 23})

    assert response.status_code == 400


def test_place_raise_empty_order_exception(client, monkeypatch):
    day = 2
    order = __dummy_order()
    def __fake_place_order(customer_id: str, milk: float, skins: int, day: int) -> Order:
        raise EmptyOrderException()
    monkeypatch.setattr('shepherd.service.place_order', __fake_place_order)

    response = client.post(f'{base_url}/order/{day}', json=__make_body(order))

    assert response.status_code == 400


def test_place_raise_negative_value_exception(client, monkeypatch):
    day = 2
    order = __dummy_order()
    def __fake_place_order(customer_id: str, milk: float, skins: int, day: int) -> Order:
        raise NegativeValueException()
    monkeypatch.setattr('shepherd.service.place_order', __fake_place_order)

    response = client.post(f'{base_url}/order/{day}', json=__make_body(order))

    assert response.status_code == 400


def test_order_to_view(client, monkeypatch):
    order = __dummy_order()
    view = order_to_view(order)
    assert view['customer'] == order.customer_id
    assert view['status'] == order.status.value
    assert view['requested']['milk'] == order.milk_requested
    assert view['requested']['skins'] == order.skins_requested
    assert view['allocated']['milk'] == order.milk_allocated
    assert view['allocated']['skins'] == order.skins_allocated


def test_find_orders(client, monkeypatch):
    day = 66
    order1 = __dummy_order()
    order1.customer_id = 'c1'
    order2 = __dummy_order()
    order2.customer_id = 'c2'

    def fake_order_to_view(order: Order) -> dict:
        return {'id': order.customer_id}

    monkeypatch.setattr('shepherd.service.find_orders_by_day', lambda d: [order1, order2])
    monkeypatch.setattr('shepherd.yakshopapi.order_to_view', fake_order_to_view)

    response = client.get(f'{base_url}/order/{day}')

    assert response.status_code == 200
    assert response.get_json() == [{'id': 'c1'}, {'id': 'c2'}]


def test_labyak_to_view(monkeypatch):
    day = 15
    labyak = __dummy_labyak()
    labyak.age_in_days = 400

    monkeypatch.setattr('shepherd.product_calculator.latest_shaving_day', lambda l, d: 13)

    view = labyak_to_view(labyak, day)

    assert view['name'] == labyak.name
    assert view['age'] == 4.15
    assert view['age-last-shaved'] == 4.13


def test_read_all_labyaks(client, monkeypatch):
    day = 500

    labyak1 = __dummy_labyak()
    labyak1.name = 'L1'
    labyak2 = __dummy_labyak()
    labyak2.name = 'L2'

    def fake_labyak_to_view(labyak: LabYak, _day: int) -> dict:
        assert _day == day
        return {'id': labyak.name}

    monkeypatch.setattr('shepherd.yakshopapi.labyak_to_view', fake_labyak_to_view)
    monkeypatch.setattr('shepherd.service.find_all_labyaks', lambda: [labyak1, labyak2])

    response = client.get(f'{base_url}/herd/{day}')

    assert response.status_code == 200
    assert response.get_json() == {'herd': [{'id': 'L1'}, {'id': 'L2'}]}
