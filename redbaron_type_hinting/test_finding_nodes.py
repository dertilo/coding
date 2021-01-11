import json
import os
import sys
from abc import abstractmethod
from dataclasses import asdict, dataclass
from functools import wraps
from pprint import pprint

import pytest
from baron.path import Position, BoundingBox
from typing import List

from redbaron import NameNode
from typeguard.util import TYPEGUARD_CACHE, TypesLog
from util import data_io

from redbaron_type_hinting.util import read_red, find_node

"""
pytest -s --typeguard-packages=redbaron_type_hinting redbaron_type_hinting/test_finding_nodes.py
"""


class Clazz:
    @staticmethod
    def fun(x):
        return x


def fun(x):
    return x


def some_decorator(f):
    @wraps(f)
    def fun(*args):
        return f(*args)

    return fun


class DecoratedStaticMethod:
    @staticmethod
    @some_decorator
    def fun(x):
        return x


class StaticMethod:
    @staticmethod
    def fun(x):
        return x + "what"


class ClazzWithClassmethod:
    @classmethod
    def fun(cls, x):
        return x


class ClazzDecoratedClassmethod:
    @classmethod
    @some_decorator
    def fun(cls, x):
        return x


@pytest.fixture
def red():
    return read_red(__file__)


# def test_cannot_find_by_name(red):
#     def_node = red.find("def", name="fun")
#     assert def_node.absolute_bounding_box != BoundingBox(((13, 1), (17, 0)))
#
# def test_find_by_name_and_bounding_box(red):
#     def_nodes = red.find_all("def", name="fun")
#     assert len(def_nodes) == 2
#     found_nodes = list(
#         filter(
#             lambda n: n.absolute_bounding_box == BoundingBox(((13, 1), (17, 0))),
#             def_nodes,
#         )
#     )
#     assert len(found_nodes) == 1
#

# def test_find_by_name_and_line(red):
#     def_nodes:List[NameNode] = red.find_all("def", name="fun")
#     assert len(def_nodes) == 2
#     assert def_nodes[0].absolute_bounding_box.top_left.line == 12 # decorator makes it start one line above
#     assert def_nodes[1].absolute_bounding_box.top_left.line == 17


foo = StaticMethod.fun("bar")
foo = DecoratedStaticMethod.fun("bar")
foo = ClazzWithClassmethod.fun("bar")
foo = ClazzDecoratedClassmethod.fun("bar")


TYPES_LOGS = [
    tl
    for tl in TYPEGUARD_CACHE.values()
    if f"{tl.func_module.replace('.','/')}.py" == __file__.strip(os.getcwd())
    if tl.qualname.endswith("fun")
]
assert len(TYPES_LOGS) == 4  #


@pytest.mark.parametrize(
    "type_log", TYPES_LOGS, ids=[json.dumps(asdict(tl)) for tl in TYPES_LOGS]
)
def test_find_decorated_fun_by_name_and_line_typegard(red, type_log: TypesLog):
    match = find_node(red, type_log)
    assert match is not None


def test_cannot_find(red):
    type_log = TypesLog("bla", "fun", line=-1)
    assert find_node(red, type_log) is None
