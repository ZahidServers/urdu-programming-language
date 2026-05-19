"""Urdu package installer — wraps pip with Urdu package name resolution."""

from __future__ import annotations
import sys
import subprocess

# Urdu module aliases → pip packages
URDU_PACKAGE_MAP: dict[str, list[str]] = {
    "اردو/ذہین":      ["tensorflow", "scikit-learn", "pandas", "numpy", "llama-cpp-python"],
    "اردو/ویب":       ["fastapi", "flask", "django", "uvicorn", "python-multipart", "python-socketio", "websockets"],
    "اردو/رمز":       ["cryptography", "bcrypt", "python-jose[cryptography]"],
    "اردو/ڈیٹا_بیس": ["sqlalchemy", "pymysql", "psycopg2-binary", "aiosqlite"],
    "اردو/سوکٹ":      ["python-socketio", "websockets"],
    "اردو/لاگ":       ["colorlog"],
    "اردو/دھاگہ":     [],   # stdlib only
    "اردو/تاریخ":     [],   # stdlib only (datetime, time)
    "اردو/کرل":       ["requests", "httpx", "aiohttp", "pycurl"],
    "اردو/کھرچنی":    ["beautifulsoup4", "lxml"],
    "اردو/فائلیں":    ["openpyxl", "xlrd"],   # zipfile is stdlib
}


def install_packages(packages: list[str]) -> int:
    resolved: list[str] = []

    for pkg in packages:
        if pkg in URDU_PACKAGE_MAP:
            pip_pkgs = URDU_PACKAGE_MAP[pkg]
            if pip_pkgs:
                print(f"  📦 {pkg}  →  {', '.join(pip_pkgs)}")
                resolved.extend(pip_pkgs)
            else:
                print(f"  ✓ {pkg} — stdlib (کوئی نصب درکار نہیں)")
        else:
            resolved.append(pkg)

    if not resolved:
        return 0

    print(f"\n  نصب کر رہے ہیں: {' '.join(resolved)}\n")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install"] + resolved,
        check=False,
    )
    if result.returncode == 0:
        print(f"\n  ✓ نصب مکمل")
    else:
        print(f"\n  ✗ نصب ناکام (exit {result.returncode})", file=sys.stderr)
    return result.returncode
