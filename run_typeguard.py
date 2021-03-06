from dataclasses import asdict
from pprint import pprint

from typeguard.importhook import install_import_hook
install_import_hook('dummy_package')

from typeguard.util import TYPEGUARD_CACHE
from util import data_io

from test_type_hinting import main_dummy


if __name__ == '__main__':

    main_dummy()
    type_logs = [asdict(x) for x in TYPEGUARD_CACHE.values()]
    pprint(type_logs)
    data_io.write_jsonl("types.jsonl",type_logs)