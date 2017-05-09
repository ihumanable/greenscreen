from textwrap import wrap
from typing import List, Union, Set, Optional

from blessed import Terminal


class StyledFragment(object):
    def __init__(self,
                 text: str,
                 foreground: Optional['Color']=None,
                 background: Optional['Color']=None,
                 capabilities: Set['Capability']=None):
        self.text: str = text
        self.foreground: Optional['Color'] = foreground
        self.background: Optional['Color'] = background
        self.capabilities: Set['Capability'] = capabilities or set()

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
        return '<StyledFragment "{}" foreground={} background={} capabilities={}>'.format(
            self.text,
            self.foreground,
            self.background,
            self.capabilities
        )

    def __str__(self):
        return self.text


class StyledText(object):
    def __init__(self, fragments: List[StyledFragment]=None):
        self.fragments: List[StyledFragment] = fragments or []

    def apply_capability(self, capability: 'Capability'):
        for fragment in self.fragments:
            fragment.capabilities.add(capability)

    def set_foreground_color(self, color: 'Color'):
        for fragment in self.fragments:
            if fragment.foreground is None:
                fragment.foreground = color

    def set_background_color(self, color: 'Color'):
        for fragment in self.fragments:
            if fragment.background is None:
                fragment.background = color

    def justify(self, length, expand=True):
        current_length = 0
        fragments = list(reversed(self.fragments))
        result: List[StyledFragment] = []

        while current_length < length and fragments:
            current = fragments.pop()
            result.append(current)
            current_length += len(current)

        if current_length < length:
            # Not enough content to match length
            if expand and result:
                # Expand the final fragment
                last = result.pop()
                padded = ''.join([
                    last.text,
                    ' ' * (length - current_length)
                ])
                result.append(StyledFragment(padded, last.foreground, last.background, last.capabilities))
            else:
                # Create a new StyledFragment with the appropriate padding
                result.append(StyledFragment(' ' * (length - current_length)))

        return StyledText(result)

    def wrap(self, width):
        result = []

        raw = str(self)
        lines = wrap(raw, width)
        fragments = list(reversed(self.fragments))
        for line in lines:
            length = len(line)
            text_fragments: List[StyledFragment] = []
            while length > 0 and fragments:
                fragment = fragments.pop()
                length -= len(fragment)
                text_fragments.append(fragment)

            if length < 0:
                # Split is within the last fragment
                last = text_fragments.pop()
                head = StyledFragment(last.text[:length], last.foreground, last.background, last.capabilities)
                tail = StyledFragment(last.text[length:].lstrip(), last.foreground, last.background, last.capabilities)
                text_fragments.append(head)
                fragments.append(tail)

            result.append(StyledText(text_fragments))

        return result

    def escape(self, terminal: Terminal):
        return ''.join([fragment.escape(terminal) for fragment in self.fragments])

    def __len__(self):
        return sum(len(fragment) for fragment in self.fragments)

    def __repr__(self):
        return '<StyledText fragments={}>'.format(self.fragments)

    def __str__(self):
        return ''.join([str(fragment) for fragment in self.fragments])


Text = Union[str, StyledText]
