import pytest
from redbaron import RedBaron


@pytest.mark.parametrize(
    "pysource,expected",
    [
        ("import pytest", (None, "pytest", None)),
        ("import foo as bar", (None, "foo", "bar")),
    ],
)
def test_parse_imports(pysource, expected):
    parsed = (None, None, None)
    r = RedBaron(pysource)[0]
    if r.type == "import":
        value_root = r.value[0]
        target = value_root.target
        value = value_root.value[0].value
        if target == "":
            parsed = (None, value, None)
        else:
            parsed = (None, value, target)
    assert expected == parsed
