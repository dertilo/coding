import numpy

from dummy_package.dummy_module import JustDistraction, DummyClass


def dummy_fun(x):
    x.foo = "dings"
    return x,"bar"

def dummy_fun_2(x):
    return x,"bar"

class DummyClass2:

    def __init__(self) -> None:
        super().__init__()
        self.foo = None


    def dummy_method(self,x):
        return x

    @classmethod
    def dummy_class_method(cls,x):
        return x

    @staticmethod
    def dummy_static_method(x):
        return x

def generator(g):
    yield from (DummyClass2() for i in g)

def build_generator(g):
    return (DummyClass2() for i in g)
