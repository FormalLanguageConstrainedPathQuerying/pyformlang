""" Interface representing the ability of conversion to cfg object """

from typing import Optional, Any


class CFGConvertible:
    """ Interface representing the ability of conversion to cfg object """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.index_cfg_converter: Optional[int] = None
