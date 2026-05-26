"""
اردو پروگرامنگ لینگویج — Nuitka Build Script
Urdu Programming Language — Standalone Executable Builder

Output: dist/__main__.dist/urdu.exe  (portable, no Python needed)

Usage:
    python build.py               -- full standalone build
    python build.py --fast        -- core + web only (quick test build)
    python build.py --onefile     -- single urdu.exe (slower startup)
    python build.py --with-tf     -- also bundle TensorFlow (adds ~1.1 GB)
    python build.py --check       -- dry run, print command only
"""

from __future__ import annotations
import sys
import io
import shutil
import subprocess
import importlib
import argparse
from pathlib import Path

HERE = Path(__file__).parent

# ─── Post-build paths (edit if yours differ) ─────────────────────────────────

ICO          = HERE / "URDU_ICO.ico"
ANACONDA_BIN = Path(r"C:\ProgramData\anaconda3\Library\bin")
VCRUNTIME    = Path(r"C:\Windows\System32\vcruntime140_threads.dll")


# ─── Fix stdout for Urdu output on Windows ───────────────────────────────────

def _fix_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


# ─── Package lists ────────────────────────────────────────────────────────────
# Map: import_name -> human label (for reporting)

CORE = {
    "urdu": "Urdu interpreter",
}

WEB = {
    "flask":         "Flask",
    "werkzeug":      "Werkzeug",
    "jinja2":        "Jinja2",
    "itsdangerous":  "itsdangerous",
    "click":         "Click",
    "fastapi":       "FastAPI",
    "starlette":     "Starlette",
    "uvicorn":       "Uvicorn",
    "anyio":         "AnyIO",
    "h11":           "h11",
    "django":        "Django",
    "websockets":    "WebSockets",
    "socketio":      "Socket.IO",      # optional — python-socketio
    "engineio":      "Engine.IO",      # optional — python-engineio
    "httpx":         "HTTPX",
    "httpcore":      "HTTPCore",
    "aiohttp":       "aiohttp",
    "aiosignal":     "aiosignal",
    "frozenlist":    "frozenlist",
    "multidict":     "multidict",
    "yarl":          "yarl",
    "jose":          "python-jose",    # optional
    "pydantic":      "Pydantic",
    "multipart":     "python-multipart",
}

HTTP = {
    "requests":           "Requests",
    "pycurl":             "pycurl",
    "certifi":            "certifi",
    "charset_normalizer": "charset-normalizer",
    "idna":               "idna",
    "urllib3":            "urllib3",
}

SCRAPING = {
    "bs4":  "BeautifulSoup4",
    "lxml": "lxml",
}

FILES = {
    "openpyxl": "openpyxl",
    "xlrd":     "xlrd",     # optional — not always installed
}

DB = {
    "psycopg2":       "psycopg2 (PostgreSQL)",
    "pymysql":        "PyMySQL",               # optional
    "pymongo":        "PyMongo",
    "firebase_admin": "Firebase Admin",         # optional
    "cassandra":      "Cassandra Driver",       # optional
    "google.auth":    "google-auth",
    "aiosqlite":      "aiosqlite",
}

CRYPTO = {
    "cryptography": "cryptography",
    "Crypto":       "PyCryptodome",            # installed as Crypto
}

ML = {
    "numpy":          "NumPy",
    "pandas":         "Pandas",
    "sklearn":        "scikit-learn",
    "scipy":          "SciPy",
    "joblib":         "joblib",
    "threadpoolctl":  "threadpoolctl",
    "llama_cpp":      "llama-cpp-python",
    "torch":          "PyTorch",
    "matplotlib":     "matplotlib",
    "PIL":            "Pillow",
}

TF = {
    "tensorflow":    "TensorFlow",
    "keras":         "Keras",
    "tensorboard":   "TensorBoard",
    "google.protobuf": "protobuf",
    "absl":          "absl-py",
    "h5py":          "h5py",
    "opt_einsum":    "opt-einsum",
    "wrapt":         "wrapt",
    "termcolor":     "termcolor",
    "flatbuffers":   "flatbuffers",
    "astunparse":    "astunparse",
    "gast":          "gast",
}


# ─── Availability check ───────────────────────────────────────────────────────

def _available(pkg: str) -> bool:
    """Check if an import name is importable."""
    # Handle dotted names (google.auth → google)
    top = pkg.split(".")[0]
    try:
        importlib.import_module(top)
        return True
    except ImportError:
        return False


def _filter(pkg_dict: dict) -> tuple[list[str], list[tuple[str, str]]]:
    """Return (available_import_names, skipped_[(name, label)] )."""
    ok, skip = [], []
    for imp, label in pkg_dict.items():
        if _available(imp):
            ok.append(imp)
        else:
            skip.append((imp, label))
    return ok, skip


# ─── Post-build steps ────────────────────────────────────────────────────────

def _post_build(exe: Path, standalone: bool) -> None:
    """Copy DLLs that Nuitka missed into the dist folder."""
    dist_folder = exe.parent

    if not standalone:
        return

    # 1. All Anaconda Library/bin DLLs Nuitka may have missed
    if ANACONDA_BIN.is_dir():
        copied = 0
        for dll in ANACONDA_BIN.glob("*.dll"):
            dest = dist_folder / dll.name
            if not dest.exists():
                shutil.copy2(dll, dest)
                copied += 1
        print(f"  Anaconda DLLs کاپی    : {copied} نئی فائلیں")
    else:
        print(f"  ⚠ Anaconda bin نہیں ملا: {ANACONDA_BIN}")

    # 2. vcruntime140_threads.dll from System32
    if VCRUNTIME.exists():
        shutil.copy2(VCRUNTIME, dist_folder / VCRUNTIME.name)
        print(f"  vcruntime140_threads  : کاپی ✓")
    else:
        print(f"  ⚠ vcruntime140_threads.dll نہیں ملا: {VCRUNTIME}")


# ─── Build ────────────────────────────────────────────────────────────────────

def build(fast: bool = False, onefile: bool = False,
          check: bool = False, include_tf: bool = False) -> int:
    _fix_stdout()

    dist_dir = HERE / "dist"
    dist_dir.mkdir(exist_ok=True)

    # Collect packages, skipping anything not installed
    all_pkgs: list[str] = []
    skipped: list[tuple[str, str]] = []

    groups = [CORE, WEB, HTTP, SCRAPING, FILES, CRYPTO]
    if not fast:
        groups += [DB, ML]
    if include_tf:
        groups += [TF]

    for g in groups:
        ok, sk = _filter(g)
        all_pkgs.extend(ok)
        skipped.extend(sk)

    # Build command
    cmd = [
        sys.executable, "-m", "nuitka",
        "--onefile" if onefile else "--standalone",
        "--assume-yes-for-downloads",
        "--output-dir=dist",
        "--output-filename=urdu.exe",
        "--windows-console-mode=attach",
        # icon + version branding (embedded by Nuitka at compile time)
        f"--windows-icon-from-ico={ICO}",
        "--windows-file-version=1.0.0.0",
        "--windows-product-version=1.0.0.0",
        "--windows-file-description=Urdu Programming Language Runtime Engine",
        "--windows-company-name=Webaon",
        "--windows-product-name=Urdu",
        "--copyright=© 2026 Webaon. All rights reserved.",
        "--lto=no",
        "--jobs=4",
        "--noinclude-unittest-mode=nofollow",
        "--noinclude-setuptools-mode=nofollow",
        "--noinclude-numba-mode=nofollow",
        "--module-parameter=torch-disable-jit=yes",
        "--module-parameter=numba-disable-jit=yes",
        "--module-parameter=django-settings-module=_build_settings",
        # disable Qt bindings — we use no Qt
        "--enable-plugins=no-qt",
        # torch anti-bloat: skip testing internals (Python 3.12 syntax) and
        # disable anti-bloat plugin to avoid DLL init failure on Windows when
        # the plugin evaluates torch.utils._config_module at compile time
        "--nofollow-import-to=torch.testing._internal",
        "--nofollow-import-to=django.core.management",
        "--disable-plugin=anti-bloat",
        "--include-package=ctypes",
        "--include-module=_ctypes",
        # ffi.dll is _ctypes.pyd's libffi dependency; Nuitka misses it because
        # Anaconda keeps it in Library/bin rather than DLLs/
        r"--include-data-file=C:\ProgramData\anaconda3\Library\bin\ffi.dll=ffi.dll",
        # sqlite3.dll is _sqlite3.pyd's dependency; same Anaconda Library/bin pattern
        r"--include-data-file=C:\ProgramData\anaconda3\Library\bin\sqlite3.dll=sqlite3.dll",
        "--include-module=ssl",
        "--include-module=hashlib",
        *[f"--include-package={p}" for p in all_pkgs],
        "--python-flag=-m",
        "urdu",
    ]

    # ─── Print summary ────────────────────────────────────────────────────────
    print("╔══════════════════════════════════════════════╗")
    print("║   اردو پروگرامنگ لینگویج — Nuitka Build     ║")
    print("╚══════════════════════════════════════════════╝")
    print()
    print(f"  موڈ      : {'onefile' if onefile else 'standalone'}")
    print(f"  تیز موڈ  : {'ہاں' if fast else 'نہیں'}")
    print(f"  TF شامل  : {'ہاں' if include_tf else 'نہیں'}")
    print(f"  پیکجز    : {len(all_pkgs)}")
    print()

    if skipped:
        print("  چھوڑے گئے (نصب نہیں):")
        for imp, label in skipped:
            print(f"    - {label} ({imp})")
        print()

    if check:
        print("  [DRY RUN] کمانڈ:")
        print("  " + " \\\n    ".join(str(c) for c in cmd))
        return 0

    print("  بناوٹ شروع... (20-60 منٹ لگ سکتے ہیں)")
    print()

    result = subprocess.run(cmd, cwd=HERE)

    print()
    if result.returncode == 0:
        # Find the output exe
        candidates = list(dist_dir.rglob("urdu.exe"))
        exe = candidates[0] if candidates else None

        print("╔══════════════════════════════════════════════╗")
        print("║   بناوٹ مکمل ✓                               ║")
        print("╚══════════════════════════════════════════════╝")

        if exe:
            if onefile:
                print(f"  exe     : {exe}")
                print(f"  سائز    : {exe.stat().st_size / 1_048_576:.0f} MB")
            else:
                folder = exe.parent
                total = sum(f.stat().st_size for f in folder.rglob("*") if f.is_file())
                print(f"  فولڈر   : {folder}")
                print(f"  کل سائز : {total / 1_048_576:.0f} MB")
                print(f"  exe     : {exe}")

            print()
            print("  بعد از بناوٹ...")
            _post_build(exe, standalone=not onefile)

        print()
        print("  استعمال:")
        print("    urdu.exe run my_program.urdu")
        print("    urdu.exe مدد")
        print("    urdu.exe repl")
        if skipped:
            print()
            print("  اختیاری نصب:")
            for imp, label in skipped:
                print(f"    pip install {label.split()[0].lower()}")
    else:
        print(f"  ✗ بناوٹ ناکام (exit code: {result.returncode})")
        print("  لاگ دیکھیں: dist/urdu.exe.build/")

    return result.returncode


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main() -> None:
    p = argparse.ArgumentParser(description="اردو پروگرامنگ لینگویج — Nuitka بناوٹ")
    p.add_argument("--fast",    action="store_true", help="صرف core + web (بغیر ML/DB)")
    p.add_argument("--onefile", action="store_true", help="ایک فائل exe")
    p.add_argument("--with-tf", action="store_true", dest="with_tf",
                   help="TensorFlow بھی شامل کریں (+1.1 GB, +30 منٹ)")
    p.add_argument("--check",   action="store_true", help="صرف کمانڈ دکھائیں")
    args = p.parse_args()
    sys.exit(build(fast=args.fast, onefile=args.onefile,
                   check=args.check, include_tf=args.with_tf))


if __name__ == "__main__":
    main()
