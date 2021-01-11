from typing import Tuple, List, Union, Dict


def parse_annotation_build_imports(qualname: str) -> Tuple[str, set]:
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


typing_list = ["List", "Dict", "Tuple", "Generator", "Any"]
replace_map = {"NoneType": "None"}


def build_path_name(type_name: str) -> Tuple[str, str]:
    if "." in type_name:
        s = type_name.split(".")
        module_path = ".".join(s[:-1])
        type_name = s[-1]
    else:
        module_path = None
    return module_path, type_name
