from pprint import pprint
from typing import List, Dict, Union, Generator

import pytest

STOP_SIGNS = ["[", ",", "]"]


def dict_lists(mother, children=None):
    if children is not None:
        return {mother: list(children)}
    else:
        assert False


def parse_tree(seq: List[str], accum_siblings=dict_lists):
    while len(seq) > 0:
        node, stop_sign = eat_node(seq)

        if stop_sign == "[":
            yield accum_siblings(node, parse_tree(seq, accum_siblings))
        elif stop_sign == "]":
            if len(node) > 0:
                yield node
            break
        elif stop_sign == ",":
            if len(node) > 0:
                yield node
        else:
            assert False


def eat_node(seq):
    x = seq.pop(0)
    node = ""
    while x not in STOP_SIGNS:
        node += x
        x = seq.pop(0)
    return node, x


def to_string(mother: str, children: Generator[str, None, None]):
    children = list(children)
    assert all([isinstance(c, str) for c in children])
    return f"{mother}[{','.join(children)}]"


@pytest.mark.parametrize(
    "string",
    [
        "a[Bbb[Dd,Ee],xx[what],Cccc]",
        "Aa[Bbb,Cccc[Dd,Eee]]",
        "Aa[Bbb[Dd,Ee],Cccc]",
    ],
)
def test_tree_parsing(string):
    assert string == next(iter(parse_tree(list(string), to_string)))