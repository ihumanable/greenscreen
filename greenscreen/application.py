import signal

from blessed import Terminal

from greenscreen.state import State
from greenscreen.exceptions import DuplicateRegistration, NoActiveState


class Application(object):
    def __init__(self):
        self.states = {}
        self.active = None
        self.repaint = True
        self.terminal = Terminal()
        self.timeout = 0.5

    @property
    def active_state(self) -> State:
        if not self.active:
            raise NoActiveState('No active State selected')

        if self.active not in self.states:
            raise NoActiveState('Active State {} is not registered'.format(self.active))

        return self.states[self.active]

    def register_state(self, key: str, state: State):
        if key in self.states:
            raise DuplicateRegistration('{} is already assigned a State'.format(key))
        self.states[key] = state

    def clear_state(self, key: str):
        self.states.pop(key, None)

    def register_signal_handler(self):
        signal.signal(signal.SIGWINCH, self.on_resize)

    def on_resize(self, sig, action):
        self.repaint = True

    def run(self):
        self.register_signal_handler()

        with self.terminal.fullscreen(), self.terminal.cbreak():
            while self.active:
                if self.repaint:
                    print(self.terminal.clear)
                    print(self.active_state.render(self.terminal))
                    self.repaint = False

                key = self.terminal.inkey(timeout=self.timeout)
                if key:
                    self.active_state.keypress(key)
                    self.repaint = True
