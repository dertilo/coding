from typing import List
from typing import NamedTuple, Optional


def str_fun(x:str)->str:
    return x

def list_str_fun(x:List[str])->List[str]:
    return x

class AudioConfig(NamedTuple):
    format: str = "wav"
    bitrate: Optional[int] = None
    min_dur_secs: float = 0.5 # seconds

def named_tuple_fun(x:AudioConfig)->AudioConfig:
    return x

def main():
    s = str_fun("foo")
    s = list_str_fun(["foo"])
    _ = named_tuple_fun(AudioConfig())
