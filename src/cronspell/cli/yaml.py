import enum
import logging
import sys
from pathlib import Path

from yamlpath import Processor
from yamlpath.common import Parsers


class LogLevel(str, enum.Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


def setup_logging(log_level: LogLevel):
    """Setup basic logging"""
    log_format = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    numeric_level = getattr(logging, log_level.upper(), None)
    logging.basicConfig(
        level=numeric_level,
        stream=sys.stdout,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


yaml = Parsers.get_yaml_editor()


def get_processor(file: Path) -> Processor:
    logging.raiseExceptions = True
    logging.logThreads = False

    log = logging.getLogger("root")
    yaml_file = file
    (yaml_data, _) = Parsers.get_yaml_data(yaml, log, yaml_file)
    return Processor(log, yaml_data)
