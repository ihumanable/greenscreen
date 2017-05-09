from typing import Optional, List

from blessed import Terminal
from math import floor

from collections import defaultdict

from greenscreen.components.base import Component


class Layout(Component):
    pass


class HorizontalLayout(Layout):
    def __init__(self, children: List[Component]=None, weights: List[int]=None):
        self.weights: List[int] = weights or []
        self.children: List[Component] = children or []
        self.repack(self.weights)

    def repack(self, weights: List[int]):
        self.weights = weights + ([1] * (max(0, len(self.children) - len(weights))))

    def append(self, child: Component, weight: int=1):
        self.children.append(child)
        self.weights.append(weight)

    def widths(self, width: int) -> List[int]:
        columns = sum(self.weights)
        column = int(floor(width / columns))
        result = [column * weight for weight in self.weights]
        if width % column == 0:
            return result

        remainder = width - sum(result)
        targets = sorted(result)[:remainder]

        width_counts = defaultdict(int)
        for target in targets:
            width_counts[target] += 1

        for idx, col in enumerate(result):
            if col in width_counts and width_counts[col] > 0:
                result[idx] += 1
                width_counts[col] -= 1

        return result

    def render(self, terminal: Terminal, width: Optional[int]=None) -> str:
        width = width or terminal.width
        widths = self.widths(width)

        result = ''
        for idx, w in enumerate(widths):
            c = str(idx)[0]
            result += c * w

        return result
