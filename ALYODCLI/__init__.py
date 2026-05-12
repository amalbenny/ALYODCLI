from .terminal import Terminal
from .style import Style
from .text import Text
from .layout import Layout
from .widgets import Widgets
from .help import helpfn

__version__ = "0.2.0"
__all__ = [
    "Activate",
    "help",
    "Terminal",
    "Style",
    "Text",
    "Layout",
    "Widgets",
    "__version__",
]

class Activate:
        
    """
    Main interface tying all components together.
    Provides a cohesive API for building terminal applications.

    - Terminal: Handles terminal interactions and configurations.
        - check_support
        - _getch

    - Style: Manages text styles and formatting options.
        - paint
        - ext
        - hex

    - Text: Handles text content and manipulation.
        - align

    - Layout: Manages the layout and structure of the text.
        - box
        - table

    - Widgets: Provides additional UI components and widgets for the CLI.
        - progress
        - hr ( horizontal rule )
        - bullet ( bulleted list items )
        - navigation ( arrow key navigation for lists and menus ) 
    """
    def __init__(self):
        is_supported = Terminal.check_support()
        self.style = Style(enabled=is_supported)
        self.text = Text(style_manager=self.style)
        self.layout = Layout(text_manager=self.text, style_manager=self.style)
        self.widgets = Widgets(style_manager=self.style, text_manager=self.text)


    def paint(self, text: str, *styles: str) -> str:
        """Convenience method to apply styles directly from the main interface."""
        return self.style.paint(text, *styles)


    def help(self, topic: str = "all") -> str:
        """Print a developer-friendly help guide for first-time usage."""
        return helpfn(topic)
