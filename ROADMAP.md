# اردو پروگرامنگ لینگویج — Roadmap

Future plans for the Urdu Programming Language. Items are grouped by category, not strictly ordered by priority.

---

## 📦 Package Manager — `urdu نصب`

### Full-Fledged Urdu Package Manager
The current `urdu نصب` is a thin pip wrapper. The goal is a proper, self-contained package manager for the Urdu ecosystem:

- **Urdu Package Registry** — a central hosted registry (e.g. `packages.urdu-lang.org`) where developers can publish and discover Urdu-native packages (`.urdu` libraries, compiled `.urduc` modules, and mixed Python/Urdu packages)
- **`urdu نصب <پیکج>`** — install from the Urdu registry or fall back to PyPI
- **`urdu شائع`** — publish a package to the registry with a `package.urdu.json` manifest (name, version, author, dependencies)
- **`urdu ہٹائیں <پیکج>`** — uninstall
- **`urdu تازہ_کریں`** — update all installed packages
- **`urdu فہرست`** — list installed packages with versions
- **Dependency resolution** — semver-aware resolver, lockfile (`urdu.lock`) for reproducible installs
- **Virtual environments** — `urdu ماحول بنائیں` / `urdu ماحول چالو` to isolate project dependencies
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

### Django ORM
Full Django ORM support inside single-file Urdu Django apps — define models as Urdu classes, run `ایپ.میزیں_بنائیں()` for auto-migration, query with `ماڈل.objects.filter(...)` etc. Currently the programmatic Django wrapper works best with raw SQL; ORM needs the app registry and model discovery to be wired into the `ڈجانگو` class properly.

### PyQt Library — `اردو/پائی_کیو_ٹی`
Urdu-named wrappers around PyQt6 — windows, widgets, layouts, signals/slots, dialogs, and the event loop. Complement the existing `اردو/گوئی` (Tkinter) module for users who need richer desktop UI.

### PyGame Library — `اردو/کھیل`
2D game development wrappers in Urdu — surfaces, sprites, event loop, keyboard/mouse input, sound, and clock. Allow writing games entirely in Urdu syntax.

### OpenGL Library — `اردو/تھری_ڈی`
Urdu-named wrappers around PyOpenGL and optionally ModernGL — shaders, buffers, textures, and the render loop. Enables 3D graphics and GPU-accelerated rendering from Urdu code.

### Arduino / Embedded — `اردو/آردوینو`
Serial communication and microcontroller interfacing via `pyserial` — send/receive data from Arduino and other serial devices, define pin modes and digital/analog read-write in Urdu syntax. Long-term: MicroPython-compatible subset that can run directly on microcontrollers.

### TensorBoard — `اردو/ٹینسر_بورڈ`
Urdu-named wrappers around TensorBoard — log training metrics, visualise model graphs, display histograms and images from within Urdu ML programs. Integrate with `اردو/ذہین` so that model training loops can call `لاگ.میٹرک(نام, قدر, قدم)` and `لاگ.گراف(ماڈل)`. Launch the dashboard with `urdu بورڈ چلائیں`. Makes the ML training loop fully inspectable from Urdu code without dropping into Python.

### Native Libraries — مقامی لائبریریاں
A set of pure-Urdu standard-library modules written in `.urdu` source (not Python wrappers) — data structures, algorithms, string utilities, and math helpers expressed entirely in the Urdu language. Goals:
- Ship as part of the language distribution — no pip install needed
- Serve as reference implementations showing idiomatic Urdu code
- `اردو/ڈھانچے` — linked lists, stacks, queues, trees, graphs in Urdu
- `اردو/الگورتھم` — sorting, searching, hashing algorithms
- `اردو/متن` — advanced string manipulation, Urdu-specific text utilities (Nastaliq normalisation, diacritic stripping, word tokenisation)
- Long-term: a C extension path where performance-critical native modules compile to `.pyd` via Cython or CFFI, keeping the Urdu API surface but native speed

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
- Thread-safe global lock mechanism accessible from Urdu code
- `اردو/دھاگہ` improvements: thread pools, `Future`-style objects, cancellation support
- Better error propagation from worker threads back to the main thread

### Better Error Messages
- Map transpiler/runtime errors back to the original `.urdu` source line (already partially done — improve completeness)
- Friendly Urdu-language error descriptions instead of raw Python tracebacks for common mistakes
- Suggestions: "کیا آپ کا مطلب `شامل` تھا؟" for unknown method names

### Bug Fixes
Ongoing — known areas:
- Decorator chaining with arguments

**Fixed in v1.0.x:**
- ~~`.join()` method disambiguation~~ — transpiler now tracks the original Urdu method name (`جوڑو`) before normalisation; raw `.join()` calls (`os.path.join`, `str.join`) pass through unchanged
- ~~Edge cases in the transpiler for deeply nested ternary expressions~~ — condition is now wrapped in parens to prevent Python operator-precedence issues
- ~~REPL multi-line input handling~~ — brace-counting heuristic (`{` > `}` → keep buffering) correctly distinguishes incomplete blocks from real syntax errors
- ~~Windows path handling in `__file__`-relative imports~~ — transpiler strips `./` and `.\` prefixes before module-name conversion
- ~~Django compiled-exe crash (`django.core.management` not found)~~ — `django.contrib.auth` and `django.contrib.contenttypes` removed from default INSTALLED_APPS in the `ڈجانگو` wrapper; add them explicitly via the `ایپس` config key when needed
- ~~FastAPI/SocketIO and Flask MySQL compiled-exe crash (`cannot locate package '' associated with metadata`)~~ — `build.py` now includes explicit `--include-distribution-metadata` flags for `opentelemetry-api`, `opentelemetry-sdk`, `opentelemetry-semantic-conventions`, `anyio`, `uvicorn`, and `flask` instead of the unsupported wildcard `*`

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

### File Manager — فائل مینیجر
Better cross-platform file and directory management:
- Urdu-named wrappers around `pathlib`, `shutil`, and `os` — `فائل_کاپی()`, `فولڈر_بنائیں()`, `راستہ_ملائیں()`, `فائل_تلاش()`, `فائل_دیکھو()`
- File watcher (`فائل_نظارہ`) using `watchdog` — trigger Urdu callbacks on create/modify/delete events
- Cross-platform temp files, atomic writes, and file locking
- Glob and recursive search with Urdu filter syntax
- Windows: long path support (UNC `\\?\` prefix), ACL/permission helpers
- Linux: symlink management, `inotify` watcher
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

## Version Milestones (Tentative)

| Version | Focus |
|---------|-------|
| v1.1 | Bug fixes, CLI improvements, Linux binary, better `urdu مدد` |
| v1.2 | PyQt + PyGame libraries, macOS binary, Docker image |
| v1.3 | Django ORM, improved threading, Arduino, VS Code extension |
| v1.4 | OpenGL, Termux support, Jupyter kernel, `urdu بنائیں` command |
| v1.5 | TensorBoard library, native Urdu libraries (`اردو/ڈھانچے`, `اردو/الگورتھم`, `اردو/متن`) |
| v1.6 | Full package manager, Urdu package registry, `urdu شائع` |
| v1.7 | Official website, online playground, MicroPython subset, debugger |
| v1.8 | Binary/hex/assembly execution, OS-level registry & system access |
| v1.9 | Cross-platform file manager library, IntelliSense / LSP engine |
| v1.10 | HarmonyOS support, natural language synthesis (`اردو/آواز`, NLP) |
| v1.11 | GPU compute, bare-metal chip target, SIMD intrinsics, custom ISA simulator |

---

*اردو پروگرامنگ لینگویج — Mohammed Zahid Wadiwale*
