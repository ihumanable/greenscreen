from typing import List

from greenscreen.style.text import Text, StyledText, StyledFragment


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


def normal(root: Text, *additional: Text) -> StyledText:
    def _fragments(target: Text) -> List[StyledFragment]:
        return target.fragments if isinstance(target, StyledText) else [StyledFragment(target)]

    fragments = _fragments(root)
    for text in additional:
        fragments.extend(_fragments(text))

    return StyledText(fragments)


def _apply_capability(text: Text, capability: Capability) -> List[StyledFragment]:
    if isinstance(text, StyledText):
        text.apply_capability(capability)
        return text.fragments
    else:
        return [StyledFragment(text, capabilities={capability})]


def _capabled(capability: Capability, root: Text, *additional: Text):
    fragments = _apply_capability(root, capability)
    for text in additional:
        fragments.extend(_apply_capability(text, capability))
    return StyledText(fragments)


def bold(root: Text, *additional: Text):
    return _capabled(Capabilities.BOLD, root, *additional)


def reverse(root: Text, *additional: Text):
    return _capabled(Capabilities.REVERSE, root, *additional)


def blink(root: Text, *additional: Text):
    return _capabled(Capabilities.BLINK, root, *additional)


def dim(root: Text, *additional: Text):
    return _capabled(Capabilities.DIM, root, *additional)


def underline(root: Text, *additional: Text):
    return _capabled(Capabilities.UNDERLINE, root, *additional)


def italic(root: Text, *additional: Text):
    return _capabled(Capabilities.ITALIC, root, *additional)


def shadow(root: Text, *additional: Text):
    return _capabled(Capabilities.SHADOW, root, *additional)


def standout(root: Text, *additional: Text):
    return _capabled(Capabilities.STANDOUT, root, *additional)


def subscript(root: Text, *additional: Text):
    return _capabled(Capabilities.SUBSCRIPT, root, *additional)


def superscript(root: Text, *additional: Text):
    return _capabled(Capabilities.SUPERSCRIPT, root, *additional)


def flash(root: Text, *additional: Text):
    return _capabled(Capabilities.FLASH, root, *additional)
