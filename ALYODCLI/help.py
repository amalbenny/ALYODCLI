from .style import Style
from .terminal import Terminal


def helpfn(topic: str = "all") -> str:
    topic = str(topic).lower().strip()

    style = Style(enabled=Terminal.check_support())

    def paint(text: str, *styles: str) -> str:
        return style.paint(text, *styles) if style.enabled else text

    def heading(text: str) -> str:
        return paint(text, "cyan", "bold")

    def name(text: str) -> str:
        return paint(text, "yellow", "bold")

    def example(text: str) -> str:
        return paint(text, "green")

    def add_heading(lines: list[str], text: str) -> None:
        lines.append(heading(text))

    def add_hex_examples(lines: list[str], items: list[tuple[str, str]], background: bool = False) -> None:
        for color_code, label_text in items:
            if background:
                lines.append(
                    "  "
                    + example("cli.style.hex")
                    + "("
                    + example(color_code)
                    + ", "
                    + example("background=True")
                    + ")  # "
                    + example(label_text)
                )
            else:
                lines.append("  " + example("cli.style.hex") + "(" + example(color_code) + ")  # " + example(label_text))

    overview: list[str] = []
    add_heading(overview, "ALYODCLI Developer Help")
    overview.extend(
        [
            "",
            heading("Purpose:"),
            "  Build styled terminal output, formatted text, layout blocks, and interactive widgets.",
            "",
            heading("How to start:"),
            "  " + example("from") + " " + name("ALYODCLI") + " " + example("import") + " " + name("Activate"),
            "  " + name("cli") + " " + example("=") + " " + name("Activate") + example("()"),
            "  " + name("cli") + "." + name("help") + example("()"),
            "",
            heading("Core objects exposed by Activate:"),
            "  " + name("cli.style") + " -> " + example("Style helper for ANSI, ext, and hex colors"),
            "  " + name("cli.text") + " -> " + example("Text helper for length and alignment"),
            "  " + name("cli.layout") + " -> " + example("Layout helper for boxes and tables"),
            "  " + name("cli.widgets") + " -> " + example("Widgets helper for bullets, progress, and navigation"),
            "",
        ]
    )

    public_api: list[str] = []
    add_heading(public_api, "Public API Reference")
    public_api.extend(
        [
            "",
            heading("Activate:"),
            "  - " + name("paint(text, *styles)") + ": " + example("format text with named styles or raw ANSI sequences"),
            "  - " + name("help(topic='all')") + ": " + example("print this help guide"),
            "",
            heading("Style:"),
            "  - " + name("get(name)") + ": " + example("resolve a named ANSI code"),
            "  - " + name("paint(text, *styles)") + ": " + example("wrap text in one or more styles"),
            "  - " + name("ext(n, background=False)") + ": " + example("use 256-color ANSI output"),
            "  - " + name("hex(hex_code, background=False)") + ": " + example("use truecolor RGB output"),
            "",
            heading("Text:"),
            "  - " + name("get_visual_len(text)") + ": " + example("measure visible width while ignoring ANSI codes"),
            "  - " + name("align(text, width, align='left', *styles)") + ": " + example("align and optionally style text"),
            "",
            heading("Layout:"),
            "  - " + name("box(content, width=40, align='center', color='cyan')") + ": " + example("draw a boxed block"),
            "  - " + name("table(data, header_color='cyan', border_color='dim')") + ": " + example("render a table from dictionaries"),
            "",
            heading("Widgets:"),
            "  - " + name("hr(width=40, char='-', color='dim')") + ": " + example("draw a horizontal rule"),
            "  - " + name("bullet(text, char='*', color='green', indent=0)") + ": " + example("print a bullet item"),
            "  - "
            + name("progress(iteration, total, prefix='Progress:', length=30, color='cyan')")
            + ": "
            + example("show a progress bar"),
            "  - " + name("navigation(options, title='Select an option:')") + ": " + example("interactive arrow-key menu"),
            "",
            heading("Terminal helpers used internally:"),
            "  - " + name("check_support()") + ": " + example("detect terminal ANSI capability"),
            "  - " + name("_getch()") + ": " + example("read a key press for navigation"),
            "",
        ]
    )

    quickstart: list[str] = []
    add_heading(quickstart, "Quickstart")
    quickstart.extend(
        [
            "",
            heading("1. Create the main object:"),
            "  " + name("cli") + " " + example("=") + " " + name("Activate") + example("()"),
            "",
            heading("2. Print styled text:"),
            "  " + example("print(") + name("cli.paint('Hello', 'cyan', 'bold')") + example(")"),
            "  " + example("print(") + name("cli.paint('Underline', 'underline')") + example(")"),
            "",
            heading("3. Build a box and a table:"),
            "  " + name("cli.layout.box(['Title', 'Subtitle'], color='cyan')"),
            "  " + name("cli.layout.table([{'Name': 'ALYODCLI', 'Status': 'Ready'}])"),
            "",
            heading("4. Show bullets and progress:"),
            "  " + name("cli.widgets.bullet('First item', color='green')"),
            "  " + name("cli.widgets.progress(5, 10)"),
            "",
        ]
    )

    style_help: list[str] = []
    add_heading(style_help, "Style Helper")
    style_help.extend(
        [
            "",
            heading("Named style tokens accepted by cli.paint():"),
            "  "
            + name("red")
            + ", "
            + name("green")
            + ", "
            + name("yellow")
            + ", "
            + name("blue")
            + ", "
            + name("magenta")
            + ", "
            + name("cyan")
            + ", "
            + name("white")
            + ", "
            + name("black"),
            "  "
            + name("bg_red")
            + ", "
            + name("bg_green")
            + ", "
            + name("bg_yellow")
            + ", "
            + name("bg_blue")
            + ", "
            + name("bg_magenta")
            + ", "
            + name("bg_cyan")
            + ", "
            + name("bg_white")
            + ", "
            + name("bg_black"),
            "  " + name("bold") + ", " + name("underline") + ", " + name("dim") + ", " + name("italic") + ", " + name("strike"),
            "",
            heading("Example combinations:"),
            "  " + name("cli.paint('Primary', 'cyan', 'bold')"),
            "  " + name("cli.paint('Muted', 'dim')"),
            "  " + name("cli.paint('Alert', 'red', 'bold', 'underline')"),
            "",
            heading("Raw ANSI escape sequences are also supported:"),
            "  " + name("cli.paint('Custom', '\033[95m', '\033[1m')"),
        ]
    )

    text_help: list[str] = []
    add_heading(text_help, "Text Helper")
    text_help.extend(
        [
            "",
            example("Visible-width handling keeps alignment correct for ANSI styles and wide characters."),
            "",
            heading("Methods:"),
            "  " + name("cli.text.get_visual_len(text)"),
            "  " + name("cli.text.align(text, width, align='left', *styles)"),
            "",
            heading("Examples:"),
            "  " + name("cli.text.align('Left', 20, 'left')"),
            "  " + name("cli.text.align('Center', 20, 'center', 'bold')"),
            "  " + name("cli.text.align('Right', 20, 'right', 'dim')"),
        ]
    )

    layout_help: list[str] = []
    add_heading(layout_help, "Layout Helper")
    layout_help.extend(
        [
            "",
            name("box(content, width=40, align='center', color='cyan')"),
            "  - " + example("Accepts a string or a list of lines."),
            "  - " + example("Automatically expands to fit the widest visible line."),
            "",
            name("table(data, header_color='cyan', border_color='dim')"),
            "  - " + example("Accepts a list of dictionaries."),
            "  - " + example("Uses the first row's keys as table headers."),
            "",
            heading("Examples:"),
            "  " + name("cli.layout.box('Single line box')"),
            "  " + name("cli.layout.box(['One', 'Two', 'Three'], color='magenta')"),
            "  " + name("cli.layout.table([{'Module': 'Style', 'Status': 'Ready'}])"),
        ]
    )

    widgets_help: list[str] = []
    add_heading(widgets_help, "Widgets Helper")
    widgets_help.extend(
        [
            "",
            name("hr(width=40, char='-', color='dim')"),
            "  - " + example("Prints a horizontal divider."),
            "",
            name("bullet(text, char='*', color='green', indent=0)"),
            "  - " + example("Prints a bullet item with optional indentation."),
            "",
            name("progress(iteration, total, prefix='Progress:', length=30, color='cyan')"),
            "  - " + example("Prints an inline progress bar."),
            "",
            name("navigation(options, title='Select an option:')"),
            "  - " + example("Lets users move with arrow keys, W/S, or Vim keys."),
            "",
            heading("Examples:"),
            "  " + name("cli.widgets.hr()"),
            "  " + name("cli.widgets.bullet('Item')"),
            "  " + name("cli.widgets.progress(3, 10)"),
            "  " + name("cli.widgets.navigation(['One', 'Two'])"),
        ]
    )

    hex_help: list[str] = []
    add_heading(hex_help, "Hex Color Guide")
    hex_help.extend(["", heading("Truecolor foreground examples:")])

    foreground_examples = [
        ("#ff6b6b", "coral"),
        ("#4dabf7", "blue"),
        ("#51cf66", "green"),
        ("#fcc419", "amber"),
        ("#f97316", "orange"),
        ("#8b5cf6", "violet"),
    ]
    for color_code, label_text in foreground_examples:
        hex_help.append("  " + example("cli.style.hex") + "(" + example(color_code) + ")  # " + example(label_text))

    hex_help.extend(["", heading("Truecolor background examples:")])

    background_examples = [
        ("#1f2937", "slate background"),
        ("#0f766e", "teal background"),
        ("#7c2d12", "brown background"),
        ("#312e81", "indigo background"),
    ]
    add_hex_examples(hex_help, background_examples, background=True)
    hex_help.extend(
        [
            "",
            heading("Common combinations:"),
            "  " + name("cli.paint('Warning', cli.style.hex('#f59e0b'), 'bold')"),
            "  " + name("cli.paint('Info', cli.style.hex('#38bdf8'), 'bold')"),
            "  " + name("cli.paint('Success', cli.style.hex('#22c55e'), 'bold')"),
            "  " + name("cli.paint('Error', cli.style.hex('#ef4444'), 'bold')"),
            "",
            heading("Resetting output:"),
            "  " + name("cli.style.get('reset')"),
            "  " + name("print(cli.style.hex('#22c55e') + 'OK' + cli.style.get('reset'))"),
        ]
    )

    ext_help: list[str] = []
    add_heading(ext_help, "256-Color Guide")
    ext_help.extend(["", heading("Foreground examples:")])

    ext_examples = [
        (196, "bright red"),
        (202, "orange"),
        (82, "green"),
        (45, "cyan"),
        (93, "purple"),
        (250, "gray"),
    ]
    for code, label_text in ext_examples:
        ext_help.append("  " + example("cli.style.ext") + "(" + example(str(code)) + ")  # " + example(label_text))

    ext_help.extend(["", heading("Background examples:")])

    background_ext_examples = [
        (196, "bright red background"),
        (45, "cyan background"),
        (22, "dark green background"),
        (237, "gray background"),
    ]
    for code, label_text in background_ext_examples:
        ext_help.append(
            "  " + example("cli.style.ext") + "(" + example(str(code)) + ", " + example("background=True") + ")  # " + example(label_text)
        )

    ext_help.extend(
        [
            "",
            heading("Common combinations:"),
            "  " + name("cli.paint('Alert', cli.style.ext(196), 'bold')"),
            "  " + name("cli.paint('Info', cli.style.ext(45), 'bold')"),
            "  " + name("cli.paint('Muted', cli.style.ext(250))"),
        ]
    )

    guides: dict[str, list[str]] = {
        "all": overview + [""] + public_api + [""] + quickstart + [""] + style_help + [""] + text_help + [""] + layout_help + [""] + widgets_help + [""] + hex_help + [""] + ext_help,
        "quickstart": quickstart,
        "style": style_help,
        "text": text_help,
        "layout": layout_help,
        "widgets": widgets_help,
        "hex": hex_help,
        "ext": ext_help,
    }

    if topic in ("", "help", "all", "quickstart"):
        selected = guides["all"]
    elif topic in guides:
        selected = guides[topic]
    else:
        selected = [
            heading("Unknown help topic."),
            "",
            heading("Available topics:") + " all, quickstart, style, text, layout, widgets, hex, ext",
            "",
            *guides["all"],
        ]

    message = "\n".join(selected)
    print(message)
    return message