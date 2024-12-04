from pathlib import Path
from types import SimpleNamespace

from yamlpath import Processor
from yamlpath.common import Parsers
from yamlpath.wrappers import ConsolePrinter

logging_args = SimpleNamespace(quiet=True, verbose=False, debug=False)
log = ConsolePrinter(logging_args)

yaml = Parsers.get_yaml_editor()


def get_processor(file: Path) -> Processor:
    yaml_file = file
    (yaml_data, doc_loaded) = Parsers.get_yaml_data(yaml, log, yaml_file)
    if not doc_loaded:
        msg = f"Can not load file {file}"
        raise OSError(msg)

    return Processor(log, yaml_data)
