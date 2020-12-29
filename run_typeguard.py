import os

import numpy
from typeguard.importhook import install_import_hook
from dummy_package.dummy_module_2 import DummyClass2, dummy_fun

TYPES_JSONL = "dummy_types.jsonl"
os.environ["TYPES_JSONL"] = TYPES_JSONL
install_import_hook('dummy_package')
from dummy_package.dummy_module import DummyClass
from dummy_package.another_dummy_module import AnotherDummyClass




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