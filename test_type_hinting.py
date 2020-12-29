import os

import numpy

from dummy_module_2 import DummyClass2, dummy_fun
from dummy_package.another_dummy_module import AnotherDummyClass
from dummy_package.dummy_module import DummyClass
from run_redbaron import redbaron_add_typ_hints


def test_type_hinting():
    TYPES_JSONL = "/tmp/types_1.jsonl"
    os.environ["TYPES_JSONL"] = TYPES_JSONL

    if os.path.isfile(TYPES_JSONL):
        os.remove(TYPES_JSONL)

    x = DummyClass()
    x.bla(numpy.zeros((1,3)))

    c = DummyClass2()
    y = dummy_fun(x)

    c.foo = x
    bla = c.dummy_method(x)
    bla = c.dummy_class_method(x)
    bla = c.dummy_static_method(x)


    x = AnotherDummyClass()
    x.bla(numpy.zeros((1,3)))

    redbaron_add_typ_hints(TYPES_JSONL)

