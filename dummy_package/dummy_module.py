from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class DummyClass:
    foo:str = "bar"
    def bla(self,x):
        return x

class JustDistraction:
    pass

class AudioConfig(NamedTuple):
    format: str = "wav"
    bitrate: int = -1
    min_dur_secs:float = 0.5 # seconds
