from greenscreen.application import Application
from greenscreen.components.text import Text
from greenscreen.state import SimpleState

app = Application()
state = SimpleState('main', app, Text('a b c d e f g ' * 500))

app.active = 'main'
app.run()
