# Installation Guide — نصب کرنے کا طریقہ

This guide walks you through every step needed to run Urdu Programming Language programs on your machine.

> **اردو:** یہ رہنما آپ کو اپنے کمپیوٹر پر اردو پروگرامنگ زبان نصب (install) کرنے کے تمام مراحل سے گزارتا ہے۔

---

## Option 1 — Pre-built Executable (Recommended, No Python Required) — پہلے سے تیار قابل عمل (تجویز کردہ)

The easiest way to use the Urdu Programming Language is to download the pre-built Windows executable from GitHub Releases. **No Python installation needed.**

> **اردو:** اردو پروگرامنگ زبان استعمال کرنے کا آسان ترین طریقہ GitHub ریلیزز سے پہلے سے تیار Windows قابل عمل ڈاؤن لوڈ کرنا ہے۔ **Python نصب کرنے کی ضرورت نہیں۔**

### Steps — اقدامات

1. Go to the **[GitHub Releases page](https://github.com/ZahidServers/urdu-programming-language/releases)**
2. Download the latest release: `urdu-windows-vX.X.X.zip`
3. Extract the ZIP file — you will get a folder called `urdu.dist`
4. Inside the folder is `urdu.exe`

### Usage — استعمال

Open a terminal (PowerShell or Windows Terminal) in the `urdu.dist` folder:

```powershell
# Run a .urdu file
.\urdu.exe run myprogram.urdu

# Open the interactive REPL
.\urdu.exe repl

# Show help
.\urdu.exe مدد

# Show version
.\urdu.exe نسخہ
```

You can also add the folder to your system `PATH` so you can run `urdu.exe` from anywhere:

```powershell
# Add to PATH permanently (run in PowerShell as Administrator)
$env:PATH += ";C:\path\to\urdu.dist"
[Environment]::SetEnvironmentVariable("PATH", $env:PATH, "Machine")
```

> **Note:** The Windows executable is ~600 MB as a standalone folder because it includes the Python runtime and all libraries. It runs on any Windows 10/11 machine without any additional installation.

> **اردو:** Windows قابل عمل فائل تقریباً 600 MB کی ایک خودکفیل فولڈر ہے کیونکہ اس میں Python رن ٹائم اور تمام لائبریریاں شامل ہیں۔ یہ کسی بھی اضافی نصب کاری کے بغیر Windows 10/11 پر چلتی ہے۔

> **Linux/macOS:** Pre-built executables for Linux and macOS are planned for future releases. For now, use Option 2 (from source).

---

## Option 2 — From Source (Python Required) — ماخذ سے (Python درکار)

> **اردو:** اگر آپ ماخذ کوڈ سے نصب کرنا چاہتے ہیں تو Python 3.8 یا جدید درکار ہے۔

---

## System Requirements — نظام کی ضروریات

> **اردو:** اردو پروگرامنگ زبان چلانے کے لیے کم از کم اور تجویز کردہ تقاضے۔

| Requirement | Minimum | Recommended |
|---|---|---|
| **Python** | 3.8 | 3.11 or 3.12 |
| **Operating System** | Windows 10 / Ubuntu 20.04 / macOS 11 | Windows 11 / Ubuntu 22.04 / macOS 14 |
| **RAM** | 256 MB | 1 GB+ |
| **Disk space** | 50 MB (core only) | 2 GB (with all optional libraries) |
| **Terminal encoding** | UTF-8 | UTF-8 |

> **Note on Windows:** Windows Terminal and PowerShell 7 both support UTF-8 natively. The older Command Prompt (`cmd.exe`) may display Urdu script incorrectly — use Windows Terminal for the best experience.

> **اردو:** Windows Terminal اور PowerShell 7 UTF-8 کو فطری طور پر سپورٹ کرتے ہیں۔ بہترین تجربے کے لیے Windows Terminal استعمال کریں۔

---

## Step 1 — Install Python — مرحلہ ۱ — Python نصب کریں

If Python 3.8 or newer is not already installed:

> **اردو:** اگر Python 3.8 یا جدید نصب نہیں ہے تو درج ذیل اقدامات کریں۔

### Windows
1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the latest Python 3.x installer.
3. Run the installer. **Check the box "Add Python to PATH"** before clicking Install.
4. Verify the install:
   ```
   python --version
   ```

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### macOS
```bash
brew install python
```

---

## Step 2 — Get the Urdu Programming Language — مرحلہ ۲ — اردو پروگرامنگ زبان حاصل کریں

### Option A — Clone from GitHub (recommended)
```
git clone https://github.com/ZahidServers/urdu-programming-language.git
cd urdu-programming-language
```

### Option B — Download a ZIP release
1. Go to the GitHub Releases page.
2. Download the latest `Source code (zip)`.
3. Extract it and open the extracted folder in your terminal.

---

## Step 3 — Install (editable / development mode) — مرحلہ ۳ — نصب کریں

From inside the project folder:

```
pip install -e .
```

This makes `python -m urdu` available anywhere on your system. No further configuration is required for basic usage.

> **اردو:** یہ `python -m urdu` کو آپ کے نظام میں ہر جگہ دستیاب کرتا ہے۔ بنیادی استعمال کے لیے مزید ترتیب درکار نہیں۔

---

## Step 4 — Verify the Installation — مرحلہ ۴ — نصب کاری تصدیق کریں

Create a file called `hello.urdu` with this single line:

> **اردو:** `hello.urdu` نام کی فائل بنائیں اور اس ایک سطر سے نصب کاری جانچیں۔

```urdu
لکھو("السلام علیکم، دنیا!")
```

Run it:

```
python -m urdu run hello.urdu
```

Expected output:

```
السلام علیکم، دنیا!
```

If you see that output, the installation is complete and working.

> **اردو:** اگر یہ آؤٹ پٹ نظر آئے تو نصب کاری مکمل اور کار آمد ہے۔

---

## CLI Commands Reference — CLI احکام کا حوالہ

The Urdu Programming Language ships with a full command-line interface. All commands are invoked as:

> **اردو:** اردو پروگرامنگ زبان مکمل کمانڈ لائن انٹرفیس کے ساتھ آتی ہے۔ تمام احکام اس طرح چلائیں۔

```
python -m urdu <command> [arguments]
```

### `run` — Run a .urdu file — فائل چلائیں

```
python -m urdu run myfile.urdu
python -m urdu run myfile.urdu -- arg1 arg2   # pass arguments to the program
python -m urdu run myfile.urdu --show-python  # also print the generated Python
python -m urdu run myfile.urdu --debug        # print lexer tokens
```

### `compile` — Transpile to Python without running — Python میں تبدیل کریں

```
python -m urdu compile myfile.urdu
python -m urdu compile myfile.urdu -o output.py
```

Writes a `.py` file containing the generated Python source. Useful for debugging or deployment.

> **اردو:** ایک `.py` فائل لکھتا ہے جس میں تیار کردہ Python ماخذ ہوتا ہے۔ ڈیبگ یا تعیناتی کے لیے مفید ہے۔

### `repl` — Interactive REPL — تعاملی REPL

```
python -m urdu repl
```

Starts an interactive Read-Eval-Print Loop where you can type Urdu code line by line and see results immediately. Exit with `خروج()` or Ctrl+D.

> **اردو:** تعاملی ریڈ-ایول-پرنٹ لوپ شروع ہوتا ہے جہاں آپ اردو کوڈ سطر بہ سطر لکھ کر فوری نتائج دیکھ سکتے ہیں۔ `خروج()` یا Ctrl+D سے باہر نکلیں۔

```
اردو> متغیر x = 10
اردو> لکھو(x * 2)
20
اردو> فنکشن مربع(n): واپس n ** 2
اردو> لکھو(مربع(5))
25
```

### `مدد` — Help (in Urdu) — مدد اردو میں

```
python -m urdu مدد
python -m urdu مدد زبان
python -m urdu مدد فلاسک
python -m urdu مدد متغیر
```

Displays help topics in Urdu. Pass a topic name to get focused help on that subject.

### `نسخہ` / `version` — Show version information — نسخہ دکھائیں

```
python -m urdu version
```

Output:

```
════════════════════════════════════════════════════════
  Urdu Programming Language
  (Urdu: اردو پروگرامنگ لینگویج)
════════════════════════════════════════════════════════
  Version   : 1.0.0
  Developer : Mohammed Zahid Wadiwale
  Released  : 2026-05-16
  Platform  : Windows | Linux | macOS
  Features  : OOP | Async | GUI | ML | DB | Web | Threads
  License   : MIT
════════════════════════════════════════════════════════
```

### `نصب` — Install optional library dependencies — اختیاری لائبریریاں نصب کریں

```
python -m urdu نصب "اردو/ویب"
python -m urdu نصب "اردو/ذہین"
python -m urdu نصب "اردو/ڈیٹا_بیس"
python -m urdu نصب "اردو/رمز"
```

This command resolves the Urdu library name to the correct pip packages and installs them. For example, `اردو/ویب` installs FastAPI, Flask, Django, uvicorn, websockets, python-socketio, and related dependencies automatically.

> **اردو:** یہ حکم اردو لائبریری (library) کا نام درست pip پیکیجوں میں تبدیل کر کے انہیں نصب کرتا ہے۔

### `check` — Syntax check without running — چلائے بغیر نحوی جانچ

```
python -m urdu check myfile.urdu
```

Parses the file and reports any syntax errors without executing it. Useful in CI pipelines and editors.

> **اردو:** فائل کو پارس کرتا ہے اور چلائے بغیر نحوی غلطیاں رپورٹ کرتا ہے۔

---

## Optional Library Dependencies — اختیاری لائبریری انحصار

The core interpreter has **no pip dependencies** beyond Python itself. Libraries are optional and installed on demand:

> **اردو:** مرکزی تفسیر کار Python کے علاوہ کوئی pip انحصار نہیں رکھتا۔ لائبریریاں (libraries) اختیاری ہیں اور ضرورت پر نصب کی جاتی ہیں۔

| Library module | Install command | Pip packages installed |
|---|---|---|
| `اردو/ویب` | `python -m urdu نصب "اردو/ویب"` | fastapi, flask, django, uvicorn, websockets, python-socketio |
| `اردو/ذہین` | `python -m urdu نصب "اردو/ذہین"` | tensorflow, scikit-learn, pandas, numpy, llama-cpp-python |
| `اردو/ڈیٹا_بیس` | `python -m urdu نصب "اردو/ڈیٹا_بیس"` | sqlalchemy, pymysql, psycopg2-binary, aiosqlite |
| `اردو/رمز` | `python -m urdu نصب "اردو/رمز"` | cryptography, bcrypt, python-jose |
| `اردو/کرل` | `python -m urdu نصب "اردو/کرل"` | requests, httpx, aiohttp, pycurl |
| `اردو/کھرچنی` | `python -m urdu نصب "اردو/کھرچنی"` | beautifulsoup4, lxml |
| `اردو/فائلیں` | `python -m urdu نصب "اردو/فائلیں"` | openpyxl, xlrd |
| `اردو/لاگ` | `python -m urdu نصب "اردو/لاگ"` | colorlog |

You can also install pip packages directly:

```
pip install fastapi uvicorn
pip install tensorflow numpy pandas
```

---

## File Extension — فائل ایکسٹینشن

Urdu source files use the `.urdu` extension:

> **اردو:** اردو ماخذ فائلیں `.urdu` ایکسٹینشن استعمال کرتی ہیں۔ فائل کے نام اردو رسم الخط، لاطینی، یا ملی جلی شکل میں ہو سکتے ہیں۔

```
میرا_پروگرام.urdu
حساب_کتاب.urdu
ویب_سرور.urdu
```

File names themselves can be Urdu script, Latin, or a mix — the file system and interpreter handle all of them correctly.

---

## Using the Standalone Executable (urdu.exe) — خودکفیل قابل عمل استعمال کرنا

For users who do not want to install Python at all, a precompiled standalone executable is available in the GitHub Releases section under the `dist/` folder of each release.

> **اردو:** جو صارفین Python نصب نہیں کرنا چاہتے، ان کے لیے GitHub ریلیزز میں پہلے سے تیار خودکفیل قابل عمل دستیاب ہے۔

### Download — ڈاؤن لوڈ

Download the `urdu-windows-vX.X.X.zip` from the latest GitHub release and extract it.

### Structure — ساخت

```
urdu.dist\
    urdu.exe          ← main executable
    python312.dll     ← embedded Python runtime
    ...               ← all bundled packages (web, database, ML, crypto, etc.)
```

### Run — چلائیں

```
urdu.dist\urdu.exe run hello.urdu
urdu.dist\urdu.exe repl
urdu.dist\urdu.exe version
```

### Distribute — تقسیم کریں

Copy the **entire `urdu.dist` folder** to any Windows machine. No Python installation is required on the target machine. The folder is approximately 600 MB when all standard libraries are included.

> **اردو:** پوری `urdu.dist` فولڈر کسی بھی Windows مشین پر کاپی کریں۔ منزل مشین پر Python نصب ہونا ضروری نہیں۔

> See [Building](building.md) if you want to compile the executable yourself from source.

---

## Terminal Encoding (Windows) — ٹرمینل انکوڈنگ (Windows)

For the best experience on Windows, set your terminal to UTF-8 before running Urdu programs:

> **اردو:** Windows پر بہترین تجربے کے لیے اردو پروگرام چلانے سے پہلے ٹرمینل کو UTF-8 پر مقرر کریں۔

```powershell
# PowerShell — set once per session
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

Or use **Windows Terminal**, which defaults to UTF-8 and renders Urdu script correctly right-to-left.

---

## Troubleshooting — مسائل کا حل

> **اردو:** عام مسائل اور ان کے حل۔

| Problem | Solution |
|---|---|
| `python` not found | Add Python to PATH during install, or use `python3` |
| Urdu text shows as `???` | Set terminal to UTF-8 (`chcp 65001` on Windows) |
| `ModuleNotFoundError: urdu` | Run `pip install -e .` from the project root |
| `SyntaxError` on Urdu file | Ensure the file is saved as **UTF-8** (not UTF-16 or ANSI) |
| Import error for `fastapi` etc. | Run `python -m urdu نصب "اردو/ویب"` |

---

*Next: [Quick Start →](quick-start.md)*
