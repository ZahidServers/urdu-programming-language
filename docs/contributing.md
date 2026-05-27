# Contributing Guide — تعاون کا طریقہ

Thank you for your interest in contributing to the Urdu Programming Language. This guide explains how the project is structured and how to add new features — from a single keyword to a complete library module.

> **اردو:** اردو پروگرامنگ زبان میں تعاون کرنے میں آپ کی دلچسپی کا شکریہ۔ یہ رہنما کتابچہ بتاتا ہے کہ منصوبے کی ساخت کیسی ہے اور نئی خصوصیات — ایک کلیدی لفظ سے لے کر مکمل لائبریری ماڈیول تک — کیسے شامل کی جاتی ہیں۔

---

## Code of Conduct — ضابطہ اخلاق

This project is open and welcoming to contributors of all backgrounds. Please be respectful and constructive in all discussions and pull requests.

> **اردو:** یہ منصوبہ ہر پس منظر کے تعاون کاروں کے لیے کھلا اور خیرمقدمی ہے۔ براہ کرم تمام بحثوں اور پل ریکوئسٹوں میں احترام اور تعمیری رویہ اپنائیں۔

---

## How to Fork and Clone — فورک اور کلون کا طریقہ

### 1. Fork the repository — ریپوزیٹری فورک کریں

On GitHub, click the **Fork** button on the repository page. This creates your own copy of the project.

> **اردو:** GitHub پر ریپوزیٹری صفحے پر **Fork** کا بٹن دبائیں۔ اس سے منصوبے کی آپ کی اپنی نقل بن جاتی ہے۔

### 2. Clone your fork — اپنا فورک کلون کریں

```
git clone https://github.com/YOUR-USERNAME/urdu-programming-language.git
cd urdu-programming-language
```

### 3. Add the upstream remote — اپ اسٹریم ریموٹ شامل کریں

```
git remote add upstream https://github.com/zahidwadiwale/urdu-programming-language.git
```

### 4. Set up your development environment — ترقیاتی ماحول ترتیب دیں

```
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
# or: source venv/bin/activate  # Linux / macOS

pip install -e .
pip install fastapi flask django uvicorn requests  # optional — for testing web features
```

---

## Project Structure — منصوبے کی ساخت

```
urdu-programming-language\
│
├── urdu\                      ← main package
│   ├── __init__.py            ← VERSION, DEVELOPER, version_info()
│   ├── __main__.py            ← entry point for `python -m urdu`
│   ├── tokens.py              ← TokenType enum + URDU_KEYWORDS dict
│   ├── lexer.py               ← Lexer: source text → token list
│   ├── ast_nodes.py           ← dataclass nodes for every AST construct
│   ├── parser.py              ← Parser: token list → AST
│   ├── transpiler.py          ← Transpiler: AST → Python source string
│   ├── compiler.py            ← UrduCompiler: orchestrates lex→parse→transpile→exec
│   ├── cli.py                 ← argparse CLI (run / repl / compile / check / نصب / مدد)
│   ├── installer.py           ← `نصب` command: Urdu package name → pip packages
│   ├── error_messages.py      ← Urdu-language error messages
│   │
│   └── runtime\               ← Python modules imported by generated code
│       ├── builtins.py        ← all built-in functions injected into every program
│       ├── web.py             ← FastAPI, Flask, Django, WebSocket, Socket.IO wrappers
│       ├── database.py        ← SQLAlchemy ORM + MongoDB + Firebase wrappers
│       ├── ml.py              ← NumPy, Pandas, scikit-learn, TensorFlow, llama.cpp
│       ├── crypto.py          ← AES, RSA, hashing, JWT wrappers
│       ├── gui.py             ← Tkinter wrappers
│       ├── curl.py            ← HTTP client wrappers (requests, httpx, aiohttp)
│       ├── scraper.py         ← BeautifulSoup4 / lxml web scraping
│       ├── files.py           ← ZIP, Excel, CSV, text file helpers
│       ├── threading_lib.py   ← thread / asyncio task wrappers
│       ├── datetime_lib.py    ← date, time, timedelta helpers
│       ├── logging_lib.py     ← coloured structured logging
│       ├── python_bridge.py   ← passthrough to Python stdlib (اردو/پایتھن)
│       └── help_lib.py        ← content for the `مدد` command
│
├── examples\                  ← example .urdu programs and test files
├── docs\                      ← documentation (you are here)
├── build.py                   ← Nuitka build script
├── setup.py                   ← pip install configuration
└── requirements.txt           ← optional dependency documentation
```

### How a program runs — the pipeline

```
.urdu source
    → Lexer (tokens.py + lexer.py)
    → Parser (parser.py)          builds AST using ast_nodes.py
    → Transpiler (transpiler.py)  emits Python source
    → compiler.py                 calls exec() on the generated Python
                                  with runtime/builtins.py injected as globals
```

When debugging a failure, first check which stage failed:
- A **LexerError** means the Urdu source text could not be tokenised.
- A **ParseError** means the token sequence does not form a valid AST.
- A **TranspilerError** means the AST could not be converted to Python.
- A **Python exception** at runtime means the generated Python failed — inspect the generated `.py` file (use `--show-python`).

> **اردو:** جب کسی ناکامی کو ڈیبگ کریں تو پہلے جانچیں کہ کون سا مرحلہ ناکام ہوا: **LexerError** کا مطلب ہے اردو سورس کو ٹوکن نہیں کیا جا سکا۔ **ParseError** کا مطلب ہے ٹوکن کی ترتیب درست AST نہیں بناتی۔ **TranspilerError** کا مطلب ہے AST کو پائتھن میں تبدیل نہیں کیا جا سکا۔ رن ٹائم پر **Python exception** کا مطلب ہے کہ تیار شدہ پائتھن ناکام رہی۔

---

## Adding New Keywords — نئے کلیدی الفاظ شامل کرنا

Keywords live in two files: `urdu/tokens.py` and `urdu/parser.py`.

> **اردو:** کلیدی الفاظ دو فائلوں میں موجود ہوتے ہیں: `urdu/tokens.py` اور `urdu/parser.py`۔

### Step 1 — Add the TokenType — ٹوکن قسم شامل کریں

Open `urdu/tokens.py`. Add a new entry to the `TokenType` enum in the appropriate section:

```python
# In the TokenType enum:
MY_NEW_KEYWORD = auto()      # میرا_نیا_کلمہ
```

### Step 2 — Register the Urdu word — اردو لفظ رجسٹر کریں

Still in `urdu/tokens.py`, add the mapping to the `URDU_KEYWORDS` dict at the bottom of the file:

```python
URDU_KEYWORDS: dict[str, TokenType] = {
    ...
    "میرا_نیا_کلمہ": TokenType.MY_NEW_KEYWORD,
    ...
}
```

### Step 3 — Parse it — اسے پارس کریں

Open `urdu/parser.py`. Find the method that handles the surrounding construct (statement, expression, declaration). Add a branch to consume your new token and build the correct AST node.

> **اردو:** `urdu/parser.py` کھولیں۔ وہ میتھڈ تلاش کریں جو متعلقہ ساخت (بیان، اظہار، اعلان) کو سنبھالتا ہے۔ نئے ٹوکن کو استعمال کرنے اور درست AST نوڈ بنانے کے لیے ایک شاخ شامل کریں۔

Example — adding a `رک_جاؤ` (pause / sleep) statement:

```python
# in parser.py — _parse_statement():
elif self._check(TokenType.MY_NEW_KEYWORD):
    return self._parse_my_statement()

def _parse_my_statement(self):
    self._expect(TokenType.MY_NEW_KEYWORD)
    expr = self._parse_expression()
    return MyStatementNode(expr=expr, line=self._current_line())
```

### Step 4 — Add an AST node — AST نوڈ شامل کریں

Open `urdu/ast_nodes.py`. Add a dataclass for your new node:

```python
@dataclass
class MyStatementNode:
    expr: ExprNode
    line: int = 0
```

### Step 5 — Transpile it — اسے ٹرانسپائل کریں

Open `urdu/transpiler.py`. Add a visitor method for your new node. The method name must follow the pattern `_visit_<NodeClassName>`:

> **اردو:** `urdu/transpiler.py` کھولیں۔ اپنے نئے نوڈ کے لیے ایک وزیٹر میتھڈ شامل کریں۔ میتھڈ کا نام `_visit_<NodeClassName>` کے نمونے پر ہونا چاہیے۔

```python
def _visit_MyStatementNode(self, node: MyStatementNode):
    expr = self._expr(node.expr)
    self._w(f"import time; time.sleep({expr})")
```

### Step 6 — Test it — اسے آزمائیں

Write a small `.urdu` test file:

```urdu
میرا_نیا_کلمہ 2
لکھو("2 سیکنڈ بعد")
```

Run it:

```
python -m urdu run examples/test_my_keyword.urdu
```

---

## Adding New Built-in Functions — نئے بلٹ-ان فنکشن شامل کرنا

All built-in functions are defined in `urdu/runtime/builtins.py` and injected into every Urdu program's global namespace by `urdu/compiler.py`.

> **اردو:** تمام بلٹ-ان فنکشن `urdu/runtime/builtins.py` میں تعریف کیے گئے ہیں اور `urdu/compiler.py` کے ذریعے ہر اردو پروگرام کی عالمی فضا میں داخل کیے جاتے ہیں۔

### Step 1 — Write the function — فنکشن لکھیں

Open `urdu/runtime/builtins.py` and add your function:

```python
def _میری_فنکشن(قدر):
    """My new built-in: does something useful."""
    return str(قدر).upper()
```

### Step 2 — Export it — اسے برآمد کریں

Find the `_URDU_BUILTINS` dict (or the `globals()` injection at the bottom of the file) and add your function under its Urdu name:

```python
_URDU_BUILTINS = {
    ...
    "میری_فنکشن": _میری_فنکشن,
    ...
}
```

### Step 3 — Test it — اسے آزمائیں

```urdu
لکھو(میری_فنکشن("hello"))   # expect: HELLO
```

```
python -m urdu run examples/test_builtin.urdu
```

---

## Adding New Library Modules — نئے لائبریری ماڈیول شامل کرنا

Library modules live in `urdu/runtime/` and are imported with the `درآمد` (import) statement using Urdu paths.

> **اردو:** لائبریری ماڈیول `urdu/runtime/` میں موجود ہوتے ہیں اور اردو راستوں کے ساتھ `درآمد` بیان کے ذریعے درآمد کیے جاتے ہیں۔

### Step 1 — Create the runtime module — رن ٹائم ماڈیول بنائیں

Create `urdu/runtime/mymod.py`:

```python
"""My new Urdu library module."""

class میری_کلاس:
    def __init__(self, قدر):
        self.قدر = قدر

    def کریں(self):
        return f"نتیجہ: {self.قدر}"

def میری_فنکشن(پیرامیٹر):
    return پیرامیٹر * 2
```

### Step 2 — Register the Urdu import path — اردو درآمد راستہ رجسٹر کریں

Open `urdu/transpiler.py`. Find the `_MODULE_MAP` dict near the top of the file and add your entry:

```python
_MODULE_MAP = {
    "اردو/گوئی":        "urdu.runtime.gui",
    "اردو/ویب":          "urdu.runtime.web",
    ...
    "اردو/میری_لائبریری": "urdu.runtime.mymod",   # ← add this line
}
```

### Step 3 — Register optional pip dependencies — اختیاری pip انحصار رجسٹر کریں

If your library requires pip packages, open `urdu/installer.py` and add an entry to `URDU_PACKAGE_MAP`:

> **اردو:** اگر آپ کی لائبریری کو pip پیکجوں کی ضرورت ہے تو `urdu/installer.py` کھولیں اور `URDU_PACKAGE_MAP` میں اندراج شامل کریں۔

```python
URDU_PACKAGE_MAP = {
    ...
    "اردو/میری_لائبریری": ["some-pip-package", "another-package"],
}
```

### Step 4 — Use it in a .urdu file — .urdu فائل میں استعمال کریں

```urdu
درآمد { میری_کلاس، میری_فنکشن } سے "اردو/میری_لائبریری"

متغیر شے = نیا میری_کلاس(42)
لکھو(شے.کریں())
لکھو(میری_فنکشن(10))
```

### Step 5 — Test it — اسے آزمائیں

```
python -m urdu run examples/test_mymod.urdu
```

---

## Running Tests — ٹیسٹ چلانا

There is no separate test runner. Tests are plain `.urdu` files in the `examples/` folder that print `PASS` / `FAIL` lines.

> **اردو:** کوئی الگ ٹیسٹ رنر نہیں ہے۔ ٹیسٹ `examples/` فولڈر میں سادہ `.urdu` فائلیں ہیں جو `PASS` / `FAIL` سطریں پرنٹ کرتی ہیں۔

Run a test file:

```
python -m urdu run examples/fastapi_test.urdu
python -m urdu run examples/flask_test.urdu
python -m urdu run examples/crud_test.urdu
```

Run all test files (PowerShell):

```powershell
Get-ChildItem examples\*_test.urdu | ForEach-Object {
    Write-Host "Running: $($_.Name)"
    python -m urdu run $_.FullName
}
```

### Checking generated Python — تیار شدہ پائتھن جانچنا

Use `--show-python` to inspect the transpiled output:

```
python -m urdu run myfile.urdu --show-python
```

Or use the `compile` command to write it to disk:

```
python -m urdu compile myfile.urdu -o myfile.py
```

Then open `myfile.py` to see exactly what Python code was generated.

> **اردو:** پھر `myfile.py` کھولیں تاکہ دیکھ سکیں کہ بالکل کون سا پائتھن کوڈ تیار ہوا۔

---

## Code Style — کوڈ کا انداز

- **Python files:** Follow PEP 8. Use 4-space indentation. Keep lines under 100 characters.
- **Type hints:** Add type hints to all new public functions and methods.
- **Docstrings:** Write a one-line docstring for every new class and non-trivial function.
- **Urdu names:** Runtime functions and classes that are exposed to Urdu programs should have Urdu names (Arabic script). Internal helpers can use ASCII names prefixed with `_`.
- **Error messages:** Use `urdu/error_messages.py` for all user-facing error text. Provide both Urdu and English versions where possible.
- **No print statements in library code:** Use the logging library or raise exceptions instead.

> **اردو:** پائتھن فائلیں PEP 8 پر عمل کریں۔ 4 اسپیس انڈینٹیشن استعمال کریں۔ سطریں 100 حروف سے کم رکھیں۔ تمام نئے عوامی فنکشن اور میتھڈ پر ٹائپ ہنٹس لگائیں۔ ہر نئی کلاس اور غیر معمولی فنکشن کے لیے ایک سطری docstring لکھیں۔ رن ٹائم فنکشن اور کلاسوں کے اردو نام (عربی رسم الخط میں) ہونے چاہئیں۔ غلطی کے پیغامات `urdu/error_messages.py` سے لیں اور جہاں ممکن ہو اردو اور انگریزی دونوں نسخے فراہم کریں۔

---

## Submitting a Pull Request — پل ریکوئسٹ جمع کرنا

1. Create a new branch from `main`:
   ```
   git checkout -b feature/my-new-keyword
   ```

2. Make your changes. Write a test `.urdu` file in `examples/`.

3. Verify your changes work:
   ```
   python -m urdu run examples/my_test.urdu
   python -m urdu check examples/my_test.urdu
   ```

4. Commit with a clear message:
   ```
   git add urdu/tokens.py urdu/parser.py urdu/transpiler.py examples/my_test.urdu
   git commit -m "Add میرا_نیا_کلمہ keyword for X feature"
   ```

5. Push to your fork:
   ```
   git push origin feature/my-new-keyword
   ```

6. Open a Pull Request on GitHub. In the PR description, explain:
   - **What** was added or changed.
   - **Why** it is useful.
   - Which `.urdu` test file demonstrates the feature.
   - Any known limitations.

> **اردو:** GitHub پر پل ریکوئسٹ کھولیں۔ PR کی وضاحت میں بتائیں: **کیا** شامل یا تبدیل کیا گیا، **کیوں** یہ مفید ہے، کون سی `.urdu` ٹیسٹ فائل خصوصیت ظاہر کرتی ہے، اور کوئی معروف حدود۔

---

## GitHub Releases — GitHub ریلیز

Releases are tagged on `main` with a version number (e.g., `v1.0.0`). Each release includes:

- Source code ZIP and TAR (automatic from GitHub).
- The compiled `urdu.dist.zip` — the standalone `urdu.exe` bundle — attached as a release asset.

> **اردو:** ریلیزیں `main` پر ورژن نمبر (مثلاً `v1.0.0`) کے ساتھ ٹیگ کی جاتی ہیں۔ ہر ریلیز میں سورس کوڈ ZIP اور TAR (GitHub سے خودکار) اور مرتب شدہ `urdu.dist.zip` — خود مختار `urdu.exe` بنڈل — بطور ریلیز اثاثہ شامل ہوتا ہے۔

To prepare a release asset:
1. Build with `python build.py` (see [Building](building.md)).
2. Zip the `dist\urdu.dist\` folder.
3. Attach the zip to the GitHub release.

---

## License — لائسنس

The Urdu Programming Language is released under the **MIT License**.

> **اردو:** اردو پروگرامنگ زبان **MIT لائسنس** کے تحت جاری کی گئی ہے۔ تعاون کر کے آپ اتفاق کرتے ہیں کہ آپ کے تعاونات اسی MIT لائسنس کے تحت لائسنس ہوں گے۔

```
MIT License

Copyright (c) 2026 Mohammed Zahid Wadiwale

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

By contributing, you agree that your contributions will be licensed under the same MIT License.

---

## Getting Help — مدد حاصل کرنا

- Open a GitHub Issue with the `question` label.
- Include the `.urdu` source, the full error output, and the generated Python (from `--show-python`) in your issue.

> **اردو:** `question` لیبل کے ساتھ GitHub Issue کھولیں۔ اپنے مسئلے میں `.urdu` سورس، مکمل غلطی کا آؤٹ پٹ، اور تیار شدہ پائتھن (`--show-python` سے) شامل کریں۔

---

*Previous: [Building](building.md) | Back to [Index →](index.md)*
