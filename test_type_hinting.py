import os

import numpy

from dummy_package.another_dummy_module import AnotherDummyClass
from dummy_package.dummy_module import DummyClass
from dummy_package.dummy_module_2 import DummyClass2, dummy_fun
from redbaron_type_hinting.adding_type_hints import enrich_pyfiles_by_type_hints

FILE_NAME = "types.jsonl"

def test_type_hinting(tmp_path):
    TYPES_JSONL = str(tmp_path / FILE_NAME)
    os.environ["TYPES_JSONL"] = TYPES_JSONL

    run_dummy()

    enrich_pyfiles_by_type_hints(TYPES_JSONL)


def run_dummy():
    x = DummyClass()
    x.bla(numpy.zeros((1, 3)))
    c = DummyClass2()
    y = dummy_fun(x)
    c.foo = x
    bla = c.dummy_method(x)
    bla = c.dummy_class_method(x)
    bla = c.dummy_static_method(x)
    x = AnotherDummyClass()
    x.bla(numpy.zeros((1, 3)))


def test_dogfooding(tmp_path):
    TYPES_JSONL = str(tmp_path / FILE_NAME)
    os.environ["TYPES_JSONL"] = TYPES_JSONL

    enrich_pyfiles_by_type_hints("dummy_types.jsonl")

    enrich_pyfiles_by_type_hints(TYPES_JSONL)

