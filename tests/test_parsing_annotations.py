import pytest

from redbaron_type_hinting.parsing_annotations import parse_annotation_build_imports


@pytest.mark.parametrize(
    "annotation,expected_ann,expected_imports",
    [
        (
            "List[str,numpy.ndarray]",
            "List[str,ndarray]",
            {"from typing import List", "from numpy import ndarray"},
        ),
        ("numpy.ndarray","ndarray", {"from numpy import ndarray"})
    ],
)
def test_parse_annotation(annotation, expected_ann, expected_imports):
    ann_name, imports = parse_annotation_build_imports(annotation)
    assert ann_name == expected_ann
    assert imports == expected_imports
