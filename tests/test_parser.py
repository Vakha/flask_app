import os

from shepherd.model import Sex, LabYak
from shepherd.parser import get_herd_from_file


def test_get_herd_from_file():
    path = os.path.join(os.path.dirname(__file__), 'test_herd.xml')
    expected_herd = [LabYak(name='Princess', age_in_days=400, sex=Sex.female),
                     LabYak(name='Prince', age_in_days=800, sex=Sex.male)]
    actual_herd = get_herd_from_file(path)
    assert actual_herd == expected_herd
