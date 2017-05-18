from blessed import Terminal
from blessed.keyboard import Keystroke

from greenscreen.components.base import Component
from greenscreen.input import Result, Unhandled


class Screen(object):
    def __init__(self, key, parent, root: Component):
        self.key = key
        self.parent = parent
        self.parent.register_screen(key, self)
        self.root = root

    def render(self, terminal: Terminal) -> str:
        raise NotImplementedError('{cls} has not implemented render()'.format(
            cls=self.__class__.__name__
        ))

    def handle_keypress(self, key: Keystroke) -> Result:
        result = self.keypress(key)
        if result.handled:
            return result

        result = self.dispatch_keypress(key)
        if result.handled:
            return result

        return self.after_keypress(key)

    def keypress(self, key: Keystroke) -> Result:
        return Unhandled()

    def dispatch_keypress(self, key: Keystroke) -> Result:
        return self.root.handle_keypress(key)

    def after_keypress(self, key: Keystroke) -> Result:
        return Unhandled()


class SimpleScreen(Screen):
    def render(self, terminal: Terminal) -> str:
        return '\n'.join([
            line.escape(terminal)
            for line in self.root.render(terminal.width, terminal.height - 1)
        ])
