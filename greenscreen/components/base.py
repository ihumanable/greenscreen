from typing import List, Set

from greenscreen.exceptions import InvalidContent
from greenscreen.display.border import Borders, Border
from greenscreen.display.sizing import Sizing
from greenscreen.display.text import Line, Fragment, Color, Capability


class Component(object):
    def __init__(self,
                 border: Border=Borders.NONE,
                 padding: Sizing=None,
                 margin: Sizing=None,
                 foreground: Color=None,
                 background: Color=None,
                 capabilities: Set[Capability]=None):
        self.border = border
        self.padding = padding or Sizing()
        self.margin = margin or Sizing()
        self.foreground = foreground
        self.background = background
        self.capabilities = capabilities or set()

    def line(self, value: str) -> Line:
        return Line(self.fragment(value))

    def fragment(self, value: str) -> Fragment:
        return Fragment(
            value,
            foreground=self.foreground,
            background=self.background,
            capabilities=self.capabilities
        )

    def render(self, width: int, height: int) -> List[Line]:
        return (
            self.render_vertical_margin(width, self.margin.top) +
            self.render_border_top(width) +
            self.render_vertical_padding(width, self.padding.top) +
            self.render_content(width, height) +
            self.render_vertical_padding(width, self.padding.bottom) +
            self.render_border_bottom(width) +
            self.render_vertical_margin(width, self.margin.bottom)
        )

    def render_vertical_margin(self, width: int, height: int) -> List[Line]:
        return [self.line(' ' * width)] * height

    def render_border_top(self, width: int) -> List[Line]:
        if not self.border.has_top:
            return []

        border_width = width - self.margin.left - self.margin.right
        return [self.line(''.join([
            ' ' * self.margin.left,
            self.border.top_border(border_width),
            ' ' * self.margin.right,
        ]))]

    def render_vertical_padding(self, width: int, height: int) -> List[Line]:
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

        return [self.line(line)] * height

    def render_content(self, width: int, height: int) -> List[Line]:
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

        prefix = self.fragment(''.join([
            ' ' * self.margin.left,
            self.border.left_border(),
            ' ' * self.padding.left,
        ]))

        suffix = self.fragment(''.join([
            ' ' * self.padding.right,
            self.border.right_border(),
            ' ' * self.margin.right,
        ]))

        result = []
        content = self.content(inner_width, inner_height)
        if len(content) != inner_height:
            raise InvalidContent('{}: Expected content height {}, actual height {}'.format(
                self.__class__.__name__,
                inner_height,
                len(content)
            ))

        invalid_lines = [
            (idx, len(line))
            for idx, line in enumerate(content)
            if len(line) != inner_width
        ]

        if invalid_lines:
            raise InvalidContent('{}: Expected content width {}, lines with widths {}'.format(
                self.__class__.__name__,
                inner_width,
                invalid_lines
            ))

        for line in content:
            line.fragments.insert(0, prefix)
            line.fragments.append(suffix)
            result.append(line)

        return result

    def render_border_bottom(self, width: int) -> List[Line]:
        if not self.border.has_bottom:
            return []

        border_width = width - self.margin.left - self.margin.right
        return [self.line(''.join([
            ' ' * self.margin.left,
            self.border.bottom_border(border_width),
            ' ' * self.margin.right,
        ]))]

    def content(self, width: int, height: int) -> List[Line]:
        raise NotImplementedError('{cls} has not implemented render()'.format(
            cls=self.__class__.__name__
        ))
