from dataclasses import dataclass
from typing import NamedTuple, Optional


@dataclass
class DummyClass:
    foo:str = "bar"
    def bla(self,x):
        return x

class JustDistraction:
    pass

class AudioConfig(NamedTuple):
    format: str = "wav"
    bitrate: Optional[int] = None
    min_dur_secs:float = 0.5 # seconds
