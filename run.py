from greenscreen.application import Application
from greenscreen.components.layout import HorizontalLayout, VerticalLayout
from greenscreen.components.text import Text
from greenscreen.display.sizing import Sizing
from greenscreen.display.text import Colors
from greenscreen.screen import SimpleScreen
from greenscreen.display.border import Borders

app = Application()
state = SimpleScreen(
    'main',
    app,
    HorizontalLayout(
        [
            VerticalLayout([
                Text('Alpha'),
                Text('Beta'),
            ]),
            VerticalLayout([
                Text('Gamma'),
                Text('Delta'),
                Text('Epsilon')
            ]),
            VerticalLayout([
                Text('Phi'),
            ])
        ],
        border=Borders.HEAVY,
        margin=Sizing(2, 2, 2, 2),
        padding=Sizing(2, 2, 2, 2),
        foreground=Colors.MAGENTA,
    ),
)

app.active = 'main'

if __name__ == '__main__':
    app.run()
