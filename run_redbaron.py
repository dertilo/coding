import json
from redbaron import RedBaron, NameNode, Node

if __name__ == '__main__':

    with open("dummy_module_2.py", "r") as source_code:
        red = RedBaron(source_code.read())

    print(json.dumps(red.fst(), indent=4))
    annotation_fst = {
        "type": "name",
        "value": "str"
    }
    node = Node.from_fst(annotation_fst)

    red.find_all("def")[0].return_annotation = node
    red.find_all("def")[0].arguments[0].annotation = Node.from_fst({'type': 'name', 'value': 'DummyClass'})
    red.insert(1,"from bla import dings")
    # import_fs = {'type': 'from_import', 'first_formatting': [{'type': 'space', 'value': ' '}], 'value': [{'type': 'name', 'value': 'dummy_module'}], 'second_formatting': [{'type': 'space', 'value': ' '}], 'third_formatting': [{'type': 'space', 'value': ' '}], 'targets': [{'type': 'name_as_name', 'value': 'DummyClass', 'target': '', 'first_formatting': [], 'second_formatting': []}]}


    with open("modified_code.py", "w") as source_code:
        source_code.write(red.dumps())