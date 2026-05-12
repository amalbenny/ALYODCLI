import re
import unicodedata
from .style import Style
# ---------------------------------------------------------
# Text Component
# ---------------------------------------------------------
class Text:
    """Handles text content length calculations and structural manipulation."""
    
    ANSI_ESCAPE_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def __init__(self, style_manager: Style):
        self.style = style_manager

    def get_visual_len(self, text: str) -> int:
        """Calculate visual length accounting for ANSI codes and wide characters (emojis, CJK)."""
        text_no_ansi = self.ANSI_ESCAPE_RE.sub('', str(text))
        visual_len = 0
        for char in text_no_ansi:
            # East Asian Wide and Fullwidth characters (emojis, CJK) take 2 columns
            width_attr = unicodedata.east_asian_width(char)
            visual_len += 2 if width_attr in ('W', 'F') else 1
        return visual_len

    def align(self, text: str, width: int, align: str = 'left', *styles: str) -> str:
        text_str = str(text)
        pad = width - self.get_visual_len(text_str)

        if pad <= 0:
            formatted = text_str
        elif align == 'right':
            formatted = ' ' * pad + text_str
        elif align == 'center':
            left = pad // 2
            formatted = ' ' * left + text_str + ' ' * (pad - left)
        else:
            formatted = text_str + ' ' * pad

        return self.style.paint(formatted, *styles)