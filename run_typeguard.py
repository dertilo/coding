import os
from dataclasses import asdict

import numpy
from typeguard.importhook import install_import_hook
from typeguard.util import TYPEGUARD_CACHE
from util import data_io

TYPES_JSONL = "dummy_types.jsonl"
os.environ["TYPES_JSONL"] = TYPES_JSONL
install_import_hook('dummy_package')
from dummy_package.dummy_module import DummyClass
from dummy_package.another_dummy_module import AnotherDummyClass
from dummy_package.dummy_module_2 import DummyClass2, dummy_fun, generator, \
    build_generator

if __name__ == '__main__':


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
    x = list(generator((DummyClass() for _ in range(3))))
    x = list(build_generator((DummyClass() for _ in range(3))))

    data_io.write_jsonl("types.jsonl",[asdict(x) for x in TYPEGUARD_CACHE.values()])