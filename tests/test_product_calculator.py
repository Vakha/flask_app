from pprint import pprint
from typing import List

import pytest

from shepherd.product_calculator import milking, skins_grown, production_report, print_production_report, \
    shaving_schedule, latest_shaving_day
from shepherd.model import LabYak, Sex, StockReport


@pytest.mark.parametrize(('age', 'day', 'milk_liters'), (
    (400, 0, 0),
    (400, 1, 38.0),
    (400, 13, 491.66),
    (800, 13, 335.66),
    (950, 13, 277.16),
    (400, 14, 529.27),
    (800, 14, 361.27),
    (950, 14, 298.27),
    (950, 50, 1038.25),
))
def test_milk_production(age, day, milk_liters):
    labyak = LabYak('Princess', age, Sex.female)
    milk_produced = round(milking(labyak, day), 3)
    assert milk_produced == milk_liters


@pytest.mark.parametrize(('age', 'day', 'milk_liters'), (
    (950, 51, 1038.25),
    (950, 52, 1038.25),
))
def test_milk_production_after_death(age, day, milk_liters):
    labyak = LabYak('Princess', age, Sex.female)
    milk_produced = round(milking(labyak, day), 3)
    assert milk_produced == milk_liters


def test_male_doesnt_produce_milk():
    labyak = LabYak('Prince', 100, Sex.male)
    milk_produced = round(milking(labyak, 200), 3)
    assert milk_produced == 0


@pytest.mark.parametrize(('age', 'day', 'skins'), (
    (400, 0, 1),
    (400, 13, 1),
    (800, 13, 1),
    (950, 13, 1),
    (400, 14, 2),
    (800, 14, 1),
    (950, 14, 1),
    (950, 50, 3),
))
def test_wool_production(age, day, skins):
    labyak = LabYak('Princess', age, Sex.female)
    skins_produced = round(skins_grown(labyak, day), 3)
    assert skins_produced == skins


@pytest.mark.parametrize(('age', 'day', 'skins'), (
    (950, 100, 3),
    (950, 200, 3),
))
def test_wool_production_after_death(age, day, skins):
    labyak = LabYak('Princess', age, Sex.female)
    skins_produced = round(skins_grown(labyak, day), 3)
    assert skins_produced == skins


@pytest.mark.parametrize(('age', 'day', 'skins'), (
    (10, 0, 0),
    (10, 50, 0),
    (10, 89, 0),
    (10, 90, 1),
    (10, 91, 1),
))
def test_wool_production_before_shaving_age(age, day, skins):
    labyak = LabYak('Princess', age, Sex.female)
    skins_produced = round(skins_grown(labyak, day), 3)
    assert skins_produced == skins


def test_production_report(monkeypatch):
    def fake_milking(labyak: LabYak, day: int) -> float:
        return labyak.age_in_days

    def fake_skins_grown(labyak: LabYak, day: int) -> float:
        return labyak.age_in_days

    monkeypatch.setattr("shepherd.product_calculator.milking", fake_milking)
    monkeypatch.setattr("shepherd.product_calculator.skins_grown", fake_skins_grown)
    herd = [
        LabYak("Princess", 1, Sex.female),
        LabYak("Princess", 10, Sex.female),
        LabYak("Princess", 100, Sex.female),
    ]

    produced = production_report(herd, 3)

    assert produced == StockReport(3, 111, 111)


def test_print_production_report(monkeypatch):
    def fake_production_report(herd: List[LabYak], day: int) -> StockReport:
        return StockReport(3, 111.0047, 111)

    monkeypatch.setattr("shepherd.product_calculator.production_report", fake_production_report)

    herd = [
        LabYak("Princess", 10, Sex.female),
        LabYak("Princess", 100, Sex.female),
        LabYak("Princess", 809, Sex.female),
    ]

    expected_report = 'In stock:\n' \
                      '    111.005 liters of milk\n' \
                      '    111 skins of wool\n' \
                      'Herd:\n' \
                      '    Princess  0.13 years old\n' \
                      '    Princess  1.03 years old\n' \
                      '    Princess  8.12 years old'
    actual_report = print_production_report(herd, 3)

    assert actual_report == expected_report


def test_shaving_schedule():
    labyak = LabYak("Princess", 950, Sex.female)
    expected_schedule = [0, 18, 36]
    actual_schedule = shaving_schedule(labyak)
    assert actual_schedule == expected_schedule


def test_shaving_schedule_starts_after_certain_age():
    labyak = LabYak("Princess", 10, Sex.female)
    actual_schedule = shaving_schedule(labyak)
    assert actual_schedule[0] == 90
    assert all(d >= 90 for d in actual_schedule)


def test_empty_shaving_schedule_for_dead_labyak():
    labyak = LabYak("Princess", 1000, Sex.female)
    actual_schedule = shaving_schedule(labyak)
    assert not actual_schedule


@pytest.mark.parametrize(('age', 'day', 'latest_day'), (
    (40, 14, -1),
    (400, 13, 0),
    (400, 14, 13),
))
def test_latest_shaving_day(age, day, latest_day):
    labyak = LabYak("Princess", age, Sex.female)
    assert latest_shaving_day(labyak, day) == latest_day

