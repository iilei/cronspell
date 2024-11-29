from datetime import datetime
from functools import cache, partial
from typing import Union

from cronspell.cronspell import Cronspell

cronspell = Cronspell()


@cache
def parser(now: Union[None, datetime] = None):
    return partial(cronspell.parse, now=now)


@cache
def resolve(expression: str = "now", now: Union[None, datetime] = None):
    return parser(now)(expression).replace(microsecond=0)
