import re
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
        return len(self.ANSI_ESCAPE_RE.sub('', str(text)))

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

