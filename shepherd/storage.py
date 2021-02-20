from typing import List

from shepherd.db import get_db
from shepherd.model import LabYak, Sex, Order, StockReport
from shepherd.records import labyak_to_model, order_to_model, order_to_record


def find_all_labyaks() -> List[LabYak]:
    db = get_db()
    labyaks_from_db = db.execute(
        'SELECT name, age, sex '
        'FROM labyak '
        'ORDER BY name'
    ).fetchall()

    return [labyak_to_model(record) for record in labyaks_from_db]


def save_order(order: Order):
    db = get_db()
    db.execute(
        'INSERT INTO orders ('
        '    customer_id,'
        '    day,'
        '    milk_requested,'
        '    skins_requested,'
        '    milk_allocated,'
        '    skins_allocated,'
        '    status'
        ') '
        'VALUES (?, ?, ?, ?, ?, ?, ?)',
        order_to_record(order)
    )
    db.commit()


def find_orders_by_day(day: int) -> List[Order]:
    db = get_db()
    records = db.execute(
        'SELECT customer_id, day, milk_requested, skins_requested, milk_allocated, skins_allocated, status '
        'FROM orders '
        'WHERE day = ?',
        (day,)
    ).fetchall()

    return [order_to_model(record) for record in records]


def stock_allocated(day: int) -> StockReport:
    db = get_db()
    results = db.execute(
        'SELECT coalesce(sum(milk_allocated), 0) AS milk, '
        '       coalesce(sum(skins_allocated), 0) AS skins '
        'FROM orders '
        'WHERE day <= ?',
        (day,)
    ).fetchone()
    return StockReport(
        day=day,
        milk_liters=results['milk'],
        skins=results['skins']
    )
