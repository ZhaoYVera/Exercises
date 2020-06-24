from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable

# @dataclass()
# class LinkedListItem:
#     data: "An elepant"
#     next: Any
#     prev: "Any"

# SLLItem = make_dataclass("SingleLinkedListItem", fields=['body', 'next'],
#                          repr=False, eq=False)
# DLLItem = make_dataclass("DoubleLinkedListItem", fields=['body', 'next', 'prev'],
#                          repr=False, eq=False)

@dataclass()
class SLinkedListItem:
    """Single linked list item."""
    body: Any
    next: SLinkedListItem = field(default=None, compare=False, repr=False)

    def __str__(self):
        return f"body={str(self.body)}, next={str(self.next.body)}"


class SLinkedList:
    """Single linked list, of first-in-last-out (i.e stack) style """

    def __init__(self, items: Iterable = ()):
        self.next = None  # Attribute "next" is chosen to mimic SLinkedListItem behavior
        for item in items:
            self.push(item)

    def __iter__(self):
        curr = self.next  # current
        while curr is not None:
            yield curr.body
            curr = curr.next

    def push(self, item):
        """insert item between self and self.next"""
        item = SLinkedListItem(item, self.next)
        self.next = item

    def pop(self):
        first = self.next
        if first is None:
            raise ValueError("Cannot pop item from an empty list")
        self.next = first.next
        return first.body

    def pop_min(self):
        """delete and return the minimum item in self, given that item.body is comparable.
        If self is empty, raise ValueError
        """
        curr = self.next
        if curr is None:
            raise ValueError(f"Cannot extract min from an empty list")
        best_pred = self
        best = curr
        pred, curr = curr, curr.next
        while curr is not None:
            if curr.body < best.body:
                best = curr
                best_pred = pred
            pred, curr = curr, curr.next
        best_pred.next = best.next
        return best.body

    @property
    def empty(self) -> bool:
        return self.next is None


class DoubleLinkedList:
    pass


class CircularLinkedList:
    pass

if __name__ == '__main__':
    sll = SLinkedList(range(3))
    print('haha')