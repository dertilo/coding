from typing import List

import pytest
from redbaron import RedBaron, NameNode

from redbaron_type_hinting.parsing_annotations import parse_annotation_build_imports
from redbaron_type_hinting.parsing_imports import parse_imports


@pytest.mark.parametrize(
    "annotation,expected_ann,expected_imports",
    [
        (
            "List[str,numpy.ndarray]",
            "List[str,ndarray]",
            {"from typing import List", "from numpy import ndarray"},
        ),
        ("numpy.ndarray", "ndarray", {"from numpy import ndarray"}),
    ],
)
def test_parse_annotation(annotation, expected_ann, expected_imports):
    ann_name, imports = parse_annotation_build_imports(annotation)
    assert ann_name == expected_ann
    assert imports == expected_imports


@pytest.mark.parametrize(
    "typpe,imports,exp_annotation,exp_new_imports",
    [
        (
            "woo.foo.bar",
            "from bazz import bar\nfrom woo.foo import waa",
            "woo_foo_bar",
            {"from woo.foo import bar as woo_foo_bar"},
        )
    ],
)
def test_parse_type_build_annotation_imports(
    typpe, imports, exp_annotation, exp_new_imports
):
    DOT_REPLACEMENT = "_____"
    type_red = RedBaron(typpe.replace(".", DOT_REPLACEMENT))
    name_nodes: List[NameNode] = [m for m in type_red.find_all("NameNode")]
    imports = [parse_imports(r) for r in RedBaron(imports)]
    ann2import = {i.target if i.target is not None else i.value: i for i in imports}
    new_imports = set()
    for nn in name_nodes:
        fullpath_ann = nn.value.replace(DOT_REPLACEMENT, ".")
        *packages, import_name = fullpath_ann.split(".")
        module = ".".join(packages)
        if import_name in ann2import.keys():
            target = fullpath_ann.replace(".", "_")
            annotation = target
            new_imports.add(f"from {module} import {import_name} as {target}")
        else:
            annotation = import_name
            new_imports.add(f"from {module} import {import_name}")
        nn.value = annotation

    assert type_red.dumps() == exp_annotation
    assert new_imports == exp_new_imports
