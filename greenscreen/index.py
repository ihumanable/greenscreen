from typing import List, Optional


class ListIndex(object):
    def __init__(self, target: List):
        self.target = target
        self._index = 0

    @property
    def index(self) -> Optional[int]:
        return self._index if self.target else None

    @property
    def value(self):
        return self.target[self.index] if self.target else None

    def incr(self, amount=1):
        if self.target:
            self._index = min(len(self.target) - 1, self._index + amount)

    def decr(self, amount=1):
        if self.target:
            self._index = max(0, self._index - amount)
