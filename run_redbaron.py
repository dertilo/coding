from redbaron_type_hinting.adding_type_hints import enrich_pyfiles_by_type_hints

if __name__ == '__main__':
    enrich_pyfiles_by_type_hints("types.jsonl",overwrite=True)