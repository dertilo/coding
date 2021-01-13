from typing import Union

def union_fun(x:Union[str,int])->Union[str,int]:
    return x

def main():
    s = union_fun("foo")
    s = union_fun(1)
