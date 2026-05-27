# Examples — مثالیں

Complete, runnable program examples for the Urdu Programming Language. Every example is in the `examples/` folder of the repository.

> **اردو:** اردو پروگرامنگ زبان کے مکمل، قابل چلانے پروگرام کی مثالیں۔ ہر مثال ریپوزیٹری کے `examples/` فولڈر میں ہے۔

---

## Getting Started — شروع کرنا

| Example | Description | Source |
|---------|-------------|--------|
| [Hello World](hello-world.md) | Absolute basics — `لکھو`, variables, input, arithmetic, comments | inline |
| [Quick Start Guide](../quick-start.md) | 10-step tour of the full language | inline |

---

## Web Applications — ویب ایپلیکیشنز

| Example | Framework | Description | Source |
|---------|-----------|-------------|--------|
| [Web Server Examples](web-server.md) | FastAPI | Todo REST API, HTML web app, WebSocket chat | inline |
| [FastAPI Socket.IO Chat](fastapi-socket-chat.md) | FastAPI + Socket.IO | Real-time multi-user chat with ASGI | `FASTAPI_SOCKET_CHAT_APP/` |
| [Flask Blog](flask-blog.md) | Flask | Multi-page blog with Urdu Jinja2 templates | `FLASK_BLOG_App/` |
| [Flask Billing System](flask-billing.md) | Flask + SQLite | Invoice management with async DB helpers | `FLASK_BILLING_APP/` |
| [Flask MySQL Books](flask-mysql-books.md) | Flask + MySQL | Library catalogue with search and pagination | `FLASK_MYSQL_BOOKS_APP/` |
| [Django Calculator](django-calc.md) | Django + Socket.IO | Real-time calculator with history | `DJANGO_CALC_APP/` |

---

## Data & Analysis — ڈیٹا اور تجزیہ

| Example | Libraries | Description | Source |
|---------|-----------|-------------|--------|
| [Data Analysis](data-analysis.md) | Pandas, NumPy | CSV loading, statistics, filtering, Excel export | inline |
| [Web Scraping](web-scraping.md) | اردو/کھرچنی | Parse HTML, CSS selectors, scrape live sites | inline |

---

## Internal Diagnostic Scripts — اندرونی تشخیصی اسکرپٹ

| Script | What it tests |
|--------|---------------|
| [Diagnostic Scripts](diagnostic-scripts.md) | `test_ctypes.urdu`, `test_ctypes2.urdu`, `test_uvicorn.urdu` — verify asyncio, ctypes, and uvicorn work in the compiled executable |

---

## How to Run Any Example — کوئی بھی مثال کیسے چلائیں

### From source (Python installed)

```
python -m urdu run examples/FLASK_BLOG_App/app.urdu
```

### From the compiled executable

```
urdu.exe run examples/FLASK_BLOG_App/app.urdu
```

### Install dependencies first

Each example lists its dependencies at the top of the doc page. For web examples:

```
pip install flask
pip install fastapi uvicorn python-socketio
pip install django werkzeug
pip install mysql-connector-python   # for MySQL examples
```

> **اردو:** ہر مثال اپنے صفحے کے اوپر انحصارات درج کرتی ہے۔ ویب مثالوں کے لیے Flask، FastAPI یا Django نصب کریں۔ ڈیٹا بیس مثالوں کے لیے متعلقہ ڈیٹا بیس کنیکٹر نصب کریں۔
