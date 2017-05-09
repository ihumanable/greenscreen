from typing import Optional, List

from blessed import Terminal

from greenscreen.exceptions import InvalidContent
from greenscreen.style.border import Borders, Border
from greenscreen.style.sizing import Sizing


class Component(object):
    def __init__(self, border: Border=Borders.NONE, padding: Sizing=None, margin: Sizing=None):
        self.border = border
        self.padding = padding or Sizing()
        self.margin = margin or Sizing()

    def render(self, terminal: Terminal, width: Optional[int]=None, height: Optional[int]=None) -> List[str]:
        width = width or terminal.width
        height = height or terminal.height

        return (
            self.render_vertical_margin(width, self.margin.top) +
            self.render_border_top(width) +
            self.render_vertical_padding(width, self.padding.top) +
            self.render_content(terminal, width, height) +
            self.render_vertical_padding(width, self.padding.bottom) +
            self.render_border_bottom(width) +
            self.render_vertical_margin(width, self.margin.bottom)
        )

    def render_vertical_margin(self, width: int, height: int) -> List[str]:
        return [' ' * width] * height

    def render_border_top(self, width: int) -> List[str]:
        if not self.border.has_top:
            return []

        border_width = width - self.margin.left - self.margin.right
        return [''.join([
            ' ' * self.margin.left,
            self.border.top_border(border_width),
            ' ' * self.margin.right,
        ])]

    def render_vertical_padding(self, width: int, height: int) -> List[str]:
        if height == 0:
            return []

        inner_width = width - sum([
            self.margin.left,
            self.border.left_width,
            self.border.right_width,
            self.margin.right,
        ])

        line = ''.join([
            ' ' * self.margin.left,
            self.border.left_border(),
            ' ' * inner_width,
            self.border.right_border(),
            ' ' * self.margin.right,
        ])

        return [line] * height

    def render_content(self, terminal: Terminal, width: int, height: int) -> List[str]:
        reserved_width = sum([
            self.margin.left,
            self.border.left_width,
            self.padding.left,
            self.padding.right,
            self.border.right_width,
            self.margin.right,
        ])

        reserved_height = sum([
            self.margin.top,
            self.border.top_height,
            self.padding.top,
            self.padding.bottom,
            self.border.bottom_height,
            self.margin.bottom
        ])

        inner_width = width - reserved_width
        inner_height = height - reserved_height

        prefix = ''.join([
            ' ' * self.margin.left,
            self.border.left_border(),
            ' ' * self.padding.left,
        ])

        suffix = ''.join([
            ' ' * self.padding.right,
            self.border.right_border(),
            ' ' * self.margin.right,
        ])

        result = []
        content = self.content(terminal, inner_width, inner_height)
        if len(content) != inner_height:
            raise InvalidContent('Expected content height {}, actual height {}'.format(
                inner_height,
                len(content)
            ))

        invalid_lines = [len(line) for line in content if len(line) != inner_width]
        if invalid_lines:
            raise InvalidContent('Expected content width {}, lines with widths {}'.format(
                inner_width,
                invalid_lines
            ))

        for line in content:
            if len(line) > inner_width:
                line = line[:inner_width - 3] + '...'
            result.append(''.join([
                prefix,
                line,
                ' ' * (inner_width - len(line)),
                suffix,
            ]))
        return result

    def render_border_bottom(self, width: int) -> List[str]:
        if not self.border.has_bottom:
            return []

        border_width = width - self.margin.left - self.margin.right
        return [''.join([
            ' ' * self.margin.left,
            self.border.bottom_border(border_width),
            ' ' * self.margin.right,
        ])]

    def content(self, terminal: Terminal, width: int, height: int) -> List[str]:
        raise NotImplementedError('{cls} has not implemented render()'.format(
            cls=self.__class__.__name__
        ))
