# Building a Standalone Executable — urdu.exe بنانا

This guide explains how to compile the Urdu Programming Language into a standalone `urdu.exe` executable using **Nuitka**. The resulting executable runs on any Windows machine without requiring Python to be installed.

> **اردو:** یہ رہنما بتاتا ہے کہ **Nuitka** سے اردو پروگرامنگ زبان کو ایک خودکفیل `urdu.exe` قابل عمل میں کیسے مرتب کریں۔ نتیجتاً قابل عمل Python نصب کیے بغیر کسی بھی Windows مشین پر چلتی ہے۔

---

## Overview — جائزہ

The build system uses [Nuitka](https://nuitka.net/) to compile the Python interpreter and all bundled runtime libraries into a self-contained Windows executable. The process:

1. Nuitka analyses the `urdu` package and all included pip packages.
2. It compiles everything to C, then links a native Windows binary.
3. The output is a `dist/__main__.dist/` folder containing `urdu.exe` and all required DLLs.

> **اردو:** تعمیراتی نظام [Nuitka](https://nuitka.net/) استعمال کرتا ہے جو Python تفسیر کار اور تمام بنڈل رن ٹائم لائبریریاں ایک خودکفیل Windows قابل عمل میں مرتب کرتا ہے۔

**Output size:** approximately 600 MB for the full standalone build (including web frameworks, databases, ML libraries, and cryptography). A fast build (core + web only) is roughly 250–350 MB.

**Build time:**
- Full build: 20–60 minutes on a modern machine.
- Fast build (core + web): 10–20 minutes.
- Adding TensorFlow (`--with-tf`): adds ~30 minutes and ~1.1 GB to the output.

> **اردو:** آؤٹ پٹ کا سائز: مکمل خودکفیل تعمیر کے لیے تقریباً 600 MB۔ تیز تعمیر (صرف مرکز + ویب) تقریباً 250-350 MB ہے۔

---

## Requirements — ضروریات

### System — نظام

> **اردو:** نظامی ضروریات: Windows 10/11 (64 بٹ)، کم از کم 4 GB RAM، 5 GB خالی ڈسک جگہ، اور Visual Studio Build Tools۔

- Windows 10 or Windows 11 (64-bit)
- At least 4 GB RAM (8 GB recommended)
- At least 5 GB free disk space
- A C compiler: install **Visual Studio Build Tools** (free) or full Visual Studio.
  - Download: [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - Select workload: **"Desktop development with C++"**

### Python environment — Python ماحول

> **Important:** Use a clean virtual environment — **not** Anaconda base. Anaconda includes hundreds of extra packages (scipy, matplotlib, IPython, Jupyter, etc.) that Nuitka will include even if you do not use them, inflating build time from ~1 hour to 6+ hours and doubling the output size.

> **اردو:** **اہم:** صاف ورچوئل ماحول استعمال کریں — Anaconda بیس نہیں۔ Anaconda میں سینکڑوں اضافی پیکیج ہوتے ہیں جو Nuitka شامل کر لیتا ہے اور تعمیراتی وقت 1 گھنٹے سے 6+ گھنٹے تک بڑھ جاتا ہے۔

The project ships a pre-configured `build_env/` virtual environment in the repository for convenience. If it does not exist or you prefer to create your own, follow the steps below.

---

## Step-by-Step Build Instructions — قدم بہ قدم تعمیری ہدایات

### Step 1 — Create a clean virtual environment — مرحلہ ۱ — صاف ورچوئل ماحول بنائیں

Open a terminal in the project root folder:

```
python -m venv build_env
```

### Step 2 — Activate the virtual environment — مرحلہ ۲ — ورچوئل ماحول فعال کریں

**Windows (PowerShell):**
```powershell
build_env\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```
build_env\Scripts\activate.bat
```

Your prompt should now show `(build_env)` at the beginning.

> **اردو:** آپ کی پرامپٹ اب شروع میں `(build_env)` دکھائے گی۔

### Step 3 — Install required packages — مرحلہ ۳ — درکار پیکیج نصب کریں

Install Nuitka and all the runtime packages you want to bundle:

> **اردو:** Nuitka اور تمام رن ٹائم پیکیج نصب کریں جو آپ بنڈل کرنا چاہتے ہیں۔

```
pip install nuitka

# Core
pip install -e .

# Web frameworks
pip install fastapi flask django uvicorn websockets python-socketio python-multipart
pip install httpx aiohttp requests pydantic

# Cryptography
pip install cryptography bcrypt python-jose[cryptography]

# Databases
pip install sqlalchemy pymysql psycopg2-binary aiosqlite pymongo

# Machine learning (skip if not needed — saves ~30 min build time)
pip install numpy pandas scikit-learn scipy

# Scraping and files
pip install beautifulsoup4 lxml openpyxl

# Logging
pip install colorlog
```

> You do not need to install all packages. The build script (`build.py`) automatically detects which packages are installed and includes only those. Packages that are not installed are listed as "skipped" in the build summary and will not be available in the compiled executable.

> **اردو:** تمام پیکیج نصب کرنا ضروری نہیں۔ تعمیری اسکرپٹ خودکار طور پر نصب شدہ پیکیج پہچانتا اور صرف انہی کو شامل کرتا ہے۔

### Step 4 — Run the build script — مرحلہ ۴ — تعمیری اسکرپٹ چلائیں

```
python build.py
```

The build script will:
1. Check which packages are installed.
2. Print a summary of what will be included and what will be skipped.
3. Invoke Nuitka with the correct flags.
4. Report success and the output path when complete.

> **اردو:** تعمیری اسکرپٹ نصب شدہ پیکیج جانچے گا، خلاصہ پیش کرے گا، Nuitka چلائے گا، اور مکمل ہونے پر نتیجہ رپورٹ کرے گا۔

---

## Build Modes — تعمیری طریقے

### Default — Full standalone build — ڈیفالٹ — مکمل خودکفیل تعمیر

```
python build.py
```

Includes: core interpreter, web frameworks, databases, ML (excluding TensorFlow), cryptography, scraping, file I/O, threading, date/time, logging.

Output: `dist\__main__.dist\urdu.exe`

### `--fast` — Core + Web only — تیز — صرف مرکز + ویب

```
python build.py --fast
```

Skips database and ML packages. Faster to build, smaller output. Ideal for web application deployments.

Output: `dist\__main__.dist\urdu.exe` (~250 MB)

### `--onefile` — Single executable file — یک فائل قابل عمل

```
python build.py --onefile
```

Packages everything into a single `urdu.exe` file (using a self-extracting archive). Startup is slower because the archive is unpacked into a temp folder on first run, but distribution is a single file.

Output: `dist\urdu.exe` (single file)

> **اردو:** سب کچھ ایک `urdu.exe` فائل میں بند کرتا ہے۔ پہلی بار چلانے پر سست ہوتا ہے مگر تقسیم ایک فائل سے ہوتی ہے۔

### `--with-tf` — Include TensorFlow — TensorFlow شامل کریں

```
python build.py --with-tf
```

Also bundles TensorFlow, Keras, and TensorBoard. Adds approximately 1.1 GB and 30 minutes to the build.

**Requires:** `pip install tensorflow` before running the build.

### `--check` — Dry run (print Nuitka command only) — جانچ — صرف Nuitka حکم پرنٹ کریں

```
python build.py --check
python build.py --fast --check
python build.py --onefile --with-tf --check
```

Prints the full Nuitka command that would be executed, without actually running it. Useful for inspecting or customising the command.

> **اردو:** چلائے بغیر Nuitka حکم پرنٹ کرتا ہے — معائنے یا تبدیلی کے لیے مفید۔

### Combining flags — جھنڈے ملائیں

```
python build.py --fast --onefile
python build.py --with-tf --onefile
```

---

## Output Structure — آؤٹ پٹ کی ساخت

After a successful standalone build:

> **اردو:** کامیاب خودکفیل تعمیر کے بعد آؤٹ پٹ کی ساخت۔

```
dist\
  __main__.dist\
    urdu.exe              ← main executable (run this)
    python311.dll         ← embedded CPython runtime
    _asyncio.pyd          ┐
    _ctypes.pyd           │ compiled Python extension modules
    _decimal.pyd          ┘
    fastapi\              ┐
    flask\                │ bundled pip packages (as compiled modules)
    django\               ┘
    ...                   ← ~600 MB total
```

After a `--onefile` build:

```
dist\
  urdu.exe                ← single self-extracting executable
```

---

## Using the Built Executable — تیار شدہ قابل عمل استعمال کرنا

From the `dist\__main__.dist\` folder:

```
urdu.exe run myprogram.urdu
urdu.exe repl
urdu.exe version
urdu.exe مدد
urdu.exe compile myfile.urdu
```

Or add `dist\__main__.dist\` to your system PATH so you can type `urdu` from anywhere.

> **اردو:** `dist\__main__.dist\` فولڈر کو PATH میں شامل کریں تاکہ `urdu` کہیں سے بھی ٹائپ کر سکیں۔

---

## Distribution — تقسیم

To distribute the compiled executable:

> **اردو:** تیار شدہ قابل عمل تقسیم کرنے کے لیے۔

1. Copy the **entire `dist\__main__.dist\` folder** to the target machine.
2. No Python installation is required on the target machine.
3. The target machine must be Windows 64-bit (same architecture as the build machine).
4. The Visual C++ runtime (`vcruntime140.dll`) is included automatically by Nuitka.

For GitHub releases, zip the `__main__.dist` folder and attach it as a release asset.

---

## build.py Options Reference — build.py اختیارات کا حوالہ

| Flag | Description | Default |
|---|---|---|
| *(none)* | Full standalone build with all detected packages | — |
| `--fast` | Skip database and ML packages | False |
| `--onefile` | Single self-extracting .exe instead of folder | False |
| `--with-tf` | Include TensorFlow (+1.1 GB, +~30 min) | False |
| `--check` | Dry run — print the Nuitka command, do not build | False |

### Nuitka flags used internally — اندرونی طور پر استعمال شدہ Nuitka جھنڈے

| Nuitka flag | Purpose |
|---|---|
| `--standalone` | Self-contained folder with all DLLs |
| `--onefile` | Alternate: single file with embedded archive |
| `--output-dir=dist` | Place output in `dist/` |
| `--output-filename=urdu.exe` | Name the executable `urdu.exe` |
| `--windows-console-mode=attach` | Attach to existing console (no new window) |
| `--lto=no` | Disable link-time optimisation (faster build) |
| `--jobs=4` | Parallel C compilation with 4 threads |
| `--enable-plugins=no-qt` | Do not bundle Qt bindings |
| `--include-package=<pkg>` | Explicitly include each detected package |
| `--python-flag=-m` | Run as `python -m urdu` |

---

## Troubleshooting — مسائل کا حل

> **اردو:** عام مسائل اور ان کے حل۔

| Problem | Solution |
|---|---|
| `nuitka: command not found` | Activate the virtual environment first |
| Build fails after 1–2 minutes | Ensure Visual Studio Build Tools are installed with the C++ workload |
| Build takes 6+ hours | You are building from Anaconda base — create a clean `venv` instead |
| `urdu.exe` crashes on another machine | Ensure the target machine is 64-bit Windows; check that the full `__main__.dist` folder was copied |
| Missing library at runtime | The package was not installed when `build.py` ran — install it, then rebuild |
| TensorFlow not found | Run `pip install tensorflow` inside the build venv first |
| Low disk space error | Nuitka needs ~3 GB working space during the build |

---

## Quick Reference — فوری حوالہ

> **اردو:** تعمیر کی فوری یاد دہانی۔

```
# One-time setup
python -m venv build_env
build_env\Scripts\Activate.ps1
pip install -e . nuitka fastapi flask django uvicorn cryptography ...

# Build
python build.py              # full build  → dist\__main__.dist\urdu.exe
python build.py --fast       # quick build → dist\__main__.dist\urdu.exe
python build.py --onefile    # single file → dist\urdu.exe
python build.py --check      # dry run, no compilation

# Run the result
dist\__main__.dist\urdu.exe run hello.urdu
```

---

*Previous: [Quick Start](quick-start.md) | Next: [Contributing →](contributing.md)*
