from collections import defaultdict, deque
from math import floor
from typing import List, Iterable, Set

from greenscreen.components.base import Component
from greenscreen.display.border import Border, Borders
from greenscreen.display.sizing import Sizing
from greenscreen.display.text import Line, Color, Capability


class Layout(Component):
    @classmethod
    def weighted(cls, amount: int, weights: List[int]):
        """
        Separates a given amount into distinct whole-number weighted areas.  
        If the area does not even divide, it will apportion the remainder 
        evenly starting with the smallest area.
        
        Weights are expressed as integers and express the relative weight of
        each section.  An even split would have the weight [1, 1] (technically
        it would be any where the weights are the same integer, so [3, 3] or 
        [10, 10] would work equally well).
        
        This allows for the easy representation of proportional layouts.
        
        +-----+---------------+
        |  S  |               |
        |  I  |   Main        |
        |  D  |      Area     |
        |  E  |               |
        +-----+---------------+
           5          15              Weights [1, 3]
           
        This allows layouts to dynamically reallocate space as overall display
        space changes.
        
        Layout.weighted(20, [1, 3]) -> [5, 15]
        Layout.weighted(80, [1, 3]) -> [20, 60]
        Layout.weighted(81, [1, 3]) -> [21, 60]
        Layout.weighted(82, [1, 3]) -> [21, 61]
        
        Weighted does guarantee that the sum of the result will always equal the
        input amount.
        
        :param amount: Amount to subdivide 
        :param weights: List of weights
        :return: List of subdivided amounts 
        """
        partition_count = len(weights)
        bank_count = sum(weights)
        size = int(floor(amount / bank_count))
        bank = [size] * bank_count

        remainder = amount - (size * bank_count)
        for idx in range(remainder):
            bank[idx] += 1

        partitions = defaultdict(deque)
        for current, weight in enumerate(sorted(weights)):
            partition = 0
            indices = cls.indices(weight, partition_count - current)
            for idx in indices:
                partition += bank.pop(idx)
            partitions[weight].appendleft(partition)

        result = []
        for weight in weights:
            result.append(partitions[weight].pop())

        return result

    @classmethod
    def indices(cls, size: int, count: int) -> Iterable[int]:
        return range((size - 1) * count, -1, -count)


class HorizontalLayout(Layout):
    def __init__(self,
                 children: List[Component]=None,
                 weights: List[int]=None,
                 border: Border=Borders.NONE,
                 padding: Sizing=None,
                 margin: Sizing=None,
                 foreground: Color=None,
                 background: Color=None,
                 capabilities: Set[Capability]=None):
        super().__init__(border, padding, margin, foreground, background, capabilities)
        self.weights: List[int] = weights or []
        self.children: List[Component] = children or []
        self.repack(self.weights)

    def repack(self, weights: List[int]):
        self.weights = weights + ([1] * (max(0, len(self.children) - len(weights))))

    def append(self, child: Component, weight: int = 1):
        self.children.append(child)
        self.weights.append(weight)

    def combine(self, lines: Iterable[Line]) -> Line:
        result, *tail = lines
        for line in tail:
            result += line
        return result

    def content(self, width: int, height: int) -> List[Line]:
        widths = self.weighted(width, self.weights)

        debug = Line('{}x{} Weights: {}, Widths: {}'.format(width, height, self.weights, widths))

        columns = []
        for child_width, component in zip(widths, self.children):
            columns.append(component.render(child_width, height - 1))

        return [debug.fit(width)] + [self.combine(group) for group in zip(*columns)]

    def keypress(self, key):
        if key.name == 'KEY_UP':
            self.weights[0] += 1
        elif key.name == 'KEY_DOWN':
            self.weights[0] = max(1, self.weights[0] - 1)


class VerticalLayout(Layout):
    def __init__(self,
                 children: List[Component]=None,
                 weights: List[int]=None,
                 border: Border=Borders.NONE,
                 padding: Sizing=None,
                 margin: Sizing=None,
                 foreground: Color=None,
                 background: Color=None,
                 capabilities: Set[Capability]=None):
        super().__init__(border, padding, margin, foreground, background, capabilities)
        self.weights: List[int] = weights or []
        self.children: List[Component] = children or []
        self.repack(self.weights)

    def repack(self, weights: List[int]):
        self.weights = weights + ([1] * (max(0, len(self.children) - len(weights))))

    def append(self, child: Component, weight: int = 1):
        self.children.append(child)
        self.weights.append(weight)

    def content(self, width: int, height: int) -> List[Line]:
        height = height - 1

        heights = self.weighted(height, self.weights)

        debug = Line('{}x{} Weights: {}, Heights: {}'.format(width, height, self.weights, heights))

        result = [debug.fit(width)]

        for child_height, component in zip(heights, self.children):
            result.extend(component.render(width, child_height))

        return result

    def keypress(self, key):
        if key.name == 'KEY_UP':
            self.weights[0] += 1
        elif key.name == 'KEY_DOWN':
            self.weights[0] = max(1, self.weights[0] - 1)
