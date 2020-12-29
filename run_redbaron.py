import json
from redbaron import RedBaron, NameNode, Node
from util import data_io
from typeguard.util import TYPES_JSONL,TypesLog

def add_type_annotations(py_file):
    with open(py_file, "r") as source_code:
        red = RedBaron(source_code.read())

    annotation_fst = {
        "type": "name",
        "value": "str"
    }
    node = Node.from_fst(annotation_fst)
    red.find_all("def")[0].return_annotation = node
    red.find_all("def")[0].arguments[0].annotation = Node.from_fst(
        {'type': 'name', 'value': 'DummyClass'})
    red.insert(1, "from bla import dings")
    # formatting = [{'type': 'space', 'value': ' '}]
    # import_fs = {'type': 'from_import', 'first_formatting': formatting, 'value': [{'type': 'name', 'value': 'dummy_module'}], 'second_formatting': formatting, 'third_formatting': formatting, 'targets': [{'type': 'name_as_name', 'value': 'DummyClass', 'target': '', 'first_formatting': [], 'second_formatting': []}]}
    with open("modified_code.py", "w") as source_code:
        source_code.write(red.dumps())


if __name__ == '__main__':

    py_file = "dummy_module_2.py"
    print([TypesLog(**d) for d in data_io.read_jsonl(TYPES_JSONL)])

    # add_type_annotations()