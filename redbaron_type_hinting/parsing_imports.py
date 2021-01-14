from typing import NamedTuple

from redbaron import RedBaron


class Import(NamedTuple):
    module: str
    value: str
    target: str


def parse_imports(r: RedBaron) -> Import:
    get_target = lambda x: x.target if len(x.target) > 0 else None
    if r.type == "import":
        value_root = r.value[0]
        value = value_root.value[0].value
        parsed = (None, value, get_target(value_root))
    elif r.type == "from_import":
        module = ".".join([x.value for x in r.value])
        value = [t.value for t in r.targets]
        value = value[0] if len(value) == 1 else value
        parsed = (module, value, get_target(r.targets[0]))
    else:
        parsed = (None, None, None)
    return Import(*parsed)
