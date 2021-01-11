from functools import partial
from typing import Tuple, List, Union, Dict, Set, Optional

import pytest

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


@pytest.mark.parametrize(
    "annotation,expected_ann,expected_imports",
    [
        (
            "List[str,numpy.ndarray]",
            "List[str,ndarray]",
            {"from typing import List", "from numpy import ndarray"},
        )
    ],
)
def test_parse_annotation(annotation, expected_ann, expected_imports):
    ann_name, imports = parse_annotation_build_imports("List[str,numpy.ndarray]")
    assert ann_name == expected_ann
    assert imports == expected_imports


if __name__ == "__main__":
    ann_name, imports = parse_annotation_build_imports("List[str,numpy.ndarray]")
    print(ann_name)
    print(imports)
