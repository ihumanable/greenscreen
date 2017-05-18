class Result(object):
    def __init__(self):
        self.handled = None
        self.repaint = False


class Unhandled(Result):
    def __init__(self):
        super().__init__()
        self.handled = False


class Handled(Result):
    def __init__(self, source):
        super().__init__()
        self.source = source
        self.handled = True


class Continue(Handled):
    pass


class Repaint(Handled):
    def __init__(self, source):
        super().__init__(source)
        self.repaint = True


class Transition(Repaint):
    def __init__(self, source, key: str):
        super().__init__(source)
        self.key = key


class Async(Repaint):
    def __init__(self, source, func: callable, *args, **kwargs):
        super().__init__(source)
        self.func = func
        self.args = args
        self.kwargs = kwargs
