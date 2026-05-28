# Text Utilities — اردو/متن

The `اردو/متن` library provides Urdu-named string operations — both general-purpose string helpers and Urdu-specific functions (diacritic removal, Nastaliq normalisation, numeral conversion, word tokenisation, and similarity scoring). No pip install needed.

> **اردو:** `اردو/متن` لائبریری اردو نامی متن آپریشن فراہم کرتی ہے — عام اسٹرنگ مددگار اور اردو مخصوص فنکشن (اعراب ہٹانا، نستعلیق معیاری سازی، اعداد تبدیل کرنا، الفاظ توڑنا، مماثلت)۔ کوئی نصب کاری ضروری نہیں۔

**Import:**

```urdu
درآمد {
    بڑے_حروف, چھوٹے_حروف, عنوانی, الٹا_کریں,
    تراشو, تقسیم, ملائیں, بدلیں, گنو,
    شروع_سے, آخر_سے, تلاش_کریں, ذیل_متن,
    پیڈ_بائیں, پیڈ_دائیں, پیڈ_وسط, صفر_بھریں,
    ریجیکس_تلاش, ریجیکس_بدلیں, ریجیکس_تمام,
    اعراب_ہٹائیں, نستعلیق_معیاری, الفاظ,
    اردو_حروف_ہیں, ہندی_اعداد, ہندی_اعداد_میں,
    اردو_میں_گنتی, مماثلت,
    انکوڈ, ڈیکوڈ, حروف_گنو, ایک_جیسا_ہے
} سے "اردو/متن"
```

---

## General String Operations — عام متن آپریشن

### Case & Transformation

```urdu
لکھو(بڑے_حروف("hello"))       // "HELLO"
لکھو(چھوٹے_حروف("URDU"))      // "urdu"
لکھو(عنوانی("اردو زبان"))      // "اردو زبان"
لکھو(الٹا_کریں("اردو"))        // "وڈرا"
```

| Function | Python equivalent | Description |
|----------|-------------------|-------------|
| `بڑے_حروف(متن)` | `.upper()` | All uppercase |
| `چھوٹے_حروف(متن)` | `.lower()` | All lowercase |
| `عنوانی(متن)` | `.title()` | Title case |
| `الٹا_کریں(متن)` | `متن[::-1]` | Reverse string |

---

### Trim & Pad

```urdu
لکھو(تراشو("  اردو  "))               // "اردو"
لکھو(بائیں_تراشو("###کتاب", "#"))     // "کتاب"
لکھو(پیڈ_بائیں("5", 4, "0"))          // "0005"
لکھو(پیڈ_دائیں("اردو", 8))            // "اردو    "
لکھو(پیڈ_وسط("اردو", 10, "-"))        // "---اردو---"
```

| Function | Description |
|----------|-------------|
| `تراشو(متن, حروف=None)` | Strip whitespace / given chars from both sides |
| `بائیں_تراشو(متن, حروف=None)` | Strip from left |
| `دائیں_تراشو(متن, حروف=None)` | Strip from right |
| `پیڈ_بائیں(متن, چوڑائی, حرف=" ")` | Left-justify (pad right) |
| `پیڈ_دائیں(متن, چوڑائی, حرف=" ")` | Right-justify (pad left) |
| `پیڈ_وسط(متن, چوڑائی, حرف=" ")` | Center |
| `صفر_بھریں(متن, چوڑائی)` | Zero-pad numeric string |

---

### Split, Join, Replace

```urdu
لکھو(تقسیم("الف,ب,ج", ","))         // ["الف", "ب", "ج"]
لکھو(ملائیں(" - ", ["الف", "ب", "ج"])) // "الف - ب - ج"
لکھو(بدلیں("اردو اردو", "اردو", "Urdu"))  // "Urdu Urdu"
لکھو(بدلیں("اردو اردو", "اردو", "Urdu", 1)) // "Urdu اردو"
```

| Function | Description |
|----------|-------------|
| `تقسیم(متن, جدا=None, زیادہ=-1)` | Split on separator; `-1` = unlimited |
| `سطر_تقسیم(متن)` | Split on newlines |
| `ملائیں(جوڑ, فہرست)` | Join list with separator |
| `بدلیں(متن, پرانا, نیا, گنتی=-1)` | Replace occurrences; limit with `گنتی` |
| `گنو(متن, ذیل)` | Count occurrences of substring |

---

### Search & Test

```urdu
لکھو(تلاش_کریں("اردو زبان", "زبان"))   // 5
لکھو(شروع_سے("اردو", "ار"))            // True
لکھو(آخر_سے("اردو", "دو"))             // True
لکھو(موجود_ہے("اردو زبان", "زبان"))    // True
لکھو(صرف_اعداد("12345"))               // True
لکھو(صرف_حروف("hello"))                // True
```

| Function | Description |
|----------|-------------|
| `تلاش_کریں(متن, ذیل, آغاز=0)` | Index of first occurrence, or `-1` |
| `ذیل_متن(متن, آغاز, آخر=None)` | Slice `متن[آغاز:آخر]` |
| `شروع_سے(متن, پیشوند)` | `startswith` |
| `آخر_سے(متن, لاحقہ)` | `endswith` |
| `موجود_ہے(متن, ذیل)` | Substring membership |
| `خالی_ہے(متن)` | `True` if blank / whitespace only |
| `صرف_اعداد(متن)` | All digits? |
| `صرف_حروف(متن)` | All alphabetic? |
| `لمبائی(متن)` | `len(متن)` |

---

### Regex

```urdu
متغیر م = ریجیکس_تلاش(r"\d+", "قیمت: 450 روپے")
لکھو(م.group())                              // "450"

لکھو(ریجیکس_بدلیں(r"\d+", "***", "ص 123 ص"))  // "ص *** ص"

لکھو(ریجیکس_تمام(r"\d+", "1 اور 2 اور 3"))    // ["1", "2", "3"]
```

| Function | Description |
|----------|-------------|
| `ریجیکس_تلاش(نمونہ, متن)` | `re.search` — returns match object or `None` |
| `ریجیکس_بدلیں(نمونہ, نیا, متن)` | `re.sub` |
| `ریجیکس_تمام(نمونہ, متن)` | `re.findall` — returns list of all matches |

---

## Urdu-Specific Functions — اردو مخصوص فنکشن

### Diacritics & Normalisation

```urdu
متغیر اعراب_والا = "کِتَابُ"
لکھو(اعراب_ہٹائیں(اعراب_والا))    // "کتاب"

لکھو(نستعلیق_معیاری("كتاب"))      // "کتاب"  (Arabic kaf/ya → Urdu equivalents)
```

| Function | Description |
|----------|-------------|
| `اعراب_ہٹائیں(متن)` | Remove diacritical marks (زیر/زبر/پیش etc.) |
| `نستعلیق_معیاری(متن)` | Normalise Arabic glyphs to Urdu equivalents, remove diacritics, NFC |

---

### Word Tokenisation

```urdu
متغیر جملہ = "اردو بولنے والے دنیا بھر میں ہیں"
لکھو(الفاظ(جملہ))    // ["اردو", "بولنے", "والے", "دنیا", "بھر", "میں", "ہیں"]

لکھو(اردو_حروف_ہیں("hello"))    // False
لکھو(اردو_حروف_ہیں("اردو"))     // True
```

| Function | Description |
|----------|-------------|
| `الفاظ(متن)` | Tokenise into Urdu/Arabic words — ignores punctuation and Latin |
| `اردو_حروف_ہیں(متن)` | Returns `True` if the string contains any Urdu/Arabic characters |

---

### Numeral Conversion

```urdu
لکھو(ہندی_اعداد("۲۰۲۶"))        // "2026"
لکھو(ہندی_اعداد_میں("2026"))    // "۲۰۲۶"

لکھو(اردو_میں_گنتی(42))         // "بیالیس"
لکھو(اردو_میں_گنتی(1001))       // "ایک ہزار ایک"
لکھو(اردو_میں_گنتی(2500000))    // "پچیس لاکھ"
لکھو(اردو_میں_گنتی(-7))         // "منفی سات"
```

| Function | Description |
|----------|-------------|
| `ہندی_اعداد(متن)` | Eastern Arabic digits (۰–۹) → Western (0–9) |
| `ہندی_اعداد_میں(متن)` | Western digits (0–9) → Eastern Arabic (۰–۹) |
| `اردو_میں_گنتی(ن)` | Integer → Urdu words (supports کروڑ scale, negative numbers) |

---

### Similarity & Comparison

```urdu
لکھو(مماثلت("اردو", "اردو"))       // 1.0
لکھو(مماثلت("کتاب", "کتابیں"))     // 0.625 (approx)
لکھو(مماثلت("hello", "helo"))      // 0.8

لکھو(ایک_جیسا_ہے("URDU", "urdu", حساسیت=جھوٹ))  // True
```

| Function | Description |
|----------|-------------|
| `مماثلت(الف, ب)` | Levenshtein-based similarity — `0.0` (completely different) to `1.0` (identical) |
| `ایک_جیسا_ہے(الف, ب, حساسیت=True)` | Equality check; `حساسیت=False` for case-insensitive |

---

### Encoding & Misc

```urdu
لکھو(انکوڈ("اردو"))                    // b'\xd8\xa7\xd8\xb1\xd8\xaf\xd9\x88'
لکھو(ڈیکوڈ(b'\xd8\xa7\xd8\xb1\xd8\xaf\xd9\x88'))  // "اردو"
لکھو(حروف_گنو("اردو اردو"))           // {'ا': 2, 'ر': 2, 'د': 2, 'و': 2, ' ': 1}
لکھو(دہرائیں("اردو ", 3))              // "اردو اردو اردو "
```

| Function | Description |
|----------|-------------|
| `انکوڈ(متن, کوڈنگ="utf-8")` | Encode string to bytes |
| `ڈیکوڈ(بائٹس, کوڈنگ="utf-8")` | Decode bytes to string |
| `حروف_گنو(متن)` | Character frequency dict |
| `دہرائیں(متن, تعداد)` | Repeat string n times |
