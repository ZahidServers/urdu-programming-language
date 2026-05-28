# اردو پروگرامنگ لینگویج — Roadmap

Future plans for the Urdu Programming Language. Items are grouped by category, not strictly ordered by priority.

---

## 📦 Package Manager — `urdu نصب`

### Full-Fledged Urdu Package Manager
The current `urdu نصب` is a thin pip wrapper. The goal is a proper, self-contained package manager for the Urdu ecosystem:

- **Urdu Package Registry** — a central hosted registry (e.g. `packages.urdu-lang.org`) where developers can publish and discover Urdu-native packages (`.urdu` libraries, compiled `.urduc` modules, and mixed Python/Urdu packages)
- **`urdu نصب <پیکج>`** — install from the Urdu registry or fall back to PyPI
- **`urdu شائع`** — publish a package to the registry with a `package.urdu.json` manifest (name, version, author, dependencies)
- ~~**`urdu ہٹائیں <پیکج>`** — uninstall~~ ✓ implemented
- ~~**`urdu تازہ_کریں`** — update all installed packages~~ ✓ implemented
- ~~**`urdu فہرست`** — list installed packages with versions~~ ✓ implemented (supports name filter)
- **Dependency resolution** — semver-aware resolver, lockfile (`urdu.lock`) for reproducible installs
- ~~**Virtual environments** — `urdu ماحول بنائیں` / `urdu ماحول چالو`~~ ✓ implemented
- **Urdu-native packages** — allow `.urdu` source packages that install directly without needing Python packaging knowledge

---

## 🔨 Compiler & Build Improvements

### Better `urdu compile` — Urdu to Executable
- Simplify the Nuitka build into a single `urdu بنائیں` command — no separate `build.py` needed
- `urdu بنائیں --ہدف=windows` / `--ہدف=linux` / `--ہدف=mac` cross-compilation targets
- `urdu بنائیں --ایک_فائل` for a single portable `.exe` / binary
- Auto-detect and bundle only the packages actually used (tree-shaking)
- Build cache — only recompile changed modules, not the entire project from scratch every time
- Progress bar during C compilation phase
- Signed Windows executables with proper code-signing certificate

---

## 🗄️ Framework & Library Support

### Django ORM ✅ Fully Implemented
~~Full Django ORM support inside single-file Urdu Django apps~~ — `ڈجانگو_ماڈل` base class added; field constructors `متن_خانہ`, `طویل_متن`, `عدد_خانہ`, `اعشاریہ_خانہ`, `بولین_خانہ`, `تاریخ_خانہ`, `وقت_خانہ`, `غیر_ملکی_کلید`, `ای_میل_خانہ`, `فائل_خانہ` all available from `اردو/ویب`. ORM query shortcuts `سب_حاصل()`, `فلٹر()`, `ایک_حاصل()`, `بنائیں()`, `حذف_کریں()` also exported. `ایپ.میزیں_بنائیں()` runs syncdb to create tables. `ایپ.چلائیں()` passes `--noreload` by default to prevent auto-reloader from breaking single-file setups.

Django ORM example app **کتابستان** (Kitabistan) — complete CRUD app with two ORM models (`ناشر`, `کتاب`), FK relation, search, middleware, JSON API, and Urdu templates — at `examples/DJANGO_KITABISTAN_APP/`. See [docs/examples/django-kitabistan.md](docs/examples/django-kitabistan.md).

Remaining: auto-discovery of models defined in Urdu classes without manually registering an `INSTALLED_APPS` module.

### PyQt Library — `اردو/پائی_کیو_ٹی`
Urdu-named wrappers around PyQt6 — windows, widgets, layouts, signals/slots, dialogs, and the event loop. Complement the existing `اردو/گوئی` (Tkinter) module for users who need richer desktop UI.

### PyGame Library — `اردو/کھیل`
2D game development wrappers in Urdu — surfaces, sprites, event loop, keyboard/mouse input, sound, and clock. Allow writing games entirely in Urdu syntax.

### OpenGL Library — `اردو/تھری_ڈی`
Urdu-named wrappers around PyOpenGL and optionally ModernGL — shaders, buffers, textures, and the render loop. Enables 3D graphics and GPU-accelerated rendering from Urdu code.

### Arduino / Embedded — `اردو/آردوینو` ✓ Implemented (native pyfirmata2)
Full native pyfirmata2 integration:
- **Board classes**: `آردوینو`, `آردوینو_میگا`, `آردوینو_نانو`, `آردوینو_ڈیو` — each wraps the matching pyfirmata2 class, starts the background iterator and sampling automatically
- **`پن` class**: first-class pin object — `آؤٹ_پٹ_بنائیں()`, `ان_پٹ_بنائیں(پل_اپ)`, `PWM_بنائیں()`, `سرو_بنائیں()`, `لکھو()`, `پڑھو()`, `خام_پڑھو()`, `کال_بیک_مقرر()`, `رپورٹنگ_چالو/بند()`; callable shorthand: `p()` → read, `p(قدر)` → write
- **Direct board methods**: `ڈیجیٹل_لکھو/پڑھو`, `اینالاگ_لکھو/پڑھو/خام`, `سرو_لکھو`, `بلند_کریں`, `نیچے_کریں`, `ٹاگل`, `ان_پٹ_پل_اپ_موڈ`
- **Callbacks**: `ڈیجیٹل_تبدیلی(n, fn)`, `اینالاگ_تبدیلی(n, fn)` — interrupt-style, no polling needed
- **Sampling control**: `نمونہ_چالو(ms)`, `نمونہ_بند()`, `نمونہ_وقفہ(ms)`
- **I2C**: `I2C_آغاز()`, `I2C_لکھو(پتہ, *بائٹس)`, `I2C_پڑھو(پتہ, تعداد, کال_بیک)`, `I2C_آلہ` wrapper class
- **`سیریل`**: full raw pyserial wrapper; **`سیریل_آردوینو`**: text-command protocol (no Firmata needed)
- Install: `urdu نصب اردو/آردوینو`

Long-term: MicroPython-compatible subset that can run directly on microcontrollers.

### TensorBoard — `اردو/ٹینسر_بورڈ` ✅ (implemented v1.0)
Urdu-named wrappers around TensorBoard — log training metrics, visualise model graphs, display histograms and images from within Urdu ML programs. Integrate with `اردو/ذہین` so that model training loops can call `لاگ.میٹرک(نام, قدر, قدم)` and `لاگ.گراف(ماڈل)`. Launch the dashboard with `urdu بورڈ چلائیں`. Makes the ML training loop fully inspectable from Urdu code without dropping into Python.

**Implemented** (`urdu/runtime/tensorboard_lib.py`):
- `ٹینسر_لاگ(فولڈر, تبصرہ)` — main logger; auto-selects PyTorch → pure-tensorboard backend
- `لاگ.میٹرک(نام, قدر, قدم)`, `لاگ.میٹرکس(نام, ڈکٹ, قدم)` — scalar logging
- `لاگ.ہسٹوگرام(نام, قدریں, قدم)`, `لاگ.تصویر(نام, تصویر, قدم)`, `لاگ.متن(نام, مواد, قدم)`
- `لاگ.ہائپر_پیرامیٹر(پیرامیٹرز, میٹرکس)` — HParams tab
- `لاگ.کیراس_کال_بیک()` — drop-in Keras callback for `model.fit()`
- `لاگ.نقصان(v, قدم)`, `لاگ.درستگی(v, قدم)`, `لاگ.وزن(نام, ماڈل, قدم)` — shorthands
- `بورڈ_چلائیں(فولڈر, پورٹ)` — launch TensorBoard browser UI
- `میٹرک_لاگ(نام, قدر, قدم)` — one-shot convenience function
- `ٹینسر_قدم` — thread-safe step counter
- CLI: `urdu بورڈ چلائیں [فولڈر] [--پورٹ PORT]`
- Install: `urdu نصب اردو/ٹینسر_بورڈ`

### Native Libraries — مقامی لائبریریاں ✅ (implemented v1.0)
A set of Urdu-API standard-library modules — data structures, algorithms, string utilities, and math helpers. No pip install needed; all stdlib-only.

**`اردو/ڈھانچے`** (`urdu/runtime/structures.py`):
- `مربوط_فہرست` — Singly Linked List (شامل_کریں / نکالیں / الٹا_کریں)
- `ڈھیر` — Stack LIFO (دھکیلیں / نکالیں / جھانکیں)
- `قطار` — Queue FIFO (شامل_کریں / نکالیں / اگلا)
- `دوطرفہ_قطار` — Deque (بائیں_شامل / دائیں_نکالیں / ...)
- `ترجیحی_قطار` — Priority Queue / Min-Heap (`زیادہ_سے_زیادہ=True` → Max-Heap)
- `بائنری_تلاش_درخت` — BST (داخل_کریں / نکالیں / ترتیب_سے / سب_سے_چھوٹا / اونچائی)
- `گراف` — Adjacency-list graph (BFS / DFS / مختصر_راستہ Dijkstra / طوپو_ترتیب)

**`اردو/الگورتھم`** (`urdu/runtime/algorithms.py`):
- Sorting: `بلبلہ_ترتیب`, `انتخاب_ترتیب`, `اندراج_ترتیب`, `ضم_ترتیب`, `تیز_ترتیب`, `ڈھیر_ترتیب`
- Search: `خطی_تلاش`, `دوئی_تلاش`
- `ہیش_جدول` — chaining hash table with dict-style `ج["key"] = value`
- Math: `اعظم_مشترک_قاسم` (GCD), `اقل_مشترک_ضرب` (LCM), `فیبوناچی`, `فیکٹوریل`, `عدد_زائی_ہے`, `اعداد_زائیہ` (sieve), `قوت` (fast pow), `اعداد_زائیہ_عوامل`
- String: `لمبی_مشترک_ذیل_ترتیب` (LCS), `لیوینشٹین_فاصلہ`, `کے_ایم_پی_تلاش` (KMP)

**`اردو/متن`** (`urdu/runtime/text_lib.py`):
- Full string API: `تقسیم`, `ملائیں`, `بدلیں`, `تراشو`, `پیڈ_بائیں/دائیں/وسط`, etc.
- Urdu-specific: `اعراب_ہٹائیں` (diacritic removal), `نستعلیق_معیاری` (Nastaliq normalisation), `الفاظ` (word tokenisation), `اردو_حروف_ہیں`
- Numeral conversion: `ہندی_اعداد` (۱۲۳ → 123), `ہندی_اعداد_میں` (123 → ۱۲۳)
- `اردو_میں_گنتی(n)` — integer to Urdu words (supports کروڑ scale)
- `مماثلت(الف, ب)` — string similarity 0.0–1.0
- Regex wrappers: `ریجیکس_تلاش`, `ریجیکس_بدلیں`, `ریجیکس_تمام`

Long-term: a C extension path where performance-critical native modules compile to `.pyd` via Cython or CFFI, keeping the Urdu API surface but native speed.

---

## 🖥️ Platform & Distribution

### Linux Executable Binary
A standalone `urdu` binary for Linux (x86_64 and ARM) built with Nuitka — no Python installation required. Distribute via `.deb`, `.rpm`, AppImage, and direct binary download. Essential for server-side deployment and Linux developer adoption.

### macOS Executable Binary
A standalone `urdu` binary and `.app` bundle for macOS (Intel + Apple Silicon / Universal 2) — distribute via `.dmg` or Homebrew tap. Requires macOS CI runner for signing and notarization.

### Docker Image
An official `urdu-lang/urdu` Docker image on Docker Hub — enables running Urdu programs in containers without any local install, and simplifies CI/CD pipelines for Urdu-based web apps.

### GitHub Actions / CI Integration
A ready-made GitHub Actions workflow (`urdu-lang/setup-urdu`) to install the Urdu runtime and run `.urdu` test files in any CI pipeline.

---

## ⚙️ CLI & Shell Experience

### Better CLI Handling
Improve the `urdu` command-line experience across all common shells and terminals:

- **Windows CMD** — correct encoding, ANSI colour output, proper exit codes
- **PowerShell** — native completion script (`Register-ArgumentCompleter`), UTF-8 pipeline
- **Termux (Android)** — tested path handling, `urdu نصب` working via pip inside Termux
- **Linux/macOS Terminal** — bash and zsh completion scripts, `man` page
- **`urdu نیا <پروجیکٹ>`** — scaffold a new project with folder structure and starter files
- **`urdu جانچ`** — built-in test runner for `.urdu` test files
- **`urdu فارمیٹ`** — auto-formatter (currently a stub)
- **`urdu لنٹ`** — static analysis / linter with Urdu-aware error messages
- Better error messages with file:line context and suggested fixes

### Improved `urdu مدد` Help Tool
The current `urdu مدد` command shows basic topic info. Planned improvements:
- Searchable by keyword: `urdu مدد تلاش فلاسک`
- Show runnable examples inline
- `urdu مدد <فنکشن_نام>` for function-level lookup
- Offline-first with optional online fetch for latest docs
- Coloured, formatted terminal output with syntax-highlighted code snippets

---

## 🧵 Runtime Improvements

### Improve Threading
- Fix edge cases when mixing `غیر_متزامن` (async) and threaded WSGI servers
- ~~`اردو/دھاگہ` improvements: `Future`-style objects, cancellation support~~ — ✓ `مستقبل` class and `منسوخ_ہونے_والا` cancellable-task wrapper added; `دھاگہ_تالاب.جمع_کرو_مستقبل()` returns a `مستقبل`; `غیر_متزامن_مستقبل()` helper added
- Thread-safe global lock mechanism accessible from Urdu code
- Better error propagation from worker threads back to the main thread

### Better Error Messages
- Map transpiler/runtime errors back to the original `.urdu` source line (already partially done — improve completeness)
- ~~Suggestions: "کیا آپ کا مطلب `شامل` تھا؟" for unknown method names~~ — ✓ `did_you_mean()`, `suggest_name()`, `suggest_attr()` added to `error_messages.py`; compiler now prints a `💡 شاید آپ کا مطلب تھا:` hint on `NameError` and `AttributeError`
- Friendly Urdu-language error descriptions instead of raw Python tracebacks for common mistakes

### Bug Fixes
Ongoing — known areas: none currently open.

**Fixed in v1.0.x:**
- ~~`.join()` method disambiguation~~ — transpiler now tracks the original Urdu method name (`جوڑو`) before normalisation; raw `.join()` calls (`os.path.join`, `str.join`) pass through unchanged
- ~~Edge cases in the transpiler for deeply nested ternary expressions~~ — condition is now wrapped in parens to prevent Python operator-precedence issues
- ~~REPL multi-line input handling~~ — brace-counting heuristic (`{` > `}` → keep buffering) correctly distinguishes incomplete blocks from real syntax errors
- ~~Windows path handling in `__file__`-relative imports~~ — transpiler strips `./` and `.\` prefixes before module-name conversion
- ~~Django compiled-exe crash (`django.core.management` not found)~~ — `django.contrib.auth` and `django.contrib.contenttypes` removed from default INSTALLED_APPS in the `ڈجانگو` wrapper; add them explicitly via the `ایپس` config key when needed
- ~~FastAPI/SocketIO and Flask MySQL compiled-exe crash (`cannot locate package '' associated with metadata`)~~ — `build.py` now includes explicit `--include-distribution-metadata` flags for `opentelemetry-api`, `opentelemetry-sdk`, `opentelemetry-semantic-conventions`, `anyio`, `uvicorn`, and `flask` instead of the unsupported wildcard `*`
- ~~`xlrd` missing from standalone build~~ — `xlrd` added to `requirements.txt` and installed; future builds will automatically include `.xls` legacy Excel file support
- ~~Decorator chaining with arguments~~ — `_s_ClassDecl` in the transpiler now emits `@decorator` lines before the class definition, exactly like `_s_FunctionDecl` already did

---

## 🌐 Website & Community

### Official Website — `urdu-lang.org`
A dedicated website for the Urdu Programming Language:
- **Landing page** — what the language is, who it is for, quick demo
- **Online Playground** — browser-based REPL to write and run Urdu code without installing anything
- **Documentation site** — full searchable docs (MkDocs or Docusaurus), hosted and versioned
- **Package Registry** — browse and search published Urdu packages
- **Showcase** — gallery of apps and projects built with Urdu PL
- **Blog / announcements** — release notes, tutorials, community highlights
- **Download page** — installers for Windows, Linux, macOS, with checksums

### Community
- Discord server or forum for Urdu PL developers and learners
- GitHub Discussions enabled on the repo
- Contributing guide in Urdu

---

## 📚 Documentation

### Better Documentation for Everything
- Complete API reference for every class and function in all `اردو/*` libraries
- More worked examples per library page
- Video tutorials in Urdu (YouTube)
- Translate all doc pages fully into Urdu
- Searchable online docs site
- Changelog and migration guides between versions
- Beginner course: "اردو میں پروگرامنگ سیکھیں" (Learn Programming in Urdu)

---

## 🛠️ Developer Tooling

### IDE & Editor Support
- VS Code extension: syntax highlighting, snippets, run button, inline error display
- JetBrains plugin
- Notepad++ / Sublime Text syntax definition files
- Language Server Protocol (LSP) implementation for any editor

### Jupyter Kernel
An `urdu-kernel` for Jupyter Notebook and JupyterLab — write and run Urdu code in notebook cells, great for data science and teaching.

### Debugger
`urdu debug app.urdu` — step-through debugger that shows Urdu source lines (not generated Python), with breakpoints, variable inspection, and call stack in Urdu variable names.

### IntelliSense — ذہین تکمیل
A full IntelliSense engine for the Urdu Programming Language — auto-complete Urdu keywords, identifiers, and library symbols as you type. Requires an LSP (Language Server Protocol) implementation that understands the Urdu lexer and type system:
- Keyword completion: type `فنکشن` and get a snippet
- Library member completion: type `ایپ.` and get all route decorators
- Parameter hints: show argument names and types on function calls
- Hover documentation: display the Urdu doc for any symbol under the cursor
- Go to definition: jump to where a function or variable is declared
- Works in VS Code (via extension), JetBrains, and any LSP-capable editor

---

## 🔬 Low-Level & Systems Programming

### Binary, Hex, and Assembly Execution — بائنری، ہیکساڈیسیمل اور اسمبلی
Bring low-level execution capabilities into Urdu programs:
- **Binary literals and operations** — `0b10110101` literals, bitwise ops (`AND`, `OR`, `XOR`, `NOT`, shifts) with Urdu-named operators
- **Hexadecimal I/O** — `ہیکس_پڑھو()` / `ہیکس_لکھو()` for reading and writing raw hex data, memory dump formatting
- **Inline assembly** — `اسمبلی { ... }` block that passes raw x86/ARM assembly to a backend assembler (e.g. `keystone-engine`) and executes the resulting machine code
- **Byte buffers** — a `بائٹ_سرنی` type that wraps Python `bytearray` / `ctypes` for direct memory manipulation
- **Machine code inspection** — disassemble compiled bytecode back to readable hex/ASM for educational purposes

### OS-Level Registry & System Access — آپریٹنگ سسٹم رجسٹری
Native operating-system integration:
- **Windows Registry** — `رجسٹری` class wrapping `winreg` — read/write/create/delete keys and values in `HKEY_LOCAL_MACHINE`, `HKEY_CURRENT_USER`, etc. with Urdu-named methods
- **Environment variables** — `ماحول_متغیر` helpers for reading, setting, and persisting environment variables across processes
- **Process management** — list running processes, start/stop processes, query CPU and memory usage in Urdu
- **System information** — hostname, username, OS version, disk usage, network interfaces — all queryable from Urdu code
- **Linux / macOS** — `/proc` filesystem helpers, `sysctl` wrappers, `dbus` integration for desktop notifications

### File Manager — فائل مینیجر ✓ Implemented
~~Urdu-named wrappers around `pathlib`, `shutil`, and `os`~~ — path ops (`راستہ_ملائیں`, `مطلق_راستہ`, `والد_فولڈر`, `فائل_نام`, `فائل_لاحقہ`, `فائل_موجود`, `فائل_سائز`), file ops (`فائل_پڑھو`, `فائل_لکھو`, `فائل_شامل`, `فائل_کاپی`, `فائل_منتقل`, `فائل_حذف`, `فائل_نام_بدلیں`), directory ops (`فولڈر_بنائیں`, `فولڈر_کاپی`, `فولڈر_حذف`, `فولڈر_خالی_کریں`), search (`فائل_تلاش`, `فائل_تلاش_متن`, `فولڈر_فہرست`, `فولڈر_فائلیں`), and `فائل_نگران` watcher class (requires `pip install watchdog`) — all in `اردو/فائلیں`.

Remaining: cross-platform temp files, atomic writes, Windows ACL helpers.
- macOS: FSEvents integration, `.DS_Store` awareness

---

## 🌐 Platform Expansion

### HarmonyOS Support — ہارمونی OS
Support for running Urdu programs on Huawei HarmonyOS devices:
- Investigate ArkTS / ArkUI bridge or Python-compatible runtime layer on HarmonyOS
- Urdu CLI tools installable via HarmonyOS package manager
- Basic I/O and networking from Urdu on HarmonyOS
- UI wrappers for ArkUI components with Urdu-named classes

### Natural Language Synthesis — قدرتی زبان ترکیب
Integrate natural language processing capabilities written in Urdu:
- **Text-to-speech** — `اردو/آواز` library wrapping `pyttsx3` or `coqui-tts` with Urdu-language voice models; call `بولو("السلام علیکم")` to produce spoken audio
- **Speech-to-text** — `آواز_سنو()` using `whisper` or `vosk` to transcribe spoken Urdu into source text
- **NLP utilities** — Urdu tokeniser, POS tagger, stemmer, and named entity recogniser using `urduhack` or `camel-tools`
- **Conversational AI** — `اردو/ذہانت` module wrapping local LLMs (llama.cpp) with Urdu-language prompt templates
- Long-term: an Urdu-native REPL mode where you describe what you want in plain Urdu and the language generates `.urdu` code

---

## 🖥️ Chip-Level & Bare-Metal

### Native Chip Architecture Drawing — چپ فن تعمیر
Deep hardware integration for drawing directly into chip architecture:
- **GPU compute** — `اردو/جی_پی_یو` module wrapping CUDA/OpenCL/Vulkan compute shaders; dispatch parallel kernels written in Urdu-like pseudocode that compiles to SPIR-V or PTX
- **Direct framebuffer** — write pixels directly to `/dev/fb0` (Linux) or a DirectX surface (Windows) without a windowing system; useful for embedded displays and kiosk applications
- **Bare-metal target** — a subset of Urdu that compiles via LLVM IR to a standalone binary with no OS dependency; target Raspberry Pi bare-metal, STM32, and ESP32
- **SIMD / intrinsics** — Urdu-named wrappers for SSE/AVX/NEON vector instructions for high-performance numeric code
- **Custom ISA** — educational mode where Urdu programs run on a simple custom instruction set architecture (ISA) simulated in software — ideal for teaching computer architecture in Urdu

---

## Version Milestones

| Version | Status | Focus |
|---------|--------|-------|
| v1.0.0 | ✅ released 2026-05-16 | Initial release — core language, OOP, async, GUI, ML, DB, Web, CLI |
| v1.0.1 | ✅ released 2026-05-29 | Arduino/Firmata (`اردو/آردوینو`), TensorBoard (`اردو/ٹینسر_بورڈ`), Data Structures (`اردو/ڈھانچے`), Algorithms (`اردو/الگورتھم`), Text utilities (`اردو/متن`), File manager enhancements, Threading futures, Smart error suggestions; Django ORM fully working — `ڈجانگو_ماڈل`, 10 field types, FK relations, query helpers, `میزیں_بنائیں()`, `--noreload` server; Django Kitabistan CRUD example app (`examples/DJANGO_KITABISTAN_APP/`); fixed `خالی` keyword conflict in field constructors (`اجازت` parameter) |
| v1.1 | 🔜 planned | Bug fixes, CLI improvements, Linux binary, better `urdu مدد` |
| v1.2 | 🔜 planned | PyQt + PyGame libraries, macOS binary, Docker image |
| v1.3 | 🔜 planned | VS Code extension / LSP, Jupyter kernel, `urdu بنائیں` command |
| v1.4 | 🔜 planned | Full package manager, Urdu package registry, `urdu شائع` |
| v1.5 | 🔜 planned | Official website, online playground, MicroPython subset, debugger |
| v1.6 | 🔜 planned | OpenGL, Termux / Android support, HarmonyOS |
| v1.7 | 🔜 planned | Natural language synthesis (`اردو/آواز`, NLP), GPU compute |
| v1.8 | 🔜 planned | Bare-metal chip target, SIMD intrinsics, custom ISA simulator |

---

*اردو پروگرامنگ لینگویج — Mohammed Zahid Wadiwale*
