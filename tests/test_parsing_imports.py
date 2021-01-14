import pytest
from redbaron import RedBaron
from redbaron_type_hinting.parsing_imports import parse_imports


@pytest.mark.parametrize(
    "pysource,expected",
    [
        ("import pytest", (None, "pytest", None)),
        ("import foo as bar", (None, "foo", "bar")),
        ("from foo import bar", ("foo", "bar", None)),
        ("from foo.woo import bar", ("foo.woo", "bar", None)),
        ("from foo.woo import bar as bazz", ("foo.woo", "bar", "bazz")),
        (
            "from foo.woo import bar, bazz, woo",
            ("foo.woo", ["bar", "bazz", "woo"], None),
        ),
    ],
)
def test_parse_imports(pysource, expected):
    r = RedBaron(pysource)[0]
    parsed = parse_imports(r)
    assert expected == parsed
