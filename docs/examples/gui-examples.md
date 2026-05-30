# GUI Examples — گرافیکی مثالیں

Thirteen complete desktop GUI applications built with the `اردو/گوئی` library (a Tkinter-based framework). All examples are in the `examples/GUI/` folder.

> **اردو:** `اردو/گوئی` لائبریری (Tkinter پر مبنی فریم ورک) سے بنی تیرہ مکمل ڈیسک ٹاپ گرافیکی ایپلیکیشنیں۔ تمام مثالیں `examples/GUI/` فولڈر میں ہیں۔

**Install dependency:**

```
pip install ttkbootstrap
```

**Run any example:**

```
urdu run examples/GUI/01_HELLO_WORLD/app.urdu
```

---

## Table of Contents

1. [01 — Hello World](#01--hello-world)
2. [02 — Simple Calculator](#02--simple-calculator)
3. [03 — Full Calculator](#03--full-calculator)
4. [04 — Tic-Tac-Toe](#04--tic-tac-toe)
5. [05 — Rock Paper Scissors](#05--rock-paper-scissors)
6. [06 — Billing System (SQLite)](#06--billing-system-sqlite)
7. [07 — Billing System (MySQL)](#07--billing-system-mysql)
8. [08 — Billing System (Cassandra)](#08--billing-system-cassandra)
9. [09 — Billing System (PostgreSQL)](#09--billing-system-postgresql)
10. [10 — Billing System (MongoDB)](#10--billing-system-mongodb)
11. [11 — Website Downloader](#11--website-downloader)
12. [12 — Text Browser](#12--text-browser)
13. [13 — Crypto Tool](#13--crypto-tool)

---

## 01 — Hello World

**Source:** `examples/GUI/01_HELLO_WORLD/app.urdu`

A welcoming introduction to Urdu GUI programming. Shows the current date and time, an Islamic quote, and two buttons.

> **اردو:** اردو GUI پروگرامنگ کا ابتدائی تعارف۔ موجودہ تاریخ و وقت، ایک اسلامی اقتباس، اور دو بٹن دکھاتا ہے۔

**What it demonstrates:**
- Creating a window with `گوئی`
- Labels with heading styles (`h1`, `h2`)
- Buttons with click handlers (`پر_کلک`)
- Reading live date/time with `اردو/وقت`

**Key snippet:**

```urdu
درآمد { گوئی, کنٹینر, لیبل, بٹن } سے "اردو/گوئی";

متغیر ونڈو = نیا گوئی("ہیلو ورلڈ — اردو", 500, 400);
ونڈو.مرکز();
متغیر مرکزی = نیا کنٹینر(ونڈو, پیڈنگ=20);

نیا لیبل(مرکزی, "!ہیلو ورلڈ", کلاس="h1 text-primary fw-bold");
نیا بٹن(مرکزی, "سلام کریں %", کلاس="btn btn-primary p-2", پر_کلک=سلام_فنکشن);

ونڈو.چلائیں();
```

**Run:**
```
urdu run examples/GUI/01_HELLO_WORLD/app.urdu
```

---

## 02 — Simple Calculator

**Source:** `examples/GUI/02_SIMPLE_CALCULATOR/app.urdu`

A basic arithmetic calculator with a number pad and +, −, ×, ÷ operations.

> **اردو:** بنیادی حسابی کیلکولیٹر جس میں نمبر پیڈ اور جمع، تفریق، ضرب، تقسیم آپریشن ہیں۔

**What it demonstrates:**
- Grid-style button layout with `ردیف` / `کالم`
- Managing application state in a dictionary
- String-to-number conversion with `اعشاریہ()` / `عدد()`

**Run:**
```
urdu run examples/GUI/02_SIMPLE_CALCULATOR/app.urdu
```

---

## 03 — Full Calculator

**Source:** `examples/GUI/03_FULL_CALCULATOR/app.urdu`

An expression-based calculator that evaluates full arithmetic expressions including operator precedence.

> **اردو:** اظہار پر مبنی کیلکولیٹر جو آپریٹر ترجیح سمیت مکمل حسابی اظہارات کا حساب کرتا ہے۔

**What it demonstrates:**
- Storing and displaying a running expression string
- Using `.replace()` chain to parse multi-operator expressions
- `eval()` via Python interop for expression evaluation
- Backspace / clear operations on strings

**Run:**
```
urdu run examples/GUI/03_FULL_CALCULATOR/app.urdu
```

---

## 04 — Tic-Tac-Toe

**Source:** `examples/GUI/04_TICTACTOE/app.urdu`

A two-player Tic-Tac-Toe game with win detection and board reset.

> **اردو:** دو کھلاڑیوں کا ٹک ٹاک ٹو کھیل جس میں جیت کا پتہ لگانا اور بورڈ دوبارہ ترتیب دینا شامل ہے۔

**What it demonstrates:**
- 3×3 grid of buttons that update dynamically
- Win condition checking with nested loops
- Toggling state between two values with `اگر/ورنہ`
- Disabling buttons after a win

**Run:**
```
urdu run examples/GUI/04_TICTACTOE/app.urdu
```

---

## 05 — Rock Paper Scissors

**Source:** `examples/GUI/05_ROCK_PAPER_SCISSORS/app.urdu`

Rock-Paper-Scissors against the computer with a score counter and match history.

> **اردو:** کمپیوٹر کے خلاف پتھر-کاغذ-قینچی کھیل جس میں اسکور کاؤنٹر اور میچ تاریخ شامل ہے۔

**What it demonstrates:**
- Random choices with `اردو/بے_ترتیب`
- Conditional win logic across three outcomes
- Live label updates on button click

**Run:**
```
urdu run examples/GUI/05_ROCK_PAPER_SCISSORS/app.urdu
```

---

## 06 — Billing System (SQLite)

**Source:** `examples/GUI/06_BILLING_SQLITE/app.urdu`

A full billing and inventory management system backed by a local SQLite database.

> **اردو:** مقامی SQLite ڈیٹا بیس پر مبنی مکمل بلنگ اور انوینٹری مینجمنٹ سسٹم۔

**What it demonstrates:**
- Multi-tab UI with `ٹیب_ویو`
- SQLite CRUD via `اردو/ڈیٹا`
- Sortable table widget (`جدول`)
- Dialog boxes for confirmation (`ڈائیلاگ`)

**No external dependencies** — SQLite is built into Python.

**Run:**
```
urdu run examples/GUI/06_BILLING_SQLITE/app.urdu
```

---

## 07 — Billing System (MySQL)

**Source:** `examples/GUI/07_BILLING_MYSQL/app.urdu`

The same billing and inventory system as 06, but backed by a MySQL database (WAMP/XAMPP compatible).

> **اردو:** بلنگ سسٹم 06 جیسا ہی لیکن MySQL ڈیٹا بیس پر مبنی ہے۔ WAMP یا XAMPP کے ساتھ کام کرتا ہے۔

**Prerequisites:**
```
pip install mysql-connector-python
```
- MySQL running on `localhost:3306`
- Default credentials: `user=root`, `password=` (blank) — matches WAMP default

**What it demonstrates:**
- Connecting to MySQL with `mysql-connector-python` using `use_pure=True` (avoids C-extension crashes in the standalone binary)
- Auto-creating the `urdu_billing` database and tables on first run
- UTF-8 / `utf8mb4` charset support for Urdu text in column data

> **نوٹ:** `use_pure=سچ` — MySQL connector کا خالص Python نفاذ استعمال کریں۔ یہ Nuitka تعمیر شدہ `urdu.exe` میں C ایکسٹینشن (`_cmysql`) کے حادثے سے بچاتا ہے۔

**Run:**
```
urdu run examples/GUI/07_BILLING_MYSQL/app.urdu
```

If MySQL is not running, the app shows a "کنکشن ناکام" screen and exits cleanly when closed.

---

## 08 — Billing System (Cassandra)

**Source:** `examples/GUI/08_BILLING_CASSANDRA/app.urdu`

Billing and inventory system backed by Apache Cassandra, using UUIDs as primary keys.

> **اردو:** Apache Cassandra ڈیٹا بیس پر مبنی بلنگ سسٹم جو UUID کو بنیادی کلید کے طور پر استعمال کرتا ہے۔

**Prerequisites:**
```
pip install cassandra-driver
```
- Cassandra running on `localhost:9042`
- Recommended: Docker — `docker run -d -p 9042:9042 --name cassandra cassandra:5.0.8`

> **اہم:** Docker container کو `-p 9042:9042` کے ساتھ شروع کریں۔ پورٹ میپنگ کے بغیر `localhost:9042` کام نہیں کرے گا۔

**What it demonstrates:**
- Cassandra keyspace and table creation on startup
- UUID generation with `uuid.uuid4()`
- CQL SELECT / INSERT queries
- **Note:** CQL table and column names must be ASCII — Cassandra does not support Unicode identifiers

**Run:**
```
urdu run examples/GUI/08_BILLING_CASSANDRA/app.urdu
```

---

## 09 — Billing System (PostgreSQL)

**Source:** `examples/GUI/09_BILLING_POSTGRESQL/app.urdu`

Billing and inventory system backed by PostgreSQL with full CRUD operations.

> **اردو:** PostgreSQL ڈیٹا بیس پر مبنی مکمل CRUD بلنگ سسٹم۔

**Prerequisites:**
```
pip install psycopg2-binary
```
- PostgreSQL running on `localhost:5432`
- Credentials: `user=postgres`, `password=root` (pgAdmin default)

**What it demonstrates:**
- `psycopg2` connection with `autocommit=True`
- `RealDictCursor` for dictionary-style row access
- Auto-creating the `urdu_billing` database if it doesn't exist
- Parameterized queries to prevent SQL injection

**Run:**
```
urdu run examples/GUI/09_BILLING_POSTGRESQL/app.urdu
```

---

## 10 — Billing System (MongoDB)

**Source:** `examples/GUI/10_BILLING_MONGODB/app.urdu`

Billing and inventory system backed by MongoDB. Uses ObjectId for document identifiers.

> **اردو:** MongoDB ڈیٹا بیس پر مبنی بلنگ سسٹم جو ObjectId کو دستاویز شناخت کے لیے استعمال کرتا ہے۔

**Prerequisites:**
```
pip install pymongo
```
- MongoDB running on `localhost:27017`
- Requires MongoDB 4.2+ (wire protocol version 8)

**What it demonstrates:**
- `pymongo.MongoClient` with `serverSelectionTimeoutMS=3000`
- Collection-based document storage (no schema)
- ObjectId truncation for display (last 6 characters)
- Graceful connection failure handling

**Run:**
```
urdu run examples/GUI/10_BILLING_MONGODB/app.urdu
```

---

## 11 — Website Downloader

**Source:** `examples/GUI/11_WEBSITE_DOWNLOADER/app.urdu`

A GUI tool for downloading files and websites. Supports URL input, progress tracking, and save-to-folder selection.

> **اردو:** فائلیں اور ویب سائٹیں ڈاؤنلوڈ کرنے کا گرافیکی ٹول۔ URL ان پٹ، پیش رفت ٹریکنگ، اور فولڈر انتخاب کی سہولت دیتا ہے۔

**Prerequisites:**
```
pip install requests
```

**What it demonstrates:**
- Running downloads in a background thread (non-blocking UI)
- Progress bar widget integration
- File dialog for save-path selection
- `requests` streaming download with chunk writing

**Run:**
```
urdu run examples/GUI/11_WEBSITE_DOWNLOADER/app.urdu
```

---

## 12 — Text Browser

**Source:** `examples/GUI/12_TEXT_BROWSER/app.urdu`

A minimal text-mode web browser. Fetches a URL, strips HTML tags, and displays the readable text content.

> **اردو:** سادہ متنی ویب براؤزر۔ URL حاصل کرتا ہے، HTML ٹیگ ہٹاتا ہے، اور پڑھنے کے قابل متن دکھاتا ہے۔

**Prerequisites:**
```
pip install requests
```

**What it demonstrates:**
- Fetching web pages with `requests.get()`
- A custom `html_سے_متن()` tag-stripping function (character-by-character parser — no external HTML library needed)
- Browser-style navigation history (back / forward)
- Scrollable text widget

> **نوٹ:** HTML پارسنگ Urdu میں لکھی ہوئی کردار بہ کردار ریاستی مشین سے کی جاتی ہے کیونکہ `HTMLParser` کلاس سے وراثت اردو پارسر میں تعاون یافتہ نہیں ہے۔

**Run:**
```
urdu run examples/GUI/12_TEXT_BROWSER/app.urdu
```

---

## 13 — Crypto Tool

**Source:** `examples/GUI/13_CRYPTO_TOOL/app.urdu`

A cryptography workbench supporting AES encryption/decryption, RSA key generation and signing, and hashing (MD5, SHA-256, SHA-512).

> **اردو:** خفیہ نگاری ورک بنچ جو AES خفیہ کاری/ڈی خفیہ کاری، RSA کلید بنانا اور دستخط، اور ہیشنگ (MD5، SHA-256، SHA-512) کی سہولت دیتا ہے۔

**Prerequisites:**
```
pip install pycryptodome
```

**What it demonstrates:**
- AES-256 CBC mode encryption with key derivation
- RSA 2048-bit key pair generation
- RSA digital signatures and verification
- Multiple hash algorithms side-by-side
- Tab-based UI separating three cryptographic operations

**Tabs:**
| Tab | Function |
|-----|----------|
| AES | Encrypt/decrypt text with a passphrase |
| RSA | Generate key pair, sign a message, verify signature |
| ہیش | Hash any input with MD5, SHA-256, or SHA-512 |

**Run:**
```
urdu run examples/GUI/13_CRYPTO_TOOL/app.urdu
```

---

## Connection Failure Handling — کنکشن ناکام ہونے پر

All database-backed GUI apps (07–10) handle missing database connections gracefully:

1. Connection is attempted at startup inside a `کوشش/پکڑو` block.
2. If it fails, a red "کنکشن ناکام" message is shown in the window.
3. Closing the error window exits the application cleanly.
4. If the database IS available, the full multi-tab interface loads automatically.

> **اردو:** تمام ڈیٹا بیس ایپلیکیشنیں (07–10) اسٹارٹ اپ پر کنکشن آزماتی ہیں۔ ناکامی کی صورت میں ایک سرخ پیغام دکھایا جاتا ہے اور ونڈو بند کرنے پر ایپ صاف طور پر بند ہو جاتی ہے۔
