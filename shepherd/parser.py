from typing import List

import xmltodict

from shepherd.model import LabYak, Sex


def __remove_at_symbols(some_dict):
    return {k.replace('@', ''): v for k, v in some_dict.items()}


def __dict_to_labyak(d: dict) -> LabYak:
    return LabYak(
        name=d['name'],
        age_in_days=int(float(d['age']) * 100),
        sex=Sex.male if d['sex'] == 'm' else Sex.female
    )


def get_herd_from_file(file_name: str) -> List[LabYak]:
    with open(file_name, 'rb') as file:
        labyaks_raw = (__remove_at_symbols(labyak) for labyak in xmltodict.parse(file)['herd']['labyak'])
        return [__dict_to_labyak(labyak_dict) for labyak_dict in labyaks_raw]
