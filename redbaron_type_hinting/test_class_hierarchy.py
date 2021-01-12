import json
import os
from dataclasses import asdict
from pprint import pprint

import pytest
from typeguard.util import TYPEGUARD_CACHE

from redbaron_type_hinting.adding_type_hints import add_annotations
from redbaron_type_hinting.util import read_red

"""
pytest -s --typeguard-packages=redbaron_type_hinting redbaron_type_hinting/test_class_hierarchy.py
"""


@pytest.fixture
def red():
    return read_red(__file__)


class Mother:
    pass


class Child(Mother):
    pass


def fun(x):
    return x


foo = fun(Mother())
foo = fun(Child())

TYPES_LOGS = [
    tl
    for tl in TYPEGUARD_CACHE.values()
    if f"{tl.func_module.replace('.','/')}.py" == __file__.strip(os.getcwd())
    if tl.qualname.endswith("fun")
]
print(TYPES_LOGS)
assert len(TYPES_LOGS) == 1


@pytest.mark.parametrize(
    "type_log", TYPES_LOGS, ids=[json.dumps(asdict(tl)) for tl in TYPES_LOGS]
)
def test_child(red, type_log):
    add_annotations(red, type_log)
    pprint(red.dumps())
