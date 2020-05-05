############################################################
#   DOUBLY LINKED LIST (DLL)
############################################################

########################################
#   NODE
########################################


class DoublyLinkedNode:
    """
    Each DoublyLinkedNode contains
    -   `value`: a value
    -   `prev_node`: a reference to its previous node
    -   `next_node`: a reference to its next node
    """

    def __init__(self, value, prev_node=None, next_node=None):

        self.value = value
        self.prev_node = prev_node
        self.next_node = next_node

        return

    def push_before(self, value):
        """
        Wrap `value` in a node and insert it before this node (`self`).
        """

        self_prev_node = self.prev_node
        self.prev_node = DoublyLinkedNode(value, self_prev_node, self)

        if self_prev_node:
            self_prev_node.next_node = self.prev_node

        return

    def push_after(self, value):
        """
        Wrap `value` in a node and insert it after this node (`self`).
        """

        self_next_node = self.next_node
        self.next_node = DoublyLinkedNode(value, self, self_next_node)

        if self_next_node:
            self_next_node.prev_node = self.next_node

        return

    def pop_before(self):
        pass

    def pop_after(self):
        pass

    def pop(self):
        """
        Rearranges this node's references, effectively deleting this node.
        Returns the `value` of this node.
        """

        value = self.value

        if self.prev_node:
            self.prev_node.next_node = self.next_node

        if self.next_node:
            self.next_node.prev_node = self.prev_node

        return value


########################################
#   LIST
########################################


class DoublyLinkedList:
    """
    Each DoublyLinkedList contains
    -   `head_node`: a reference to the list's head node.
    -   `tail_node`: a reference to the list's tail node.
    """

    def __init__(self, node=None):

        self.head_node = node
        self.tail_node = node
        self.__length = 1 if node is not None else 0

        return

    def __len__(self):

        return self.__length

    def push_to_head(self, value):
        """
        Wrap `value` in a node and insert it as this list's new `head_node`.
        Returns the list's new length.
        """

        new_node = DoublyLinkedNode(value)

        if not self.head_node and not self.tail_node:
            self.head_node = new_node
            self.tail_node = new_node

        else:
            old_head = self.head_node
            new_node.next_node = old_head
            old_head.prev_node = new_node
            self.head_node = new_node

        self.__length += 1

        return len(self)

    def push_to_tail(self, value):
        """
        Wrap `value` in a node and insert it as this list's new `tail_node`.
        Returns the list's new length.
        """

        new_node = DoublyLinkedNode(value)

        if not self.head_node and not self.tail_node:
            self.head_node = new_node
            self.tail_node = new_node

        else:
            old_tail = self.tail_node
            new_node.prev_node = old_tail
            old_tail.next_node = new_node
            self.tail_node = new_node

        self.__length += 1

        return len(self)

    def pop_node(self, node):
        """
        Remove `node` from the list.
        Handles cases where `node` was the list's head or tail.
        Returns the removed node's `value` and the list's new length.
        """

        # if it's the only node
        if node is self.head_node and node is self.tail_node:
            self.head_node = None
            self.tail_node = None

        # if it's the head
        elif node is self.head_node:
            self.head_node = node.next_node

        # if it's the tail
        elif node is self.tail_node:
            self.tail_node = node.prev_node

        # if it's in the middle
        else:
            pass

        value = node.pop()
        self.__length -= 1

        return (value, len(self))

    def pop_from_head(self):
        """
        Replace the list's current `head_node` with `head_node.next_node`.
        Returns the removed node's `value` and the list's new length.
        """

        if self.head_node is not None:
            return self.pop_node(self.head_node)

        else:
            return (None, len(self))

    def pop_from_tail(self):
        """
        Replace the list's current `tail_node` with `tail_node.next_node`.
        Returns the removed node's `value` and the list's new length.
        """

        if self.tail_node is not None:
            return self.pop_node(self.tail_node)

        else:
            return (None, len(self))

    def move_to_head(self, node):
        """
        Remove `node` from its current spot in the list.
        Insert `node` as the list's `head_node`.
        Returns the list's new length, which should be unchanged.
        """

        if node is not self.head_node:
            self.pop_node(node)
            self.push_to_head(node.value)

        return len(self)

    def move_to_tail(self, node):
        """
        Remove `node` from its current spot in the list.
        Insert `node` as the list's `tail_node`.
        Returns the list's new length, which should be unchanged.
        """

        if node is not self.tail_node:
            self.pop_node(node)
            self.push_to_tail(node.value)

        return len(self)
