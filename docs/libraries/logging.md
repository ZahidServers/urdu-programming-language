# Logging Library — اردو/لاگ

The `اردو/لاگ` library provides structured application logging with optional coloured console output, file output, JSON formatting, and rotating file handlers.

> **اردو:** `اردو/لاگ` لائبریری منظم لاگنگ (logging) فراہم کرتی ہے — رنگدار کنسول آؤٹ پٹ، فائل آؤٹ پٹ، JSON فارمیٹنگ، اور گھماؤ فائل ہینڈلر کے ساتھ۔

**Import:**

```urdu
درآمد { لاگر } سے "اردو/لاگ"
```

---

## Table of Contents — فہرست مضامین

1. [Constructor](#constructor)
2. [Configuration Options](#configuration-options)
3. [Log Level Constants — سطح](#log-level-constants--سطح)
4. [Logging Methods](#logging-methods)
5. [Examples](#examples)

---

## Constructor — تعمیر

```urdu
متغیر لاگ = نیا لاگر(نام, ترتیب)
```

> **اردو:** لاگر (logger) بنانے کے لیے نام اور اختیاری ترتیب دیں۔ نام ہر پیغام میں ظاہر ہوگا۔

| Parameter | Type | Description |
|-----------|------|-------------|
| `نام` | string | Logger name shown in every message |
| `ترتیب` | object | Optional configuration (all keys optional) |

**Minimal setup:**

```urdu
متغیر لاگ = نیا لاگر("ایپ")
```

**Full setup:**

```urdu
متغیر لاگ = نیا لاگر("ایپ", {
    سطح_:   20,
    فائل:   "لاگز/app.log",
    رنگ:    سچ,
    جیسن:   جھوٹ,
    گھماؤ:  سچ,
    زیادہ_سائز: 10 * 1024 * 1024,
    نسخے:   5
})
```

---

## Configuration Options — ترتیب کے اختیارات

> **اردو:** یہ اختیارات لاگر کی فائل (file)، سطح (level)، اور فارمیٹ کو کنٹرول کرتے ہیں۔

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `سطح_` | int | `20` | Minimum level to emit (see table below) |
| `فائل` | string | `null` | File path for log output (null = console only) |
| `رنگ` | bool | `سچ` | Coloured terminal output (ANSI) |
| `جیسن` | bool | `جھوٹ` | Emit each line as a JSON object |
| `گھماؤ` | bool | `جھوٹ` | Use a rotating file handler |
| `زیادہ_سائز` | int | `10485760` | Max file size in bytes before rotation (10 MB) |
| `نسخے` | int | `5` | Number of rotated backup files to keep |

---

## Log Level Constants — سطح

Import the `سطح` namespace if you want symbolic names:

> **اردو:** سطح (level) سے پیغام کی اہمیت ظاہر ہوتی ہے — ڈیبگ (debug) سب سے کم، بحران (critical) سب سے زیادہ۔

```urdu
درآمد { لاگر, سطح } سے "اردو/لاگ"
```

| Constant | Int | English |
|----------|-----|---------|
| `سطح.ڈیبگ` | `10` | DEBUG |
| `سطح.معلومات` | `20` | INFO |
| `سطح.تنبیہ` | `30` | WARNING |
| `سطح.غلطی` | `40` | ERROR |
| `سطح.بحران` | `50` | CRITICAL |

---

## Logging Methods — لاگنگ کے طریقے

Each method has both an Urdu name and an English alias.

> **اردو:** ہر طریقے کا اردو نام اور انگریزی عرف (alias) دونوں استعمال کیے جا سکتے ہیں۔

| Urdu method | English alias | Level | Colour |
|-------------|--------------|-------|--------|
| `لاگ.ڈیبگ(پیغام)` | `لاگ.debug(پیغام)` | 10 | grey |
| `لاگ.معلومات(پیغام)` | `لاگ.info(پیغام)` | 20 | cyan |
| `لاگ.تنبیہ(پیغام)` | `لاگ.warn(پیغام)` | 30 | yellow |
| `لاگ.غلطی(پیغام, استثناء=جھوٹ)` | `لاگ.error(پیغام)` | 40 | red |
| `لاگ.بحران(پیغام)` | `لاگ.critical(پیغام)` | 50 | bold red |

Pass `استثناء=سچ` (or an exception object) to `غلطی()` to include a stack trace in the log output.

**Output format (text mode):**

```
2026-05-19 14:30:45 [INFO] ایپ: سرور شروع ہو گیا پورٹ 8000 پر
2026-05-19 14:30:46 [WARNING] ایپ: میموری 80% سے زیادہ استعمال
2026-05-19 14:30:47 [ERROR] ایپ: ڈیٹابیس سے رابطہ ناکام
```

**Output format (JSON mode, `جیسن=سچ`):**

```json
{"وقت": "2026-05-19T14:30:45", "سطح": "INFO", "نام": "ایپ", "پیغام": "سرور شروع ہو گیا"}
```

---

## Examples — مثالیں

### Example 1 — Basic logging

> **اردو:** مثال ۱ — بنیادی لاگ (log) پیغامات

```urdu
درآمد { لاگر } سے "اردو/لاگ"

متغیر لاگ = نیا لاگر("میرا_پروگرام")

لاگ.ڈیبگ("ڈیبگ پیغام — تفصیلی معلومات")
لاگ.معلومات("پروگرام شروع ہو گیا")
لاگ.تنبیہ("یہ آگاہی ہے، کچھ غلط نہیں")
لاگ.غلطی("کچھ غلط ہوا")
لاگ.بحران("سنگین خرابی!")
```

**Output:**

```
2026-05-19 12:00:00 [DEBUG]    میرا_پروگرام: ڈیبگ پیغام — تفصیلی معلومات
2026-05-19 12:00:00 [INFO]     میرا_پروگرام: پروگرام شروع ہو گیا
2026-05-19 12:00:00 [WARNING]  میرا_پروگرام: یہ آگاہی ہے، کچھ غلط نہیں
2026-05-19 12:00:00 [ERROR]    میرا_پروگرام: کچھ غلط ہوا
2026-05-19 12:00:00 [CRITICAL] میرا_پروگرام: سنگین خرابی!
```

### Example 2 — Log to file with rotation

> **اردو:** مثال ۲ — فائل میں لاگ لکھنا اور گھماؤ (rotation) کے ساتھ سطح (level) کا انتخاب

```urdu
درآمد { لاگر, سطح } سے "اردو/لاگ"

متغیر لاگ = نیا لاگر("ویب_سرور", {
    سطح_:   سطح.معلومات,    // DEBUG پیغامات نہ لکھو
    فائل:   "لاگز/server.log",
    رنگ:    سچ,
    گھماؤ:  سچ,
    زیادہ_سائز: 5 * 1024 * 1024,   // 5MB
    نسخے:   10
})

فنکشن درخواست_لاگ_کرو(طریقہ, راستہ, حالت) {
    متغیر پیغام = `${طریقہ} ${راستہ} → ${حالت}`;
    اگر (حالت >= 500) {
        لاگ.غلطی(پیغام);
    } ورنہ_اگر (حالت >= 400) {
        لاگ.تنبیہ(پیغام);
    } ورنہ {
        لاگ.معلومات(پیغام);
    }
}

درخواست_لاگ_کرو("GET",    "/",           200)
درخواست_لاگ_کرو("POST",   "/login",       200)
درخواست_لاگ_کرو("GET",    "/admin",       403)
درخواست_لاگ_کرو("DELETE", "/users/99",    404)
درخواست_لاگ_کرو("POST",   "/api/data",    500)
```

### Example 3 — JSON logging for log aggregators

> **اردو:** مثال ۳ — ELK / Splunk / CloudWatch کے لیے JSON فارمیٹ میں لاگ لکھنا

```urdu
درآمد { لاگر, سطح } سے "اردو/لاگ"

// JSON فارمیٹ — ELK / Splunk / CloudWatch کے لیے
متغیر لاگ = نیا لاگر("api_سروس", {
    سطح_:  سطح.ڈیبگ,
    فائل:  "لاگز/api.jsonl",
    جیسن:  سچ,
    رنگ:   جھوٹ
})

لاگ.معلومات("API سرور شروع ہوا")
لاگ.ڈیبگ("ترتیبات لوڈ ہوئیں")
لاگ.تنبیہ("ریٹ لمٹ سے قریب")
```

**Output (لاگز/api.jsonl):**

```json
{"timestamp": "2026-05-19T12:00:00.123", "level": "INFO", "logger": "api_سروس", "message": "API سرور شروع ہوا"}
{"timestamp": "2026-05-19T12:00:00.124", "level": "DEBUG", "logger": "api_سروس", "message": "ترتیبات لوڈ ہوئیں"}
{"timestamp": "2026-05-19T12:00:00.125", "level": "WARNING", "logger": "api_سروس", "message": "ریٹ لمٹ سے قریب"}
```

### Example 4 — Exception logging with stack trace

> **اردو:** مثال ۴ — استثناء (exception) کا سٹیک ٹریس لاگ کرنا

```urdu
درآمد { لاگر } سے "اردو/لاگ"

متغیر لاگ = نیا لاگر("ڈیٹابیس", {
    فائل: "لاگز/errors.log",
    سطح_: 10
})

فنکشن ڈیٹابیس_سے_پڑھو(سوال) {
    لاگ.ڈیبگ(`سوال: ${سوال}`);
    کوشش {
        // ... ڈیٹابیس کوڈ ...
        پھینکو نیا Error("Connection refused");
    } پکڑو (ے) {
        لاگ.غلطی(`ڈیٹابیس سوال ناکام: ${ے.message}`, استثناء=ے);
        واپس خالی;
    }
}

ڈیٹابیس_سے_پڑھو("SELECT * FROM users");
```

### Example 5 — Multiple loggers (one per module)

> **اردو:** مثال ۵ — ہر ماڈیول (module) کا اپنا لاگر

```urdu
درآمد { لاگر, سطح } سے "اردو/لاگ"

// ہر ماڈیول کا اپنا لاگر
متغیر auth_لاگ = نیا لاگر("auth",     { فائل: "لاگز/app.log" })
متغیر db_لاگ   = نیا لاگر("database", { فائل: "لاگز/app.log" })
متغیر api_لاگ  = نیا لاگر("api",      { فائل: "لاگز/app.log" })

فنکشن لاگ_ان_کرو(نام, پاسورڈ) {
    auth_لاگ.ڈیبگ(`لاگ ان کوشش: ${نام}`);
    اگر (نام == "admin" اور پاسورڈ == "secret") {
        auth_لاگ.معلومات(`لاگ ان کامیاب: ${نام}`);
        واپس سچ;
    } ورنہ {
        auth_لاگ.تنبیہ(`ناکام لاگ ان: ${نام}`);
        واپس جھوٹ;
    }
}

فنکشن سوال_چلاؤ(sql) {
    db_لاگ.ڈیبگ(`SQL: ${sql}`);
    db_لاگ.معلومات("سوال مکمل");
}

فنکشن API_درخواست(endpoint) {
    api_لاگ.معلومات(`GET ${endpoint}`);
}

لاگ_ان_کرو("admin", "secret")
لاگ_ان_کرو("hacker", "wrong")
سوال_چلاؤ("SELECT * FROM users WHERE active=1")
API_درخواست("/api/users")
```

### Example 6 — Production-ready logger setup

> **اردو:** مثال ۶ — پروڈکشن اور ڈیولپمنٹ ماحول کے لیے لاگر ترتیب دینا

```urdu
درآمد { لاگر, سطح } سے "اردو/لاگ"

// ─── پروڈکشن ترتیب ───────────────────────────
فنکشن لاگر_بنائیں(نام, پروڈکشن=جھوٹ) {
    اگر (پروڈکشن) {
        واپس نیا لاگر(نام, {
            سطح_:   سطح.معلومات,    // DEBUG لاگ نہ کرو
            فائل:   `لاگز/${نام}.log`,
            رنگ:    جھوٹ,
            جیسن:   سچ,
            گھماؤ:  سچ,
            زیادہ_سائز: 50 * 1024 * 1024,  // 50MB
            نسخے:   30
        });
    } ورنہ {
        واپس نیا لاگر(نام, {
            سطح_:  سطح.ڈیبگ,
            رنگ:   سچ,
            جیسن:  جھوٹ
        });
    }
}

// ─── استعمال ─────────────────────────────────
متغیر ماحول = "development"  // یا "production"
متغیر لاگ = لاگر_بنائیں("پروگرام", ماحول == "production")

لاگ.معلومات("پروگرام شروع")
لاگ.ڈیبگ("ڈیبگ موڈ فعال")
```

---

*Previous: [Date & Time →](datetime.md) | Next: [Threading →](threading.md)*
