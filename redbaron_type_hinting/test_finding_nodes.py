import os

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
    assert len(def_nodes) == 2
    assert type_log.qualname == "fun"
    assert def_nodes[1].absolute_bounding_box.top_left.line == type_log.line
