from typing import List

from greenscreen.style.text import StyledFragment, StyledText, Text


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


def _apply_foreground_color(fragment: Text, color: Color) -> List[StyledFragment]:
    if isinstance(fragment, StyledText):
        fragment.set_foreground_color(color)
        return fragment.fragments
    else:
        return [StyledFragment(fragment, foreground=color)]


def _foreground_colored(color, root: Text, *additional: Text):
    fragments = _apply_foreground_color(root, color)
    for text in additional:
        fragments.extend(_apply_foreground_color(text, color))
    return StyledText(fragments)


def black(root: Text, *additional: Text):
    return _foreground_colored(Colors.BLACK, root, *additional)


def red(root: Text, *additional: Text):
    return _foreground_colored(Colors.RED, root, *additional)


def green(root: Text, *additional: Text):
    return _foreground_colored(Colors.GREEN, root, *additional)


def yellow(root: Text, *additional: Text):
    return _foreground_colored(Colors.YELLOW, root, *additional)


def blue(root: Text, *additional: Text):
    return _foreground_colored(Colors.BLUE, root, *additional)


def magenta(root: Text, *additional: Text):
    return _foreground_colored(Colors.MAGENTA, root, *additional)


def cyan(root: Text, *additional: Text):
    return _foreground_colored(Colors.CYAN, root, *additional)


def white(root: Text, *additional: Text):
    return _foreground_colored(Colors.WHITE, root, *additional)


def bright_black(root: Text, *additional: Text):
    return _foreground_colored(Colors.BRIGHT_BLACK, root, *additional)


def bright_red(root: Text, *additional: Text):
    return _foreground_colored(Colors.BRIGHT_RED, root, *additional)


def bright_green(root: Text, *additional: Text):
    return _foreground_colored(Colors.BRIGHT_GREEN, root, *additional)


def bright_yellow(root: Text, *additional: Text):
    return _foreground_colored(Colors.BRIGHT_YELLOW, root, *additional)


def bright_blue(root: Text, *additional: Text):
    return _foreground_colored(Colors.BRIGHT_BLUE, root, *additional)


def bright_magenta(root: Text, *additional: Text):
    return _foreground_colored(Colors.BRIGHT_MAGENTA, root, *additional)


def bright_cyan(root: Text, *additional: Text):
    return _foreground_colored(Colors.BRIGHT_CYAN, root, *additional)


def bright_white(root: Text, *additional: Text):
    return _foreground_colored(Colors.BRIGHT_WHITE, root, *additional)


def _apply_background_color(fragment: Text, color: Color) -> List[StyledFragment]:
    if isinstance(fragment, StyledText):
        fragment.set_background_color(color)
        return fragment.fragments
    else:
        return [StyledFragment(fragment, background=color)]


def _background_colored(color: Color, root: Text, *additional: Text):
    fragments = _apply_background_color(root, color)
    for text in additional:
        fragments.extend(_apply_background_color(text, color))
    return StyledText(fragments)


def on_black(root: Text, *additional: Text):
    return _background_colored(Colors.BLACK, root, *additional)


def on_red(root: Text, *additional: Text):
    return _background_colored(Colors.RED, root, *additional)


def on_green(root: Text, *additional: Text):
    return _background_colored(Colors.GREEN, root, *additional)


def on_yellow(root: Text, *additional: Text):
    return _background_colored(Colors.YELLOW, root, *additional)


def on_blue(root: Text, *additional: Text):
    return _background_colored(Colors.BLUE, root, *additional)


def on_magenta(root: Text, *additional: Text):
    return _background_colored(Colors.MAGENTA, root, *additional)


def on_cyan(root: Text, *additional: Text):
    return _background_colored(Colors.CYAN, root, *additional)


def on_white(root: Text, *additional: Text):
    return _background_colored(Colors.WHITE, root, *additional)


def on_bright_black(root: Text, *additional: Text):
    return _background_colored(Colors.BRIGHT_BLACK, root, *additional)


def on_bright_red(root: Text, *additional: Text):
    return _background_colored(Colors.BRIGHT_RED, root, *additional)


def on_bright_green(root: Text, *additional: Text):
    return _background_colored(Colors.BRIGHT_GREEN, root, *additional)


def on_bright_yellow(root: Text, *additional: Text):
    return _background_colored(Colors.BRIGHT_YELLOW, root, *additional)


def on_bright_blue(root: Text, *additional: Text):
    return _background_colored(Colors.BRIGHT_BLUE, root, *additional)


def on_bright_magenta(root: Text, *additional: Text):
    return _background_colored(Colors.BRIGHT_MAGENTA, root, *additional)


def on_bright_cyan(root: Text, *additional: Text):
    return _background_colored(Colors.BRIGHT_CYAN, root, *additional)


def on_bright_white(root: Text, *additional: Text):
    return _background_colored(Colors.BRIGHT_WHITE, root, *additional)
