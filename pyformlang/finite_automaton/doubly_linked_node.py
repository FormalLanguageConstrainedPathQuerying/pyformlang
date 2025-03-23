"""Nodes linked in both directions."""

from typing import Optional, Any


class DoublyLinkedNode:
    """A node in the doubly linked list."""

    def __init__(self,
                 next_node: "DoublyLinkedNode" = None,
                 previous_node: "DoublyLinkedNode" = None,
                 value: Any = None) -> None:
        """Initializes the node."""
        self.next_node: Optional[DoublyLinkedNode] = next_node
        self.previous_node: Optional[DoublyLinkedNode] = previous_node
        self.value: Any = value

    def append(self, value: Any) -> "DoublyLinkedNode":
        """Appends a new node with the given value.

        Parameters
        ----------
        value:
            A value of the new node.

        Returns
        -------
        The created node.
        """
        next_node = DoublyLinkedNode(self.next_node, self, value)
        self.next_node = next_node
        return next_node
