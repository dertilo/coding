from typing import Dict

import os
import pytest
from typeguard.util import TYPEGUARD_CACHE

from redbaron_type_hinting.adding_type_hints import (
    add_annotations,
    add_annotations_build_imports,
)
from redbaron_type_hinting.util import read_red

"""
pytest -s --typeguard-packages=redbaron_type_hinting redbaron_type_hinting/test_annotations.py
"""


@pytest.fixture
def red():
    return read_red(__file__)


def fun(x):
    return x


def build_type_log(run, filter_for="fun"):
    keys = list(TYPEGUARD_CACHE.keys())
    [TYPEGUARD_CACHE.pop(k) for k in keys]

    run()
    print(TYPEGUARD_CACHE)
    TYPES_LOGS = [
        tl
        for tl in TYPEGUARD_CACHE.values()
        if f"{tl.func_module.replace('.', '/')}.py" == __file__.strip(os.getcwd())
        if tl.qualname.endswith(filter_for)
    ]
    assert len(TYPES_LOGS) == 1
    type_log = TYPES_LOGS[0]
    return type_log


def test_unwanted_annotations(red):
    type_log = build_type_log(lambda: fun(None), filter_for="fun")
    assert len(type_log.call_logs) == 1
    add_annotations_build_imports(red, [type_log])

    def_node = red.find("def", name="fun")
    return_anno = def_node.return_annotation.dumps()
    assert return_anno != "None"


def already_annotated_fun(x) -> Dict[str, str]:
    return x


def test_already_annotated(red):
    type_log = build_type_log(
        lambda: already_annotated_fun({"foo": "bar"}),
        filter_for="already_annotated_fun",
    )
    assert len(type_log.call_logs) == 1
    add_annotations_build_imports(red, [type_log])

    def_node = red.find("def", name="already_annotated_fun")
    return_anno = def_node.return_annotation.dumps()
    assert return_anno == "Dict[str,str]"
