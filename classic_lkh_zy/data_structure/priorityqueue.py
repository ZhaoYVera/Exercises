from __future__ import annotations
import abc
from dataclasses import dataclass, field
from typing import Any
from linked_list import SLinkedList, SLinkedListItem


class PriorityQueue(abc.ABC):
    @abc.abstractmethod
    def put(self, item):
        """Put a new item into the queue."""

    @abc.abstractmethod
    def report_first(self):
        """find and return the item with the highest priority."""

    @abc.abstractmethod
    def pop_first(self):
        """Find, delete and return the item with the highest priority."""

    @abc.abstractmethod
    def change_key(self, target, new_key, is_pointer: bool = True):
        """change the target's key to new_key. If is_pointer, this can be quickly done
        depending on the specific implementation. Else, one needs to search target in the queue first,
        which can be computationally expensive.
        """

    @abc.abstractmethod
    def empty(self) -> bool:
        """whether the queue is empty"""


class PQLL(SLinkedList):
    """Single linked list implementation of priority queue."""

    def __init__(self, items=()):
        super().__init__(items)
        self.put = self.push
        self.pop_first = self.pop_min

    def report_first(self):
        return min(self)

    def change_key(self, target, new_key, is_pointer: bool = True):
        if is_pointer:
            # In the linked
            target.key = new_key
        else:
            for item in self:
                if item.body == target:
                    item.body.key = new_key
            else:
                raise ValueError(f"{target} is not in the list")


if __name__ == '__main__':
    ll = PQLL(reversed(range(5)))
    ll.pop_first()
    print('haha')
