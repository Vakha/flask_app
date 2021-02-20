from shepherd.model import LabYak, Sex, OrderStatus, Order


def labyak_to_model(record) -> LabYak:
    return LabYak(
        name=record['name'],
        age_in_days=record['age'],
        sex=Sex.male if record['sex'] else Sex.female,
    )


__status_to_model = {
    1: OrderStatus.succeeded,
    2: OrderStatus.partially_succeeded,
    3: OrderStatus.failed,
}

__status_to_record = {v: k for k, v in __status_to_model.items()}


def __status_id_to_model(status_id: int) -> OrderStatus:
    model = __status_to_model.get(status_id)
    if model is None:
        raise Exception(f'Unknown order status {status_id}')
    return model


def order_to_model(record) -> Order:
    return Order(
        customer_id=record['customer_id'],
        day=record['day'],
        milk_requested=record['milk_requested'],
        skins_requested=record['skins_requested'],
        milk_allocated=record['milk_allocated'],
        skins_allocated=record['skins_allocated'],
        status=__status_id_to_model(record['status'])
    )


def order_to_record(order: Order) -> tuple:
    return (
        order.customer_id,
        order.day,
        order.milk_requested,
        order.skins_requested,
        order.milk_allocated,
        order.skins_allocated,
        __status_to_record[order.status]
    )
