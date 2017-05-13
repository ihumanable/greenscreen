from textwrap import wrap
from typing import List, Union, Set, Optional

from blessed import Terminal
from copy import copy


class Capability(object):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return '<Capability {}>'.format(self.name)


class Capabilities(object):
    BOLD = Capability('bold')
    REVERSE = Capability('reverse')
    BLINK = Capability('blink')
    DIM = Capability('dim')
    UNDERLINE = Capability('underline')
    ITALIC = Capability('italic')
    SHADOW = Capability('shadow')
    STANDOUT = Capability('standout')
    SUBSCRIPT = Capability('subscript')
    SUPERSCRIPT = Capability('superscript')
    FLASH = Capability('flash')


class Color(object):
    def __init__(self, color: str, bright: bool=False):
        self.color = color
        self.bright = bright

    def __repr__(self):
        template = '<Color bright {}>' if self.bright else '<Color {}>'
        return template.format(self.color)

    def blessed(self):
        template = 'bright_{}' if self.bright else '{}'
        return template.format(self.color)


class Colors(object):
    BLACK = Color('black', bright=False)
    RED = Color('red', bright=False)
    GREEN = Color('green', bright=False)
    YELLOW = Color('yellow', bright=False)
    BLUE = Color('blue', bright=False)
    MAGENTA = Color('magenta', bright=False)
    CYAN = Color('cyan', bright=False)
    WHITE = Color('white', bright=False)

    BRIGHT_BLACK = Color('black', bright=True)
    BRIGHT_RED = Color('red', bright=True)
    BRIGHT_GREEN = Color('green', bright=True)
    BRIGHT_YELLOW = Color('yellow', bright=True)
    BRIGHT_BLUE = Color('blue', bright=True)
    BRIGHT_MAGENTA = Color('magenta', bright=True)
    BRIGHT_CYAN = Color('cyan', bright=True)
    BRIGHT_WHITE = Color('white', bright=True)


class Fragment(object):
    def __init__(self,
                 text: str,
                 foreground: Optional[Color]=None,
                 background: Optional[Color]=None,
                 capabilities: Set[Capability]=None):
        self.text: str = text
        self.foreground: Optional[Color] = foreground
        self.background: Optional[Color] = background
        self.capabilities: Set[Capability] = capabilities or set()

    def escape(self, terminal: Terminal):
        attributes = []

        if self.foreground:
            attributes.append(self.foreground.blessed())

        if self.background:
            attributes.append('on_{}'.format(self.background.blessed()))

        for capability in self.capabilities:
            attributes.append(capability.name)

        result = self.text

        for attr in attributes:
            method = getattr(terminal, attr)
            result = method(result)

        return result

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return '<Fragment "{}" foreground={} background={} capabilities={}>'.format(
            self.text,
            self.foreground,
            self.background,
            self.capabilities
        )

    def __str__(self):
        return self.text


FragmentLike = Union[str, Fragment]


class Line(object):
    def __init__(self,
                 root: FragmentLike,
                 *additional: FragmentLike,
                 foreground: Optional[Color]=None,
                 background: Optional[Color]=None,
                 capabilities: Set[Capability]=None):
        self.fragments: List[Fragment] = (
            [self._fragment(root)] +
            [self._fragment(a) for a in additional]
        )

        if foreground:
            self.set_foreground_color(foreground)

        if background:
            self.set_background_color(background)

        capabilities = capabilities or set()

        for capability in capabilities:
            self.apply_capability(capability)

    @classmethod
    def _fragment(cls, value: FragmentLike) -> Fragment:
        return value if isinstance(value, Fragment) else Fragment(value)

    def apply_capability(self, capability: Capability):
        for fragment in self.fragments:
            fragment.capabilities.add(capability)

    def set_foreground_color(self, color: Color):
        for fragment in self.fragments:
            if fragment.foreground is None:
                fragment.foreground = color

    def set_background_color(self, color: Color):
        for fragment in self.fragments:
            if fragment.background is None:
                fragment.background = color

    def fit(self, length: int, indicator: str='…', expand: bool=True) -> 'Line':
        current_length = len(self)

        if current_length < length:
            return self.justify(length, expand=expand)
        elif current_length > length:
            return self.truncate(length, indicator=indicator)

        return self.copy()

    def truncate(self, length: int, indicator: str='…') -> 'Line':
        current_length = 0
        fragments = self.fragments
        result: List[Fragment] = []

        while current_length < length and fragments:
            current = fragments.pop()
            result.append(current)
            current_length += len(current)

        if current_length < length:
            # No need to truncate
            return Line(*result)

        remove = (current_length - length) + len(indicator)

        last = result.pop()
        last.text = ''.join([last.text[:-remove], indicator])
        result.append(last)

        return Line(*result)

    def justify(self, length: int, expand: bool=True) -> 'Line':
        current_length = 0
        fragments = list(reversed(self.copy_fragments()))
        result: List[Fragment] = []

        while current_length < length and fragments:
            current = fragments.pop()
            result.append(current)
            current_length += len(current)

        if current_length > length:
            # No need to pad
            return Line(*result)

        if expand and result:
            # Expand the final fragment
            last = result.pop()
            padded = ''.join([
                last.text,
                ' ' * (length - current_length)
            ])
            result.append(Fragment(padded, last.foreground, last.background, last.capabilities))
        else:
            # Create a new Fragment with the appropriate padding
            result.append(Fragment(' ' * (length - current_length)))

        return Line(*result)

    def wrap(self, width):
        result = []

        raw = str(self)
        lines = wrap(raw, width)
        fragments = list(reversed(self.fragments))
        for line in lines:
            length = len(line)
            text_fragments: List[Fragment] = []
            while length > 0 and fragments:
                fragment = fragments.pop()
                length -= len(fragment)
                text_fragments.append(fragment)

            if length < 0:
                # Split is within the last fragment
                last = text_fragments.pop()
                head = Fragment(last.text[:length], last.foreground, last.background, last.capabilities)
                tail = Fragment(last.text[length:].lstrip(), last.foreground, last.background, last.capabilities)
                text_fragments.append(head)
                fragments.append(tail)

            result.append(Line(*text_fragments))

        return result

    def escape(self, terminal: Terminal) -> str:
        return ''.join([fragment.escape(terminal) for fragment in self.fragments])

    def copy_fragments(self) -> List[Fragment]:
        return [copy(f) for f in self.fragments]

    def copy(self) -> 'Line':
        return Line(*self.copy_fragments())

    def __add__(self, other: 'Line') -> 'Line':
        fragments = self.copy_fragments() + other.copy_fragments()
        head, *tail = fragments
        return Line(head, *tail)

    def __len__(self):
        return sum(len(fragment) for fragment in self.fragments)

    def __repr__(self):
        fragments = ',\n       '.join([repr(f) for f in self.fragments])
        return '<Line [{}]>'.format(fragments)

    def __str__(self):
        return ''.join([str(fragment) for fragment in self.fragments])
