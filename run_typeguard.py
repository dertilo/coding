import os
from typeguard.util import TYPES_JSONL
from typeguard.importhook import install_import_hook
install_import_hook('dummy_module_2')

from dummy_module_2 import dummy_fun, DummyClass2
from package.dummy_module import DummyClass




if __name__ == '__main__':

    if os.path.isfile(TYPES_JSONL):
        os.remove(TYPES_JSONL)

    x = DummyClass()
    c = DummyClass2()
    y = dummy_fun(x)

    c.foo = x
    bla = c.dummy_method(x)
    bla = c.dummy_class_method(x)
    bla = c.dummy_static_method(x)
    # print(x)
    # print(y)
    # print(bla)