""" Interface representing the ability of conversion to cfg object """

from typing import Optional, Any
from abc import abstractmethod

from ..formal_object import FormalObject


class CFGObjectConvertible(FormalObject):
    """ Interface representing the ability of conversion to cfg object """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.index_cfg_converter: Optional[int] = None

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError
