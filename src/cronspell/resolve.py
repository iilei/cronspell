from cronspell.cronspell import Cronspell

cronspell = Cronspell()


def resolve(expression: str = "now"):
    return cronspell.parse(expression).replace(microsecond=0)
