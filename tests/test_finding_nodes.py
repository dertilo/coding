import pytest
from redbaron import RedBaron
from typeguard.util import TypesLog, TYPEGUARD_CACHE
from typing import List

from redbaron_type_hinting.util import find_node, read_red
from tests.resources.to_be_found import (
    DecoratedStaticMethod,
    StaticMethod,
    ClazzWithClassmethod,
    ClazzDecoratedClassmethod,
)

"""
pycharm: run -> edit -> Additional Arguments: --typeguard-packages=tests.resources.to_be_found
"""


@pytest.fixture
def red():
    return read_red(f"tests/resources/to_be_found.py")


def build_type_log(run):
    keys = list(TYPEGUARD_CACHE.keys())
    [TYPEGUARD_CACHE.pop(k) for k in keys]
    run()
    type_logs = list(TYPEGUARD_CACHE.values())
    return type_logs


@pytest.mark.parametrize(
    "type_logs",
    [
        build_type_log(lambda: StaticMethod.fun("bar")),
        build_type_log(lambda: DecoratedStaticMethod.fun("bar")),
        build_type_log(lambda: ClazzWithClassmethod.fun("bar")),
        build_type_log(lambda: ClazzDecoratedClassmethod.fun("bar")),
    ],
)
def test_find_decorated_fun_by_name_and_line_typegard(
    red: RedBaron, type_logs: List[TypesLog]
):
    type_log = next(filter(lambda x: x.qualname.endswith("fun"), type_logs))
    match = find_node(red, type_log)
    assert match is not None


def test_cannot_find(red):
    type_log = TypesLog("bla", "fun", line=-1)
    assert find_node(red, type_log) is None
