import signal

from blessed import Terminal
from blessed.keyboard import Keystroke

from greenscreen.input import Result, Unhandled, Continue
from greenscreen.screen import Screen
from greenscreen.exceptions import DuplicateRegistration, NoActiveScreen


class Application(object):
    def __init__(self):
        self.screens = {}
        self.active = None
        self.repaint = True
        self.terminal = Terminal()
        self.timeout = 0.5

    @property
    def active_screen(self) -> Screen:
        if not self.active:
            raise NoActiveScreen('No active Screen selected')

        if self.active not in self.screens:
            raise NoActiveScreen('Active Screen {} is not registered'.format(self.active))

        return self.screens[self.active]

    def register_screen(self, key: str, screen: Screen):
        if key in self.screens:
            raise DuplicateRegistration('{} is already assigned a Screen'.format(key))
        self.screens[key] = screen

    def clear_screen(self, key: str):
        self.screens.pop(key, None)

    def register_signal_handler(self):
        signal.signal(signal.SIGWINCH, self.on_resize)

    def on_resize(self, sig, action):
        self.repaint = True

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
        return self.active_screen.handle_keypress(key)

    def after_keypress(self, key: Keystroke) -> Result:
        if key == 'q':
            self.active = False
        return Continue(self)

    def run(self):
        self.register_signal_handler()

        with self.terminal.fullscreen(), self.terminal.cbreak():
            while self.active:
                if self.repaint:
                    print(self.terminal.clear)
                    print(self.active_screen.render(self.terminal))
                    self.repaint = False

                key = self.terminal.inkey(timeout=self.timeout)
                if key:
                    result = self.handle_keypress(key)
                    self.repaint = result.repaint
