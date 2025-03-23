"""Production rules with features."""

from typing import List, Iterable

from pyformlang.cfg import CFGObject, Variable, Production

from .feature_structure import FeatureStructure


class FeatureProduction(Production):
    """A feature production or rule of a FCFG.

    Parameters
    ----------
    head:
        The head of the production.
    body:
        The body of the production.
    head_feature:
        The feature structure of the head.
    body_features:
        The feature structures of the elements of the body.
        Must be the same size as the body.
    filtering:
        Whether to ignore the epsilon terminals in body.
    """

    def __init__(self,
                 head: Variable,
                 body: List[CFGObject],
                 head_feature: FeatureStructure,
                 body_features: Iterable[FeatureStructure],
                 filtering: bool = True) -> None:
        """Initializes the feature production."""
        super().__init__(head, body, filtering)
        self._features = FeatureStructure()
        self._features.add_content("head", head_feature)
        for i, feature_structure in enumerate(body_features):
            self._features.add_content(str(i), feature_structure)

    @property
    def features(self) -> FeatureStructure:
        """Gets the merged features of the production rules."""
        return self._features

    def __repr__(self) -> str:
        """Gets the string representation of the feature grammar."""
        res = [self.head.to_text()]
        cond_head = str(self._features.get_feature_by_path(["head"]))
        if cond_head:
            res.append("[" + cond_head + "]")
        res.append("->")
        for i, body_part in enumerate(self.body):
            res.append(body_part.to_text())
            body_part_cond = str(self._features.get_feature_by_path([str(i)]))
            if body_part_cond:
                res.append("[" + body_part_cond + "]")
        return " ".join(res)
