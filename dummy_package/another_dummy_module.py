from dataclasses import dataclass

@dataclass
class JustDistraction:
    foo:str = "bar"
    def bla(self,x):
        return x

@dataclass
class AnotherDummyClass:
    foo:str = "bar"
    def bla(self,x):
        return x

