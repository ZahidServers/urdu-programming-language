"""
Logging library for the Urdu Programming Language.

Usage from Urdu:
    درآمد { لاگ, لاگر } سے "اردو/لاگ";
    لاگ.معلومات("ایپ شروع ہوئی");
"""

from __future__ import annotations
import logging
import sys
import os
import json
import datetime
import traceback
from typing import Any, Optional
from pathlib import Path


# ─── Log levels ──────────────────────────────────────────────────────────────

class سطح:
    ڈیبگ     = logging.DEBUG
    معلومات  = logging.INFO
    تنبیہ    = logging.WARNING
    غلطی     = logging.ERROR
    بحران    = logging.CRITICAL

    DEBUG    = logging.DEBUG
    INFO     = logging.INFO
    WARNING  = logging.WARNING
    ERROR    = logging.ERROR
    CRITICAL = logging.CRITICAL


# ─── Coloured formatter ───────────────────────────────────────────────────────

_COLOURS = {
    "DEBUG":    "\033[36m",   # Cyan
    "INFO":     "\033[32m",   # Green
    "WARNING":  "\033[33m",   # Yellow
    "ERROR":    "\033[31m",   # Red
    "CRITICAL": "\033[35m",   # Magenta
}
_RESET = "\033[0m"

_LEVEL_NAMES_UR = {
    "DEBUG":    "ڈیبگ",
    "INFO":     "معلومات",
    "WARNING":  "تنبیہ",
    "ERROR":    "غلطی",
    "CRITICAL": "بحران",
}


class _UrduFormatter(logging.Formatter):
    def __init__(self, رنگ: bool = True, اردو: bool = True, json_mode: bool = False):
        super().__init__()
        self._colour = رنگ and sys.stdout.isatty() if hasattr(sys.stdout, "isatty") else False
        self._urdu = اردو
        self._json = json_mode

    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        level = record.levelname
        msg = record.getMessage()
        name = record.name
        line = record.lineno

        if self._json:
            return json.dumps({
                "وقت": ts,
                "سطح": _LEVEL_NAMES_UR.get(level, level) if self._urdu else level,
                "پیغام": msg,
                "ماڈیول": name,
                "سطر": line,
            }, ensure_ascii=False)

        level_display = _LEVEL_NAMES_UR.get(level, level) if self._urdu else level

        if self._colour:
            colour = _COLOURS.get(level, "")
            return f"{colour}[{ts}] [{level_display:^10}] [{name}:{line}] {msg}{_RESET}"
        return f"[{ts}] [{level_display:^10}] [{name}:{line}] {msg}"

    def formatException(self, exc_info) -> str:
        return "".join(traceback.format_exception(*exc_info))


# ─── Urdu Logger ─────────────────────────────────────────────────────────────

class لاگر:
    """Full-featured Urdu logger."""

    def __init__(self, نام: str = "اردو", *,
                 سطح_: int = logging.INFO,
                 فائل: str | None = None,
                 رنگ: bool = True,
                 جیسن: bool = False,
                 گھماؤ: bool = False,
                 زیادہ_سائز: int = 10 * 1024 * 1024,  # 10 MB
                 نسخے: int = 5):
        self._logger = logging.getLogger(نام)
        self._logger.setLevel(سطح_)
        self._logger.handlers.clear()
        self._logger.propagate = False

        fmt = _UrduFormatter(رنگ=رنگ, اردو=True, json_mode=جیسن)

        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        self._logger.addHandler(ch)

        # File handler
        if فائل:
            Path(فائل).parent.mkdir(parents=True, exist_ok=True)
            if گھماؤ:
                from logging.handlers import RotatingFileHandler
                fh = RotatingFileHandler(فائل, maxBytes=زیادہ_سائز, backupCount=نسخے, encoding="utf-8")
            else:
                fh = logging.FileHandler(فائل, encoding="utf-8")
            fh.setFormatter(_UrduFormatter(رنگ=False, اردو=True, json_mode=جیسن))
            self._logger.addHandler(fh)

    # ── log methods ───────────────────────────────────────────────────────────

    def ڈیبگ(self, پیغام: Any, *args, **kwargs):
        self._logger.debug(str(پیغام), *args, **kwargs)

    def معلومات(self, پیغام: Any, *args, **kwargs):
        self._logger.info(str(پیغام), *args, **kwargs)

    def تنبیہ(self, پیغام: Any, *args, **kwargs):
        self._logger.warning(str(پیغام), *args, **kwargs)

    def غلطی(self, پیغام: Any, *, استثناء: bool = False, **kwargs):
        self._logger.error(str(پیغام), exc_info=استثناء, **kwargs)

    def بحران(self, پیغام: Any, *, استثناء: bool = True, **kwargs):
        self._logger.critical(str(پیغام), exc_info=استثناء, **kwargs)

    # aliases
    def debug(self, msg, *a, **kw): self.ڈیبگ(msg, *a, **kw)
    def info(self, msg, *a, **kw): self.معلومات(msg, *a, **kw)
    def warn(self, msg, *a, **kw): self.تنبیہ(msg, *a, **kw)
    def warning(self, msg, *a, **kw): self.تنبیہ(msg, *a, **kw)
    def error(self, msg, **kw): self.غلطی(msg, **kw)
    def critical(self, msg, **kw): self.بحران(msg, **kw)

    def گروپ(self, نام: str) -> "_LogGroup":
        return _LogGroup(self, نام)

    def وقت(self, عنوان: str = ""):
        """Context manager to time a block."""
        return _Timer(self, عنوان)

    def سطح_مقرر(self, سطح_: int):
        self._logger.setLevel(سطح_)
        return self


class _LogGroup:
    """Group related log messages."""

    def __init__(self, logger: لاگر, نام: str):
        self._logger = logger
        self._name = نام

    def __enter__(self):
        self._logger.معلومات(f"┌─── {self._name} ───")
        return self

    def __exit__(self, *_):
        self._logger.معلومات(f"└─── /{self._name} ───")

    def معلومات(self, msg): self._logger.معلومات(f"│ {msg}")
    def غلطی(self, msg): self._logger.غلطی(f"│ {msg}")


class _Timer:
    """Time a block of code."""

    def __init__(self, logger: لاگر, عنوان: str):
        self._logger = logger
        self._title = عنوان
        self._start = None

    def __enter__(self):
        import time
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_):
        import time
        elapsed = (time.perf_counter() - self._start) * 1000
        self._logger.معلومات(f"⏱ {self._title}: {elapsed:.2f}ms")


# ─── Module-level default logger ─────────────────────────────────────────────

لاگ = لاگر("اردو")


def لاگر_بنائیں(نام: str, **kwargs) -> لاگر:
    """Create a named logger."""
    return لاگر(نام, **kwargs)


# ─── Structured logging ───────────────────────────────────────────────────────

class StructuredLog:
    """JSON structured logging."""

    def __init__(self, نام: str = "اردو_structured", فائل: str | None = None):
        self._log = لاگر(نام, جیسن=True, فائل=فائل)

    def لکھو(self, واقعہ: str, **fields):
        import json
        self._log.معلومات(json.dumps({"واقعہ": واقعہ, **fields}, ensure_ascii=False))


__all__ = [
    "لاگر", "لاگ", "لاگر_بنائیں", "سطح", "StructuredLog",
]
