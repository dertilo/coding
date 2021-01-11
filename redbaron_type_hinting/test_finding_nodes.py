import json
import os
from dataclasses import asdict
from pprint import pprint

import pytest
from baron.path import Position, BoundingBox
from typing import List

from redbaron import NameNode
from typeguard.util import TYPEGUARD_CACHE, TypesLog

from redbaron_type_hinting.util import read_red


class Clazz:
    @staticmethod
    def fun(x):
        return x


def fun(x):
    return x


def some_decorator(f):
    def fun(f):
        return f

    return fun


class SecondDecoratedFun:
    @some_decorator
    @staticmethod
    def fun(x):
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


def test_find_by_name_and_line_typegard(red):
    foo = fun("bar")
    file_to_typelog = {
        f"{tl.func_module.replace('.','/')}.py": tl for tl in TYPEGUARD_CACHE.values()
    }
    type_log = file_to_typelog[f"{__file__.strip(os.getcwd())}"]

    def_nodes: List[NameNode] = red.find_all("def", name="fun")
    assert len(def_nodes) == 4
    assert type_log.qualname == "fun"
    assert def_nodes[1].absolute_bounding_box.top_left.line == type_log.line


foo = SecondDecoratedFun.fun("bar")
TYPES_LOGS = [
    tl
    for tl in TYPEGUARD_CACHE.values()
    if f"{tl.func_module.replace('.','/')}.py" == __file__.strip(os.getcwd())
]


@pytest.mark.parametrize("type_log", TYPES_LOGS,ids=[json.dumps(asdict(tl)) for tl in TYPES_LOGS])
def test_find_decorated_fun_by_name_and_line_typegard(red, type_log: TypesLog):
    node_name = type_log.qualname.split(".")[-1]
    def_nodes = red.find_all("def", name=node_name)
    assert len(def_nodes)>0


    def match_type_log_to_node(dn):
        num_decorators = len(dn.decorators)
        return (dn.absolute_bounding_box.top_left.line + num_decorators) == type_log.line

    assert len(list(filter(match_type_log_to_node, def_nodes))) == 1


# if __name__ == "__main__":
#     red = read_red(__file__)
#     def_nodes = red.find_all("def", name="fun")
#     dn = def_nodes[3]
#     print()
