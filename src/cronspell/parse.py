from cronspell.cronspell import Cronspell

cronspell = Cronspell()


def parse(expression: str = "now"):
    return cronspell.parse(expression)
