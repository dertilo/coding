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


def test_annotate_with_super_class(red):
    foo = fun(Mother())
    foo = fun(Child())

    TYPES_LOGS = [
        tl
        for tl in TYPEGUARD_CACHE.values()
        if f"{tl.func_module.replace('.', '/')}.py" == __file__.strip(os.getcwd())
        if tl.qualname.endswith("fun")
    ]
    assert len(TYPES_LOGS) == 1
    type_log = TYPES_LOGS[0]
    assert len(type_log.call_logs) == 2
    add_annotations(red, type_log)
    def_node = red.find("def", name="fun")
    assert def_node.return_annotation.dumps() == "Mother"
