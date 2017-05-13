from greenscreen.application import Application
from greenscreen.components.layout import HorizontalLayout, VerticalLayout
from greenscreen.components.text import Text
from greenscreen.display.sizing import Sizing
from greenscreen.display.text import Colors
from greenscreen.state import SimpleState
from greenscreen.display.border import Borders

app = Application()
state = SimpleState(
    'main',
    app,
    HorizontalLayout(
        [
            VerticalLayout([
                Text('Alpha', border=Borders.DOUBLE),
                Text('Beta'),
            ]),
            VerticalLayout([
                Text('Gamma'),
                Text('Delta')
            ]),
        ],
        border=Borders.HEAVY,
        margin=Sizing(4, 4, 4, 4),
        padding=Sizing(4, 4, 4, 4),
        foreground=Colors.MAGENTA,
        background=Colors.BRIGHT_BLUE,
    ),
)

app.active = 'main'
app.run()
