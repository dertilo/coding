import sys
import traceback

from redbaron import Node, RedBaron
from typeguard.util import TypesLog


def build_node(type_ann: str):
    return Node.from_fst({"type": "name", "value": type_ann})


def just_try(verbose=False):
    def decorator(func):
        def inner_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if verbose:
                    traceback.print_exc(file=sys.stderr)
                return None

        return inner_function
    return decorator

def read_red(py_file: str) -> RedBaron:
    with open(py_file, "r") as source_code:
        red = RedBaron(source_code.read())
    return red


@just_try(verbose=False)
def find_node(red: RedBaron, type_log: TypesLog):
    node_name = type_log.qualname.split(".")[-1]
    def_nodes = red.find_all("def", name=node_name)
    assert len(def_nodes) > 0

    def match_typelog_to_node(dn):
        num_decorators = len(dn.decorators)
        is_class_or_static_method = any(
            [dec.dumps() in ["@classmethod", "@staticmethod"] for dec in dn.decorators]
        )
        return (
            dn.absolute_bounding_box.top_left.line
            + num_decorators
            - is_class_or_static_method
        ) == type_log.line

    matches = filter(match_typelog_to_node, def_nodes)
    return next(matches)
