from os.path import realpath

from cronspell.cronspell import Cronspell


def locate():
    """
    \b
    * finds the location of the meta model. For your convenience
    """
    print(realpath(Cronspell().meta_model_src))  # noqa: T201
