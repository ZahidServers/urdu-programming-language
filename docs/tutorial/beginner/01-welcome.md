# 1. Welcome & Overview — خوش آمدید

**Difficulty:** Beginner — مبتدی  
**Time:** ~5 minutes

---

## What Is the Urdu Programming Language? — اردو پروگرامنگ لینگویج کیا ہے؟

The **Urdu Programming Language** lets you write real, runnable programs using Urdu words instead of English. Instead of `if`, `while`, `function`, and `print`, you write `اگر`, `جبکہ`, `فنکشن`, and `لکھو`.

Under the hood, your `.urdu` file is converted to Python and run immediately. This means the entire Python ecosystem — web frameworks, databases, machine learning, data analysis — is available to you, all through Urdu syntax.

> **اردو:** **اردو پروگرامنگ لینگویج** آپ کو انگریزی کی بجائے اردو الفاظ استعمال کر کے حقیقی پروگرام لکھنے دیتی ہے۔ آپ کی `.urdu` فائل پردے کے پیچھے Python میں تبدیل ہو کر چلتی ہے — اس لیے Python کا پورا ماحولیاتی نظام: ویب فریم ورک، ڈیٹا بیس، مشین لرننگ — سب اردو نحو میں دستیاب ہے۔

---

## What Can You Build? — آپ کیا بنا سکتے ہیں؟

| Type | Examples |
|------|---------|
| **Web apps** | FastAPI REST APIs, Flask websites, Django apps with full ORM |
| **Desktop GUIs** | Tkinter-based windows, buttons, tables, dialogs |
| **Data analysis** | Load CSVs, compute statistics, export Excel with Pandas |
| **Machine learning** | Train classifiers, run LLMs, visualise with TensorBoard |
| **Databases** | SQLite, MySQL, PostgreSQL, MongoDB, Firebase, Cassandra |
| **Cryptography** | AES encryption, RSA keys, JWT tokens, password hashing |
| **Embedded / IoT** | Control Arduino boards over serial (Firmata) |
| **Scripts & automation** | File operations, HTTP calls, web scraping |

> **اردو:** آپ ویب ایپس، ڈیسک ٹاپ GUI، ڈیٹا تجزیہ، مشین لرننگ، ڈیٹا بیس، رمزنگاری، Arduino کنٹرول، اور آٹومیشن اسکرپٹس بنا سکتے ہیں — سب اردو میں۔

---

## A Quick Taste — ایک مختصر مثال

```urdu
// متغیر اور شرط — Variable and condition
متغیر نام = "احمد";
متغیر عمر = 20;

اگر (عمر >= 18) {
    لکھو(نام + " بالغ ہیں");
} ورنہ {
    لکھو(نام + " نابالغ ہیں");
}

// فنکشن — Function
فنکشن مربع(ن) {
    واپس ن * ن;
}

لکھو("4 کا مربع:", مربع(4));

// حلقہ — Loop
کے_لیے (متغیر عدد کا [1, 2, 3, 4, 5]) {
    لکھو(عدد, end=" ");
}
```

**Output:**
```
احمد بالغ ہیں
4 کا مربع: 16
1 2 3 4 5
```

> **اردو:** یہ چھوٹی مثال دکھاتی ہے: متغیر، شرط، فنکشن، اور حلقہ — سب اردو کلیدی الفاظ میں۔ باقی ٹیوٹوریل میں ہم ہر ایک کو تفصیل سے سیکھیں گے۔

---

## How the Language Works — یہ کیسے کام کرتا ہے

```
yourfile.urdu
      │
      ▼ Lexer — ٹوکن بناتا ہے
      │
      ▼ Parser — AST درخت بناتا ہے
      │
      ▼ Transpiler — Python کوڈ بناتا ہے
      │
      ▼ Python exec() — چلاتا ہے
```

You never see the generated Python — it is executed in memory and discarded. Your source file always stays in Urdu.

> **اردو:** آپ کو Python کبھی دیکھنے کی ضرورت نہیں — یہ میموری میں بنتا ہے، چلتا ہے، اور ختم ہو جاتا ہے۔ آپ کی سورس فائل ہمیشہ اردو میں رہتی ہے۔

---

## Key Points — اہم نکات

- Every keyword (`اگر`, `جبکہ`, `فنکشن`, …) is Urdu
- Variable names can be written entirely in Urdu script
- The full Python package ecosystem is available via `pip`
- Runs on Windows, macOS, and Linux (Python 3.8+ required)
- A standalone `urdu.exe` for Windows is available — no Python installation needed

> **اردو:** ہر کلیدی لفظ اردو میں ہے۔ متغیر کے نام مکمل اردو میں لکھے جا سکتے ہیں۔ pip کے تمام پیکیجز استعمال ہو سکتے ہیں۔ Windows کے لیے `urdu.exe` بھی ہے جسے Python نصب کیے بغیر چلایا جا سکتا ہے۔

---

[Next: Installation →](02-installation.md)
