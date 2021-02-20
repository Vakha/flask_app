from typing import List

from flask import make_response, abort

from shepherd import product_calculator, service
from shepherd.model import LabYak, Order, OrderStatus


def labyak_to_view(labyak: LabYak, day: int) -> dict:
    latest_shaving = product_calculator.latest_shaving_day(labyak, day)
    return {
        'name': labyak.name,
        'age': (labyak.age_in_days + day) / 100,
        'age-last-shaved': (labyak.age_in_days + latest_shaving) / 100
    }


def read_all_labyaks(day: int):
    labyaks = service.find_all_labyaks()
    return {
        'herd': [labyak_to_view(labyak, day) for labyak in labyaks]
    }


def report_stocks(day: int) -> dict:
    report = service.in_stock_report(day)
    return {
        'milk': round(report.milk_liters, 3),
        'skins': report.skins
    }


def __validate(order: dict) -> List[str]:
    errors = []

    if order.get('customer') is None:
        errors.append('customer field is required')
    if order.get('order', {}).get('milk') is None:
        errors.append('order.milk field is required')
    if order.get('order', {}).get('skins') is None:
        errors.append('order.skins field is required')
    return errors


def place_order(order: dict, day: int):
    errors = __validate(order)

    if errors:
        errors_combined = '[' + ', '.join(errors) + ']'
        abort(400, f'Invalid request! Errors found: {errors_combined}')

    placed_order = service.place_order(
        customer_id=order['customer'],
        milk=order['order']['milk'],
        skins=order['order']['skins'],
        day=day
    )

    res = {
        'milk': placed_order.milk_allocated,
        'skins': placed_order.skins_allocated,
    }

    if placed_order.status == OrderStatus.succeeded:
        return make_response(res, 201)
    if placed_order.status == OrderStatus.partially_succeeded:
        return make_response(res, 206)
    abort(404, 'Not enough resources in stock')


def order_to_view(order: Order) -> dict:
    return {
        'customer': order.customer_id,
        'status': order.status.value,
        'requested': {
            'milk': order.milk_requested,
            'skins': order.skins_requested,
        },
        'allocated': {
            'milk': order.milk_allocated,
            'skins': order.skins_allocated,
        },
    }


def find_orders(day: int):
    orders = service.find_orders_by_day(day)
    orders_view = [order_to_view(order) for order in orders]
    return orders_view


