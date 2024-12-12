import logging
from pathlib import Path

from yamlpath import Processor
from yamlpath.common import Parsers

yaml = Parsers.get_yaml_editor()


def get_processor(file: Path) -> Processor:
    logging.raiseExceptions = True
    logging.logThreads = False

    log = logging.getLogger("root")
    yaml_file = file
    (yaml_data, _) = Parsers.get_yaml_data(yaml, log, yaml_file)
    return Processor(log, yaml_data)
