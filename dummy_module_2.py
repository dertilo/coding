import numpy

from package.dummy_module import DummyClass


def dummy_fun(x):
    x.foo = "dings"
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

# def dummy_fun_annotated(x:DummyClass)->str:
#     x.foo = "dings"
#     return x,"bar"
