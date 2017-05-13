from typing import Optional

Char = Optional[str]


class Border(object):
    def __init__(self,
                 top: Char=None,
                 bottom: Char=None,
                 left: Char=None,
                 right: Char=None,
                 top_left: Char=None,
                 top_right: Char=None,
                 bottom_left: Char=None,
                 bottom_right: Char=None):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right

    @property
    def has_top(self):
        return any([
            self.top_left is not None,
            self.top is not None,
            self.top_right is not None,
        ])

    @property
    def has_bottom(self):
        return any([
            self.bottom_left is not None,
            self.bottom is not None,
            self.bottom_right is not None,
        ])

    @property
    def has_left(self):
        return any([
            self.top_left is not None,
            self.left is not None,
            self.bottom_left is not None,
        ])

    @property
    def has_right(self):
        return any([
            self.top_right is not None,
            self.right is not None,
            self.bottom_right is not None,
        ])

    @property
    def top_height(self):
        return 1 if self.has_top else 0

    @property
    def bottom_height(self):
        return 1 if self.has_bottom else 0

    @property
    def left_width(self):
        return 1 if self.has_left else 0

    @property
    def right_width(self):
        return 1 if self.has_right else 0

    def top_border(self, width: int) -> str:
        top_left = ''
        top = ''
        top_right = ''

        if self.top_left is not None:
            width -= 1
            top_left = self.top_left

        if self.top_right is not None:
            width -= 1
            top_right = self.top_right

        if self.top is not None:
            top = self.top * width

        return ''.join([top_left, top, top_right])

    def bottom_border(self, width: int) -> str:
        bottom_left = ''
        bottom = ''
        bottom_right = ''

        if self.bottom_left is not None:
            width -= 1
            bottom_left = self.bottom_left

        if self.bottom_right is not None:
            width -= 1
            bottom_right = self.bottom_right

        if self.bottom is not None:
            bottom = self.bottom * width

        return ''.join([bottom_left, bottom, bottom_right])

    def left_border(self) -> str:
        return self.left or ''

    def right_border(self) -> str:
        return self.right or ''


class Borders(object):
    NONE = Border()
    LIGHT = Border(
        top='─',
        bottom='─',
        left='│',
        right='│',
        top_left='┌',
        top_right='┐',
        bottom_left='└',
        bottom_right='┘',
    )
    HEAVY = Border(
        top='━',
        bottom='━',
        left='┃',
        right='┃',
        top_left='┏',
        top_right='┓',
        bottom_left='┗',
        bottom_right='┛',
    )
    DOUBLE = Border(
        top='═',
        bottom='═',
        left='║',
        right='║',
        top_left='╔',
        top_right='╗',
        bottom_left='╚',
        bottom_right='╝',
    )
