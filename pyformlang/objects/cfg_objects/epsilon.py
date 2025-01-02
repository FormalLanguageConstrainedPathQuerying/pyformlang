"""An epsilon terminal in CFG."""

from .terminal import Terminal
from ..base_epsilon import BaseEpsilon


class Epsilon(BaseEpsilon, Terminal):
    """An epsilon terminal in CFG."""
