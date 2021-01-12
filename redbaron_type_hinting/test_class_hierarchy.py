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


def build_type_log(run):
    keys = list(TYPEGUARD_CACHE.keys())
    [TYPEGUARD_CACHE.pop(k) for k in keys]

    run()

    TYPES_LOGS = [
        tl
        for tl in TYPEGUARD_CACHE.values()
        if f"{tl.func_module.replace('.', '/')}.py" == __file__.strip(os.getcwd())
        if tl.qualname.endswith("fun")
    ]
    assert len(TYPES_LOGS) == 1
    type_log = TYPES_LOGS[0]
    return type_log


def test_annotate_with_class(red):
    type_log = build_type_log(lambda: fun(Child()))

    assert len(type_log.call_logs) == 1
    add_annotations(red, type_log)
    def_node = red.find("def", name="fun")
    assert def_node.return_annotation.dumps() == "Child"


def test_annotate_with_super_class(red):
    def run():
        foo = fun(Mother())
        foo = fun(Child())

    type_log = build_type_log(run)

    assert len(type_log.call_logs) == 2
    add_annotations(red, type_log)
    def_node = red.find("def", name="fun")
    assert def_node.return_annotation.dumps() == "Mother"
