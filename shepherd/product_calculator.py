from typing import List

from shepherd.model import LabYak, Sex, StockReport

MAX_AGE_DAYS = 1000
START_SHAVING_AGE_DAYS = 100


def __labyak_to_str(labyak: LabYak, day: int = 0) -> str:
    return f"{labyak.name} {(labyak.age_in_days + day) / 100:5.2f} years old"


def is_dead(labyak: LabYak) -> bool:
    return labyak.age_in_days >= MAX_AGE_DAYS


def milk_produced_in_a_day(age: int) -> float:
    return 50 - 0.03 * age


def milking(labyak: LabYak, day: int) -> float:
    if labyak.sex == Sex.male or is_dead(labyak):
        return 0.0

    start_milking_age = labyak.age_in_days

    stop_milking_age = labyak.age_in_days + day
    if stop_milking_age > MAX_AGE_DAYS:
        stop_milking_age = labyak.age_in_days + MAX_AGE_DAYS - labyak.age_in_days

    return sum(milk_produced_in_a_day(age) for age in range(start_milking_age, stop_milking_age))


def wool_grown_in_a_day(age: int) -> float:
    return 1 / (8 + age * 0.01)


def skins_grown(labyak: LabYak, day: int) -> int:
    if is_dead(labyak):
        return 0

    first_day_shaving = 1

    start_shaving_age = labyak.age_in_days
    if labyak.age_in_days < START_SHAVING_AGE_DAYS:
        start_shaving_age += START_SHAVING_AGE_DAYS - labyak.age_in_days

    stop_shaving_age = labyak.age_in_days + day
    if labyak.age_in_days + day > MAX_AGE_DAYS:
        stop_shaving_age = labyak.age_in_days + MAX_AGE_DAYS - labyak.age_in_days

    if stop_shaving_age < start_shaving_age:
        first_day_shaving = 0

    wool_grown_per_day = (wool_grown_in_a_day(age) for age in range(start_shaving_age, stop_shaving_age - 1))
    shavings = int(sum(wool_grown_per_day))
    return first_day_shaving + shavings


def production_report(herd: List[LabYak], day: int) -> StockReport:
    milk_produced = sum(milking(labyak, day) for labyak in herd)
    produced_skins = sum(skins_grown(labyak, day) for labyak in herd)
    return StockReport(
        day=day,
        milk_liters=milk_produced,
        skins=produced_skins
    )


def print_production_report(herd: List[LabYak], day: int) -> str:
    products = production_report(herd, day)
    herd_str = (__labyak_to_str(labyak, day) for labyak in herd)
    herd_list = '\n'.join('    ' + labyak_str for labyak_str in herd_str)
    return \
        f'In stock:\n' \
        f'    {products.milk_liters:.3f} liters of milk\n' \
        f'    {products.skins} skins of wool\n' \
        f'Herd:\n' \
        f'{herd_list}'


def shaving_schedule(labyak: LabYak) -> [int]:
    if is_dead(labyak):
        return []

    start_shaving_day = 0
    if labyak.age_in_days < START_SHAVING_AGE_DAYS:
        start_shaving_day = START_SHAVING_AGE_DAYS - labyak.age_in_days

    stop_shaving_day = MAX_AGE_DAYS - labyak.age_in_days

    shaving_days = [start_shaving_day]
    wool_grown = 0
    for day in range(start_shaving_day + 1, stop_shaving_day):
        wool_grown += wool_grown_in_a_day(labyak.age_in_days + day)
        if wool_grown >= 1:
            shaving_days.append(day)
            wool_grown = 0

    return shaving_days


def latest_shaving_day(lamyak: LabYak, day: int) -> int:
    shaving_days = shaving_schedule(lamyak)
    past_shaving_days = list(filter(lambda d: d < day, shaving_days))
    if not past_shaving_days:
        return -1
    return max(past_shaving_days)
