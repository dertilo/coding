import pytest
from redbaron import RedBaron


@pytest.mark.parametrize(
    "pysource,expected", [("import pytest", (None, "pytest", None))]
)
def test_parse_imports(pysource, expected):
    exp_module, exp_value, exp_target = expected
    value = None
    r = RedBaron(pysource)[0]
    if r.type == "import":
        if r.value[0].target == "":
            value = r.value[0].value[0].value
    assert exp_value == value
