from pprint import pprint
from typing import List, Dict, Union, Generator

import pytest

END = "<END>"
STOP_SIGNS = ["[", ",", "]", END]


def dict_lists(mother, children=None):
    if children is not None:
        return {mother: list(children)}
    else:
        return mother


def parse_tree(seq: List[str], build_branch=dict_lists, process_node=lambda x: x):
    while len(seq) > 0:
        node, stop_sign = eat_node(seq)

        if node is not None:
            node = process_node(node)

        if stop_sign == "[":
            yield build_branch(node, parse_tree(seq, build_branch, process_node))
        elif stop_sign == "]":
            if node is not None:
                yield node
            break
        elif stop_sign == ",":
            if node is not None:
                yield node
        elif stop_sign == END:
            yield node


def eat_node(seq: List[str]):
    assert len(seq) > 0
    x = seq.pop(0)
    node = ""
    while x not in STOP_SIGNS and len(seq) > 0:
        node += x
        x = seq.pop(0)

    if len(seq) == 0 and x not in STOP_SIGNS:
        node += x
        x = END
    elif len(node) == 0:
        node = None
    elif x in STOP_SIGNS:
        pass
    else:
        assert False

    return node, x


def branch_to_string(mother: str, children: Generator[str, None, None] = None):
    if children is not None:
        children = list(children)
        assert all([isinstance(c, str) for c in children])
        return f"{mother}[{','.join(children)}]"
    else:
        return mother


@pytest.mark.parametrize(
    "string",
    [
        "Aa",
        "a[Bbb[Dd,Ee],xx[what],Cccc]",
        "Aa[Bbb,Cccc[Dd,Eee]]",
        "Aa[Bbb[Dd,Ee],Cccc]",
    ],
)
def test_tree_parsing(string):
    assert string == next(iter(parse_tree(list(string), branch_to_string)))


def capitalize_node(n):
    return n.capitalize()


@pytest.mark.parametrize(
    "inputt,output",
    [
        ("a[b[cc[ddd]]]", "A[B[Cc[Ddd]]]"),
    ],
)
def test_nod_capitalizing(inputt, output):
    assert output == next(
        iter(parse_tree(list(inputt), branch_to_string, capitalize_node))
    )
