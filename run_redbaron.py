import json
from itertools import groupby

from redbaron import RedBaron, NameNode, Node
from util import data_io
from typeguard.util import TYPES_JSONL,TypesLog


def read_red(py_file: str):
    with open(py_file, "r") as source_code:
        red = RedBaron(source_code.read())
    return red


def add_type_annotations(py_file):
    red = read_red(py_file)
    annotation_fst = {
        "type": "name",
        "value": "str"
    }
    node = Node.from_fst(annotation_fst)
    red.find_all("def")[0].return_annotation = node
    red.find_all("def")[0].arguments[0].annotation = Node.from_fst(
        {'type': 'name', 'value': 'DummyClass'})
    red.insert(1, "from bla import dings")
    # formatting = [{'type': 'space', 'value': ' '}]
    # import_fs = {'type': 'from_import', 'first_formatting': formatting, 'value': [{'type': 'name', 'value': 'dummy_module'}], 'second_formatting': formatting, 'third_formatting': formatting, 'targets': [{'type': 'name_as_name', 'value': 'DummyClass', 'target': '', 'first_formatting': [], 'second_formatting': []}]}
    with open("modified_code.py", "w") as source_code:
        source_code.write(red.dumps())


def build_annotation_add_to_imports(qualname,imports):
    if "Tuple" in qualname:
        assert qualname[-1] == "]"
        types = qualname.replace("Tuple[","")[:-1].split(",")
        type_names = []
        for t in types:
            module_path, type_name = build_path_name(t)
            type_names.append(type_name)
            if module_path is not None:
                imports.add(f"from {module_path} import {type_name}")
        ann_name = f"Tuple{type_names}"
    else:
        module_path, ann_name = build_path_name(qualname)
        imports.add(f"from {module_path} import {ann_name}")

    assert "'" not in ann_name
    return ann_name


def build_path_name(type_name):
    if "." in type_name:
        s = type_name.split(".")
        module_path = ".".join(s[:1])
        type_name = s[-1]
    else:
        module_path = None
    return module_path, type_name

blacklist = ["NoneType", "None"]


def build_annotation_fst(arg_type,imports):
    if not any([b in arg_type for b in blacklist]):
        type_ann = build_annotation_add_to_imports(arg_type, imports)
        annotation_fst = Node.from_fst({"type": "name", "value": type_ann})
    else:
        annotation_fst = None
    return annotation_fst


if __name__ == "__main__":

    type_logs = [TypesLog(**d) for d in data_io.read_jsonl(TYPES_JSONL)]
    type_logs_grouped = groupby(type_logs,lambda x:x.func_module)
    for module, tls in type_logs_grouped:
        py_file = f"{module}.py"
        red = read_red(py_file)
        imports = set()
        for tl in tls:
            def_node = red.find("def", name=tl.qualname.split(".")[-1])
            for arg in def_node.arguments:
                arg_name = arg.name.fst()["value"]
                arg_type = tl.arg2type[arg_name]
                fst = build_annotation_fst(arg_type, imports)
                if fst is not None:
                    arg.annotation = fst

            fst = build_annotation_fst(tl.return_type, imports)
            if fst is not None:
                def_node.return_annotation = fst

        [red.insert(1, imp) for imp in imports]

        with open("modified_code.py", "w") as source_code:
            source_code.write(red.dumps())