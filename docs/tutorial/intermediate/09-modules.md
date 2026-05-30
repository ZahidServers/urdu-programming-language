# 9. Modules — ماڈیولز

**Difficulty:** Intermediate — متوسط  
**Time:** ~20 minutes

---

## What Is a Module? — ماڈیول کیا ہے؟

A module is a separate file of code that you can **import** and use in your program. Urdu PL has built-in modules for dates, files, databases, and more.

> **اردو:** ماڈیول الگ کوڈ کا ذخیرہ ہے جو `درآمد` سے اپنے پروگرام میں لایا جا سکتا ہے۔

---

## Import Syntax — درآمد نحو

**Import specific names:**
```urdu
درآمد { نام1, نام2 } سے "ماڈیول";
```

**Import everything:**
```urdu
درآمد * بطور عرف سے "ماڈیول";
```

**Import a single default:**
```urdu
درآمد نام سے "ماڈیول";
```

---

## Built-in Modules — بنا بنایا ماڈیولز

| Module Path | Purpose |
|-------------|---------|
| `"اردو/تاریخ"` | Date and time operations |
| `"اردو/فائلیں"` | File read/write |
| `"اردو/ویب"` | Web server (Flask-style) |
| `"اردو/ڈیٹا_بیس"` | SQLite database |
| `"اردو/دھاگہ"` | Threading |
| `"اردو/رمز"` | Cryptography |
| `"اردو/کرل"` | HTTP requests |
| `"اردو/ذہین"` | Machine learning |
| `"اردو/متن"` | Advanced text processing |
| `"اردو/لاگ"` | Logging |

---

## Using the Date Module — تاریخ ماڈیول

```urdu
درآمد { تاریخ, مدت } سے "اردو/تاریخ";

متغیر آج = تاریخ.آج();
لکھو(آج.سال);        // e.g. 2026
لکھو(آج.مہینہ);      // e.g. 5
لکھو(آج.دن);         // e.g. 30
لکھو(آج.دن_نام);     // e.g. ہفتہ

// Format
لکھو(آج.فارمیٹ("%d %B %Y"));    // 30 May 2026

// Arithmetic with مدت
متغیر اگلا_ہفتہ = آج + نیا مدت(ہفتے=1);
لکھو(متن(اگلا_ہفتہ));
```

> **اردو:** `تاریخ.آج()` آج کی تاریخ دیتا ہے۔ `مدت` کو جوڑنے کے لیے `+` آپریٹر استعمال کریں۔

---

## Python Standard Library Bridge — پایتھن ماڈیولز

You can import any Python standard library module via `"اردو/پایتھن"`:

```urdu
درآمد { json, os, random } سے "اردو/پایتھن";

لکھو(json.dumps({ "نام": "احمد", "عمر": 25 }));
لکھو(random.randint(1, 10));
```

---

## The ریاضی Object (built-in) — ریاضی آبجیکٹ

The math object is always available without importing:

```urdu
لکھو(ریاضی.پائی);         // 3.14159...
لکھو(ریاضی.جذر(25));      // 5.0
لکھو(ریاضی.فرش(3.7));     // 3
لکھو(ریاضی.چھت(3.2));     // 4
لکھو(ریاضی.سائن(0));       // 0.0
لکھو(ریاضی.لاگ(100));      // 4.605...
```

---

## Creating Your Own Module — اپنا ماڈیول بنانا

Save functions in a separate `.urdu` file and import them:

**math_helpers.urdu:**
```urdu
فنکشن دائرہ_رقبہ(رداس) {
    واپس ریاضی.پائی * رداس ** 2;
}

فنکشن مربع_محیط(ضلع) {
    واپس 4 * ضلع;
}
```

**main.urdu:**
```urdu
درآمد { دائرہ_رقبہ, مربع_محیط } سے "./math_helpers";

لکھو(گول(دائرہ_رقبہ(5), 2));    // 78.54
لکھو(مربع_محیط(6));               // 24
```

> **اردو:** اپنا ماڈیول بنانے کے لیے `.urdu` فائل میں فنکشنز لکھیں۔ `./` سے اسی فولڈر میں تلاش کریں، `"نام"` سے اردو ماڈیول۔

---

## Key Points — اہم نکات

- `درآمد { الف, ب } سے "ماڈیول"` — import named exports
- `درآمد * بطور عرف سے "ماڈیول"` — import all as alias
- Built-in modules: `"اردو/تاریخ"`, `"اردو/فائلیں"`, `"اردو/ویب"`, etc.
- `ریاضی` object is always available (no import needed)
- Create your own modules as `.urdu` files and import with `./path`

> **اردو:** `درآمد` سے لائبریریاں لائیں۔ `ریاضی` ہمیشہ موجود ہے۔ اپنے ماڈیول `.urdu` فائلوں میں بنائیں۔

---

[← Previous: Error Handling](08-error-handling.md) | [Next: File I/O →](10-file-io.md)
