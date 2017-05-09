from math import floor, ceil
from typing import List

from blessed import Terminal

from greenscreen.components.base import Component
from greenscreen.style import text
from greenscreen.style.border import Borders, Border
from greenscreen.style.sizing import Sizing
from greenscreen.style.text import StyledText


class Text(Component):
    def __init__(self, content: str, border: Border=Borders.NONE, padding: Sizing=None, margin: Sizing=None):
        super().__init__(border, padding, margin)
        self.text = text.blue(content)
        self.offset = 0

    def content(self, terminal: Terminal, width: int, height: int) -> List[StyledText]:
        lines = self.text.wrap(width)
        lines = lines[self.offset:]

        if len(lines) < height:
            remainder = height - len(lines)
            top = int(floor(remainder / 2))
            bottom = int(ceil(remainder / 2))
            filler = text.blue(' ' * width)
            lines = ([filler] * top) + lines + ([filler] * bottom)

        if len(lines) > height:
            lines = lines[:height - 1] + [text.blue((' ' * (width - 3)) + ' ↓ ')]

        return [line.justify(width) for line in lines]

    def keypress(self, key):
        if key.name == 'KEY_UP':
            self.offset = max(0, self.offset - 1)
        elif key.name == 'KEY_DOWN':
            self.offset += 1

