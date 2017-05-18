from collections import defaultdict, deque
from math import floor
from typing import List, Iterable, Set

from blessed.keyboard import Keystroke

from greenscreen.components.base import Component
from greenscreen.display.border import Border, Borders
from greenscreen.display.sizing import Sizing
from greenscreen.display.text import Line, Color, Capability, Colors
from greenscreen.index import ListIndex
from greenscreen.input import Result, Repaint, Unhandled


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
        self.debug = False
        self.weights: List[int] = weights or []
        self.children: List[Component] = children or []
        self.repack(self.weights)
        self.focus = ListIndex(self.children)

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

        if self.debug:
            debug = Line('{width}x{height} Weights: {weights}, Widths: {widths}'.format(
                width=width,
                height=height,
                weights=self.weights,
                widths=widths
            ))

        height = height - 1 if self.debug else height

        columns = []
        for idx, zipped in enumerate(zip(widths, self.children)):
            child_width, component = zipped
            component.border = Borders.HEAVY if idx == self.focus.index else Borders.NONE
            component.margin = Sizing(0, 0, 0, 0) if idx == self.focus.index else Sizing(1, 1, 1, 1)
            columns.append(component.render(child_width, height))

        result = [self.combine(group) for group in zip(*columns)]
        return [debug.fit(width)] + result if self.debug else result

    def dispatch_keypress(self, key: Keystroke) -> Result:
        return self.focus.value.handle_keypress(key) if self.focus.value else Unhandled()

    def after_keypress(self, key: Keystroke) -> Result:
        if key.name == 'KEY_LEFT':
            self.focus.decr()
            return Repaint(self)

        if key.name == 'KEY_RIGHT':
            self.focus.incr()
            return Repaint(self)

        return Unhandled()


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
        self.debug = False
        self.weights: List[int] = weights or []
        self.children: List[Component] = children or []
        self.repack(self.weights)
        self.focus = ListIndex(self.children)

    def repack(self, weights: List[int]):
        self.weights = weights + ([1] * (max(0, len(self.children) - len(weights))))

    def append(self, child: Component, weight: int = 1):
        self.children.append(child)
        self.weights.append(weight)

    def content(self, width: int, height: int) -> List[Line]:
        height = height - 1 if self.debug else height

        heights = self.weighted(height, self.weights)

        if self.debug:
            debug = Line('{width}x{height} Weights: {weights}, Heights: {heights}'.format(
                width=width,
                height=height,
                weights=self.weights,
                heights=heights,
            ))

        result = [debug.fit(width)] if self.debug else []

        for idx, zipped in enumerate(zip(heights, self.children)):
            child_height, component = zipped
            component.border = Borders.HEAVY if idx == self.focus.index else Borders.NONE
            component.margin = Sizing(0, 0, 0, 0) if idx == self.focus.index else Sizing(1, 1, 1, 1)
            result.extend(component.render(width, child_height))

        return result

    def dispatch_keypress(self, key: Keystroke) -> Result:
        return self.focus.value.handle_keypress(key) if self.focus.value else Unhandled()

    def after_keypress(self, key: Keystroke) -> Result:
        if key.name == 'KEY_UP':
            self.focus.decr()
            return Repaint(self)

        if key.name == 'KEY_DOWN':
            self.focus.incr()
            return Repaint(self)

        return Unhandled()


