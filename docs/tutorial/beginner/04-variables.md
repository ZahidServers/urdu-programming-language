# 4. Variables — متغیرات

**Difficulty:** Beginner — مبتدی  
**Time:** ~15 minutes

---

## What Is a Variable? — متغیر کیا ہے؟

A variable is a named container that holds a value. Think of it as a labelled box where you store data to use later.

> **اردو:** متغیر ایک نامدار ڈبہ ہے جس میں قدر رکھی جاتی ہے۔ اسے ایک لیبل لگے ڈبے کے طور پر سوچیں جس میں ڈیٹا رکھتے ہیں تاکہ بعد میں استعمال کر سکیں۔

---

## Declaring a Variable — متغیر بنانا

Use the `متغیر` keyword:

```urdu
متغیر نام = "احمد";
متغیر عمر = 25;
متغیر قیمت = 99.5;
متغیر فعال = سچ;

لکھو(نام);     // احمد
لکھو(عمر);    // 25
لکھو(قیمت);   // 99.5
لکھو(فعال);   // True
```

**Pattern:** `متغیر` + name + `=` + value

> **اردو:** `متغیر` کلیدی لفظ لکھیں، پھر نام، پھر `=`، پھر قدر۔ بس اتنا کافی ہے۔

---

## Reassigning a Variable — قدر تبدیل کرنا

A variable declared with `متغیر` can be given a new value at any time:

```urdu
متغیر گنتی = 0;
لکھو(گنتی);    // 0

گنتی = 10;
لکھو(گنتی);    // 10

گنتی = گنتی + 5;
لکھو(گنتی);    // 15
```

> **اردو:** `متغیر` سے بنائے گئے متغیر کو جب چاہیں نئی قدر دے سکتے ہیں۔ `گنتی = گنتی + 5` کا مطلب: گنتی کی موجودہ قدر میں 5 جوڑو اور نتیجہ واپس گنتی میں رکھو۔

---

## Constants — مستقل

Use `مستقل` for values that should never change. Attempting to reassign a constant causes an error.

```urdu
مستقل پائی = 3.14159;
مستقل زبان = "اردو";
مستقل سال_قیام = 1947;

لکھو(پائی);          // 3.14159
لکھو(زبان);          // اردو
لکھو(سال_قیام);      // 1947

// پائی = 3.0;  // ← ERROR: cannot reassign a constant
```

> **اردو:** `مستقل` ایسی قدروں کے لیے جو کبھی نہیں بدلتیں: ریاضی کے ثوابت، ترتیبات، وغیرہ۔ دوبارہ اسائن کرنے پر غلطی آئے گی۔

---

## Naming Rules — نام رکھنے کے قواعد

| Rule | Example |
|------|---------|
| Can use Urdu script | `متغیر طالب_علم = "علی"` |
| Can use English letters | `متغیر studentName = "Ali"` |
| Can mix both | `متغیر myنام = "Ahmed"` |
| Must start with a letter or `_` | `متغیر _وقت = 0` ✓ |
| Cannot start with a digit | `متغیر 3رنگ = "سرخ"` ✗ |
| Cannot use reserved keywords | `متغیر اگر = 5` ✗ |
| Case-sensitive | `نام` and `نام2` are different |

> **اردو:** نام اردو، انگریزی، یا ملے جلے ہو سکتے ہیں۔ حرف یا `_` سے شروع ہونا لازم ہے۔ عدد سے شروع نہیں ہو سکتا۔ کلیدی الفاظ (جیسے `اگر`) بطور نام نہیں ہو سکتے۔

**Good naming examples — اچھے نام:**

```urdu
متغیر طالب_علم_نام = "زینب";
متغیر کل_قیمت = 1500;
متغیر محفوظ_ہے = سچ;
متغیر _خفیہ_کوڈ = "abc123";
متغیر totalCount = 0;
```

---

## Multiple Variables at Once — ایک ساتھ کئی متغیر

```urdu
// Declare multiple on one line
متغیر الف = 1, ب = 2, ج = 3;
لکھو(الف, ب, ج);    // 1 2 3

// Assign the same value to multiple variables
متغیر x, y, z;
x = y = z = 10;
لکھو(x, y, z);      // 10 10 10
```

> **اردو:** ایک ہی سطر میں کئی متغیرات بنا سکتے ہیں — کاما سے جدا کریں۔ زنجیری اسائنمنٹ `x = y = z = 10` سے تینوں ایک ساتھ 10 ہو جاتے ہیں۔

---

## Shorthand Assignment Operators — مختصر اسائنمنٹ آپریٹرز

```urdu
متغیر ن = 10;

ن += 5;    // ن = ن + 5  → 15
ن -= 3;    // ن = ن - 3  → 12
ن *= 2;    // ن = ن * 2  → 24
ن /= 4;    // ن = ن / 4  → 6
ن **= 2;   // ن = ن ** 2 → 36
ن %= 5;    // ن = ن % 5  → 1

لکھو(ن);    // 1
```

> **اردو:** `+=`، `-=`، `*=` وغیرہ مختصر لکھنے کا طریقہ ہے: `ن += 5` کا مطلب ہے `ن = ن + 5`۔

---

## Declaring Without a Value — بغیر قدر کے اعلان

A variable declared without a value is `غیر_معرف` (undefined) until assigned:

```urdu
متغیر رنگ;
لکھو(رنگ);     // None

رنگ = "نیلا";
لکھو(رنگ);     // نیلا
```

> **اردو:** اگر متغیر بناتے وقت قدر نہ دیں تو وہ `غیر_معرف` (None) ہوتا ہے۔ بعد میں جب چاہیں قدر دے سکتے ہیں۔

---

## Practical Example — عملی مثال

```urdu
// Simple shopping cart — آسان شاپنگ کارٹ
متغیر سیب_قیمت = 50;
متغیر کیلا_قیمت = 30;
متغیر آم_قیمت = 80;

متغیر سیب_تعداد = 3;
متغیر کیلا_تعداد = 6;
متغیر آم_تعداد = 2;

متغیر کل = (سیب_قیمت * سیب_تعداد) +
            (کیلا_قیمت * کیلا_تعداد) +
            (آم_قیمت * آم_تعداد);

لکھو("سیب:", سیب_قیمت * سیب_تعداد, "روپے");
لکھو("کیلا:", کیلا_قیمت * کیلا_تعداد, "روپے");
لکھو("آم:", آم_قیمت * آم_تعداد, "روپے");
لکھو("کل:", کل, "روپے");
```

Output:
```
سیب: 150 روپے
کیلا: 180 روپے
آم: 160 روپے
کل: 490 روپے
```

> **اردو:** یہ مثال دکھاتی ہے کہ متغیرات کیسے حقیقی مسئلے (شاپنگ بل) حل کرتے ہیں۔ قیمت اور تعداد الگ الگ رکھنے سے کوڈ سمجھنا آسان ہو جاتا ہے۔

---

## Key Points — اہم نکات

- `متغیر` declares a variable (can be reassigned)
- `مستقل` declares a constant (cannot be reassigned)
- Names can be in Urdu, English, or mixed
- Names cannot start with a digit or be a reserved keyword
- `+=`, `-=`, `*=` are shorthand for common operations

> **اردو:** `متغیر` قابل تبدیل ہے، `مستقل` نہیں۔ نام اردو میں لکھیں، عدد سے شروع نہ کریں۔

---

[← Previous: Hello World](03-hello-world.md) | [Next: Data Types →](05-data-types.md)
