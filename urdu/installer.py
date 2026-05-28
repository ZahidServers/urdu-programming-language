"""Urdu package installer — wraps pip with Urdu package name resolution."""

from __future__ import annotations
import sys
import subprocess
import json
import os
from pathlib import Path

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
    "اردو/آردوینو":     ["pyserial", "pyfirmata2"],
    "اردو/ٹینسر_بورڈ": ["tensorboard"],
    "اردو/ڈھانچے":     [],   # stdlib only
    "اردو/الگورتھم":   [],   # stdlib only
    "اردو/متن":        [],   # stdlib only
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


def remove_packages(packages: list[str]) -> int:
    """Uninstall one or more packages (ہٹائیں command)."""
    resolved: list[str] = []
    for pkg in packages:
        if pkg in URDU_PACKAGE_MAP:
            pip_pkgs = URDU_PACKAGE_MAP[pkg]
            if pip_pkgs:
                print(f"  🗑 {pkg}  →  {', '.join(pip_pkgs)}")
                resolved.extend(pip_pkgs)
            else:
                print(f"  ℹ {pkg} — stdlib (ہٹانے کی ضرورت نہیں)")
        else:
            resolved.append(pkg)

    if not resolved:
        return 0

    print(f"\n  ہٹا رہے ہیں: {' '.join(resolved)}\n")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y"] + resolved,
        check=False,
    )
    if result.returncode == 0:
        print(f"\n  ✓ ہٹانا مکمل")
    else:
        print(f"\n  ✗ ہٹانا ناکام (exit {result.returncode})", file=sys.stderr)
    return result.returncode


def list_packages(فلٹر: str = "") -> int:
    """List installed packages (فہرست command)."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=json"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        print(f"  ✗ فہرست حاصل نہیں ہوئی", file=sys.stderr)
        return result.returncode

    pkgs = json.loads(result.stdout)
    if فلٹر:
        pkgs = [p for p in pkgs if فلٹر.lower() in p["name"].lower()]

    print(f"\n  {'نام':<35} {'نسخہ'}")
    print(f"  {'-'*35} {'-'*15}")
    for p in pkgs:
        print(f"  {p['name']:<35} {p['version']}")
    print(f"\n  کل پیکجز: {len(pkgs)}")
    return 0


def update_packages(packages: list[str]) -> int:
    """Upgrade packages to latest (تازہ_کریں command)."""
    resolved: list[str] = []
    for pkg in packages:
        if pkg in URDU_PACKAGE_MAP:
            pip_pkgs = URDU_PACKAGE_MAP[pkg]
            resolved.extend(pip_pkgs) if pip_pkgs else None
        else:
            resolved.append(pkg)

    if not resolved:
        print("  کوئی پیکج نہیں دیا گیا")
        return 1

    print(f"\n  تازہ کر رہے ہیں: {' '.join(resolved)}\n")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade"] + resolved,
        check=False,
    )
    if result.returncode == 0:
        print(f"\n  ✓ تازہ کاری مکمل")
    else:
        print(f"\n  ✗ تازہ کاری ناکام (exit {result.returncode})", file=sys.stderr)
    return result.returncode


def create_venv(نام: str = "ماحول") -> int:
    """Create a virtual environment (ماحول بنائیں command)."""
    import venv
    path = Path(نام)
    if path.exists():
        print(f"  ✗ '{نام}' پہلے سے موجود ہے", file=sys.stderr)
        return 1
    print(f"  ماحول بنا رہے ہیں: {نام} ...")
    venv.create(str(path), with_pip=True)
    if sys.platform == "win32":
        activate = path / "Scripts" / "Activate.ps1"
        activate_cmd = f"  PowerShell:  {activate}"
        activate_bat = path / "Scripts" / "activate.bat"
        activate_cmd2 = f"  CMD:         {activate_bat}"
    else:
        activate = path / "bin" / "activate"
        activate_cmd = f"  source {activate}"
        activate_cmd2 = ""
    print(f"  ✓ ماحول بنا: {path.resolve()}")
    print(f"\n  چالو کرنے کے لیے:")
    print(f"{activate_cmd}")
    if activate_cmd2:
        print(f"{activate_cmd2}")
    return 0


def activate_venv_info(نام: str = "ماحول") -> int:
    """Show how to activate a virtual environment (ماحول چالو command)."""
    path = Path(نام)
    if not path.exists():
        print(f"  ✗ ماحول '{نام}' نہیں ملا — پہلے بنائیں: urdu ماحول بنائیں {نام}",
              file=sys.stderr)
        return 1
    if sys.platform == "win32":
        ps = path / "Scripts" / "Activate.ps1"
        bat = path / "Scripts" / "activate.bat"
        print(f"\n  ماحول چالو کریں:")
        print(f"    PowerShell:  .\\{ps}")
        print(f"    CMD:         {bat}")
    else:
        act = path / "bin" / "activate"
        print(f"\n  ماحول چالو کریں:")
        print(f"    source {act}")
    return 0
