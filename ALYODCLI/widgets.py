import sys
import re
from typing import Any, Callable, Dict, List, Optional
from .style import Style
from .text import Text
from .terminal import Terminal

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

    def button(
        self,
        label: str,
        focused: bool = False,
        width: int = 28,
        color: str = "cyan",
        focused_bg: str = "bg_white",
        focused_fg: str = "black",
    ) -> str:
        """Returns a button-like line for terminal UI screens."""
        content = f"[ {label} ]"
        aligned = self.text.align(content, width, "center")
        if focused:
            return self.style.paint(f"  {aligned}", focused_bg, focused_fg, "bold")
        return self.style.paint(f"  {aligned}", color)

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

    def _read_event(self):
        """Reads key input and parses mouse events on ANSI terminals."""
        if sys.platform == "win32":
            return "key", Terminal._getch()

        import tty
        import termios
        import select

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            first = sys.stdin.read(1)
            if first != "\x1b":
                return "key", first

            seq = first
            # Collect remaining bytes for escape sequences (arrows/mouse).
            while True:
                ready, _, _ = select.select([sys.stdin], [], [], 0.005)
                if not ready:
                    break
                seq += sys.stdin.read(1)
                if len(seq) >= 48:
                    break

            mouse_match = re.match(r"\x1b\[<(\d+);(\d+);(\d+)([Mm])", seq)
            if mouse_match:
                return "mouse", {
                    "button": int(mouse_match.group(1)),
                    "x": int(mouse_match.group(2)),
                    "y": int(mouse_match.group(3)),
                    "action": mouse_match.group(4),
                }

            return "key", seq
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _resolve_page(self, pages: Optional[Dict[str, Dict[str, Any]]], current_page: Optional[str]):
        if not pages:
            return {}
        if current_page not in pages:
            raise KeyError(f"Unknown page: {current_page}")
        return pages[current_page]

    def app(
        self,
        title: str = "ALYOD APP",
        subtitle: str = "",
        buttons: Optional[List[str]] = None,
        footer: str = "Use Up/Down (or W/S) and Enter",
        on_select: Optional[Callable[[str, int], Any]] = None,
        actions: Optional[Dict[str, Callable[[], Any]]] = None,
        pages: Optional[Dict[str, Dict[str, Any]]] = None,
        start_page: str = "main",
        routes: Optional[Dict[str, str]] = None,
        mouse: bool = True,
    ) -> str:
        """Launches an interactive terminal app screen with clickable-style buttons.

        The selected button label is returned. Use `on_select` for centralized handling
        or `actions` for per-button callbacks.

        Multi-page mode:
        - Provide `pages` as a dictionary of page configurations.
        - Each page supports: title, subtitle, content, buttons, footer, actions, routes.
        - Button callbacks may return a page name to navigate.
        """
        current_idx = 0
        actions = actions or {}
        routes = routes or {}
        current_page = start_page if pages else None

        # Hide cursor while the app screen is active.
        sys.stdout.write("\033[?25l")
        if mouse and sys.platform != "win32":
            # Enable mouse click reporting (X10 + SGR mode) on ANSI terminals.
            sys.stdout.write("\033[?1000h\033[?1006h")

        try:
            while True:
                page = self._resolve_page(pages, current_page)
                screen_title = page.get("title", title)
                screen_subtitle = page.get("subtitle", subtitle)
                screen_footer = page.get("footer", footer)
                screen_content = page.get("content", "")
                page_actions = page.get("actions", {})
                page_routes = page.get("routes", {})
                options = page.get("buttons", buttons or ["Start", "Settings", "Exit"])
                if not options:
                    raise ValueError("buttons must include at least one label")

                sys.stdout.write("\033[2J\033[H")

                header_lines = 1
                print(self.style.paint(screen_title, "bold", "cyan"))
                if screen_subtitle:
                    print(self.style.paint(screen_subtitle, "dim"))
                    header_lines += 1
                if pages and current_page is not None:
                    print(self.style.paint(f"Page: {current_page}", "dim"))
                    header_lines += 1
                print()
                header_lines += 1

                content_lines = 0

                if isinstance(screen_content, str) and screen_content:
                    print(screen_content)
                    print()
                    content_lines = len(screen_content.splitlines()) + 1
                elif isinstance(screen_content, list):
                    for line in screen_content:
                        print(str(line))
                    print()
                    content_lines = len(screen_content) + 1

                width = max(28, max(len(name) for name in options) + 8)
                start_row = header_lines + content_lines + 1

                for i, label in enumerate(options):
                    print(self.button(label, focused=(i == current_idx), width=width))

                print()
                print(self.style.paint(screen_footer, "dim"))

                event_type, event = self._read_event() if mouse else ("key", Terminal._getch())

                if event_type == "mouse":
                    if event.get("action") == "M":
                        mouse_y = event.get("y", -1)
                        mouse_x = event.get("x", -1)
                        if 1 <= mouse_x <= (width + 2):
                            clicked_idx = mouse_y - start_row
                            if 0 <= clicked_idx < len(options):
                                current_idx = clicked_idx
                                selected = options[current_idx]
                                callback = page_actions.get(selected) or actions.get(selected)
                                result = callback() if callback else None
                                if on_select:
                                    on_select(selected, current_idx)

                                target_page = page_routes.get(selected) or routes.get(selected)
                                if isinstance(result, str) and pages and result in pages:
                                    current_page = result
                                    current_idx = 0
                                    continue
                                if pages and target_page in pages:
                                    current_page = target_page
                                    current_idx = 0
                                    continue
                                return selected
                    continue

                key = event
                if key in (b"\r", "\r", "\n"):
                    selected = options[current_idx]
                    callback = page_actions.get(selected) or actions.get(selected)
                    result = callback() if callback else None
                    if on_select:
                        on_select(selected, current_idx)

                    target_page = page_routes.get(selected) or routes.get(selected)
                    if isinstance(result, str) and pages and result in pages:
                        current_page = result
                        current_idx = 0
                        continue
                    if pages and target_page in pages:
                        current_page = target_page
                        current_idx = 0
                        continue
                    return selected
                if key in ("\x1b[A", b"H", "w", "W", "k", "K", "8", b"k", b"K", b"w", b"W", b"8"):
                    current_idx = (current_idx - 1) % len(options)
                    continue
                if key in ("\x1b[B", b"P", "s", "S", "j", "J", "2", b"s", b"S", b"j", b"J", b"2"):
                    current_idx = (current_idx + 1) % len(options)
                    continue
                if key in ("\x03", b"\x03"):
                    raise KeyboardInterrupt
        finally:
            if mouse and sys.platform != "win32":
                sys.stdout.write("\033[?1000l\033[?1006l")
            sys.stdout.write("\033[?25h")
