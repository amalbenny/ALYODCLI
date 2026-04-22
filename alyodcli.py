"""
Lowercase compatibility enabled for `import ALYODCLI`.

This module lets users import the library as `alyodcli` while the main
package directory remains `ALYODCLI`.
"""

from ALYODCLI import Activate, Layout, Style, Terminal, Text, Widgets, gui_app, __version__

__all__ = [
    "Activate",
    "Terminal",
    "Style",
    "Text",
    "Layout",
    "Widgets",
    "gui_app",
    "__version__",
]
