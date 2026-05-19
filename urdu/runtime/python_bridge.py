"""
Python interoperability bridge for the Urdu Programming Language.
Allows native use of any Python library from Urdu code.

Usage from Urdu:
    درآمد { py } سے "اردو/پایتھن";
    متغیر os = py.درآمد("os");
    لکھو(os.getcwd());
"""

from __future__ import annotations
import importlib
import sys
from typing import Any


class PythonBridge:
    """Bridge to Python's ecosystem."""

    @staticmethod
    def درآمد(ماڈیول: str) -> Any:
        """Import any Python module by name."""
        return importlib.import_module(ماڈیول)

    @staticmethod
    def چلائیں(کوڈ: str, ماحول: dict = None) -> Any:
        """Execute Python code string."""
        ns = ماحول or {}
        exec(کوڈ, ns)
        return ns

    @staticmethod
    def جانچیں(کوڈ: str, ماحول: dict = None) -> Any:
        """Evaluate a Python expression."""
        return eval(کوڈ, ماحول or {})

    @staticmethod
    def نسخہ() -> str:
        return sys.version

    @staticmethod
    def راستہ() -> list:
        return sys.path

    @staticmethod
    def نصب(پیکج: str) -> bool:
        """pip install a package at runtime."""
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", پیکج],
            capture_output=True, text=True
        )
        return result.returncode == 0

    @staticmethod
    def خصوصیات(شے) -> list:
        """dir() — get all attributes of an object."""
        return [a for a in dir(شے) if not a.startswith("__")]

    @staticmethod
    def مدد(شے) -> str:
        """help() — get documentation."""
        import io, pydoc
        buf = io.StringIO()
        pydoc.Helper(output=buf)(شے)
        return buf.getvalue()

    @staticmethod
    def قسم(شے) -> type:
        return type(شے)

    @staticmethod
    def نسخ(شے) -> Any:
        import copy
        return copy.deepcopy(شے)

    @staticmethod
    def جیسن(شے) -> str:
        import json
        return json.dumps(شے, ensure_ascii=False, indent=2)

    @staticmethod
    def بائٹس(متن: str, انکوڈنگ: str = "utf-8") -> bytes:
        return متن.encode(انکوڈنگ)

    @staticmethod
    def متن(بائٹس_: bytes, انکوڈنگ: str = "utf-8") -> str:
        return بائٹس_.decode(انکوڈنگ)

    @staticmethod
    def ماحول() -> dict:
        import os
        return dict(os.environ)

    @staticmethod
    def ماحول_حاصل(نام: str, ڈیفالٹ: str = "") -> str:
        import os
        return os.environ.get(نام, ڈیفالٹ)

    @staticmethod
    def ماحول_مقرر(نام: str, قدر: str):
        import os
        os.environ[نام] = str(قدر)


py = PythonBridge()

# Common Python stdlib proxies
os_mod = importlib.import_module("os")
sys_mod = sys
path_mod = importlib.import_module("pathlib")

# Quick access to popular libraries
def pandas():
    try:
        import pandas as pd
        return pd
    except ImportError:
        raise ImportError("pip install pandas")

def numpy():
    try:
        import numpy as np
        return np
    except ImportError:
        raise ImportError("pip install numpy")

def requests():
    try:
        import requests as req
        return req
    except ImportError:
        raise ImportError("pip install requests")

def matplotlib():
    try:
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        raise ImportError("pip install matplotlib")

def pillow():
    try:
        from PIL import Image
        return Image
    except ImportError:
        raise ImportError("pip install Pillow")


__all__ = [
    "PythonBridge", "py",
    "os_mod", "sys_mod", "path_mod",
    "pandas", "numpy", "requests", "matplotlib", "pillow",
]
