from blessed import Terminal


class State(object):
    def __init__(self, key, parent):
        self.key = key
        self.parent = parent
        self.parent.register_state(key, self)

    def render(self, terminal: Terminal) -> str:
        raise NotImplementedError('{cls} has not implemented render()'.format(
            cls=self.__class__.__name__
        ))

    def keypress(self, key):
        pass


class SimpleState(State):
    def __init__(self, key, parent, component):
        super().__init__(key, parent)
        self.component = component

    def render(self, terminal: Terminal) -> str:
        return '\n'.join([
            line.escape(terminal)
            for line in self.component.render(terminal.width, terminal.height - 1)
        ])

    def keypress(self, key):
        self.component.keypress(key)


