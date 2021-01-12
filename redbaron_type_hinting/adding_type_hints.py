import importlib
from itertools import groupby
from typing import Tuple, Dict, List, Set, Optional

from redbaron import RedBaron, NameNode
from typeguard.util import TypesLog, CallLog

from redbaron_type_hinting.parse_annotations import parse_annotation_build_imports
from redbaron_type_hinting.util import build_node, just_try, read_red, find_node


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


# @just_try
def get_module(additional_imports: Set[str]):
    if len(additional_imports) == 0:
        return None
    else:
        FROM = "from "
        s = next(iter(additional_imports))
        assert s.startswith(FROM)
        return s[len(FROM) :].split(" import")[0]


def add_annotations(red: RedBaron, tl: TypesLog) -> set:
    imports = set()
    def_node = find_node(red, tl)
    assert def_node is not None
    argName_to_node = {
        arg.name.fst()["value"]: (arg, "annotation") for arg in def_node.arguments
    }
    argName_to_node["return"] = (def_node, "return_annotation")

    for call_log in tl.call_logs.values():
        process_call_log(argName_to_node, call_log, imports)

    return imports


def process_call_log(
    argName_to_node,  #: Dict[str, Tuple[NameNode, str]],
    call_log: CallLog,
    imports: Set[str],
):
    logged_names_types = [
        (n, t) for n, t in call_log.arg2type.items() if n not in arg_name_blacklist
    ]
    logged_names_types += [("return", call_log.return_type)]

    for arg_name, arg_type in logged_names_types:
        new_annotation, additional_imports = parse_annotation_build_imports(arg_type)
        assert new_annotation is not None
        arg_node, attr_name = argName_to_node[arg_name]

        annotation = getattr(arg_node, attr_name)
        if annotation is not None:
            normalize = lambda s: s.dumps().replace(" ", "") if s is not None else None
            old_annotation = normalize(annotation)

            module_s = get_module(additional_imports)
            print(f"\n module: {module_s} \n")
            if module_s is None:
                new_annotation = old_annotation
            elif is_childclass(
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

        m_ann = build_node(new_annotation)

        setattr(arg_node, attr_name, m_ann)


def remove_unwanted_annotations(red):
    blacklist = ["Any", "None", "type"]

    for node in red.find_all("def"):
        for arg in node.arguments:
            if just_try()(lambda x: arg.annotation.dumps())(node) in blacklist:
                node.annotation = ""
        if just_try()(lambda x: x.return_annotation.dumps())(node) in blacklist:
            node.return_annotation = ""


def enrich_pyfiles_by_type_hints(
    type_logs: List[TypesLog], overwrite=True, verbose=False
):
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
        add_annotations_and_imports(red, tls, module)

        py_file = py_file if overwrite else f"{py_file.replace('.py','')}_modified.py"
        with open(py_file, "w") as source_code:
            source_code.write(red.dumps())


def add_annotations_and_imports(red, tls, module):
    existent_imports = get_existent_imports(red)
    imports = add_annotations_build_imports(red, tls)
    [
        red.insert(1, imp)
        for imp in imports
        if imp not in existent_imports and module not in imp
    ]


def add_annotations_build_imports(red: RedBaron, tls: List[TypesLog]):
    imports = {
        imp
        for type_log in tls
        for imp in add_annotations(red, type_log)
        if imp is not None
    }
    remove_unwanted_annotations(red)
    return imports
