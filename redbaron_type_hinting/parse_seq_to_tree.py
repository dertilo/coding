from pprint import pprint
from typing import List, Dict, Union

Node = Union[Dict, str]
STOP_SIGNS = ["[", ",", "]"]


def parse_tree(seq: List[str]):
    while len(seq) > 0:
        node, stop_sign = eat_node(seq)

        if stop_sign == "[":
            children = list(parse_tree(seq))
            yield {node: children}
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


if __name__ == "__main__":
    pprint(list(parse_tree(list("Aa[Bbb,Cccc[Dd,Eee]]"))))
    pprint(list(parse_tree(list("Aa[Bbb[Dd,Ee],Cccc]"))))
