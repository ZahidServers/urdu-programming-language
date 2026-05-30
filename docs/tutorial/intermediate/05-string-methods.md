# 5. String Methods — متن کے طریقے

**Difficulty:** Intermediate — متوسط  
**Time:** ~20 minutes

---

## Trimming — کاٹنا

Strings are immutable — every method returns a **new** string:

```urdu
متغیر م = "  السلام علیکم اردو  ";

لکھو(م.چھاٹو());           // السلام علیکم اردو     (trim both sides)
لکھو(م.شروع_چھاٹو());      // السلام علیکم اردو     (left only — trimStart)
لکھو(م.آخر_چھاٹو());       //   السلام علیکم اردو   (right only — trimEnd)
```

---

## Case Conversion — حروف کی تبدیلی

Works for ASCII letters:

```urdu
لکھو("hello world".بڑے_حروف());    // HELLO WORLD
لکھو("HELLO WORLD".چھوٹے_حروف()); // hello world
```

---

## Searching — تلاش

```urdu
متغیر جملہ = "اردو پروگرامنگ زبان ہے";

لکھو(جملہ.شامل_ہے("پروگرامنگ"));      // True   (includes)
لکھو(جملہ.شروع_ہے("اردو"));            // True   (startsWith)
لکھو(جملہ.ختم_ہے("ہے"));              // True   (endsWith)
لکھو(جملہ.مقام("زبان"));              // 15     (indexOf — اشاریہ)
لکھو(جملہ.مقام("جاوا"));              // -1     (not found)
لکھو("اردو اردو".آخری_مقام("اردو"));  // 5      (lastIndexOf)
```

---

## Replace — تبدیل کرنا

`.بدلو()` replaces **all** occurrences (maps to `replaceAll`):

```urdu
متغیر م = "ایک ایک ایک";
لکھو(م.بدلو("ایک", "دو"));   // دو دو دو

متغیر م2 = "السلام علیکم دنیا";
لکھو(م2.بدلو("دنیا", "اردو"));   // السلام علیکم اردو
```

> **اردو:** `.بدلو(پرانا, نیا)` تمام مطابقتیں بدلتا ہے۔

---

## Repeat and Pad — دہرانا اور پیڈنگ

```urdu
لکھو("ہا".دہراؤ(4));            // ہاہاہاہا
لکھو("-".دہراؤ(20));             // --------------------

لکھو("7".padStart(4, "0"));     // 0007   (pad from left)
لکھو("7".padEnd(4, "-"));       // 7---   (pad from right)
```

> **اردو:** `.دہراؤ(تعداد)` متن کو تعداد بار دہراتا ہے۔ `padStart`/`padEnd` ابھی اردو نام نہیں رکھتے۔

---

## Slice — کاٹنا

```urdu
متغیر م = "اردو پروگرامنگ";

لکھو(م.حصہ(0, 4));     // اردو
لکھو(م.حصہ(5));        // پروگرامنگ   (from index 5 to end)
لکھو(م.حصہ(-9));       // پروگرامنگ   (last 9 chars)
```

---

## Split — تقسیم

```urdu
// Built-in تقسیم() function
لکھو(تقسیم("احمد فاطمہ علی"));
// ['احمد', 'فاطمہ', 'علی']

لکھو(تقسیم("ایک,دو,تین", ","));
// ['ایک', 'دو', 'تین']

لکھو(تقسیم("a|b|c", "|"));
// ['a', 'b', 'c']
```

---

## Join — جوڑنا

```urdu
// For string lists — .جوڑو() method
متغیر ف = ["احمد", "فاطمہ", "علی"];
لکھو(ف.جوڑو(", "));    // احمد, فاطمہ, علی
لکھو(ف.جوڑو(" | "));   // احمد | فاطمہ | علی

// For any list — ربط() built-in
لکھو(ربط(" — ", ["ایک", "دو", "تین"]));    // ایک — دو — تین
لکھو(ربط(", ", [1, 2, 3]));                 // 1, 2, 3
```

---

## Template Strings — سانچہ متن

Embed variables and expressions with backticks and `${}`:

```urdu
متغیر نام = "احمد";
متغیر عمر = 25;

لکھو(`نام: ${نام}، عمر: ${عمر}`);
لکھو(`پیدائش: ${2026 - عمر}`);
لکھو(`${عمر >= 18 ? "بالغ" : "نابالغ"}`);
```

---

## Built-in Functions — بلٹ-ان فنکشنز

```urdu
// شامل — check substring (built-in)
لکھو(شامل("اردو پروگرامنگ", "اردو"));     // True
لکھو(شامل("اردو پروگرامنگ", "جاوا"));     // False

// لمبائی — length (built-in)
لکھو(لمبائی("السلام علیکم"));              // 13
```

---

## Quick Reference — فوری حوالہ

| Urdu Method | English | Meaning |
|-------------|---------|---------|
| `.چھاٹو()` | `.trim()` | remove surrounding spaces |
| `.شروع_چھاٹو()` | `.trimStart()` | remove left spaces |
| `.آخر_چھاٹو()` | `.trimEnd()` | remove right spaces |
| `.بڑے_حروف()` | `.toUpperCase()` | uppercase |
| `.چھوٹے_حروف()` | `.toLowerCase()` | lowercase |
| `.شامل_ہے(س)` | `.includes(s)` | contains substring |
| `.شروع_ہے(س)` | `.startsWith(s)` | starts with |
| `.ختم_ہے(س)` | `.endsWith(s)` | ends with |
| `.مقام(س)` | `.indexOf(s)` | first occurrence index |
| `.آخری_مقام(س)` | `.lastIndexOf(s)` | last occurrence index |
| `.بدلو(پ, ن)` | `.replaceAll(o, n)` | replace all occurrences |
| `.دہراؤ(ن)` | `.repeat(n)` | repeat n times |
| `.حصہ(ا, آ)` | `.slice(a, b)` | substring |

> **اردو:** تمام متن کے طریقے نئی کاپی دیتے ہیں — اصل نہیں بدلتی۔

---

[← Previous: Array Methods](04-array-methods.md) | [Next: Classes →](06-classes.md)
