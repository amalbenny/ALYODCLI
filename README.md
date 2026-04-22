# ALYODCLI

ALYODCLI is a lightweight Python library for building rich terminal output with color, layout, and interactive widgets.

## Features

- ANSI styling helpers
- Text alignment and width-aware formatting
- Box and table layout rendering
- Horizontal rules, bullets, progress bars, and interactive navigation
- App-style terminal GUI with selectable buttons
- Desktop GUI windows with Tkinter/Qt backends

## Installation

```bash
pip install alyodcli
```

## Quick Start

```python
from ALYODCLI import Activate

cli = Activate()

cli.layout.box([
    "ALYODCLI",
    "Install once, use anywhere"
], color="cyan")

cli.widgets.bullet("Styled output", color="green")
```

A lowercase import alias is also provided:

```python
from alyodcli import Activate
```

## App Screen with Buttons

```python
from ALYODCLI import Activate

cli = Activate()

selected = cli.app(
    pages={
        "main": {
            "title": "Project Control Center",
            "subtitle": "Choose a module",
            "buttons": ["Build", "Test", "Settings", "Exit"],
            "actions": {
                "Build": lambda: print("Building..."),
                "Test": lambda: print("Running tests..."),
            },
            "routes": {
                "Settings": "settings"
            },
        },
        "settings": {
            "title": "Settings",
            "subtitle": "Configure your app",
            "content": ["Option A: Enabled", "Option B: Disabled"],
            "buttons": ["Back", "Exit"],
            "routes": {
                "Back": "main"
            },
        },
    },
    start_page="main",
    backend="tkinter",
    size="760x520",
)

print("Selected:", selected)
```

Use Up/Down (or W/S) to move focus and Enter to click/select.

Desktop GUI backends:
- backend="tkinter" for built-in Python GUI
- backend="qt" for PySide6-based GUI
- backend="auto" (default) tries Qt first, then Tkinter
- backend="terminal" uses the original terminal app renderer

If you use Qt backend, install dependency:

```bash
pip install PySide6
```
<!--
## Publish to PyPI

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
python -m twine upload dist/*
```
-->
## License

Apache-2.0 (see LICENSE.txt)
