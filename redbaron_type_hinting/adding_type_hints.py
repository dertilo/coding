import importlib
from itertools import groupby
from typing import Tuple, Union, Dict, List, Set, Optional

from redbaron import RedBaron, NameNode, Node
from typeguard.util import TypesLog, CallLog


def read_red(py_file: str) -> RedBaron:
    with open(py_file, "r") as source_code:
        red = RedBaron(source_code.read())
    return red


typing_list = ["List", "Dict", "Tuple", "Generator", "Any"]
replace_map = {"NoneType": "None"}


def build_annotation_add_to_imports(qualname: str) -> Tuple[str, set]:
    imports = set()

    def append_node(nodes, node_name, children: str = None):
        if len(node_name) > 0:
            module_path, ann_name = build_path_name(node_name)
            if module_path is not None:
                imports.add(f"from {module_path} import {ann_name}")
            elif ann_name.capitalize() in typing_list:
                ann_name = ann_name.capitalize()
                imports.add(f"from typing import {ann_name}")

            ann_name = replace_map.get(ann_name, ann_name)

            if children is not None:
                ann_name = f"{ann_name}[{children}]"

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


def is_childclass(mother: str, child: str, module_s: str):
    m = importlib.import_module(module_s)
    if hasattr(m, mother) and issubclass(getattr(m, child), getattr(m, mother)):
        is_sub = True
    else:
        is_sub = False

    return is_sub


def build_ann_node(
    imports, additional_imports, annotation: Optional[NameNode], new_annotation: str
):
    # TODO(tilo) fuse with build_annotation_add_to_imports
    if annotation is not None:
        normalize = lambda s: s.dumps().replace(" ", "") if s is not None else None
        old_annotation = normalize(annotation)

        module_s = next(iter(additional_imports)).strip("from ").split(" import")[0]
        if is_childclass(
            mother=old_annotation, child=new_annotation, module_s=module_s
        ):
            new_annotation = old_annotation
        else:
            imports |= additional_imports

            if "Union" in old_annotation:
                old_annotation.replace("]", f",{new_annotation}]")
            else:
                imports.add(f"from typing import Union")
                new_annotation = f"Union[{old_annotation},{new_annotation}]"
    else:
        imports |= additional_imports

    return build_node(new_annotation)


def add_annotations(red: RedBaron, tl: TypesLog) -> set:
    imports = set()
    def_node = red.find("def", name=tl.qualname.split(".")[-1])
    argName_to_node = {
        arg.name.fst()["value"]: (arg, "annotation") for arg in def_node.arguments
    }
    argName_to_node["return"] = (def_node, "return_annotation")

    for call_log in tl.call_logs.values():
        process_call_log(argName_to_node, call_log, imports)

    return imports


def process_call_log(
    argName_to_node: Dict[str, Tuple[NameNode, str]],
    call_log: CallLog,
    imports: Set[str],
):
    logged_names_types = [
        (n, t) for n, t in call_log.arg2type.items() if n not in arg_name_blacklist
    ]
    logged_names_types += [("return", call_log.return_type)]

    for arg_name, arg_type in logged_names_types:
        ann, additional_imports = build_annotation_add_to_imports(arg_type)
        if ann is not None:
            arg_node, attr_name = argName_to_node[arg_name]
            m_ann = build_ann_node(
                imports, additional_imports, getattr(arg_node, attr_name), ann
            )
            setattr(arg_node, attr_name, m_ann)


def build_node(type_ann: str):
    return Node.from_fst({"type": "name", "value": type_ann})


def just_try(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None

    return inner_function


def remove_unwanted_annotations(red):
    blacklist = ["Any", "None", "type"]

    for node in red.find_all("def"):
        if just_try(lambda x: x.annotation.dumps())(node) in blacklist:
            node.annotation = ""
        elif just_try(lambda x: x.return_annotation.dumps())(node) in blacklist:
            node.return_annotation = ""


def enrich_pyfiles_by_type_hints(
    type_logs: List[TypesLog], overwrite=True, verbose=False
):
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
        remove_unwanted_annotations(red)
        print(f"imports: {imports}")
        [
            red.insert(1, imp)
            for imp in imports
            if imp not in existent_imports and module not in imp
        ]

        py_file = py_file if overwrite else f"{py_file.replace('.py','')}_modified.py"
        with open(py_file, "w") as source_code:
            source_code.write(red.dumps())
