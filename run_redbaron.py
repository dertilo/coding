import json
from itertools import groupby
from typing import Set, List

from redbaron import RedBaron, NameNode, Node
from util import data_io
from typeguard.util import TYPES_JSONL, TypesLog


def read_red(py_file: str):
    with open(py_file, "r") as source_code:
        red = RedBaron(source_code.read())
    return red


def build_annotation_add_to_imports(qualname):
    imports = set()
    if "Tuple" in qualname:
        imports.add("from typing import Tuple")
        assert qualname[-1] == "]"
        types = qualname.replace("Tuple[", "")[:-1].split(",")
        type_names = []
        for t in types:
            module_path, type_name = build_path_name(t)
            type_names.append(type_name)
            if module_path is not None:
                imports.add(f"from {module_path} import {type_name}")
        ann_name = f"Tuple[{','.join(type_names)}]"
    else:
        module_path, ann_name = build_path_name(qualname)
        imports.add(f"from {module_path} import {ann_name}")

    return ann_name, imports


def build_path_name(type_name):
    if "." in type_name:
        s = type_name.split(".")
        module_path = ".".join(s[:-1])
        type_name = s[-1]
    else:
        module_path = None
    return module_path, type_name


blacklist = ["NoneType", "None", "type"]


def build_annotation_fst(arg_type):
    if not any([b in arg_type for b in blacklist]):
        type_ann, imports = build_annotation_add_to_imports(arg_type)
        annotation_fst = Node.from_fst({"type": "name", "value": type_ann})
    else:
        annotation_fst = None
        imports = set()
    return annotation_fst, imports


def get_existent_imports(red):
    existent_imports = set()
    for r in red:
        if r.type == "import":
            existent_imports.add(f"import {r.name.fst()['value']}")
        elif r.type == "from_import":
            module_path = ".".join([x.fst()["value"] for x in r.value])
            values = r.names()
            for v in values:
                existent_imports.add(f"from {module_path} import {v}")
    return existent_imports


arg_name_blacklist = ["self", "cls"]


def add_annotations(red, tl: TypesLog):
    imports = set()
    def_node = red.find("def", name=tl.qualname.split(".")[-1])
    for arg in def_node.arguments:
        arg_name = arg.name.fst()["value"]
        if arg_name not in arg_name_blacklist:
            arg_type = tl.arg2type[arg_name]
            fst, additional_imports = build_annotation_fst(arg_type)
            imports |= additional_imports

            if fst is not None:
                arg.annotation = fst

    fst, additional_imports = build_annotation_fst(tl.return_type)
    imports |= additional_imports
    if fst is not None:
        def_node.return_annotation = fst

    return imports


def redbaron_add_typ_hints(types_jsonl):
    type_logs = [TypesLog(**d) for d in data_io.read_jsonl(types_jsonl)]
    type_logs_grouped = groupby(type_logs, lambda x: x.func_module)
    for module, tls in type_logs_grouped:
        py_file = f"{module.replace('.','/')}.py"
        red = read_red(py_file)
        existent_imports = get_existent_imports(red)

        imports = {x for tl in tls for x in add_annotations(red, tl)}

        [
            red.insert(1, imp)
            for imp in imports
            if imp not in existent_imports and module not in imp
        ]

        with open(py_file, "w") as source_code:
            source_code.write(red.dumps())


if __name__ == "__main__":

    redbaron_add_typ_hints()
