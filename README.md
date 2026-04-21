# ALYODCLI

ALYODCLI is a lightweight Python library for building rich terminal output with color, layout, and interactive widgets.

## Features

- ANSI styling helpers
- Text alignment and width-aware formatting
- Box and table layout rendering
- Horizontal rules, bullets, progress bars, and interactive navigation

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
