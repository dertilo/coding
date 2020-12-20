import numpy

from package.dummy_module import DummyClass


def dummy_fun(x):
    x.foo = "dings"
    return x,"bar"


# def dummy_fun_annotated(x:DummyClass)->str:
#     x.foo = "dings"
#     return x,"bar"
