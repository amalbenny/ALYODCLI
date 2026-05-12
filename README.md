# ALYODCLI

ALYODCLI is a lightweight Python library for building rich terminal output with color, layout, and interactive widgets.

## Features

- ANSI styling with named colors, 256-color, and truecolor (hex) support
- Text alignment and width-aware formatting
- Box and table layout rendering
- Horizontal rules, bullets, progress bars, and interactive navigation menus
- Terminal capability detection and ANSI support validation
- **C/Cython Performance Optimization** - High-performance text processing
- **C Language Integration** - Use from C/C++ programs via socket interface or direct library
- **JSON-RPC 2.0 Protocol** - Standard protocol for client communication

## Installation

```bash
pip install alyodcli
```

## Quick Start

### 1. Import and initialize

```python
from ALYODCLI import Activate

cli = Activate()

# Or use lowercase alias
from alyodcli import Activate
```

### 2. Print styled text

```python
print(cli.paint('Hello', 'cyan', 'bold'))
print(cli.paint('Underline', 'underline'))
print(cli.paint('Custom color', cli.style.hex('#ff6b6b')))
```

### 3. Build layouts

```python
cli.layout.box(['ALYODCLI', 'Install once, use anywhere'], color='cyan')

cli.layout.table([
    {'Module': 'Style', 'Status': 'Ready'},
    {'Module': 'Text', 'Status': 'Ready'}
])
```

### 4. Use interactive widgets

```python
cli.widgets.bullet('First item', color='green')
cli.widgets.hr(width=40, color='dim')
cli.widgets.progress(5, 10)

selection = cli.widgets.navigation(['Option 1', 'Option 2', 'Option 3'])
```

## API Reference

### Activate

The main entry point that provides access to all helpers:

```python
cli = Activate()
cli.paint(text, *styles)  # Format text with named styles or raw ANSI codes
cli.help(topic='all')     # Print the built-in developer guide
```

### Style Helper

Color and formatting support:

```python
# Named colors: red, green, yellow, blue, magenta, cyan, white, black
# Background colors: bg_red, bg_green, bg_yellow, bg_blue, bg_magenta, bg_cyan, bg_white, bg_black
# Text styles: bold, underline, dim, italic, strike

# Basic usage
cli.style.get(name)                       # Get a named ANSI code
cli.style.paint(text, *styles)           # Apply one or more styles
cli.style.ext(n, background=False)       # Use 256-color palette (0-255)
cli.style.hex(hex_code, background=False) # Use truecolor RGB (e.g., '#ff6b6b')

# Examples
print(cli.paint('Error', 'red', 'bold'))
print(cli.paint('Success', cli.style.hex('#22c55e')))
print(cli.paint('Custom', cli.style.ext(45), 'bold'))
print(cli.paint('Reset', 'reset'))
```

### Text Helper

Width-aware text formatting:

```python
cli.text.get_visual_len(text)  # Measure visible width (ignores ANSI codes)
cli.text.align(text, width, align='left', *styles)  # Align text (left, center, right)

# Examples
cli.text.align('Left', 20, 'left')
cli.text.align('Center', 20, 'center', 'bold')
cli.text.align('Right', 20, 'right', 'dim')
```

### Layout Helper

Structured terminal output:

```python
cli.layout.box(content, width=40, align='center', color='cyan')
cli.layout.table(data, header_color='cyan', border_color='dim')

# Examples
cli.layout.box('Single line box')
cli.layout.box(['Line 1', 'Line 2', 'Line 3'], color='magenta')
cli.layout.table([
    {'Name': 'Alice', 'Status': 'Active'},
    {'Name': 'Bob', 'Status': 'Away'}
])
```

### Widgets Helper

Interactive and display widgets:

```python
cli.widgets.hr(width=40, char='-', color='dim')           # Horizontal rule
cli.widgets.bullet(text, char='•', color='green', indent=0)  # Bullet item
cli.widgets.progress(iteration, total, prefix='Progress:', length=30, color='cyan')  # Progress bar
cli.widgets.navigation(options, title='Select an option:')  # Interactive menu

# Examples
cli.widgets.hr()
cli.widgets.bullet('Feature one', color='green')
cli.widgets.bullet('Feature two', indent=2)
cli.widgets.progress(3, 10)
selection = cli.widgets.navigation(['First', 'Second', 'Third'])
```

## Built-in Help Topics

Access detailed guides for each module:

```python
cli.help()              # Full guide (default)
cli.help('quickstart')  # Quick start examples
cli.help('style')       # Color and styling guide
cli.help('text')        # Text formatting guide
cli.help('layout')      # Box and table rendering
cli.help('widgets')     # Widget reference
cli.help('hex')         # Truecolor RGB examples
cli.help('ext')         # 256-color palette guide
```

## Color Examples

### Named Colors

```python
print(cli.paint('Red', 'red'))
print(cli.paint('Green', 'green'))
print(cli.paint('Yellow', 'yellow'))
print(cli.paint('Cyan', 'cyan', 'bold'))
```

### Hex Colors (Truecolor)

```python
print(cli.paint('Error', cli.style.hex('#ff6b6b'), 'bold'))
print(cli.paint('Success', cli.style.hex('#22c55e'), 'bold'))
print(cli.paint('Warning', cli.style.hex('#f59e0b'), 'bold'))
print(cli.paint('Info', cli.style.hex('#38bdf8'), 'bold'))
```

### 256-Color Palette

```python
print(cli.paint('Bright Red', cli.style.ext(196), 'bold'))
print(cli.paint('Green', cli.style.ext(82)))
print(cli.paint('Cyan', cli.style.ext(45), 'bold'))
print(cli.paint('Gray', cli.style.ext(250)))
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

## C Language Integration

Use ALYODCLI from C/C++ programs using the socket server interface.

### Quick Start

1. **Start the socket server:**

```bash
alyodcli-server --host 127.0.0.1 --port 5555
```

2. **Build your C program:**

```bash
gcc -o myprogram myprogram.c c_bindings/alyodcli.c -lws2_32  # Windows
gcc -o myprogram myprogram.c c_bindings/alyodcli.c           # Unix/Linux
```

3. **Use ALYODCLI in C:**

```c
#include "c_bindings/alyodcli.h"
#include <stdio.h>

int main() {
    AlyodcliClient *client = alyodcli_connect_tcp("127.0.0.1", 5555);
    
    const char *styles[] = {"cyan", "bold"};
    AlyodcliResponse resp = alyodcli_paint(client, "Hello from C!", styles, 2);
    
    if (alyodcli_response_ok(&resp)) {
        printf("%s\n", alyodcli_response_result(&resp));
    }
    
    alyodcli_response_free(&resp);
    alyodcli_disconnect(client);
    return 0;
}
```

### Features

- **TCP Socket Interface** - Cross-platform networking
- **Unix Domain Sockets** - IPC on Unix/Linux
- **JSON-RPC 2.0 Protocol** - Standard message format
- **Full API Coverage** - Access all ALYODCLI functions from C
- **CMake & Makefile** - Easy integration into C/C++ projects

### Available Functions

- `alyodcli_paint()` - Apply text styles
- `alyodcli_style_get()` - Get color codes
- `alyodcli_style_hex()` - Convert hex colors
- `alyodcli_text_visual_len()` - Calculate text width
- `alyodcli_layout_box()` - Create boxes
- `alyodcli_layout_table()` - Create tables
- `alyodcli_widgets_hr()` - Horizontal rules
- `alyodcli_widgets_bullet()` - Bullet points
- And more...

### Documentation

See [c_bindings/README.md](c_bindings/README.md) for:
- Complete API reference
- Build instructions (Make, CMake, GCC)
- Multiple examples
- Platform support information
- Troubleshooting guide

## Performance Optimization with Cython

The package includes Cython extensions for performance-critical text processing:

```bash
# Install build tools
pip install cython setuptools wheel

# Build extensions
python setup.py build_ext --inplace

# This compiles:
# - Text processing (get_visual_len, ANSI stripping)
# - Color conversion (hex to RGB)
# - Unicode width calculations
```

**Performance gains:**
- 3-5x faster text processing for large strings
- Optimized regex ANSI stripping
- Compiled Unicode width lookups

## License

Apache-2.0 (see [LICENSE.txt](LICENSE.txt) )