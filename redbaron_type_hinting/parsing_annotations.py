from functools import partial
from typing import Tuple, List, Union, Dict, Set, Optional

from redbaron_type_hinting.parse_seq_to_tree import branch_to_string, parse_tree

typing_list = ["List", "Dict", "Tuple", "Generator", "Any"]
replace_map = {"NoneType": "None"}


def build_ann_accum_imports(node_name, imports:Set[str]):

    module_path, ann_name = parse_qualname(node_name)
    if module_path is not None:
        imp = f"from {module_path} import {ann_name}"
        imports.add(imp)
    elif ann_name.capitalize() in typing_list:
        ann_name = ann_name.capitalize()
        imp = f"from typing import {ann_name}"
        imports.add(imp)

    # TODO(tilo): check for inheritance here
    # module_s = get_module(additional_imports)
    # is_childclass(
    #         mother=old_annotation, child=new_annotation, module_s=module_s
    # ):
    #     new_annotation = old_annotation

    ann_name = replace_map.get(ann_name, ann_name)
    return ann_name


def parse_annotation_build_imports(qualname):
    imports = set()
    process_node = partial(build_ann_accum_imports, imports=imports)
    ann_name = next(iter(parse_tree(list(qualname), branch_to_string, process_node)))
    return ann_name, imports


def parse_qualname(qualname: str) -> Tuple[Optional[str], str]:
    """
    :param qualname: like: numpy.ndarray
    :return:
        module_path = numpy
        type_name = ndarry
    """
    if "." in qualname:
        s = qualname.split(".")
        module_path = ".".join(s[:-1])
        type_name = s[-1]
    else:
        type_name = qualname
        module_path = None
    return module_path, type_name