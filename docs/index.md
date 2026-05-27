# اردو پروگرامنگ لینگویج — Urdu Programming Language

> **The world's first programming language written entirely in Urdu syntax.**
> Write real, runnable programs using Urdu keywords, Urdu identifiers, and Urdu idioms — powered by Python under the hood.

> **اردو:** یہ دنیا کی پہلی پروگرامنگ زبان ہے جو مکمل طور پر اردو نحو میں لکھی گئی ہے۔ اردو کلیدی الفاظ، اردو ناموں اور اردو انداز میں حقیقی، چلنے والے پروگرام لکھیں — جو پردے کے پیچھے پائتھن پر چلتی ہے۔

---

## What Is the Urdu Programming Language? — اردو پروگرامنگ لینگویج کیا ہے؟

The **Urdu Programming Language** is a fully-featured, general-purpose programming language where every keyword, operator word, and built-in function name is written in the Urdu (Nastaliq/Arabic-script) alphabet. Instead of writing `if`, `while`, `function`, and `print`, you write `اگر`, `جبکہ`, `فنکشن`, and `لکھو`.

Source files (`.urdu`) pass through a **Lexer → Parser → AST → Transpiler** pipeline that emits clean Python, which is then executed immediately. This means:

- The full Python ecosystem (pip packages, C extensions, standard library) is available.
- Async/await, classes, decorators, generators, and exception handling all work.
- A rich Urdu-native standard library covers web servers, databases, cryptography, machine learning, GUI, file I/O, HTTP, scraping, threading, date/time, and logging.

The language was created to make programming genuinely accessible to Urdu-speaking communities — students, educators, and developers — who think and express themselves in Urdu.

> **اردو:** **اردو پروگرامنگ لینگویج** ایک مکمل، عام مقصد کی پروگرامنگ زبان ہے جس میں ہر کلیدی لفظ، آپریٹر کا نام اور بلٹ-ان فنکشن اردو (نستعلیق/عربی رسم الخط) میں لکھا گیا ہے۔ `if`، `while`، `function` اور `print` لکھنے کی بجائے آپ `اگر`، `جبکہ`، `فنکشن` اور `لکھو` لکھتے ہیں۔
>
> سورس فائلیں (`.urdu`) ایک **لیکسر → پارسر → AST → ٹرانسپائلر** پائپ لائن سے گزرتی ہیں جو صاف پائتھن کوڈ بناتی ہے، جو فوری طور پر چلایا جاتا ہے۔ اس کا مطلب ہے:
>
> - پائتھن کا پورا ماحولیاتی نظام (pip پیکیجز، C ایکسٹینشنز، اسٹینڈرڈ لائبریری) دستیاب ہے۔
> - Async/await، کلاسز، ڈیکوریٹرز، جنریٹرز اور استثناء ہینڈلنگ سب کام کرتے ہیں۔
> - ایک بھرپور اردو نیٹو اسٹینڈرڈ لائبریری ویب سرورز، ڈیٹا بیسز، رمزنگاری، مشین لرننگ، GUI، فائل I/O، HTTP، سکریپنگ، تھریڈنگ، تاریخ/وقت اور لاگنگ کا احاطہ کرتی ہے۔
>
> یہ زبان اردو بولنے والی برادریوں — طلباء، اساتذہ اور ڈویلپرز — کے لیے پروگرامنگ کو حقیقی معنوں میں قابلِ رسائی بنانے کے لیے بنائی گئی ہے جو اردو میں سوچتے اور اظہار کرتے ہیں۔

---

## Creator — تخلیق کار

**Mohammed Zahid Wadiwale**
Developer and designer of the Urdu Programming Language.
Version 1.0.0 — Released 2026-05-16
License: MIT

> **اردو:** **محمد زاہد وڈیوالے** — اردو پروگرامنگ لینگویج کے ڈویلپر اور ڈیزائنر۔
> ورژن 1.0.0 — جاری کردہ 2026-05-16 — لائسنس: MIT

---

## Key Features — اہم خصوصیات

| Feature | Description |
|---|---|
| **Urdu keywords** | Every reserved word (`اگر`، `جبکہ`، `فنکشن`، `واپس` ...) is Urdu |
| **Urdu identifiers** | Variable and function names can be pure Urdu script |
| **Python-powered** | Transpiles to Python; runs on CPython 3.8+ |
| **Async / await** | Full async support — `غیر_متزامن` / `انتظار` |
| **OOP** | Classes (`کلاس`), inheritance (`توسیع`), constructors, `یہ` (this), `سپر` |
| **Exception handling** | `کوشش` / `پکڑو` / `آخر` (try / catch / finally) |
| **Generators** | `پیداوار` (yield) |
| **Modules** | `درآمد` / `سے` / `برآمد` (import / from / export) |
| **Web framework** | FastAPI, Flask, Django, WebSocket, Socket.IO wrappers in `اردو/ویب` |
| **Databases** | SQLite, MySQL, PostgreSQL, MongoDB, Firebase via `اردو/ڈیٹا_بیس` |
| **Machine learning** | NumPy, Pandas, scikit-learn, TensorFlow, llama.cpp via `اردو/ذہین` |
| **Cryptography** | AES, RSA, hashing, JWT via `اردو/رمز` |
| **GUI** | Tkinter wrappers via `اردو/گوئی` |
| **HTTP / cURL** | requests, httpx, aiohttp via `اردو/کرل` |
| **Web scraping** | BeautifulSoup4, lxml via `اردو/کھرچنی` |
| **File I/O** | ZIP, Excel (.xlsx), CSV, text via `اردو/فائلیں` |
| **Threading** | `threading` and `asyncio` wrappers via `اردو/دھاگہ` |
| **Date / time** | `datetime`, `time` wrappers via `اردو/تاریخ` |
| **Logging** | Coloured structured logging via `اردو/لاگ` |
| **Standalone EXE** | Compile to `urdu.exe` with Nuitka — no Python needed |
| **Interactive REPL** | `python -m urdu repl` — live coding in Urdu |
| **MIT license** | Free and open source |

> **اردو:** اوپر دی گئی جدول میں اردو پروگرامنگ لینگویج کی تمام اہم خصوصیات کا خلاصہ ہے — اردو کلیدی الفاظ سے لے کر ویب فریم ورک، ڈیٹا بیس، مشین لرننگ، GUI، فائل ہینڈلنگ اور سٹینڈ الون .exe بنانے تک سب کچھ شامل ہے۔ یہ زبان مکمل طور پر مفت اور اوپن سورس ہے (MIT لائسنس)۔

---

## Hello World — ہیلو ورلڈ

```urdu
لکھو("السلام علیکم، دنیا!")
```

Output:

```
السلام علیکم، دنیا!
```

That is the entire program. Save it as `hello.urdu` and run:

```
python -m urdu run hello.urdu
```

> **اردو:** یہ پورا پروگرام ہے۔ اسے `hello.urdu` کے نام سے محفوظ کریں اور اوپر دی گئی کمانڈ سے چلائیں۔ `لکھو()` پرنٹ فنکشن ہے جو اسکرین پر آؤٹ پٹ دکھاتا ہے۔

---

## A Slightly Larger Taste — ایک بڑی مثال

```urdu
// متغیرات اور ان کا استعمال
متغیر نام = "احمد";
متغیر عمر = 20;

اگر (عمر >= 18) {
    لکھو(نام + " بالغ ہیں");
} ورنہ {
    لکھو(نام + " نابالغ ہیں");
}

// فنکشن
فنکشن سلام(شخص) {
    واپس "خوش آمدید، " + شخص + "!";
}

لکھو(سلام(نام));

// حلقہ
کے_لیے (متغیر عدد کا [1, 2, 3, 4, 5]) {
    لکھو(عدد * عدد);
}
```

> **اردو:** یہ مثال متغیر، شرط (`اگر`/`ورنہ`)، فنکشن اور حلقہ (`کے_لیے`) کا بنیادی استعمال دکھاتی ہے۔ کوڈ بالکل اسی طرح لکھا جاتا ہے جیسے اردو میں سوچتے ہیں۔

---

## How It Works — Pipeline — یہ کیسے کام کرتا ہے

```
yourfile.urdu
      │
      ▼
  Lexer (lexer.py)          — tokenises Urdu source into tokens
      │
      ▼
  Parser (parser.py)        — builds an Abstract Syntax Tree (AST)
      │
      ▼
  AST Nodes (ast_nodes.py)  — typed dataclass nodes for every construct
      │
      ▼
  Transpiler (transpiler.py)— walks AST, emits Python source
      │
      ▼
  Python exec()             — runs the generated .py in-process
```

All async constructs cause the script to be wrapped in
`async def _اردو_main()` and executed via `asyncio.run(...)` automatically.

> **اردو:** آپ کی `.urdu` فائل پہلے لیکسر سے گزرتی ہے (جو اسے ٹوکنز میں توڑتا ہے)، پھر پارسر سے (جو ایک درختی ڈھانچہ یعنی AST بناتا ہے)، پھر ٹرانسپائلر سے (جو اسے پائتھن کوڈ میں بدلتا ہے) اور آخر میں پائتھن اسے چلاتا ہے۔ تمام غیر_متزامن (async) کوڈ خودبخود `asyncio.run()` میں لپیٹ دیا جاتا ہے۔

---

## Standard Libraries — اردو لائبریریاں

| Import path | Contents |
|---|---|
| `اردو/ویب` | FastAPI, Flask, Django, WebSocket, Socket.IO, WebRTC |
| `اردو/ڈیٹا_بیس` | SQLite, MySQL, PostgreSQL, MongoDB, Firebase, Cassandra |
| `اردو/ذہین` | NumPy, Pandas, scikit-learn, TensorFlow, Keras, llama.cpp |
| `اردو/رمز` | AES, RSA, hashing (SHA/MD5/bcrypt), JWT |
| `اردو/گوئی` | Tkinter GUI windows, widgets, dialogs |
| `اردو/کرل` | HTTP GET/POST (requests, httpx, aiohttp, pycurl) |
| `اردو/کھرچنی` | HTML scraping — BeautifulSoup4, lxml |
| `اردو/فائلیں` | ZIP, Excel (.xlsx/.xls), CSV, plain text |
| `اردو/دھاگہ` | threads, thread pools, asyncio tasks |
| `اردو/تاریخ` | date, time, timedelta, formatting |
| `اردو/لاگ` | coloured log levels: معلومات, انتباہ, خطا |
| `اردو/پایتھن` | direct Python stdlib passthrough |

> **اردو:** یہ اردو پروگرامنگ لینگویج کی بلٹ-ان لائبریریاں ہیں۔ ویب ایپلیکیشن بنانی ہو، ڈیٹا بیس استعمال کرنی ہو، مشین لرننگ کرنی ہو یا فائلیں پڑھنی ہوں — سب کچھ اردو ناموں کے ساتھ دستیاب ہے۔

---

## Documentation Sections — دستاویزی حصے

| Section | What You Will Find |
|---|---|
| [Installation](installation.md) | System requirements, setup, CLI reference |
| [Quick Start](quick-start.md) | Your first programs, variables, loops, functions |
| [Syntax Reference](syntax/) | Complete language syntax — keywords, operators, OOP |
| [Built-ins](builtins/) | `لکھو`، `پڑھو`، `لمبائی`، `قسم` and all built-in functions |
| [Libraries](libraries/) | Each standard library module documented in full |
| [Examples](examples/) | Real programs: web server, Django/Flask/FastAPI apps, ML model, billing system, chat |
| [Building](building.md) | Compiling to a standalone `urdu.exe` with Nuitka |
| [Contributing](contributing.md) | How to add keywords, builtins, and library modules |

> **اردو:** یہ دستاویزات کے مختلف حصے ہیں۔ نئے صارفین انسٹالیشن اور فوری آغاز سے شروع کریں، پھر نحو کے حوالہ کی طرف بڑھیں۔

---

## Quick Navigation — فوری رہنمائی

- **New to the language?** Start with [Installation](installation.md), then [Quick Start](quick-start.md).
- **Looking for a specific keyword?** See the [Syntax Reference](syntax/).
- **Need a built-in function?** See [Built-ins](builtins/).
- **Building a web app?** See [Libraries → ویب](libraries/web.md).
- **Compiling to an .exe?** See [Building](building.md).
- **Want to contribute?** See [Contributing](contributing.md).

> **اردو:**
> - **زبان میں نئے ہیں؟** انسٹالیشن سے شروع کریں، پھر فوری آغاز پڑھیں۔
> - **کوئی خاص کلیدی لفظ ڈھونڈ رہے ہیں؟** نحو کا حوالہ دیکھیں۔
> - **بلٹ-ان فنکشن چاہیے؟** بلٹ-انز کا صفحہ دیکھیں۔
> - **ویب ایپ بنانی ہے؟** ویب لائبریری دیکھیں۔
> - **EXE فائل بنانی ہے؟** بلڈنگ گائیڈ دیکھیں۔
> - **حصہ ڈالنا چاہتے ہیں؟** کنٹریبیوٹنگ گائیڈ دیکھیں۔

---

*اردو پروگرامنگ لینگویج — MIT License — Mohammed Zahid Wadiwale*
