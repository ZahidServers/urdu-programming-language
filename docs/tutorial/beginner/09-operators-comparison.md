# 9. Comparison & Logical Operators — موازنہ اور منطقی آپریٹرز

**Difficulty:** Beginner — مبتدی  
**Time:** ~15 minutes

---

## Comparison Operators — موازنہ آپریٹرز

These compare two values and always return `سچ` or `جھوٹ`:

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | equal to — برابر | `5 == 5` | `سچ` |
| `!=` | not equal to — نابرابر | `5 != 6` | `سچ` |
| `<` | less than — کم | `5 < 10` | `سچ` |
| `>` | greater than — زیادہ | `5 > 10` | `جھوٹ` |
| `<=` | less or equal — کم یا برابر | `5 <= 5` | `سچ` |
| `>=` | greater or equal — زیادہ یا برابر | `5 >= 6` | `جھوٹ` |

```urdu
لکھو(5 == 5);     // True
لکھو(5 == 6);     // False
لکھو(5 != 6);     // True
لکھو(5 < 10);     // True
لکھو(5 > 10);     // False
لکھو(5 <= 5);     // True
لکھو(5 >= 6);     // False
```

> **اردو:** موازنہ آپریٹرز دو قدروں کو موازنہ کر کے `سچ` یا `جھوٹ` دیتے ہیں۔ `==` برابری جانچتا ہے — ایک `=` اسائنمنٹ ہے، دو `==` موازنہ۔

---

## Logical Operators — منطقی آپریٹرز

You can write logical operators in **Urdu words** or **symbols** — both work:

| Urdu | Symbol | Meaning | Example |
|------|--------|---------|---------|
| `اور` | `&&` | AND — اور | `سچ اور سچ` → `سچ` |
| `یا` | `\|\|` | OR — یا | `جھوٹ یا سچ` → `سچ` |
| `نہیں` | `!` | NOT — نہیں | `نہیں سچ` → `جھوٹ` |

```urdu
// AND — اور (both must be true)
لکھو(سچ اور سچ);     // True
لکھو(سچ اور جھوٹ);   // False

// OR — یا (at least one must be true)
لکھو(جھوٹ یا سچ);    // True
لکھو(جھوٹ یا جھوٹ);  // False

// NOT — نہیں (flips true/false)
لکھو(نہیں سچ);        // False
لکھو(نہیں جھوٹ);     // True
```

```urdu
// Symbol versions work too
لکھو(سچ && سچ);      // True
لکھو(جھوٹ || سچ);    // True
لکھو(!سچ);            // False
```

> **اردو:** `اور` (&&) دونوں شرطیں سچ ہوں تبھی سچ۔ `یا` (||) ایک بھی سچ ہو تو سچ۔ `نہیں` (!) سچ کو جھوٹ اور جھوٹ کو سچ بناتا ہے۔

---

## Combining Comparisons — موازنہ ملانا

```urdu
متغیر ن = 15;

// Both conditions must be true
لکھو(ن > 10 اور ن < 20);    // True   (15 is between 10 and 20)

// At least one condition must be true
لکھو(ن < 5 یا ن > 10);      // True   (15 > 10)

// Negation
لکھو(نہیں (ن == 15));        // False
```

> **اردو:** موازنہ آپریٹرز اور منطقی آپریٹرز ملا کر پیچیدہ شرطیں بنائیں۔

---

## Short-Circuit Evaluation — مختصر تشخیص

Urdu PL stops evaluating as soon as the result is determined:

```urdu
// اور: if first is false, second is never checked
متغیر ن = 0;
اگر (ن != 0 اور 10 / ن > 1) {
    لکھو("نہیں پہنچے گا");
} ورنہ {
    لکھو("محفوظ — n صفر ہے");    // this prints
}

// یا: if first is true, second is never checked
متغیر الف = "احمد";
اگر (الف != "" یا کچھ_فنکشن()) {
    لکھو("پہلی شرط سچ تھی");      // function never called
}
```

> **اردو:** `اور` میں پہلی شرط جھوٹ ہو تو دوسری چیک ہی نہیں ہوتی۔ `یا` میں پہلی شرط سچ ہو تو دوسری چیک نہیں ہوتی۔ اس سے غلطی سے بچاؤ ممکن ہے (جیسے صفر سے تقسیم)۔

---

## Ternary Operator — سہ رخی آپریٹر

A compact one-line if/else:

```urdu
متغیر عمر = 20;
متغیر نتیجہ = عمر >= 18 ? "بالغ" : "نابالغ";
لکھو(نتیجہ);    // بالغ

متغیر نمبر = 85;
لکھو(نمبر >= 50 ? "کامیاب" : "ناکام");    // کامیاب
```

**Pattern:** `شرط ? قدر_اگر_سچ : قدر_اگر_جھوٹ`

> **اردو:** `؟ :` (سہ رخی آپریٹر) مختصر `اگر/ورنہ` ہے۔ شرط سچ ہو تو پہلی قدر، جھوٹ ہو تو دوسری۔

---

## String Comparison — متن کا موازنہ

```urdu
لکھو("احمد" == "احمد");   // True
لکھو("احمد" == "علی");    // False
لکھو("ا" < "ب");           // True  (Unicode order)
```

> **اردو:** متن کا موازنہ یونیکوڈ ترتیب سے ہوتا ہے۔ `==` سے مساوات جانچیں۔

---

## Practical Example: Grade Checker — عملی مثال: نمبر جانچ

```urdu
فنکشن درجہ(نمبر) {
    اگر (نمبر >= 90) {
        واپس "A — ممتاز";
    } ورنہ_اگر (نمبر >= 75) {
        واپس "B — بہت اچھا";
    } ورنہ_اگر (نمبر >= 60) {
        واپس "C — اچھا";
    } ورنہ_اگر (نمبر >= 50) {
        واپس "D — قابل قبول";
    } ورنہ {
        واپس "F — ناکام";
    }
}

لکھو(درجہ(95));    // A — ممتاز
لکھو(درجہ(72));    // C — اچھا
لکھو(درجہ(45));    // F — ناکام
```

> **اردو:** موازنہ آپریٹرز کو `اگر/ورنہ_اگر/ورنہ` کے ساتھ ملا کر پیچیدہ فیصلے کریں۔

---

## Key Points — اہم نکات

- `==` tests equality; `=` is assignment — do not confuse them
- `!=`, `<`, `>`, `<=`, `>=` compare two values
- Use `اور` / `&&` and `یا` / `||` — Urdu keywords and symbols both work
- `نہیں` / `!` flips a boolean
- Ternary `شرط ? ا : ب` is a one-line if/else

> **اردو:** `==` برابری جانچتا ہے۔ `اور`/`&&`، `یا`/`||`، `نہیں`/`!` منطقی آپریٹرز۔ `? :` مختصر `اگر/ورنہ`۔

---

[← Previous: Arithmetic Operators](08-operators-arithmetic.md) | [Next: If / Else →](10-if-else.md)
