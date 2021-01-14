import pytest
from redbaron import RedBaron


@pytest.mark.parametrize(
    "pysource,expected",
    [
        ("import pytest", (None, "pytest", None)),
        ("import foo as bar", (None, "foo", "bar")),
        ("from foo import bar", ("foo", "bar", None)),
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
    elif r.type == "from_import":
        module = ".".join([x.value for x in r.value])
        value = r.targets[0].value
        parsed = (module, value, None)
    assert expected == parsed
