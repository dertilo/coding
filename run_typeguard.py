import os
from typeguard.importhook import install_import_hook
install_import_hook('dummy_module_2')

from dummy_module_2 import dummy_fun
from package.dummy_module import DummyClass




if __name__ == '__main__':
    x = DummyClass()
    y = dummy_fun(x)
    print(x)
    print(y)