""" An epsilon symbol """

from .stack_symbol import StackSymbol


class Epsilon(StackSymbol):
    """ An epsilon symbol """
    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        super().__init__("epsilon")
