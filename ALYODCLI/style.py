import re, sys
# ---------------------------------------------------------
# Style Component
# ---------------------------------------------------------
class Style:
    """Manages text styles, ANSI codes, and formatting options."""
    
    ANSI_CODES = {
        "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m", "blue": "\033[94m",
        "magenta": "\033[95m", "cyan": "\033[96m", "white": "\033[97m", "black": "\033[30m",

        "bg_red": "\033[41m", "bg_green": "\033[42m", "bg_yellow": "\033[43m",
        "bg_blue": "\033[44m", "bg_magenta": "\033[45m", "bg_cyan": "\033[46m",
        "bg_white": "\033[107m", "bg_black": "\033[40m",
        
        "bold": "\033[1m", "underline": "\033[4m", "dim": "\033[2m",
        "italic": "\033[3m", "strike": "\033[9m", "reset": "\033[0m",
    }
    FOREGROUND, BACKGROUND = 38, 48

    def __init__(self, enabled: bool):
        self.enabled = enabled

    def get(self, name: str) -> str:
        return self.ANSI_CODES.get(name.lower(), "") if self.enabled else ""

    def paint(self, text: str, *styles: str) -> str:
        if not self.enabled: return str(text)
        resolved = [s if s.startswith("\033") else self.get(s) for s in styles]
        if not any(resolved): return str(text)
        return f"{''.join(resolved)}{text}{self.get('reset')}"

    def ext(self, n: int, background=False) -> str:
        if not self.enabled or not (0 <= n <= 255): return ""
        code = self.BACKGROUND if background else self.FOREGROUND
        return f"\033[{code};5;{n}m"

    def hex(self, hex_code: str, background=False) -> str:
        if not self.enabled: return ""
        normalized = hex_code.lstrip('#')
        if not re.fullmatch(r"[0-9a-fA-F]{6}", normalized): return ""
        r, g, b = (int(normalized[i:i+2], 16) for i in (0, 2, 4))
        code = self.BACKGROUND if background else self.FOREGROUND
        return f"\033[{code};2;{r};{g};{b}m"
