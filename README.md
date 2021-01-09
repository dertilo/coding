# coding
* depends on `tilo` branch in my `typeguard` fork -> rename somewhen!

### future ideas
* autogenerate dataclass from dicts
```python
@dataclass
class Test(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    bla:str
```