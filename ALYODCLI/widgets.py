import sys
import re
import io
import contextlib
from typing import Any, Callable, Dict, List, Optional
from .style import Style
from .text import Text
from .terminal import Terminal
import subprocess,shutil

# ---------------------------------------------------------
# Widgets Component
# ---------------------------------------------------------
class Widgets:
    """Provides complex UI components and interactive widgets.
    - hr: Renders a horizontal rule with customizable width, character, and color.
    - bullet: Prints a bulleted item with optional indentation and color.
    - progress: Displays an inline progress bar with percentage completion.
    - navigation: Interactive menu for selecting options using arrow keys or WASD/Vim keys.
    """
    
    def __init__(self, style_manager: Style, text_manager: Text):
        self.style = style_manager
        self.text = text_manager

    def hr(self, width: int = 40, char: str = '─', color: str = 'dim'):
        """Prints a horizontal rule."""
        print(self.style.paint(char * width, color))

    def bullet(self, text: str, char: str = '•', color: str = 'green', indent: int = 0):
        """Prints a bulleted item."""
        space = " " * indent
        print(f"{space}{self.style.paint(char, color)} {text}")

    def progress(self, iteration: int, total: int, prefix: str = 'Progress:', length: int = 30, color: str = 'cyan'):
        """Renders an inline progress bar."""
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_len = int(length * iteration // total)
        bar = self.style.paint('█' * filled_len, color) + self.style.paint('-' * (length - filled_len), 'dim')
        
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% Complete')
        sys.stdout.flush()
        if iteration == total:
            print()

    def navigation(self, options: List[str], title: str = "Select an option:") -> str:
        """Interactive arrow-key menu."""
        current_idx = 0
        
        # Hide cursor
        sys.stdout.write("\033[?25l")
        
        try:
            while True:
                # Print menu
                print(self.style.paint(f"\n{title}", "bold", "cyan"))
                for i, option in enumerate(options):
                    if i == current_idx:
                        print(self.style.paint(f"  ❯ {option} ", "bg_white", "black", "bold"))
                    else:
                        print(f"    {option}")

                # Read key
                key = Terminal._getch()
                
                # Clear previous lines to redraw
                sys.stdout.write(f"\033[{len(options) + 2}A\033[J")
                
                # Parse keys
                if key in (b'\r', '\r', '\n'): # Enter
                    return options[current_idx]
                elif key in ('\x1b[A', b'H', 'w','W','k','K','8', b'k',b'K',b'w',b'W',b'8'):   # Up arrow, W (WASD), or K (Vim)
                    current_idx = (current_idx - 1) % len(options)
                elif key in ('\x1b[B', b'P', 's',"S",'j','J','2',b's',b'S',b'j',b'J',b'2'):   # Down arrow, S (WASD), or J (Vim)
                    current_idx = (current_idx + 1) % len(options)
                elif key in ('\x03', b'\x03'):  # Ctrl+C
                    raise KeyboardInterrupt

        finally:
            # Show cursor again
            sys.stdout.write("\033[?25h")
