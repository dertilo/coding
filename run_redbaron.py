from typeguard.util import TypesLog
from util import data_io

from redbaron_type_hinting.adding_type_hints import enrich_pyfiles_by_type_hints

if __name__ == '__main__':
    type_logs = list(map(TypesLog.from_dict,data_io.read_jsonl("types.jsonl")))
    enrich_pyfiles_by_type_hints(type_logs,overwrite=True)