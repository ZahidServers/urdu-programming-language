# Standard Libraries — اردو لائبریریاں

The Urdu Programming Language ships with a rich set of built-in library modules. All are optional — install only what your project needs.

> **اردو:** اردو پروگرامنگ زبان میں بلٹ-ان لائبریری ماڈیولز کا ایک بھرپور مجموعہ ہے۔ سبھی اختیاری ہیں — صرف وہی نصب کریں جو آپ کے منصوبے کو چاہیے۔

---

## Library Modules — لائبریری ماڈیولز

| Module | Import path | Install | What it provides |
|--------|-------------|---------|-----------------|
| [Web Framework](web.md) | `"اردو/ویب"` | `pip install fastapi flask django uvicorn python-socketio websockets` | FastAPI, Flask, Django + ORM, WebSocket, Socket.IO, HTTP client |
| [Database](database.md) | `"اردو/ڈیٹا_بیس"` | `pip install mysql-connector-python psycopg2-binary pymongo aiosqlite` | SQLite, MySQL, PostgreSQL, MongoDB, Firebase, Cassandra |
| [Machine Learning](ml.md) | `"اردو/ذہین"` | `pip install numpy pandas scikit-learn tensorflow` | NumPy, Pandas, scikit-learn, TensorFlow, Keras, LLMs |
| [Cryptography](crypto.md) | `"اردو/رمز"` | `pip install cryptography bcrypt python-jose` | Hashing, Fernet, AES-256-GCM, RSA |
| [HTTP Client](http.md) | `"اردو/کرل"` | `pip install requests httpx aiohttp pycurl` | GET, POST, file upload, REST APIs |
| [Web Scraping](scraper.md) | `"اردو/کھرچنی"` | `pip install beautifulsoup4 lxml` | HTML parsing, CSS selectors, live fetching |
| [File Utilities](files.md) | `"اردو/فائلیں"` | `pip install openpyxl xlrd` | ZIP archives, Excel (.xlsx), CSV, path/dir helpers |
| [Threading](threading.md) | `"اردو/دھاگہ"` | *(built-in)* | Threads, thread pools, process pools, locks, events, futures |
| [Date & Time](datetime.md) | `"اردو/تاریخ"` | *(built-in)* | Gregorian dates, Islamic/Hijri calendar, durations |
| [Logging](logging.md) | `"اردو/لاگ"` | `pip install colorlog` | Structured logging, colours, file rotation, JSON |
| [Data Structures](structures.md) | `"اردو/ڈھانچے"` | *(built-in)* | Linked list, stack, queue, deque, priority queue, BST, graph |
| [Algorithms](algorithms.md) | `"اردو/الگورتھم"` | *(built-in)* | Sorting, searching, hash table, math (GCD/LCM/sieve), string algorithms |
| [Text Utilities](text.md) | `"اردو/متن"` | *(built-in)* | Urdu-aware string ops, diacritic removal, numeral conversion, similarity |
| [Arduino / Embedded](arduino.md) | `"اردو/آردوینو"` | `pip install pyfirmata2 pyserial` | Arduino boards, digital/analog I/O, PWM, servo, I2C, callbacks |
| [TensorBoard](tensorboard.md) | `"اردو/ٹینسر_بورڈ"` | `pip install tensorboard` | Metric logging, histograms, images, HParams, Keras callback |

---

## Quick Install — فوری نصب

Install all common dependencies at once:

```
pip install fastapi flask django uvicorn python-socketio websockets
pip install cryptography bcrypt requests httpx aiohttp beautifulsoup4 lxml
pip install numpy pandas scikit-learn openpyxl colorlog
```

Or use the built-in installer for a specific library:

```
python -m urdu نصب "اردو/ویب"
python -m urdu نصب "اردو/ڈیٹا_بیس"
python -m urdu نصب "اردو/رمز"
python -m urdu نصب "اردو/ذہین"
```

> **اردو:** مخصوص لائبریری کے لیے `python -m urdu نصب "اردو/ویب"` استعمال کریں — یہ تمام ضروری پیکیج خودکار نصب کرتا ہے۔

---

## Import Syntax — درآمد کی شکل

```urdu
// ایک یا زیادہ نام درآمد کریں
درآمد { فاسٹ_اے_پی_آئی } سے "اردو/ویب"
درآمد { تاریخ, مدت } سے "اردو/تاریخ"
درآمد { ہیش, AES, غیر_متناسق } سے "اردو/رمز"

// سب کچھ بطور نام فضا درآمد کریں
درآمد * بطور ریاضی سے "math"
```

> **اردو:** `درآمد { نام } سے "ماڈیول"` سے مخصوص نام درآمد کریں۔ `درآمد * بطور نام سے "ماڈیول"` سے پوری نام فضا درآمد کریں۔
