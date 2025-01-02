"""The feature structure containing constraints."""

from typing import Dict, List, Iterable, Tuple, Optional, Hashable


class ContentAlreadyExistsError(Exception):
    """Exception raised when we want to add a content that already exists."""


class PathDoesNotExistError(Exception):
    """Raised when looking for a path that does not exist."""


class FeatureStructuresNotCompatibleError(Exception):
    """Raised when trying to unify incompatible structures."""


class FeatureStructure:
    """The feature structure containing constraints.

    Parameters
    ----------
    value:
        The value of the feature, if defined.
    """

    def __init__(self, value: Hashable = None) -> None:
        """Initializes the feature structure."""
        self._content: Dict[str, FeatureStructure] = {}
        self._value = value
        self._pointer: Optional[FeatureStructure] = None

    @property
    def content(self) -> Dict[str, "FeatureStructure"]:
        """Gets the content of the current node."""
        return self._content

    @property
    def pointer(self) -> Optional["FeatureStructure"]:
        """Gets the pointer of the current node."""
        return self._pointer

    @pointer.setter
    def pointer(self, new_pointer: "FeatureStructure") -> None:
        """Sets the value of the pointer."""
        self._pointer = new_pointer

    @property
    def value(self) -> Hashable:
        """Gets the value associated with the current node."""
        return self._value if self.pointer is None else self.pointer.value

    @value.setter
    def value(self, new_value: Hashable) -> None:
        """Sets the value associated with the current node."""
        self._value = new_value

    def add_content(self,
                    content_name: str,
                    feature_structure: "FeatureStructure") -> None:
        """Adds content to the current feature structure.

        Parameters
        ----------
        content_name:
            The name of the new feature.
        feature_structure:
            The value of this new feature.

        Raises
        ------
        ContentAlreadyExistsError
            When the feature already exists.
        """
        if content_name in self._content:
            raise ContentAlreadyExistsError
        self._content[content_name] = feature_structure

    def add_content_path(self,
                         content_name: str,
                         feature_structure: "FeatureStructure",
                         path: List[str]) -> None:
        """Adds content to the current feature structure at a specific path.

        Parameters
        ----------
        content_name:
             The name of the new feature.
        feature_structure:
            The value of this new feature.
        path:
            The path where to add the new feature.

        Raises
        ------
        ContentAlreadyExistsError
            When the feature already exists.
        PathDoesNotExistsError
            When the path does not exist.
        """
        to_modify = self.get_feature_by_path(path)
        to_modify.add_content(content_name, feature_structure)

    def get_dereferenced(self) -> "FeatureStructure":
        """Gets the dereferenced version of the feature structure."""
        return self._pointer.get_dereferenced() \
            if self._pointer is not None else self

    def get_feature_by_path(self, path: List[str] = None) -> "FeatureStructure":
        """Gets a feature at the given path.

        Parameters
        ----------
        path:
            The path to the feature.

        Returns
        -------
        The feature structure at the end of the path.

        Raises
        ------
        PathDoesNotExistError
            When the path does not exist.
        """
        if not path or path is None:
            return self
        current = self.get_dereferenced()
        if path[0] not in current.content:
            raise PathDoesNotExistError()
        return current.content[path[0]].get_feature_by_path(path[1:])

    def unify(self, other: "FeatureStructure") -> None:
        """Unifies the current structure with another one.

        Modifies the current structure.

        Parameters
        ----------
        other:
            The other feature structure to unify.

        Raises
        ------
        FeatureStructuresNotCompatibleError
            When the feature structure cannot be unified.
        """
        current_dereferenced = self.get_dereferenced()
        other_dereferenced = other.get_dereferenced()
        if current_dereferenced == other_dereferenced:
            return
        if len(current_dereferenced.content) == 0 \
                and len(other_dereferenced.content) == 0:
            # We have a simple feature
            if current_dereferenced.value == other_dereferenced.value:
                current_dereferenced.pointer = other_dereferenced
            elif current_dereferenced.value is None:
                current_dereferenced.pointer = other_dereferenced
            elif other_dereferenced.value is None:
                other_dereferenced.pointer = current_dereferenced
            else:
                raise FeatureStructuresNotCompatibleError()
        else:
            other_dereferenced.pointer = current_dereferenced
            for feature in other_dereferenced.content:
                if feature not in current_dereferenced.content:
                    current_dereferenced.content[feature] = FeatureStructure()
                current_dereferenced.content[feature].unify(
                    other_dereferenced.content[feature])

    def subsumes(self, other: "FeatureStructure") -> bool:
        """Checks whether the current feature structure subsumes another one.

        Parameters
        ----------
        other:
            The other feature structure.

        Returns
        -------
        Whether the current feature structure subsumes the other one.
        """
        current_dereferenced = self.get_dereferenced()
        other_dereferenced = other.get_dereferenced()
        if current_dereferenced.value != other_dereferenced.value:
            return False
        for feature in current_dereferenced.content:
            if feature not in other_dereferenced.content:
                return False
            if not current_dereferenced.content[feature].subsumes(
                    other_dereferenced.content[feature]):
                return False
        return True

    def get_all_paths(self) -> List[List[str]]:
        """Gets the list of all path in the feature structure.

        Returns
        --------
        A list of paths in the feature structure.
        """
        res = []
        for feature, content in self._content.items():
            paths = content.get_all_paths()
            for path in paths:
                res.append([feature] + path)
        if not res:
            res.append([])
        return res

    def __repr__(self) -> str:
        """Gets the string representation of the feature structure."""
        res = []
        for path in self.get_all_paths():
            if path:
                feature = self.get_feature_by_path(path)
                value = feature.value
                if value is None:
                    value = id(feature)
                res.append(".".join(path) + "=" + str(value))
        return " | ".join(res)

    def copy(self, already_copied: Dict["FeatureStructure",
                                        "FeatureStructure"] = None) \
                                            -> "FeatureStructure":
        """Copies the current feature structure.

        Parameters
        ----------
        already_copied:
            A dictionary containing the parts already copied.

        Returns
        -------
        The copied feature structure.
        """
        if already_copied is None:
            already_copied = {}
        if self in already_copied:
            return already_copied[self]
        new_fs = FeatureStructure(self.value)
        if self._pointer is not None:
            pointer_copy = self._pointer.copy(already_copied)
            new_fs.pointer = pointer_copy
        for feature, content in self._content.items():
            new_fs.content[feature] = content.copy(already_copied)
        already_copied[self] = new_fs
        return new_fs

    @classmethod
    def from_text(cls,
                  text: str,
                  structure_variables: Dict[str, "FeatureStructure"] = None) \
                      -> "FeatureStructure":
        """Constructs a feature structure from the given text.

        Parameters
        ----------
        text:
            The text to parse.
        structure_variables:
            The existing structure variables.

        Returns
        -------
        The parsed feature structure.
        """
        if structure_variables is None:
            structure_variables = {}
        preprocessed_conditions = _preprocess_conditions(text)
        return _create_feature_structure(
            preprocessed_conditions, structure_variables)


def _find_closing_bracket(condition: str,
                          start: int,
                          opening: str = "[",
                          closing: str = "]") -> int:
    counter = 0
    pos = start
    for current_char in condition[start:]:
        if current_char == opening:
            counter += 1
        elif current_char == closing:
            counter -= 1
        if counter == 0:
            return pos
        pos += 1
    return -1


class ParsingError(Exception):
    """Raised when there is a problem during parsing."""


def _preprocess_conditions(conditions: str,
                           start: int = 0,
                           end: int = -1) -> List[Tuple[str, str, str]]:
    conditions = conditions.replace("->", "=")
    conditions = conditions.strip()
    res = []
    reading_feature = True
    current_feature = ""
    current_value = ""
    reference = None
    pos = start
    end = len(conditions) if end == -1 else end
    while pos < end:
        current = conditions[pos]
        if current == "=":
            reading_feature = False
            pos += 1
        elif reading_feature:
            current_feature += current
            pos += 1
        elif current == "[":
            end_bracket = _find_closing_bracket(conditions, pos)
            if end_bracket == -1:
                raise ParsingError()
            current_value = _preprocess_conditions(
                conditions, pos + 1, end_bracket)
            pos = end_bracket + 1
        elif current == "(":
            end_bracket = _find_closing_bracket(conditions, pos, "(", ")")
            if end_bracket == -1:
                raise ParsingError()
            reference = conditions[pos+1: end_bracket]
            pos = end_bracket + 1
        elif current == ",":
            reading_feature = True
            if isinstance(current_value, str):
                current_value = current_value.strip()
            res.append((current_feature.strip(), current_value, reference))
            current_feature = ""
            current_value = ""
            reference = None
            pos += 1
        else:
            current_value += current # type: ignore
            pos += 1
    if current_feature.strip():
        if isinstance(current_value, str):
            current_value = current_value.strip()
        res.append((current_feature.strip(), current_value, reference))
    return res


def _create_feature_structure(
        conditions: Iterable[Tuple[str, str, str]],
        structure_variables: Dict[str, FeatureStructure],
        existing_references: Dict[str, FeatureStructure] = None,
        feature_structure: FeatureStructure = None) \
            -> FeatureStructure:
    if existing_references is None:
        existing_references = {}
    if feature_structure is None:
        feature_structure = FeatureStructure()
    for feature, value, reference in conditions:
        if reference is not None:
            if reference not in existing_references:
                existing_references[reference] = FeatureStructure()
            new_fs = existing_references[reference]
        else:
            new_fs = FeatureStructure()
        if value and isinstance(value, str):
            if value[0] != "?":
                new_fs.value = value
                feature_structure.add_content(feature, new_fs)
            elif value[1:] in structure_variables:
                new_fs.pointer = structure_variables[value[1:]]
                feature_structure.add_content(feature, new_fs)
            else:
                feature_structure.add_content(feature, new_fs)
                structure_variables[value[1:]] = new_fs
        elif not isinstance(value, str):
            structure = _create_feature_structure(
                value, structure_variables, existing_references, new_fs)
            feature_structure.add_content(feature, structure)
        else:
            feature_structure.add_content(feature, new_fs)
    return feature_structure
