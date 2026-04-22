from typing import Any, Callable, Dict, List, Optional


def _resolve_page(pages: Optional[Dict[str, Dict[str, Any]]], current_page: Optional[str]) -> Dict[str, Any]:
    if not pages:
        return {}
    if current_page not in pages:
        raise KeyError(f"Unknown page: {current_page}")
    return pages[current_page]


def _resolve_navigation(
    selected: str,
    pages: Optional[Dict[str, Dict[str, Any]]],
    result: Any,
    page_routes: Dict[str, str],
    routes: Dict[str, str],
) -> Optional[str]:
    if isinstance(result, str) and pages and result in pages:
        return result

    target_page = page_routes.get(selected) or routes.get(selected)
    if pages and target_page in pages:
        return target_page
    return None


def _tkinter_app(
    title: str,
    subtitle: str,
    buttons: List[str],
    footer: str,
    on_select: Optional[Callable[[str, int], Any]],
    actions: Dict[str, Callable[[], Any]],
    pages: Optional[Dict[str, Dict[str, Any]]],
    start_page: str,
    routes: Dict[str, str],
    size: str,
) -> str:
    import tkinter as tk
    from tkinter import ttk

    selected_value = {"value": ""}
    current_page = {"name": start_page if pages else None}

    root = tk.Tk()
    root.title(title)
    root.geometry(size)
    root.minsize(480, 320)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    frame = ttk.Frame(root, padding=16)
    frame.pack(fill="both", expand=True)

    title_label = ttk.Label(frame, text=title, font=("Segoe UI", 18, "bold"))
    title_label.pack(anchor="w")

    subtitle_label = ttk.Label(frame, text=subtitle)
    subtitle_label.pack(anchor="w", pady=(2, 12))

    content_frame = ttk.Frame(frame)
    content_frame.pack(fill="x")

    button_frame = ttk.Frame(frame)
    button_frame.pack(fill="x", pady=(10, 8))

    footer_label = ttk.Label(frame, text=footer)
    footer_label.pack(anchor="w", pady=(8, 0))

    def select_button(label: str, idx: int) -> None:
        page = _resolve_page(pages, current_page["name"])
        page_actions = page.get("actions", {})
        page_routes = page.get("routes", {})

        callback = page_actions.get(label) or actions.get(label)
        result = callback() if callback else None

        if on_select:
            on_select(label, idx)

        next_page = _resolve_navigation(label, pages, result, page_routes, routes)
        if next_page:
            current_page["name"] = next_page
            render()
            return

        selected_value["value"] = label
        root.quit()

    def render() -> None:
        page = _resolve_page(pages, current_page["name"])
        screen_title = page.get("title", title)
        screen_subtitle = page.get("subtitle", subtitle)
        screen_footer = page.get("footer", footer)
        screen_content = page.get("content", "")
        options = page.get("buttons", buttons)

        title_label.config(text=screen_title)
        subtitle_label.config(text=screen_subtitle)
        footer_label.config(text=screen_footer)

        for child in content_frame.winfo_children():
            child.destroy()
        for child in button_frame.winfo_children():
            child.destroy()

        if isinstance(screen_content, str) and screen_content:
            ttk.Label(content_frame, text=screen_content, justify="left").pack(anchor="w")
        elif isinstance(screen_content, list):
            for line in screen_content:
                ttk.Label(content_frame, text=str(line), justify="left").pack(anchor="w")

        for idx, label in enumerate(options):
            ttk.Button(
                button_frame,
                text=label,
                command=lambda label=label, idx=idx: select_button(label, idx),
            ).pack(fill="x", pady=4)

    def close_window() -> None:
        root.quit()

    root.protocol("WM_DELETE_WINDOW", close_window)
    render()
    root.mainloop()
    root.destroy()
    return selected_value["value"]


def _qt_app(
    title: str,
    subtitle: str,
    buttons: List[str],
    footer: str,
    on_select: Optional[Callable[[str, int], Any]],
    actions: Dict[str, Callable[[], Any]],
    pages: Optional[Dict[str, Dict[str, Any]]],
    start_page: str,
    routes: Dict[str, str],
    size: str,
) -> str:
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QFrame
    except Exception as exc:
        raise ImportError("Qt backend requires PySide6. Install with: pip install PySide6") from exc

    width, height = 640, 420
    if "x" in size:
        try:
            width_str, height_str = size.lower().split("x", 1)
            width, height = int(width_str), int(height_str)
        except Exception:
            pass

    app = QApplication.instance() or QApplication([])
    selected_value = {"value": ""}
    current_page = {"name": start_page if pages else None}

    window = QWidget()
    window.setWindowTitle(title)
    window.resize(width, height)

    layout = QVBoxLayout(window)
    layout.setContentsMargins(14, 14, 14, 14)
    layout.setSpacing(6)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    title_label = QLabel(title)
    subtitle_label = QLabel(subtitle)
    content_widgets: List[QLabel] = []
    button_widgets: List[QPushButton] = []
    footer_label = QLabel(footer)

    content_panel = QFrame()
    content_layout = QVBoxLayout(content_panel)
    content_layout.setContentsMargins(0, 2, 0, 2)
    content_layout.setSpacing(2)
    content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    button_panel = QFrame()
    button_layout = QVBoxLayout(button_panel)
    button_layout.setContentsMargins(0, 2, 0, 2)
    button_layout.setSpacing(4)
    button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    title_label.setStyleSheet("font-size: 20px; font-weight: 700;")
    subtitle_label.setStyleSheet("color: #555;")
    footer_label.setStyleSheet("color: #666;")

    def compact_label(label: QLabel) -> None:
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

    compact_label(title_label)
    compact_label(subtitle_label)
    compact_label(footer_label)

    layout.addWidget(title_label)
    layout.addWidget(subtitle_label)
    layout.addWidget(content_panel)
    layout.addWidget(button_panel)
    layout.addWidget(footer_label)
    layout.addStretch(1)

    def clear_dynamic_widgets() -> None:
        for widget in content_widgets + button_widgets:
            content_layout.removeWidget(widget)
            button_layout.removeWidget(widget)
            widget.deleteLater()
        content_widgets.clear()
        button_widgets.clear()

    def select_button(label: str, idx: int) -> None:
        page = _resolve_page(pages, current_page["name"])
        page_actions = page.get("actions", {})
        page_routes = page.get("routes", {})

        callback = page_actions.get(label) or actions.get(label)
        result = callback() if callback else None

        if on_select:
            on_select(label, idx)

        next_page = _resolve_navigation(label, pages, result, page_routes, routes)
        if next_page:
            current_page["name"] = next_page
            render()
            return

        selected_value["value"] = label
        window.close()

    def render() -> None:
        clear_dynamic_widgets()

        page = _resolve_page(pages, current_page["name"])
        screen_title = page.get("title", title)
        screen_subtitle = page.get("subtitle", subtitle)
        screen_footer = page.get("footer", footer)
        screen_content = page.get("content", "")
        options = page.get("buttons", buttons)

        title_label.setText(screen_title)
        subtitle_label.setText(screen_subtitle)
        footer_label.setText(screen_footer)

        if isinstance(screen_content, str) and screen_content:
            content_label = QLabel(screen_content)
            content_label.setWordWrap(True)
            compact_label(content_label)
            content_layout.addWidget(content_label)
            content_widgets.append(content_label)
        elif isinstance(screen_content, list):
            for line in screen_content:
                content_label = QLabel(str(line))
                content_label.setWordWrap(True)
                compact_label(content_label)
                content_layout.addWidget(content_label)
                content_widgets.append(content_label)

        for idx, label in enumerate(options):
            button = QPushButton(label)
            button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            button.setMinimumHeight(28)
            button.clicked.connect(lambda checked=False, label=label, idx=idx: select_button(label, idx))
            button_layout.addWidget(button)
            button_widgets.append(button)

    render()
    window.show()
    app.exec()
    return selected_value["value"]


def app(
    title: str = "ALYOD APP",
    subtitle: str = "",
    buttons: Optional[List[str]] = None,
    footer: str = "Click a button",
    on_select: Optional[Callable[[str, int], Any]] = None,
    actions: Optional[Dict[str, Callable[[], Any]]] = None,
    pages: Optional[Dict[str, Dict[str, Any]]] = None,
    start_page: str = "main",
    routes: Optional[Dict[str, str]] = None,
    backend: str = "auto",
    size: str = "640x420",
) -> str:
    """Launches a desktop GUI app with Tkinter or Qt backend."""
    options = buttons or ["Start", "Settings", "Exit"]
    if not options and not pages:
        raise ValueError("buttons must include at least one label")

    actions = actions or {}
    routes = routes or {}
    backend = (backend or "auto").lower()

    if backend in ("tk", "tkinter"):
        return _tkinter_app(title, subtitle, options, footer, on_select, actions, pages, start_page, routes, size)

    if backend == "qt":
        return _qt_app(title, subtitle, options, footer, on_select, actions, pages, start_page, routes, size)

    if backend == "auto":
        try:
            return _qt_app(title, subtitle, options, footer, on_select, actions, pages, start_page, routes, size)
        except Exception:
            return _tkinter_app(title, subtitle, options, footer, on_select, actions, pages, start_page, routes, size)

    raise ValueError("backend must be one of: auto, tkinter, qt")
