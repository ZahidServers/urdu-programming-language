# Strings — سٹرنگز

Strings represent text. This document covers all string creation forms, template literals, built-in string methods with their Urdu names, and practical string-handling patterns.

> **اردو:** سٹرنگز متن کو ظاہر کرتی ہیں۔ یہ دستاویز سٹرنگ بنانے کی تمام شکلیں، ٹیمپلیٹ لٹریلز، اردو ناموں کے ساتھ بنا بنایا سٹرنگ طریقے، اور عملی سٹرنگ سنبھالنے کے طریقے بیان کرتی ہے۔

---

## Table of Contents

1. [Creating Strings](#creating-strings)
2. [Template Literals](#template-literals)
3. [Multi-line Strings](#multi-line-strings)
4. [Escape Sequences](#escape-sequences)
5. [String Length — لمبائی](#string-length--لمبائی)
6. [Accessing Characters](#accessing-characters)
7. [String Methods Reference](#string-methods-reference)
8. [String Comparison](#string-comparison)
9. [String and Number Interaction](#string-and-number-interaction)
10. [Practical Examples](#practical-examples)

---

## Creating Strings — سٹرنگ بنانا

Strings can be created with single quotes, double quotes, or backtick template literals.

> **اردو:** سٹرنگز ایک قوسین، دوہری قوسین، یا بیک ٹک ٹیمپلیٹ لٹریلز سے بنائی جا سکتی ہیں۔

```urdu
متغیر الف = 'ایک قوسین والی تار';
متغیر ب   = "دوہری قوسین والی تار";
متغیر ج   = `بیک ٹک والی تار`;

لکھو(الف);   // ایک قوسین والی تار
لکھو(ب);     // دوہری قوسین والی تار
لکھو(ج);     // بیک ٹک والی تار
```

Single and double quotes are interchangeable. Use one style inside the other to avoid escaping.

> **اردو:** ایک اور دوہری قوسین قابل تبادلہ ہیں۔ ایسکیپ سے بچنے کے لیے ایک اسٹائل دوسرے کے اندر استعمال کریں۔

```urdu
متغیر جملہ1 = "وہ نے کہا 'مرحبا'";      // single quotes inside double
متغیر جملہ2 = 'اردو "پروگرامنگ" زبان';  // double quotes inside single
لکھو(جملہ1);
لکھو(جملہ2);
```

### متن() — Explicit string conversion — واضح سٹرنگ تبدیلی

> **اردو:** کسی بھی قدر کو سٹرنگ میں تبدیل کریں:

```urdu
لکھو(متن(100));       // "100"
لکھو(متن(3.14));      // "3.14"
لکھو(متن(سچ));        // "True"
لکھو(متن(خالی));      // "None"
لکھو(متن(غیر_معرف)); // "None"
لکھو(متن([1,2,3]));   // "[1, 2, 3]"
```

---

## Template Literals — ٹیمپلیٹ لٹریلز

Template literals use backticks `` ` `` and support embedded expressions with `${}`.

> **اردو:** ٹیمپلیٹ لٹریلز بیک ٹک `` ` `` استعمال کرتے ہیں اور `${}` کے ساتھ جڑے اظہارات کی حمایت کرتے ہیں۔

```urdu
متغیر نام = "فاطمہ";
متغیر عمر = 27;

لکھو(`میرا نام ${نام} ہے`);
// میرا نام فاطمہ ہے

لکھو(`${نام} کی عمر ${عمر} سال ہے`);
// فاطمہ کی عمر 27 سال ہے
```

### Expressions inside `${}` — `${}` کے اندر اظہارات

Any valid expression can appear inside `${}`.

> **اردو:** `${}` کے اندر کوئی بھی درست اظہار آ سکتا ہے۔

```urdu
متغیر قیمت = 250;
متغیر تعداد = 4;

لکھو(`کل رقم: ${قیمت * تعداد} روپے`);
// کل رقم: 1000 روپے

لکھو(`مربع جڑ: ${ریاضی.جذر(144)}`);
// مربع جڑ: 12

لکھو(`آج ${نیا Date().getFullYear()} ہے`);

متغیر سکور = 78;
لکھو(`درجہ: ${سکور >= 90 ? "A" : سکور >= 80 ? "B" : "C"}`);
// درجہ: C
```

### Nested template literals — گھونسلے دار ٹیمپلیٹ لٹریلز

> **اردو:** ٹیمپلیٹ لٹریلز کے اندر ٹیمپلیٹ لٹریلز:

```urdu
متغیر رنگ_جات = ["سرخ", "سبز", "نیلا"];
لکھو(`رنگ: ${رنگ_جات.جوڑو(", ")}`);
// رنگ: سرخ, سبز, نیلا

لکھو(`فہرست: ${رنگ_جات.تبدیل((r, i) => `${i + 1}. ${r}`).جوڑو(" | ")}`);
// فہرست: 1. سرخ | 2. سبز | 3. نیلا
```

---

## Multi-line Strings — کثیر سطری سٹرنگز

Template literals preserve newlines naturally.

> **اردو:** ٹیمپلیٹ لٹریلز قدرتی طور پر نئی سطریں محفوظ رکھتے ہیں۔

```urdu
متغیر پیغام = `پیارے صارف،

آپ کا اکاؤنٹ کامیابی سے بنایا گیا ہے۔
براہ کرم اپنی ای میل کی تصدیق کریں۔

شکریہ،
ٹیم`;

لکھو(پیغام);
```

```urdu
// HTML template
متغیر عنوان = "اردو پروگرامنگ";
متغیر متن_شے = "آسان اور قدرتی زبان میں کوڈ لکھیں";

متغیر ایچ_ٹی_ایم_ایل = `
<div class="کارڈ">
  <h1>${عنوان}</h1>
  <p>${متن_شے}</p>
</div>
`;
لکھو(ایچ_ٹی_ایم_ایل);
```

---

## Escape Sequences — ایسکیپ ترتیبات

| Sequence | Meaning |
|----------|---------|
| `\n` | New line |
| `\t` | Tab |
| `\\` | Backslash |
| `\'` | Single quote |
| `\"` | Double quote |
| `\r` | Carriage return |
| `\u{XXXX}` | Unicode code point |

> **اردو:** یہ خاص ترتیبات سٹرنگ میں خاص حروف داخل کرنے کے لیے استعمال ہوتی ہیں۔

```urdu
لکھو("پہلی سطر\nدوسری سطر");
// پہلی سطر
// دوسری سطر

لکھو("نام:\tعلی");
// نام:    علی

لکھو("راستہ: C:\\Users\\Ahmad");
// راستہ: C:\Users\Ahmad

لکھو("اردو: \u{0627}\u{0631}\u{062F}\u{0648}");
// اردو: اردو
```

---

## String Length — لمبائی

The `لمبائی` property returns the number of characters.

> **اردو:** `لمبائی` خاصیت حروف کی تعداد واپس کرتی ہے۔

```urdu
متغیر جملہ = "اردو پروگرامنگ";
لکھو(جملہ.لمبائی);    // 14

لکھو("".لمبائی);       // 0
لکھو("hello".لمبائی);  // 5

// Check if string is empty
فنکشن خالی_ہے(تار) {
    واپس تار.لمبائی === 0;
}
لکھو(خالی_ہے(""));       // true
لکھو(خالی_ہے("کچھ"));   // false
```

---

## Accessing Characters — حروف تک رسائی

Characters are accessed by index (0-based) using bracket notation or `.at()`.

> **اردو:** حروف تک انڈیکس (0 سے شروع) کے ذریعے قوسین نوٹیشن یا `.at()` سے رسائی حاصل کی جاتی ہے۔

```urdu
متغیر الفاظ = "اردو";

لکھو(الفاظ[0]);        // ا
لکھو(الفاظ[1]);        // ر
لکھو(الفاظ[-1]);       // و   (negative index — last character)
لکھو(الفاظ.at(0));     // ا
لکھو(الفاظ.at(-1));    // و
```

---

## String Methods Reference — سٹرنگ طریقوں کا حوالہ

### چھاٹو — trim / trimStart / trimEnd

Removes whitespace from one or both ends of the string.

> **اردو:** سٹرنگ کے ایک یا دونوں سروں سے خالی جگہ ہٹاتا ہے۔

```urdu
متغیر تار = "   مرحبا دنیا   ";

لکھو(تار.چھاٹو());           // "مرحبا دنیا"
لکھو(تار.شروع_چھاٹو());      // "مرحبا دنیا   "
لکھو(تار.آخر_چھاٹو());       // "   مرحبا دنیا"
```

### بڑے_حروف / چھوٹے_حروف — toUpperCase / toLowerCase

> **اردو:** بڑے/چھوٹے حروف میں تبدیل کریں:

```urdu
متغیر نام = "Ahmad Ali";

لکھو(نام.بڑے_حروف());    // AHMAD ALI
لکھو(نام.چھوٹے_حروف());   // ahmad ali

// Normalize for comparison
لکھو("اردو".چھوٹے_حروف() === "اردو".چھوٹے_حروف());   // true
```

### شروع_ہے / ختم_ہے — startsWith / endsWith

> **اردو:** سٹرنگ کا آغاز یا اختتام جانچیں:

```urdu
متغیر فائل = "رپورٹ_2024.pdf";

لکھو(فائل.شروع_ہے("رپورٹ"));    // true
لکھو(فائل.ختم_ہے(".pdf"));       // true
لکھو(فائل.ختم_ہے(".doc"));       // false

// With position argument
متغیر url = "https://example.com";
لکھو(url.شروع_ہے("https"));      // true
لکھو(url.شروع_ہے("http", 0));    // true
لکھو(url.شروع_ہے("example", 8)); // true
```

### شامل_ہے — includes

> **اردو:** جانچیں کہ سٹرنگ میں کوئی ذیلی سٹرنگ موجود ہے:

```urdu
متغیر جملہ = "اردو پروگرامنگ زبان آسان ہے";

لکھو(جملہ.شامل_ہے("پروگرامنگ"));    // true
لکھو(جملہ.شامل_ہے("مشکل"));          // false
لکھو(جملہ.شامل_ہے("اردو", 0));       // true  (start searching from index 0)
```

### مقام — indexOf / lastIndexOf

Returns the index of the first (or last) occurrence, or `-1` if not found.

> **اردو:** پہلی (یا آخری) موجودگی کا انڈیکس واپس کرتا ہے، یا نہ ملنے پر `-1`۔

```urdu
متغیر جملہ = "اردو اردو اردو";

لکھو(جملہ.مقام("اردو"));          // 0
لکھو(جملہ.آخری_مقام("اردو"));     // 10
لکھو(جملہ.مقام("فارسی"));         // -1

// Search from a specific position
لکھو(جملہ.مقام("اردو", 1));       // 5
```

> **Note:** `.مقام()` throws a runtime error if the substring is not found (unlike JavaScript's `indexOf` which returns -1). Use `.آخری_مقام()` if you need -1 behavior, or wrap in `کوشش/پکڑو`.

### بدلو — replace / replaceAll

> **اردو:** سٹرنگ میں کوئی حصہ بدلیں:

```urdu
متغیر متن_شے = "سیب اچھا ہے، سیب میٹھا ہے";

// Replace first occurrence
لکھو(متن_شے.بدلو("سیب", "آم"));
// آم اچھا ہے، سیب میٹھا ہے

// بدلو تمام موجودگیاں بدلتا ہے — سب_بدلو الگ نہیں
// بدلو replaces ALL occurrences (no separate سب_بدلو needed)
لکھو(متن_شے.بدلو("سیب", "آم"));
// آم اچھا ہے، آم میٹھا ہے

// With a regex
متغیر ان_پٹ = "  بہت   زیادہ   جگہ  ";
لکھو(ان_پٹ.بدلو(/\s+/g, " ").چھاٹو());
// بہت زیادہ جگہ
```

### دہراؤ — repeat

> **اردو:** سٹرنگ کو n مرتبہ دہرائیں:

```urdu
لکھو("ہا".دہراؤ(3));           // ہاہاہا
لکھو("-".دہراؤ(20));           // --------------------
لکھو("اردو ".دہراؤ(4).چھاٹو()); // اردو اردو اردو اردو
```

### حصہ — slice

`حصہ(شروع, آخر)` — extracts a substring. Negative indices count from the end.

> **اردو:** `حصہ(شروع, آخر)` — ذیلی سٹرنگ نکالتا ہے۔ منفی انڈیکس آخر سے گنتے ہیں۔

```urdu
متغیر پروگرامنگ = "اردو پروگرامنگ زبان";

لکھو(پروگرامنگ.حصہ(5));         // پروگرامنگ زبان
لکھو(پروگرامنگ.حصہ(5, 15));     // پروگرامنگ
لکھو(پروگرامنگ.حصہ(-5));        // زبان
لکھو(پروگرامنگ.حصہ(-5, -1));    // زبا
لکھو(پروگرامنگ.حصہ(0, 4));      // اردو
```

### تقسیم — split

Splits a string into an array using a separator.

> **اردو:** الگ کرنے والے حرف کے ذریعے سٹرنگ کو فہرست میں تقسیم کرتا ہے۔

```urdu
متغیر جملہ = "احمد، علی، فاطمہ، زینب";
متغیر نام_جات = تقسیم(جملہ, ", ");
لکھو(نام_جات);    // ["احمد", "علی", "فاطمہ", "زینب"]
لکھو(نام_جات.لمبائی);    // 4

// Split into characters
// نوٹ: خالی الگ کرنے والے سے تقسیم کام نہیں کرتی
// Note: تقسیم with empty separator is not supported

// Split by line
متغیر سطریں = تقسیم("سطر1\nسطر2\nسطر3", "\n");
لکھو(سطریں);   // ["سطر1", "سطر2", "سطر3"]

متغیر حصے = تقسیم("الف:ب:ج:د", ":");
لکھو(حصے);    // ["الف", "ب", "ج", "د"]
```

### ربط — join (array method — used with strings)

`ربط` joins an array of strings into one string.

> **اردو:** `ربط` سٹرنگز کی فہرست کو ایک سٹرنگ میں جوڑتا ہے۔

```urdu
متغیر الفاظ = ["اردو", "پروگرامنگ", "آسان", "ہے"];
لکھو(الفاظ.جوڑو(" "));     // اردو پروگرامنگ آسان ہے
لکھو(الفاظ.جوڑو("-"));     // اردو-پروگرامنگ-آسان-ہے
لکھو(الفاظ.جوڑو(""));      // اردوپروگرامنگآسانہے
```

### Padding — padStart / padEnd

> **اردو:** سٹرنگ کو بائیں یا دائیں سے بھریں:

```urdu
لکھو("5".padStart(3, "0"));       // "005"
لکھو("اردو".padEnd(10, "."));     // "اردو......"

// Format a table
کے_لیے (متغیر i کا [1, 2, 3, 10, 100]) {
    لکھو(متن(i).padStart(4, " ") + " | قدر");
}
```

### String search with regex — ریجیکس سے سٹرنگ تلاش

> **اردو:** ریجیکس کے ساتھ سٹرنگ تلاش:

```urdu
متغیر متن_شے = "فون: 0300-1234567، فون: 0321-9876543";

// Test — returns boolean
لکھو(/\d{4}-\d{7}/.تجربہ(متن_شے));    // true

// Match — returns array
متغیر نمبر_جات = متن_شے.ملاپ(/\d{4}-\d{7}/g);
لکھو(نمبر_جات);    // ["0300-1234567", "0321-9876543"]
```

### Complete methods table — مکمل طریقوں کی جدول

| Urdu method | JS equivalent | Description |
|-------------|---------------|-------------|
| `.چھاٹو()` | `.trim()` | Remove surrounding whitespace |
| `.شروع_چھاٹو()` | `.trimStart()` | Remove leading whitespace |
| `.آخر_چھاٹو()` | `.trimEnd()` | Remove trailing whitespace |
| `.بڑے_حروف()` | `.toUpperCase()` | Convert to upper case |
| `.چھوٹے_حروف()` | `.toLowerCase()` | Convert to lower case |
| `.شروع_ہے(s)` | `.startsWith(s)` | Does it start with s? |
| `.ختم_ہے(s)` | `.endsWith(s)` | Does it end with s? |
| `.شامل_ہے(s)` | `.includes(s)` | Does it contain s? |
| `.مقام(s)` | `.indexOf(s)` | First index of s |
| `.آخری_مقام(s)` | `.lastIndexOf(s)` | Last index of s |
| `.بدلو(a, b)` | `.replace(a, b)` | Replace all occurrences |
| `.دہراؤ(n)` | `.repeat(n)` | Repeat n times |
| `.حصہ(s, e)` | `.slice(s, e)` | Extract substring |
| `تقسیم(str, sep)` | `split(str, sep)` | Split into array — standalone function, not method |
| `.padStart(n, c)` | `.padStart(n, c)` | Pad at start |
| `.padEnd(n, c)` | `.padEnd(n, c)` | Pad at end |
| `.ملاپ(regex)` | `.match(regex)` | Regex match |
| `.تلاش(regex)` | `.search(regex)` | Regex search (index) |
| `.at(i)` | `.at(i)` | Character at index (supports negative) |

---

## String Comparison — سٹرنگ موازنہ

Strings compare lexicographically by Unicode code point.

> **اردو:** سٹرنگز کا موازنہ یونیکوڈ کوڈ پوائنٹ کے مطابق لغوی ترتیب سے کیا جاتا ہے۔

```urdu
لکھو("احمد" === "احمد");    // true  — exact match
لکھو("احمد" === "Ahmed");   // false — different scripts

// Comparison operators
لکھو("الف" < "ب");          // true  — lexicographic
لکھو("ز" > "ا");             // true

// Case-insensitive comparison
فنکشن برابر_ہے(الف, ب) {
    واپس الف.چھوٹے_حروف() === ب.چھوٹے_حروف();
}
لکھو(برابر_ہے("URDU", "urdu"));    // true
```

### Sorting strings — سٹرنگز کو ترتیب دینا

> **اردو:** سٹرنگز کو ترتیب دیں:

```urdu
متغیر نام_جات = ["زینب", "احمد", "فاطمہ", "علی"];
نام_جات.ترتیب_دو();
لکھو(نام_جات);    // sorted by Unicode order

// Locale-aware sort
نام_جات.ترتیب_دو((الف, ب) => الف.localeCompare(ب, "ur"));
لکھو(نام_جات);
```

---

## String and Number Interaction — سٹرنگ اور عدد کا تعامل

> **اردو:** سٹرنگ اور عدد کے درمیان تعامل کے اصول:

```urdu
// String + number → string concatenation
لکھو("قیمت: " + 500);        // "قیمت: 500"
لکھو(100 + "200");            // "100200"  ← be careful

// Arithmetic with string numbers
لکھو("10" - 5);     // 5     ← coercion
لکھو("10" * 2);     // 20    ← coercion
لکھو("10" / 2);     // 5     ← coercion
لکھو("10" + 5);     // "105" ← concatenation, NOT addition

// Safe: always convert first
متغیر ان_پٹ = "42";
لکھو(عدد(ان_پٹ) + 8);    // 50
```

---

## Practical Examples — عملی مثالیں

### Validate email format — ای میل فارمیٹ جانچنا

> **اردو:** ای میل پتے کی درستگی جانچنے کی مثال:

```urdu
فنکشن ای_میل_درست_ہے(ای_میل) {
    واپس ای_میل.شامل_ہے("@") اور
           ای_میل.شامل_ہے(".") اور
           ای_میل.مقام("@") > 0 اور
           ای_میل.آخری_مقام(".") > ای_میل.مقام("@");
}

لکھو(ای_میل_درست_ہے("user@example.com"));   // true
لکھو(ای_میل_درست_ہے("نادرست"));              // false
```

### Capitalize first letter of each word — ہر لفظ کا پہلا حرف بڑا کرنا

> **اردو:** ہر لفظ کا پہلا حرف بڑا کریں:

```urdu
فنکشن عنوان_بنائیں(متن_شے) {
    واپس تقسیم(متن_شے, " ")
        .تبدیل(لفظ => لفظ[0].بڑے_حروف() + لفظ.حصہ(1).چھوٹے_حروف())
        .جوڑو(" ");
}

لکھو(عنوان_بنائیں("اردو پروگرامنگ زبان"));
```

### Truncate long text with ellipsis — لمبی متن کو کاٹنا

> **اردو:** لمبی سٹرنگ کو ایک حد تک کاٹیں اور اختتام پر تین نقطے لگائیں:

```urdu
فنکشن کاٹو(متن_شے, حد_قدر = 50) {
    اگر (متن_شے.لمبائی <= حد_قدر) {
        واپس متن_شے;
    }
    واپس متن_شے.حصہ(0, حد_قدر - 3) + "...";
}

متغیر لمبا_متن = "یہ ایک بہت لمبا جملہ ہے جو اسکرین پر فٹ نہیں آتا اور کاٹنا پڑے گا";
لکھو(کاٹو(لمبا_متن, 40));
```

### Build a CSV row — CSV سطر بنانا

> **اردو:** CSV فارمیٹ میں ڈیٹا سطر بنائیں:

```urdu
فنکشن csv_سطر(اشیاء) {
    واپس اشیاء
        .تبدیل(شے => {
            متغیر قدر = متن(شے);
            واپس قدر.شامل_ہے(",") ? `"${قدر}"` : قدر;
        })
        .جوڑو(",");
}

لکھو(csv_سطر(["احمد", "لاہور، پاکستان", 30]));
// احمد,"لاہور، پاکستان",30
```

### Count word frequency — الفاظ کی تعداد گننا

> **اردو:** متن میں ہر لفظ کتنی بار آیا گنیں:

```urdu
فنکشن الفاظ_گنو(متن_شے) {
    مستقل گنتی = {};
    مستقل الفاظ_جات = تقسیم(متن_شے.چھوٹے_حروف(), " ");
    کے_لیے (متغیر لفظ کا الفاظ_جات) {
        گنتی[لفظ] = (گنتی[لفظ] یا 0) + 1;
    }
    واپس گنتی;
}

لکھو(الفاظ_گنو("اردو اردو زبان اردو زبان"));
// { اردو: 3, زبان: 2 }
```
