from shepherd.model import Sex, LabYak
from shepherd.parser import get_herd_from_file


def test_get_herd_from_file():
    expected_herd = [LabYak(name='Princess', age_in_days=400, sex=Sex.female),
                     LabYak(name='Prince', age_in_days=800, sex=Sex.male)]
    actual_herd = get_herd_from_file('test_herd.xml')
    assert actual_herd == expected_herd
