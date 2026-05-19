"""
GUI library for the Urdu Programming Language.
Provides a Bootstrap-inspired API built on top of tkinter.
Cross-platform: Windows, Linux, macOS.

Usage from Urdu:
    درآمد { گوئی, بٹن, لیبل, ان_پٹ } سے "اردو/گوئی";
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser, font
from typing import Any, Callable, Optional
import threading


# ─── Bootstrap colour palette ─────────────────────────────────────────────────

BOOTSTRAP = {
    # English names
    "primary":   "#0d6efd",
    "secondary": "#6c757d",
    "success":   "#198754",
    "danger":    "#dc3545",
    "warning":   "#ffc107",
    "info":      "#0dcaf0",
    "light":     "#f8f9fa",
    "dark":      "#212529",
    "white":     "#ffffff",
    "muted":     "#6c757d",
    "body":      "#212529",
    "bg":        "#ffffff",
    # اردو رنگ نام (Urdu colour aliases)
    "بنیادی":    "#0d6efd",   # primary
    "ثانوی":     "#6c757d",   # secondary
    "کامیاب":    "#198754",   # success
    "خطرہ":      "#dc3545",   # danger
    "تنبیہ":     "#ffc107",   # warning
    "معلومات":   "#0dcaf0",   # info
    "ہلکا":      "#f8f9fa",   # light
    "گہرا":      "#212529",   # dark
    "سفید":      "#ffffff",   # white
    "مدھم":      "#6c757d",   # muted
}

# ─── Urdu Bootstrap class name → English Bootstrap class name ─────────────────
# Allows writing کلاس="بٹن بٹن-بنیادی" instead of کلاس="btn btn-primary"

_URDU_CLASS_MAP: dict[str, str] = {
    # ── Layout ────────────────────────────────────────────────────────────────
    "ڈبہ":              "container",
    "ڈبہ-بڑا":         "container-lg",
    "قطار":             "row",
    "ستون":             "col",
    "لچکدار":          "d-flex",
    "چھپا":             "d-none",
    "بلاک":             "d-block",

    # ── Spacing — padding (گدی) ───────────────────────────────────────────────
    "گدی-0":            "p-0",
    "گدی-1":            "p-1",
    "گدی-2":            "p-2",
    "گدی-3":            "p-3",
    "گدی-4":            "p-4",
    "گدی-5":            "p-5",
    "گدی_افقی-1":      "px-1",
    "گدی_افقی-2":      "px-2",
    "گدی_افقی-3":      "px-3",
    "گدی_افقی-4":      "px-4",
    "گدی_افقی-5":      "px-5",
    "گدی_عمودی-1":     "py-1",
    "گدی_عمودی-2":     "py-2",
    "گدی_عمودی-3":     "py-3",
    "گدی_عمودی-4":     "py-4",
    "گدی_عمودی-5":     "py-5",

    # ── Spacing — margin (فاصلہ) ─────────────────────────────────────────────
    "فاصلہ-0":          "m-0",
    "فاصلہ-1":          "m-1",
    "فاصلہ-2":          "m-2",
    "فاصلہ-3":          "m-3",
    "فاصلہ-4":          "m-4",
    "فاصلہ-5":          "m-5",

    # ── Size helpers ─────────────────────────────────────────────────────────
    "پورا_چوڑائی":      "w-100",
    "پوری_اونچائی":    "h-100",

    # ── Buttons (دکمہ) ────────────────────────────────────────────────────────
    "دکمہ":              "btn",
    "دکمہ-بنیادی":      "btn-primary",
    "دکمہ-ثانوی":       "btn-secondary",
    "دکمہ-کامیاب":      "btn-success",
    "دکمہ-خطرہ":        "btn-danger",
    "دکمہ-تنبیہ":       "btn-warning",
    "دکمہ-معلومات":     "btn-info",
    "دکمہ-ہلکا":        "btn-light",
    "دکمہ-گہرا":        "btn-dark",
    "دکمہ-خاکہ-بنیادی":  "btn-outline-primary",
    "دکمہ-خاکہ-ثانوی":   "btn-outline-secondary",
    "دکمہ-خاکہ-کامیاب":  "btn-outline-success",
    "دکمہ-خاکہ-خطرہ":    "btn-outline-danger",
    "دکمہ-خاکہ-تنبیہ":   "btn-outline-warning",
    "دکمہ-خاکہ-گہرا":    "btn-outline-dark",
    "دکمہ-چھوٹا":       "btn-sm",
    "دکمہ-بڑا":         "btn-lg",

    # ── Background colours (پس_منظر) ─────────────────────────────────────────
    "پس_منظر-بنیادی":   "bg-primary",
    "پس_منظر-ثانوی":    "bg-secondary",
    "پس_منظر-کامیاب":   "bg-success",
    "پس_منظر-خطرہ":     "bg-danger",
    "پس_منظر-تنبیہ":    "bg-warning",
    "پس_منظر-معلومات":  "bg-info",
    "پس_منظر-ہلکا":     "bg-light",
    "پس_منظر-گہرا":     "bg-dark",
    "پس_منظر-سفید":     "bg-white",

    # ── Text colours (متن_رنگ) ───────────────────────────────────────────────
    "متن-بنیادی":       "text-primary",
    "متن-ثانوی":        "text-secondary",
    "متن-کامیاب":       "text-success",
    "متن-خطرہ":         "text-danger",
    "متن-تنبیہ":        "text-warning",
    "متن-معلومات":      "text-info",
    "متن-ہلکا":         "text-light",
    "متن-گہرا":         "text-dark",
    "متن-سفید":         "text-white",
    "متن-مدھم":         "text-muted",
    "متن-وسط":          "text-center",
    "متن-شروع":         "text-start",
    "متن-آخر":          "text-end",

    # ── Typography ────────────────────────────────────────────────────────────
    "سرخی-1":           "h1",
    "سرخی-2":           "h2",
    "سرخی-3":           "h3",
    "سرخی-4":           "h4",
    "موٹا":             "fw-bold",
    "پتلا":             "fw-light",
    "چھوٹا_متن":        "small",

    # ── Borders & shape ───────────────────────────────────────────────────────
    "گول":              "rounded",
    "گول-3":            "rounded-3",
    "گولی":             "rounded-pill",
    "سرحد":             "border",
    "سایہ":             "shadow",
    "سایہ-چھوٹا":      "shadow-sm",

    # ── Forms ────────────────────────────────────────────────────────────────
    "فارم-کنٹرول":      "form-control",
    "فارم-انتخاب":      "form-select",
    "فارم-لیبل":        "form-label",

    # ── Navbar ────────────────────────────────────────────────────────────────
    "نیوی":             "navbar",
    "نیوی-گہرا":        "navbar-dark",
    "نیوی-ہلکا":        "navbar-light",
    "نیوی-سکڑاؤ":      "navbar-collapse",

    # ── Alerts ───────────────────────────────────────────────────────────────
    "اطلاع":            "alert",
    "اطلاع-بنیادی":     "alert-primary",
    "اطلاع-ثانوی":      "alert-secondary",
    "اطلاع-کامیاب":     "alert-success",
    "اطلاع-خطرہ":       "alert-danger",
    "اطلاع-تنبیہ":      "alert-warning",
    "اطلاع-معلومات":    "alert-info",
    "اطلاع-ہلکا":       "alert-light",
    "اطلاع-گہرا":       "alert-dark",

    # ── Table ────────────────────────────────────────────────────────────────
    "جدول_طرز":         "table",
    "دھاری_دار":        "table-striped",
    "بارڈر_والا":       "table-bordered",
    "میز-گہرا":         "table-dark",

    # ── Progress ─────────────────────────────────────────────────────────────
    "ترقی":             "progress",
    "ترقی-بنیادی":      "progress bg-primary",
    "ترقی-کامیاب":      "progress bg-success",
    "ترقی-خطرہ":        "progress bg-danger",
    "ترقی-تنبیہ":       "progress bg-warning",

    # ── Card ─────────────────────────────────────────────────────────────────
    "کارڈ":             "card",
    "کارڈ-جسم":        "card-body",
    "کارڈ-سرخی":       "card-title",
}

FONT_DEFAULT = ("Segoe UI", 11) if tk.TkVersion >= 8.5 else ("Arial", 11)
FONT_HEADING  = ("Segoe UI", 18, "bold")
FONT_BOLD     = ("Segoe UI", 11, "bold")
FONT_SMALL    = ("Segoe UI", 9)
FONT_CODE     = ("Consolas", 11)


def _normalise_classes(class_str: str) -> str:
    """Translate Urdu Bootstrap class tokens → English equivalents.
    Unrecognised tokens are passed through unchanged so English classes
    keep working alongside Urdu ones."""
    if not class_str:
        return ""
    result = []
    for token in class_str.split():
        mapped = _URDU_CLASS_MAP.get(token)
        if mapped:
            result.extend(mapped.split())   # one Urdu token may expand to 2 English tokens
        else:
            result.append(token)
    return " ".join(result)


def _parse_classes(class_str: str) -> dict:
    """Parse Bootstrap-like class string into style kwargs.
    Accepts both English and Urdu Bootstrap class names."""
    class_str = _normalise_classes(class_str)
    classes = class_str.split() if class_str else []
    style: dict = {}

    for cls in classes:
        # Background colour
        if cls.startswith("bg-"):
            color = cls[3:]
            style["bg"] = BOOTSTRAP.get(color, color)
        # Text colour
        elif cls.startswith("text-"):
            color = cls[5:]
            style["fg"] = BOOTSTRAP.get(color, color)
        # Font weight
        elif cls == "fw-bold":
            style["font_weight"] = "bold"
        elif cls == "fw-light":
            style["font_weight"] = "normal"
        # Heading sizes
        elif cls in ("h1", "display-1"):
            style["font_size"] = 28
        elif cls in ("h2", "display-2"):
            style["font_size"] = 24
        elif cls in ("h3",):
            style["font_size"] = 20
        elif cls in ("h4",):
            style["font_size"] = 16
        elif cls in ("small", "text-sm"):
            style["font_size"] = 9
        # Border radius
        elif cls in ("rounded", "rounded-3"):
            style["relief"] = "groove"
        elif cls == "rounded-pill":
            style["relief"] = "groove"
        # Padding
        elif cls.startswith("p-"):
            try: style["padx"] = style["pady"] = int(cls[2:]) * 4
            except ValueError: pass
        elif cls.startswith("px-"):
            try: style["padx"] = int(cls[3:]) * 4
            except ValueError: pass
        elif cls.startswith("py-"):
            try: style["pady"] = int(cls[3:]) * 4
            except ValueError: pass
        elif cls.startswith("m-"):
            try: style["padx"] = style["pady"] = int(cls[2:]) * 4
            except ValueError: pass
        # Button variants
        elif cls.startswith("btn-"):
            variant = cls[4:]
            if variant.startswith("outline-"):
                color = variant[8:]
                style["bg"] = BOOTSTRAP.get("white", "#fff")
                style["fg"] = BOOTSTRAP.get(color, color)
                style["relief"] = "groove"
            else:
                style["bg"] = BOOTSTRAP.get(variant, variant)
                style["fg"] = "white" if variant not in ("warning", "light") else "black"
        # Form control
        elif cls == "form-control":
            style["relief"] = "solid"
            style["borderwidth"] = 1
        # Width / height helpers
        elif cls == "w-100":
            style["fill_x"] = True
        elif cls == "h-100":
            style["fill_y"] = True
        # Text alignment
        elif cls in ("text-center", "text-centre"):
            style["justify"] = "center"
        elif cls == "text-end":
            style["justify"] = "right"
        elif cls == "text-start":
            style["justify"] = "left"

    return style


def _build_font(style: dict) -> tuple:
    family = style.get("font_family", "Segoe UI")
    size = style.get("font_size", 11)
    weight = style.get("font_weight", "normal")
    slant = style.get("font_slant", "roman")
    return (family, size, weight)


# ─── Base widget ──────────────────────────────────────────────────────────────

class _UrduWidget:
    """Base class for all Urdu GUI widgets."""

    def __init__(self):
        self._widget = None

    def حاصل_کریں(self) -> Any:
        raise NotImplementedError

    def مقرر_کریں(self, value: Any):
        raise NotImplementedError

    def چھپائیں(self):
        if self._widget:
            self._widget.grid_remove()
            self._widget.pack_forget()

    def دکھائیں(self):
        if self._widget:
            self._widget.pack()

    def ہٹائیں(self):
        if self._widget:
            self._widget.destroy()

    def رنگ(self, bg=None, fg=None):
        kw = {}
        if bg: kw["bg"] = BOOTSTRAP.get(bg, bg)
        if fg: kw["fg"] = BOOTSTRAP.get(fg, fg)
        if kw and self._widget:
            self._widget.config(**kw)
        return self

    @property
    def عنصر(self):
        return self._widget


# ─── Application window ──────────────────────────────────────────────────────

class گوئی(_UrduWidget):
    """Main application window — Bootstrap App."""

    def __init__(self, عنوان: str = "اردو ایپ", چوڑائی: int = 900,
                 اونچائی: int = 600, *, موضوع: str = "light",
                 تاریک: bool = False):
        super().__init__()
        self._root = tk.Tk()
        self._root.title(عنوان)
        self._root.geometry(f"{چوڑائی}x{اونچائی}")
        self._theme = موضوع

        bg = BOOTSTRAP["dark"] if تاریک else BOOTSTRAP["light"]
        self._root.configure(bg=bg)

        # Make responsive
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        self._widget = self._root

    def عنوان(self, title: str):
        self._root.title(title)
        return self

    def سائز(self, w: int, h: int):
        self._root.geometry(f"{w}x{h}")
        return self

    def کم_سائز(self, w: int, h: int):
        self._root.minsize(w, h)
        return self

    def آئیکن(self, path: str):
        try:
            self._root.iconphoto(True, tk.PhotoImage(file=path))
        except Exception:
            pass
        return self

    def بند_پر(self, callback: Callable):
        self._root.protocol("WM_DELETE_WINDOW", callback)
        return self

    def چلائیں(self):
        self._root.mainloop()

    def بند_کریں(self):
        self._root.destroy()

    def تازہ_کریں(self):
        self._root.update()

    def مرکز(self):
        self._root.update_idletasks()
        w = self._root.winfo_width()
        h = self._root.winfo_height()
        sw = self._root.winfo_screenwidth()
        sh = self._root.winfo_screenheight()
        self._root.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")
        return self


# ─── Layout containers ───────────────────────────────────────────────────────

class کنٹینر(_UrduWidget):
    """Bootstrap .container"""

    def __init__(self, parent: _UrduWidget | None, *,
                 کلاس: str = "", پیڈنگ: int = 16):
        super().__init__()
        p = parent._widget if parent else None
        style = _parse_classes(کلاس)
        bg = style.get("bg", BOOTSTRAP["bg"])
        self._widget = ttk.Frame(p) if p else tk.Frame()
        if isinstance(self._widget, tk.Frame):
            self._widget.configure(bg=bg, padx=پیڈنگ, pady=پیڈنگ // 2)
        self._widget.pack(fill="both", expand=True, padx=پیڈنگ, pady=پیڈنگ // 2)


class ردیف(_UrduWidget):
    """Bootstrap .row"""

    def __init__(self, parent: _UrduWidget | None, *,
                 کلاس: str = "", خلا: int = 8):
        super().__init__()
        p = parent._widget if parent else None
        self._widget = tk.Frame(p, bg=BOOTSTRAP["bg"])
        self._widget.pack(fill="x", padx=خلا, pady=خلا // 2)
        self._col_index = 0

    def _next_col(self):
        idx = self._col_index
        self._col_index += 1
        return idx


class کالم(_UrduWidget):
    """Bootstrap .col / .col-N"""

    def __init__(self, parent: ردیف | _UrduWidget, کلاس: str = "col", *,
                 وزن: int = 1):
        super().__init__()
        p = parent._widget if parent else None
        style = _parse_classes(کلاس)
        bg = style.get("bg", BOOTSTRAP["bg"])
        self._widget = tk.Frame(p, bg=bg)
        if isinstance(parent, ردیف):
            idx = parent._next_col()
            self._widget.grid(row=0, column=idx, sticky="nsew", padx=4)
            p.columnconfigure(idx, weight=وزن)
        else:
            self._widget.pack(side="left", fill="both", expand=True, padx=4)


class فریم(_UrduWidget):
    """Generic frame / card"""

    def __init__(self, parent: _UrduWidget | None = None, *,
                 کلاس: str = "", عنوان: str = ""):
        super().__init__()
        p = parent._widget if parent else None
        style = _parse_classes(کلاس)
        bg = style.get("bg", BOOTSTRAP["bg"])
        if عنوان:
            self._widget = tk.LabelFrame(p, text=عنوان, bg=bg,
                                          font=FONT_BOLD, padx=8, pady=8)
        else:
            self._widget = tk.Frame(p, bg=bg,
                                     relief=style.get("relief", "flat"),
                                     bd=style.get("borderwidth", 0))
        self._widget.pack(fill="both", expand=True, padx=8, pady=4)


# ─── Widgets ──────────────────────────────────────────────────────────────────

class لیبل(_UrduWidget):
    """Bootstrap label / text"""

    def __init__(self, parent: _UrduWidget | None, متن_: str = "", *,
                 کلاس: str = ""):
        super().__init__()
        p = parent._widget if parent else None
        style = _parse_classes(کلاس)
        fnt = _build_font(style)
        bg = style.get("bg", BOOTSTRAP["bg"])
        fg = style.get("fg", BOOTSTRAP["body"])
        self._var = tk.StringVar(value=str(متن_))
        self._widget = tk.Label(p, textvariable=self._var,
                                 font=fnt, bg=bg, fg=fg,
                                 padx=style.get("padx", 4),
                                 pady=style.get("pady", 2))
        self._widget.pack(anchor="w", pady=2)

    def حاصل_کریں(self): return self._var.get()
    def مقرر_کریں(self, value): self._var.set(str(value))
    def متن(self, value): self._var.set(str(value)); return self


class بٹن(_UrduWidget):
    """Bootstrap button"""

    def __init__(self, parent: _UrduWidget | None, متن_: str = "بٹن", *,
                 کلاس: str = "btn btn-primary",
                 پر_کلک: Callable | None = None,
                 چوڑائی: int | None = None):
        super().__init__()
        p = parent._widget if parent else None
        style = _parse_classes(کلاس)
        bg = style.get("bg", BOOTSTRAP["primary"])
        fg = style.get("fg", "white")
        fnt = _build_font(style)
        kw: dict = dict(text=متن_, bg=bg, fg=fg, font=fnt,
                         relief="flat", cursor="hand2",
                         padx=style.get("padx", 12),
                         pady=style.get("pady", 6),
                         activebackground=bg, activeforeground=fg)
        if چوڑائی:
            kw["width"] = چوڑائی
        self._widget = tk.Button(p, **kw)
        if پر_کلک:
            self._widget.configure(command=پر_کلک)
        self._widget.pack(anchor="w", pady=4)

    def پر_کلک(self, callback: Callable):
        self._widget.configure(command=callback)
        return self

    def غیر_فعال(self):
        self._widget.configure(state="disabled")
        return self

    def فعال(self):
        self._widget.configure(state="normal")
        return self

    def متن(self, value): self._widget.configure(text=str(value)); return self


class ان_پٹ(_UrduWidget):
    """Bootstrap form-control / input"""

    def __init__(self, parent: _UrduWidget | None, *,
                 کلاس: str = "form-control",
                 placeholder: str = "",
                 قسم: str = "متن",
                 چوڑائی: int = 30):
        super().__init__()
        p = parent._widget if parent else None
        style = _parse_classes(کلاس)
        show = "*" if قسم == "پاس_ورڈ" else ""
        self._var = tk.StringVar()
        self._placeholder = placeholder
        self._widget = tk.Entry(p, textvariable=self._var,
                                 width=چوڑائی, show=show,
                                 font=FONT_DEFAULT,
                                 relief="solid", bd=1)
        if placeholder:
            self._widget.insert(0, placeholder)
            self._widget.config(fg="gray")
            self._widget.bind("<FocusIn>", self._on_focus)
            self._widget.bind("<FocusOut>", self._on_blur)
        self._widget.pack(fill="x", pady=4)

    def _on_focus(self, e):
        if self._widget.get() == self._placeholder:
            self._widget.delete(0, "end")
            self._widget.config(fg="black")

    def _on_blur(self, e):
        if not self._widget.get():
            self._widget.insert(0, self._placeholder)
            self._widget.config(fg="gray")

    def حاصل_کریں(self) -> str:
        val = self._var.get()
        return "" if val == self._placeholder else val

    def مقرر_کریں(self, value: str):
        self._var.set(str(value))
        return self

    def صاف_کریں(self):
        self._var.set("")
        return self


class ٹیکسٹ_ایریا(_UrduWidget):
    """Multi-line text area"""

    def __init__(self, parent: _UrduWidget | None = None, *,
                 قطاریں: int = 5, کلاس: str = "form-control"):
        super().__init__()
        p = parent._widget if parent else None
        self._widget = tk.Text(p, height=قطاریں, font=FONT_DEFAULT,
                                relief="solid", bd=1, wrap="word")
        self._widget.pack(fill="both", expand=True, pady=4)

    def حاصل_کریں(self) -> str:
        return self._widget.get("1.0", "end-1c")

    def مقرر_کریں(self, value: str):
        self._widget.delete("1.0", "end")
        self._widget.insert("1.0", str(value))
        return self

    def لگائیں(self, value: str):
        self._widget.insert("end", str(value))
        return self


class ڈراپ_ڈاؤن(_UrduWidget):
    """Bootstrap select / dropdown"""

    def __init__(self, parent: _UrduWidget | None, اختیارات: list = [], *,
                 کلاس: str = "form-select"):
        super().__init__()
        p = parent._widget if parent else None
        self._var = tk.StringVar()
        self._widget = ttk.Combobox(p, textvariable=self._var,
                                     values=[str(o) for o in اختیارات],
                                     font=FONT_DEFAULT, state="readonly")
        if اختیارات:
            self._var.set(str(اختیارات[0]))
        self._widget.pack(fill="x", pady=4)

    def حاصل_کریں(self): return self._var.get()
    def مقرر_کریں(self, v): self._var.set(str(v)); return self

    def پر_تبدیلی(self, callback):
        self._widget.bind("<<ComboboxSelected>>", lambda e: callback(self._var.get()))
        return self


class چیک_بکس(_UrduWidget):
    """Bootstrap checkbox"""

    def __init__(self, parent: _UrduWidget | None, متن_: str = "", *,
                 پر_تبدیلی: Callable | None = None):
        super().__init__()
        p = parent._widget if parent else None
        self._var = tk.BooleanVar()
        self._widget = tk.Checkbutton(p, text=متن_, variable=self._var,
                                       font=FONT_DEFAULT, bg=BOOTSTRAP["bg"],
                                       command=پر_تبدیلی)
        self._widget.pack(anchor="w", pady=2)

    def حاصل_کریں(self) -> bool: return self._var.get()
    def مقرر_کریں(self, v: bool): self._var.set(v); return self


class ریڈیو(_UrduWidget):
    """Radio button group"""

    def __init__(self, parent: _UrduWidget | None, اختیارات: list,
                 *, افقی: bool = False):
        super().__init__()
        p = parent._widget if parent else None
        self._var = tk.StringVar()
        self._frame = tk.Frame(p, bg=BOOTSTRAP["bg"])
        self._frame.pack(anchor="w", pady=4)
        self._widget = self._frame
        side = "left" if افقی else "top"
        for opt in اختیارات:
            rb = tk.Radiobutton(self._frame, text=str(opt), value=str(opt),
                                 variable=self._var, font=FONT_DEFAULT,
                                 bg=BOOTSTRAP["bg"])
            rb.pack(side=side, padx=4)
        if اختیارات:
            self._var.set(str(اختیارات[0]))

    def حاصل_کریں(self): return self._var.get()
    def مقرر_کریں(self, v): self._var.set(str(v)); return self


class سلائڈر(_UrduWidget):
    """Bootstrap-styled range slider"""

    def __init__(self, parent: _UrduWidget | None = None, *,
                 کم: float = 0, زیادہ: float = 100,
                 قدر: float = 50, پر_تبدیلی: Callable | None = None):
        super().__init__()
        p = parent._widget if parent else None
        self._var = tk.DoubleVar(value=قدر)
        self._widget = ttk.Scale(p, from_=کم, to=زیادہ,
                                  variable=self._var, orient="horizontal",
                                  command=lambda v: پر_تبدیلی(float(v)) if پر_تبدیلی else None)
        self._widget.pack(fill="x", pady=4)

    def حاصل_کریں(self): return self._var.get()
    def مقرر_کریں(self, v): self._var.set(v); return self


class پروگریس_بار(_UrduWidget):
    """Bootstrap progress bar"""

    def __init__(self, parent: _UrduWidget | None = None, *,
                 قدر: float = 0, کلاس: str = "progress"):
        super().__init__()
        p = parent._widget if parent else None
        style = _parse_classes(کلاس)
        fg = style.get("bg", BOOTSTRAP["primary"])
        self._var = tk.DoubleVar(value=قدر)
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("custom.Horizontal.TProgressbar", troughcolor=BOOTSTRAP["light"],
                     background=fg, lightcolor=fg, darkcolor=fg)
        self._widget = ttk.Progressbar(p, variable=self._var, maximum=100,
                                        style="custom.Horizontal.TProgressbar")
        self._widget.pack(fill="x", pady=4)

    def حاصل_کریں(self): return self._var.get()
    def مقرر_کریں(self, v): self._var.set(min(100, max(0, v))); return self


class جدول(_UrduWidget):
    """Bootstrap table using ttk.Treeview"""

    def __init__(self, parent: _UrduWidget | None = None,
                 کالمیں: list[str] = [], *, کلاس: str = "table"):
        super().__init__()
        p = parent._widget if parent else None
        frame = tk.Frame(p)
        frame.pack(fill="both", expand=True, pady=4)
        self._widget = frame

        self._tv = ttk.Treeview(frame, columns=کالمیں, show="headings")
        for col in کالمیں:
            self._tv.heading(col, text=col)
            self._tv.column(col, minwidth=80, width=120, anchor="center")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self._tv.yview)
        self._tv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._tv.pack(fill="both", expand=True)

    def شامل_کریں(self, قطار: list):
        self._tv.insert("", "end", values=[str(v) for v in قطار])
        return self

    def صاف_کریں(self):
        for item in self._tv.get_children():
            self._tv.delete(item)
        return self

    def حاصل_کریں(self):
        return [self._tv.item(item)["values"]
                for item in self._tv.get_children()]


class نیوی_بار(_UrduWidget):
    """Bootstrap navbar"""

    def __init__(self, parent: _UrduWidget | None = None, *,
                 عنوان: str = "", کلاس: str = "navbar navbar-dark bg-dark"):
        super().__init__()
        p = parent._widget if parent else None
        style = _parse_classes(کلاس)
        bg = style.get("bg", BOOTSTRAP["dark"])
        fg = style.get("fg", "white")
        self._widget = tk.Frame(p, bg=bg, height=50)
        self._widget.pack(fill="x")
        self._widget.pack_propagate(False)
        if عنوان:
            tk.Label(self._widget, text=عنوان, bg=bg, fg=fg,
                      font=FONT_BOLD).pack(side="left", padx=16)
        self._buttons_frame = tk.Frame(self._widget, bg=bg)
        self._buttons_frame.pack(side="right", padx=8)

    def لنک(self, متن_: str, پر_کلک: Callable | None = None):
        btn = tk.Button(self._buttons_frame, text=متن_,
                         bg=BOOTSTRAP["dark"], fg="white",
                         relief="flat", cursor="hand2", font=FONT_DEFAULT,
                         command=پر_کلک)
        btn.pack(side="left", padx=8)
        return self


class الرٹ(_UrduWidget):
    """Bootstrap alert"""

    def __init__(self, parent: _UrduWidget | None, پیغام: str, *,
                 کلاس: str = "alert alert-primary", بند: bool = True):
        super().__init__()
        p = parent._widget if parent else None
        style = _parse_classes(کلاس)
        bg = style.get("bg", BOOTSTRAP["primary"] + "33")
        fg = style.get("fg", BOOTSTRAP["primary"])
        self._widget = tk.Frame(p, bg=bg, relief="flat", bd=1)
        self._widget.pack(fill="x", pady=4)
        lbl = tk.Label(self._widget, text=پیغام, bg=bg, fg=fg,
                        font=FONT_DEFAULT, padx=12, pady=8)
        lbl.pack(side="left", fill="both", expand=True)
        if بند:
            tk.Button(self._widget, text="×", bg=bg, fg=fg,
                       relief="flat", font=FONT_BOLD,
                       command=self._widget.destroy).pack(side="right", padx=8)


class ٹیب_ویو(_UrduWidget):
    """Bootstrap tabs using ttk.Notebook"""

    def __init__(self, parent: _UrduWidget | None = None):
        super().__init__()
        p = parent._widget if parent else None
        self._nb = ttk.Notebook(p)
        self._nb.pack(fill="both", expand=True, pady=4)
        self._widget = self._nb

    def ٹیب(self, عنوان: str) -> فریم:
        f = tk.Frame(self._nb, bg=BOOTSTRAP["bg"])
        self._nb.add(f, text=عنوان)
        wrapper = فریم.__new__(فریم)
        wrapper._widget = f
        return wrapper


class مودل(_UrduWidget):
    """Bootstrap modal (Toplevel dialog)"""

    def __init__(self, parent: _UrduWidget | None, عنوان: str = "ڈائیلاگ", *,
                 چوڑائی: int = 500, اونچائی: int = 300):
        super().__init__()
        p = parent._widget if parent else None
        self._win = tk.Toplevel(p)
        self._win.title(عنوان)
        self._win.geometry(f"{چوڑائی}x{اونچائی}")
        self._win.grab_set()
        self._widget = self._win

    def بند_کریں(self):
        self._win.destroy()

    def انتظار(self):
        self._win.wait_window()


# ─── Dialogs ─────────────────────────────────────────────────────────────────

class ڈائیلاگ:
    @staticmethod
    def معلومات(پیغام: str, عنوان: str = "معلومات"):
        messagebox.showinfo(عنوان, پیغام)

    @staticmethod
    def غلطی(پیغام: str, عنوان: str = "غلطی"):
        messagebox.showerror(عنوان, پیغام)

    @staticmethod
    def تنبیہ(پیغام: str, عنوان: str = "تنبیہ"):
        messagebox.showwarning(عنوان, پیغام)

    @staticmethod
    def تصدیق(پیغام: str, عنوان: str = "تصدیق") -> bool:
        return messagebox.askyesno(عنوان, پیغام)

    @staticmethod
    def فائل_کھولیں(قسم: list = None) -> str:
        ftypes = قسم or [("تمام فائلیں", "*.*")]
        return filedialog.askopenfilename(filetypes=ftypes)

    @staticmethod
    def فائل_محفوظ(قسم: list = None) -> str:
        ftypes = قسم or [("تمام فائلیں", "*.*")]
        return filedialog.asksaveasfilename(filetypes=ftypes)

    @staticmethod
    def فولڈر() -> str:
        return filedialog.askdirectory()

    @staticmethod
    def رنگ(ابتدائی: str = "#ffffff") -> str:
        result = colorchooser.askcolor(color=ابتدائی)
        return result[1] if result[1] else ابتدائی


# ─── Canvas ───────────────────────────────────────────────────────────────────

class کینوس(_UrduWidget):
    """Drawing canvas"""

    def __init__(self, parent: _UrduWidget | None = None, *,
                 چوڑائی: int = 600, اونچائی: int = 400,
                 پس_منظر: str = "white"):
        super().__init__()
        p = parent._widget if parent else None
        self._widget = tk.Canvas(p, width=چوڑائی, height=اونچائی, bg=پس_منظر)
        self._widget.pack(fill="both", expand=True)

    def دائرہ(self, x, y, r, رنگ="blue", بارڈر="black"):
        return self._widget.create_oval(x-r, y-r, x+r, y+r, fill=رنگ, outline=بارڈر)

    def مستطیل(self, x1, y1, x2, y2, رنگ="blue", بارڈر="black"):
        return self._widget.create_rectangle(x1, y1, x2, y2, fill=رنگ, outline=بارڈر)

    def لکیر(self, x1, y1, x2, y2, رنگ="black", موٹائی=2):
        return self._widget.create_line(x1, y1, x2, y2, fill=رنگ, width=موٹائی)

    def متن(self, x, y, متن_="", رنگ="black", سائز=12):
        return self._widget.create_text(x, y, text=متن_, fill=رنگ,
                                         font=("Segoe UI", سائز))

    def تصویر(self, x, y, path: str):
        img = tk.PhotoImage(file=path)
        self._widget.create_image(x, y, image=img, anchor="nw")
        self._widget._img_ref = img  # prevent GC

    def صاف_کریں(self):
        self._widget.delete("all")
        return self


# ─── Exports ─────────────────────────────────────────────────────────────────

__all__ = [
    "گوئی", "کنٹینر", "ردیف", "کالم", "فریم",
    "لیبل", "بٹن", "ان_پٹ", "ٹیکسٹ_ایریا",
    "ڈراپ_ڈاؤن", "چیک_بکس", "ریڈیو", "سلائڈر",
    "پروگریس_بار", "جدول", "نیوی_بار", "الرٹ",
    "ٹیب_ویو", "مودل", "ڈائیلاگ", "کینوس",
    "BOOTSTRAP",
]
