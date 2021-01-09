from redbaron import Node, RedBaron


def build_node(type_ann: str):
    return Node.from_fst({"type": "name", "value": type_ann})


def just_try(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return None

    return inner_function


def read_red(py_file: str) -> RedBaron:
    with open(py_file, "r") as source_code:
        red = RedBaron(source_code.read())
    return red