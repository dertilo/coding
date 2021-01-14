import pytest
from redbaron import RedBaron


@pytest.mark.parametrize(
    "pysource,expected",
    [
        ("import pytest", (None, "pytest", None)),
        ("import foo as bar", (None, "foo", "bar")),
        ("from foo import bar", ("foo", "bar", None)),
        ("from foo.woo import bar", ("foo.woo", "bar", None)),
        ("from foo.woo import bar as bazz", ("foo.woo", "bar", "bazz")),
    ],
)
def test_parse_imports(pysource, expected):
    parsed = (None, None, None)
    r = RedBaron(pysource)[0]
    get_target = lambda x: x.target if len(x.target) > 0 else None
    if r.type == "import":
        value_root = r.value[0]
        value = value_root.value[0].value
        parsed = (None, value, get_target(value_root))
    elif r.type == "from_import":
        module = ".".join([x.value for x in r.value])
        value = r.targets[0].value
        parsed = (module, value, get_target(r.targets[0]))
    assert expected == parsed
