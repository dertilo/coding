import black
import importlib

import pytest
from typeguard.util import TYPEGUARD_CACHE

from redbaron_type_hinting.adding_type_hints import (
    add_annotations_build_imports,
    add_annotations_and_imports,
)
from redbaron_type_hinting.util import read_red


"""
pytest -s --typeguard-packages=tests/resources/test_cases
pycharm: 
    run -> edit -> Additional Arguments: --typeguard-packages=tests.resources.test_cases
    Working directory: .../coding/
"""


def build_type_log(run):
    keys = list(TYPEGUARD_CACHE.keys())
    [TYPEGUARD_CACHE.pop(k) for k in keys]
    run()
    return list(TYPEGUARD_CACHE.values())


@pytest.mark.parametrize("fun_name", [
    "simple_types",
    "union_fun"
])
def test_type_hints(fun_name):
    module_name = f"tests.resources.test_cases.{fun_name}"
    expected_module_name = f"tests.resources.expected.{fun_name}"
    m = importlib.import_module(module_name)
    input_red = read_red(f"{module_name.replace('.','/')}.py")
    with open(f"{expected_module_name.replace('.','/')}.py", "r") as f:
        expected_py = f.read()

    type_logs = build_type_log(lambda: getattr(m, "main")())

    add_annotations_and_imports(input_red, type_logs)
    input_py = input_red.dumps()
    assert input_py == expected_py
