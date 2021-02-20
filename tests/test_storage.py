import sqlite3
import pytest

from shepherd import storage
from shepherd.db import get_db
from shepherd.model import LabYak, Sex, Order, OrderStatus

test_herd = [
    LabYak("Betty-1", 400, Sex.female),
    LabYak("Betty-2", 800, Sex.female),
    LabYak("Betty-3", 950, Sex.female),
]

test_orders = [
    Order('Frodo', 14, 1100, 3, 1100, 3, OrderStatus.succeeded),
    Order('Sam', 14, 1200, 3, 0, 3, OrderStatus.partially_succeeded),
    Order('Pipin', 14, 2000, 13, 0, 0, OrderStatus.failed),
    Order('Merry', 40, 1000, 1, 1000, 1, OrderStatus.succeeded),
]


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('shepherd.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called


def test_find_all_labyaks(app):
    with app.app_context():
        assert storage.find_all_labyaks() == test_herd


def test_find_orders_by_day(app):
    with app.app_context():
        orders_14 = [o for o in test_orders if o.day == 14]
        orders_40 = [o for o in test_orders if o.day == 40]

        assert storage.find_orders_by_day(13) == []
        assert storage.find_orders_by_day(14) == orders_14
        assert storage.find_orders_by_day(40) == orders_40


def test_save_order(app):
    with app.app_context():
        to_save = Order('Bilbo', 111, 2222.002, 22, 1110.001, 11, OrderStatus.succeeded)
        storage.save_order(to_save)
        saved = storage.find_orders_by_day(111)[0]
        assert saved == to_save


@pytest.mark.parametrize(('day', 'milk', 'skins'), (
        (0, 0, 0),
        (13, 0, 0),
        (14, 1100, 6),
        (15, 1100, 6),
        (40, 2100, 7),
))
def test_stock_allocated_one_day(app, day, milk, skins):
    with app.app_context():
        allocated = storage.stock_allocated(day)
        assert allocated.day == day
        assert allocated.milk_liters == milk
        assert allocated.skins == skins
