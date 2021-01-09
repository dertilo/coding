from redbaron import Node


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