from math import floor, ceil
from typing import List, Set

from greenscreen.components.base import Component
from greenscreen.display.border import Borders, Border
from greenscreen.display.sizing import Sizing
from greenscreen.display.text import Line, Color, Capability, Colors


class Text(Component):

    def __init__(self,
                 value: str,
                 border: Border=Borders.NONE,
                 padding: Sizing=None,
                 margin: Sizing=None,
                 foreground: Color=None,
                 background: Color=None,
                 capabilities: Set[Capability]=None):
        foreground = foreground or Colors.BLUE
        super().__init__(border, padding, margin, foreground, background, capabilities)

        self.value = self.line(value)
        self.offset = 0

    def content(self, width: int, height: int) -> List[Line]:
        lines = self.value.wrap(width)
        lines = lines[self.offset:]

        if len(lines) < height:
            remainder = height - len(lines)
            top = int(floor(remainder / 2))
            bottom = int(ceil(remainder / 2))
            filler = self.line(' ' * width)
            lines = ([filler] * top) + lines + ([filler] * bottom)

        if len(lines) > height:
            lines = lines[:height - 1] + [self.line((' ' * (width - 3)) + ' ↓ ')]

        return [line.fit(width) for line in lines]

    def keypress(self, key):
        if key.name == 'KEY_UP':
            self.offset = max(0, self.offset - 1)
        elif key.name == 'KEY_DOWN':
            self.offset += 1

