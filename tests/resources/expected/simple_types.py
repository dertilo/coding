from typing import List
def str_fun(x:str)->str:
    return x

def list_str_fun(x:List[str])->List[str]:
    return x

def main():
    s = str_fun("foo")
    s = list_str_fun(["foo"])
