import json
import re
from pprint import pprint
from typing import Tuple, Union, Dict
from itertools import groupby
from typing import Set, List

from redbaron import RedBaron, NameNode, Node
from util import data_io
from typeguard.util import TypesLog


def read_red(py_file: str) -> RedBaron:
    with open(py_file, "r") as source_code:
        red = RedBaron(source_code.read())
    return red


typing_list = ["list", "dict", "tuple", "generator"]



def build_annotation_add_to_imports(qualname: str) -> Tuple[str, set]:
    imports = set()

    def append_node(nodes, node_name, children: str = None):
        if len(node_name) > 0:
            module_path, ann_name = build_path_name(node_name)
            if module_path is not None:
                imports.add(f"from {module_path} import {ann_name}")
            elif ann_name.lower() in typing_list:
                ann_name = ann_name.capitalize()
                imports.add(f"from typing import {ann_name}")

            if children is not None:
                nodes.append(f"{ann_name}[{children}]")
            else:
                nodes.append(ann_name)


    def parse_tree(seq: List[str]) -> str:
        nodes: List[Union[Dict, str]] = []
        node = ""

        while len(seq) > 0:
            x = seq.pop(0)
            if x == "[":
                append_node(nodes, node, children=parse_tree(seq))
                node = ""
            elif x == "]":
                append_node(nodes, node)
                return ",".join(nodes)
            elif x == ",":
                append_node(nodes, node)
                node = ""
            else:
                node += x

        append_node(nodes, node)
        return ",".join(nodes)


    ann_name = parse_tree(list(qualname))
    return ann_name, imports


def build_path_name(type_name: str) -> Tuple[str, str]:
    if "." in type_name:
        s = type_name.split(".")
        module_path = ".".join(s[:-1])
        type_name = s[-1]
    else:
        module_path = None
    return module_path, type_name


blacklist = ["NoneType", "None", "type"]


def build_annotation_fst(arg_type: str) -> Tuple[NameNode, set]:
    if not any([b in arg_type for b in blacklist]):
        type_ann, imports = build_annotation_add_to_imports(arg_type)
        annotation_fst = Node.from_fst({"type": "name", "value": type_ann})
    else:
        annotation_fst = None
        imports = set()
    return annotation_fst, imports


def get_existent_imports(red: RedBaron) -> set:
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


def add_annotations(red: RedBaron, tl: TypesLog) -> set:
    imports = set()
    def_node = red.find("def", name=tl.qualname.split(".")[-1])
    argName_to_node = {arg.name.fst()["value"]: arg for arg in def_node.arguments}
    logged_names_types = (
        (n, t) for n, t in tl.arg2type.items() if n not in arg_name_blacklist
    )

    for arg_name, arg_type in logged_names_types:
        arg_type = tl.arg2type[arg_name]
        fst, additional_imports = build_annotation_fst(arg_type)
        imports |= additional_imports

        if fst is not None:
            argName_to_node[arg_name].annotation = fst

    fst, additional_imports = build_annotation_fst(tl.return_type)
    imports |= additional_imports
    if fst is not None:
        def_node.return_annotation = fst

    return imports


def enrich_pyfiles_by_type_hints(types_jsonl: str, overwrite=True, verbose=False):
    type_logs = list(set([TypesLog(**d) for d in data_io.read_jsonl(types_jsonl)]))
    print(f"got {len(type_logs)} type-logs")
    type_logs_grouped = {
        t: list(g)
        for t, g in groupby(
            sorted(type_logs, key=lambda x: x.func_module), lambda x: x.func_module
        )
    }

    for module, tls in type_logs_grouped.items():
        py_file = f"{module.replace('.','/')}.py"
        if verbose:
            print(py_file)
            print(tls)
        red = read_red(py_file)
        existent_imports = get_existent_imports(red)

        imports = {imp for type_log in tls for imp in add_annotations(red, type_log)}
        print(f"imports: {imports}")
        [
            red.insert(1, imp)
            for imp in imports
            if imp not in existent_imports and module not in imp
        ]
        py_file = py_file if overwrite else f"{py_file.replace('.py','')}_modified.py"
        with open(py_file, "w") as source_code:
            source_code.write(red.dumps())
