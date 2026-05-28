<div dir="rtl" align="right">

# اردو پروگرامنگ لینگویج

پہلی مکمل اردو پروگرامنگ زبان — اردو میں کوڈ لکھیں، دنیا کی کوئی بھی ایپلیکیشن بنائیں۔

</div>

# Urdu Programming Language — اردو پروگرامنگ لینگویج

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/ZahidServers/urdu-programming-language/releases)
[![Version](https://img.shields.io/badge/Version-1.0.0-green)](https://github.com/ZahidServers/urdu-programming-language/releases/tag/v1.0.0)
[![License](https://img.shields.io/badge/License-UPL--1.0-orange)](LICENSE)
[![Author](https://img.shields.io/badge/Author-Mohammed%20Zahid%20Wadiwale-red)](https://github.com/ZahidServers)

> **The world's first fully-featured programming language written entirely in Urdu.**  
> Write code, build web servers, train ML models, manage databases — all in اردو.

---

## What is this?

The **Urdu Programming Language** lets you write real, working software using Urdu script keywords. It is not a toy or a demo — it compiles to Python and supports:

- Object-oriented programming with Urdu class syntax
- Async / await concurrency
- FastAPI, Flask, and Django web servers
- Django ORM — models, CRUD, migrations, FK relations, JSON API
- MySQL, PostgreSQL, MongoDB, Firebase, SQLite
- Machine learning (scikit-learn, TensorFlow, NumPy, Pandas)
- TensorBoard integration for ML training visualisation
- File I/O, ZIP, Excel, PDF; file system / directory helpers
- Cryptography (AES, RSA, HMAC, PBKDF2)
- Web scraping (BeautifulSoup)
- Threading, multiprocessing, and Future-based task pools
- Data structures (linked list, stack, queue, priority queue, BST, graph)
- Algorithms (sorting, searching, hash table, GCD/LCM, KMP, LCS)
- Urdu-aware text utilities (diacritic removal, numeral conversion, similarity)
- Arduino / embedded hardware (pyfirmata2 — digital, analog, PWM, servo, I2C)
- Smart error messages with Urdu "did you mean?" suggestions
- A full interactive REPL

---

## Hello World — السلام علیکم

```urdu
لکھو("السلام علیکم، دنیا!")
```

```
السلام علیکم، دنیا!
```

---

## More examples

**Variables and input:**
```urdu
متغیر نام = پڑھو("آپ کا نام: ")
لکھو(`خوش آمدید، ${نام}!`)
```

**Conditions and loops:**
```urdu
کے_لیے (متغیر i کا حد(1, 6)) {
    اگر (i % 2 == 0) {
        لکھو(i, "جفت ہے")
    } ورنہ {
        لکھو(i, "طاق ہے")
    }
}
```

**Functions:**
```urdu
فنکشن مربع(عدد) {
    واپس عدد ** 2
}

لکھو(مربع(7))    // 49
```

**Classes:**
```urdu
کلاس طالب_علم {
    تعمیر(نام, نمبر) {
        یہ.نام   = نام
        یہ.نمبر = نمبر
    }

    گریڈ() {
        اگر (یہ.نمبر >= 90) { واپس "A" }
        اگر (یہ.نمبر >= 75) { واپس "B" }
        واپس "C"
    }
}

متغیر ط = نیا طالب_علم("احمد", 92)
لکھو(`${ط.نام} کا گریڈ: ${ط.گریڈ()}`)
```

**Web server (FastAPI):**
```urdu
درآمد { فاسٹ_اے_پی_آئی, جیسن_جواب } سے "اردو/ویب"

متغیر ایپ = نیا فاسٹ_اے_پی_آئی({ عنوان: "میری API" })

@ایپ.حاصل("/")
فنکشن جڑ() {
    واپس نیا جیسن_جواب({ "پیغام": "السلام علیکم!" })
}

ایپ.چلائیں({ پورٹ: 8000 })
```

---

## Installation

### Option 1 — Pre-built Windows exe (recommended)

Download the latest release from the [**Releases page**](https://github.com/ZahidServers/urdu-programming-language/releases):

1. Download `urdu-v1.0.0-windows.zip`
2. Extract to any folder (e.g. `C:\urdu\`)
3. Add that folder to your system PATH
4. Open a terminal and run:

```
urdu version
urdu run hello.urdu
```

### Option 2 — Python package (pip)

Requires Python 3.9 or later.

```
pip install urdu-lang
```

Then run:

```
urdu run hello.urdu
urdu repl
```

### Option 3 — Run from source

```
git clone https://github.com/ZahidServers/urdu-programming-language.git
cd urdu-programming-language
pip install -r requirements.txt
python -m urdu run hello.urdu
```

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `urdu run file.urdu` | Run an Urdu source file |
| `urdu compile file.urdu` | Transpile to Python |
| `urdu repl` | Start interactive REPL |
| `urdu check file.urdu` | Check syntax without running |
| `urdu version` | Show version info |
| `urdu مدد` | Urdu help system |
| `urdu نصب <package>` | Install a pip package |

---

## Language Keywords — کلیدی الفاظ

| Urdu | English | Purpose |
|------|---------|---------|
| `متغیر` | `let` | Declare variable |
| `مستقل` | `const` | Declare constant |
| `فنکشن` | `function` | Define function |
| `کلاس` | `class` | Define class |
| `اگر` | `if` | Condition |
| `ورنہ` | `else` | Else branch |
| `جبکہ` | `while` | While loop |
| `کے_لیے` | `for` | For loop |
| `واپس` | `return` | Return value |
| `درآمد` | `import` | Import module |
| `برآمد` | `export` | Export symbol |
| `کوشش` | `try` | Try block |
| `پکڑو` | `catch` | Catch error |
| `پھینکو` | `throw` | Throw error |
| `غیر_متزامن` | `async` | Async function |
| `انتظار` | `await` | Await promise |
| `نیا` | `new` | Create instance |
| `یہ` | `this` | Current object |
| `سچ` | `true` | Boolean true |
| `جھوٹ` | `false` | Boolean false |
| `خالی` | `null` | Null value |
| `لکھو()` | `print()` | Print to console |
| `پڑھو()` | `input()` | Read user input |

---

## Libraries

| Import | Provides |
|--------|---------|
| `اردو/ویب` | FastAPI, Flask, Django + ORM, WebSocket, Socket.IO, HTTP client |
| `اردو/ڈیٹا_بیس` | MySQL, PostgreSQL, MongoDB, Firebase, Cassandra, SQLite |
| `اردو/فائلیں` | Text, CSV, JSON, ZIP, Excel, PDF, file system helpers |
| `اردو/رمز` | AES, RSA, HMAC, SHA, PBKDF2, Fernet |
| `اردو/ذہین` | Pandas, NumPy, scikit-learn, TensorFlow |
| `اردو/کھرچنی` | BeautifulSoup web scraper |
| `اردو/لاگ` | Structured logging |
| `اردو/دھاگہ` | Threading, multiprocessing, async tasks, futures |
| `اردو/تاریخ` | Date, time, timezone, formatting |
| `اردو/کرل` | HTTP client (aiohttp) |
| `اردو/ڈھانچے` | Linked list, stack, queue, priority queue, BST, graph |
| `اردو/الگورتھم` | Sorting, searching, hash table, math helpers, string algorithms |
| `اردو/متن` | Urdu string ops, diacritic removal, numeral conversion, similarity |
| `اردو/آردوینو` | Arduino hardware — digital/analog I/O, PWM, servo, I2C |
| `اردو/ٹینسر_بورڈ` | TensorBoard — metric logging, histograms, Keras callback |

---

## Documentation

Full documentation is in the [`docs/`](docs/) folder:

- [Quick Start](docs/quick-start.md)
- [Syntax Reference](docs/syntax/)
- [Built-in Functions](docs/builtins/)
- [Library Reference](docs/libraries/)
- [Examples](docs/examples/)
- [Installation Guide](docs/installation.md)
- [Building from Source](docs/building.md)
- [Contributing](docs/contributing.md)

---

## Building the exe yourself

Requires Python 3.11 and Nuitka:

```
pip install nuitka
python build.py
```

Output: `dist/__main__.dist/urdu.exe`

See [docs/building.md](docs/building.md) for full instructions.

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING](docs/contributing.md) and the [LICENSE](LICENSE) before submitting a pull request.

All contributions must credit **Mohammed Zahid Wadiwale** as the original author of this language.

---

## License

Programs you **write** in the Urdu Programming Language are entirely your own — no attribution required, no restrictions.

The **language itself** (this repository's source code) is covered by the [Urdu Programming Language License](LICENSE). Derivative works of the language must credit the original author.

**Original Author:** Mohammed Zahid Wadiwale  
**Contact:** zahid.wadiwale1234@gmail.com

---

<div dir="rtl" align="right">

**تخلیق کار:** محمد زاہد وڈیوالے  
یہ پروجیکٹ اردو بولنے والوں کو پروگرامنگ کے قابل بنانے کے لیے بنایا گیا ہے۔

</div>
