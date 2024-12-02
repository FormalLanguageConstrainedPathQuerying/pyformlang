""" Interface representing the ability of conversion to cfg object """

from typing import Optional


class CFGConvertible:
    """ Interface representing the ability of conversion to cfg object """

    def __init__(self) -> None:
        self.index_cfg_converter: Optional[int] = None
