from typing import List, Dict, Union
from .text import Text
from .style import Style
# ---------------------------------------------------------
# Layout Component
# ---------------------------------------------------------
class Layout:
    """Manages structural text displays like boxes and tables.
        - box: Renders text within a styled box with optional alignment and color.
        - table: Displays a list of dictionaries as a formatted table with headers and borders.
    """
    
    def __init__(self, text_manager: Text, style_manager: Style):
        self.text = text_manager
        self.style = style_manager

    def box(self, content: Union[str, List[str]], width=40, align='center', color='cyan'):
        tl, tr, bl, br, hz, vt = "┌", "┐", "└", "┘", "─", "│"
        lines = content.split('\n') if isinstance(content, str) else content

        output = [self.style.paint(f"{tl}{hz*(width+2)}{tr}", color)]
        side = self.style.paint(vt, color)
        for line in lines:
            output.append(f"{side} {self.text.align(line, width, align)} {side}")
        output.append(self.style.paint(f"{bl}{hz*(width+2)}{br}", color))
        
        print("\n".join(output))
        return "\n".join(output)

    def table(self, data: List[Dict[str, str]], header_color="cyan", border_color="dim"):
        if not data: return ""
        headers = list(data[0].keys())
        extracted = [{h: str(row.get(h, "")) for h in headers} for row in data]

        col_widths = {h: self.text.get_visual_len(h) for h in headers}
        for row in extracted:
            for h in headers:
                col_widths[h] = max(col_widths[h], self.text.get_visual_len(row[h]))

        vt = self.style.paint("│", border_color)
        hz = self.style.paint("─", border_color)
        divider = self.style.paint("┼", border_color).join([hz * (col_widths[h] + 2) for h in headers])

        # Updated: Wrap cells in spaces and join directly on the vertical bar
        output = [
            vt.join(f" {self.text.align(h.upper(), col_widths[h], 'center', header_color, 'bold')} " for h in headers),
            divider
        ]
        for row in extracted:
            output.append(vt.join(f" {self.text.align(row[h], col_widths[h], 'left')} " for h in headers))

        print("\n".join(output))
        return "\n".join(output)
