# cython: language_level=3, boundscheck=False, wraparound=False
"""
Performance-optimized text processing module using Cython.
Handles ANSI stripping, visual length calculation, and unicode width detection.
"""

import re
import unicodedata
from typing import List, Tuple

# Precompile regex for ANSI codes
cdef str ANSI_ESCAPE_PATTERN = r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])'
ANSI_ESCAPE_RE = re.compile(ANSI_ESCAPE_PATTERN)

cdef dict EAST_ASIAN_WIDTHS = {
    'W': 2,  # Wide
    'F': 2,  # Fullwidth
    'A': 1,  # Ambiguous (treat as 1 in terminal)
    'H': 1,  # Halfwidth
    'N': 1,  # Neutral/Not East Asian
}

def strip_ansi(str text) -> str:
    """Strip ANSI escape sequences from text. Optimized with Cython."""
    return ANSI_ESCAPE_RE.sub('', text)

def calculate_visual_length(str text) -> int:
    """
    Calculate visual length accounting for ANSI codes and wide characters.
    This is the performance-critical function optimized with Cython.
    """
    cdef str text_no_ansi = ANSI_ESCAPE_RE.sub('', text)
    cdef int visual_len = 0
    cdef str char
    cdef str width_attr
    
    for char in text_no_ansi:
        width_attr = unicodedata.east_asian_width(char)
        visual_len += EAST_ASIAN_WIDTHS.get(width_attr, 1)
    
    return visual_len

def hex_to_ansi(str hex_code, bint background=False) -> str:
    """Convert hex color code to ANSI 24-bit color code. Optimized with Cython."""
    cdef str normalized = hex_code.lstrip('#')
    
    if not re.fullmatch(r"[0-9a-fA-F]{6}", normalized):
        return ""
    
    cdef int r = int(normalized[0:2], 16)
    cdef int g = int(normalized[2:4], 16)
    cdef int b = int(normalized[4:6], 16)
    cdef int code = 48 if background else 38
    
    return f"\033[{code};2;{r};{g};{b}m"

def batch_strip_ansi(list texts) -> list:
    """Batch strip ANSI codes from multiple strings."""
    return [ANSI_ESCAPE_RE.sub('', text) for text in texts]
