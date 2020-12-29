from dataclasses import dataclass


@dataclass
class DummyClass:
    foo:str = "bar"
    def bla(self,x):
        return x

class JustDistraction:
    pass