from functools import cache, partial

from cronspell.cronspell import Cronspell

cronspell = Cronspell()


@cache
def parser():
    return partial(cronspell.parse)


@cache
def resolve(expression: str = "now"):
    return parser()(expression).replace(microsecond=0)
