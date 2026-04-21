import os, sys
# ---------------------------------------------------------
# Terminal Component
# ---------------------------------------------------------
class Terminal:
    """Handles terminal interactions and environment configurations."""
    
    @staticmethod
    def _getch():
        """Cross-platform single character read for navigation."""
        if sys.platform == "win32":
            import msvcrt
            return msvcrt.getch()
        else:
            import tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
                if ch == '\x1b': # Handle escape sequences (arrows)
                    ch += sys.stdin.read(2)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
    @staticmethod
    def check_support() -> bool:
        if "NO_COLOR" in os.environ:
            return False
        if "FORCE_COLOR" in os.environ:
            return True
        if not sys.stdout.isatty():
            return False

        if sys.platform == "win32":
            import ctypes
            try:
                h = ctypes.windll.kernel32.GetStdHandle(-11)
                mode = ctypes.c_ulong()
                if not ctypes.windll.kernel32.GetConsoleMode(h, ctypes.byref(mode)):
                    return False
                return ctypes.windll.kernel32.SetConsoleMode(h, mode.value | 0x0004) != 0
            except Exception:
                return False

        return os.environ.get("TERM") != "dumb"

