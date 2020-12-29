from dataclasses import dataclass


@dataclass
class AnotherDummyClass:
    foo:str = "bar"
    def bla(self,x):
        return x

class JustDistraction:
    pass