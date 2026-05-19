# Operators — آپریٹرز

This document covers every operator available in the Urdu Programming Language, with full examples and an operator precedence reference table.

> **اردو:** یہ دستاویز اردو پروگرامنگ لینگویج میں دستیاب ہر آپریٹر کا احاطہ کرتی ہے، مکمل مثالوں اور آپریٹر ترجیح کی حوالہ جاتی جدول کے ساتھ۔

---

## Table of Contents

1. [Arithmetic Operators](#arithmetic-operators)
2. [Assignment Operators](#assignment-operators)
3. [Comparison Operators](#comparison-operators)
4. [Logical Operators](#logical-operators)
5. [Bitwise Operators](#bitwise-operators)
6. [Special Operators](#special-operators)
7. [Increment and Decrement](#increment-and-decrement)
8. [Ternary Operator](#ternary-operator)
9. [Operator Precedence](#operator-precedence)

---

## Arithmetic Operators — حسابی آپریٹرز

These operators perform mathematical calculations.

> **اردو:** یہ آپریٹرز ریاضیاتی حسابات انجام دیتے ہیں۔

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `5 * 3` | `15` |
| `/` | Division | `10 / 4` | `2.5` |
| `%` | Modulus (remainder) | `10 % 3` | `1` |
| `**` | Exponentiation | `2 ** 8` | `256` |

> **Note:** `//` is the **comment operator** in Urdu PL (same as `//` in JavaScript/C). It is NOT floor division. For integer/floor division use `عدد(a / b)`.

> **اردو:** نوٹ: `//` اردو پروگرامنگ لینگویج میں **تبصرہ آپریٹر** ہے۔ یہ فرش تقسیم نہیں ہے۔ صحیح عددی تقسیم کے لیے `عدد(a / b)` استعمال کریں۔

```urdu
متغیر الف = 17;
متغیر ب = 5;

لکھو(الف + ب);
لکھو(الف - ب);
لکھو(الف * ب);
لکھو(الف / ب);
لکھو(الف % ب);
لکھو(الف ** ب);
لکھو(عدد(الف / ب));
```

### String concatenation with `+` — `+` سے سٹرنگ جوڑنا

When used with strings, `+` concatenates them.

> **اردو:** سٹرنگز کے ساتھ استعمال کرنے پر `+` انہیں جوڑ دیتا ہے۔

```urdu
متغیر پہلا = "اردو";
متغیر دوسرا = " پروگرامنگ";
لکھو(پہلا + دوسرا);       // اردو پروگرامنگ
لکھو("نتیجہ: " + 42);     // نتیجہ: 42
```

### Integer (floor) division — صحیح عددی تقسیم

Use `عدد()` to convert a division result to an integer:

> **اردو:** تقسیم کے نتیجے کو صحیح عدد میں بدلنے کے لیے `عدد()` استعمال کریں:

```urdu
لکھو(7 / 2);           
لکھو(عدد(7 / 2));      
لکھو(ریاضی.فرش(7 / 2));
```

### Exponentiation — قوت

```urdu
لکھو(2 ** 10);    // 1024
لکھو(9 ** 0.5);   // 3.0   (square root)
لکھو(27 ** (1/3)); // 3.0   (cube root)
```

---

## Assignment Operators — تفویض آپریٹرز

Assignment operators write a value into a variable. Compound assignment operators combine arithmetic with assignment.

> **اردو:** تفویض آپریٹرز کسی متغیر میں قدر لکھتے ہیں۔ مرکب تفویض آپریٹرز حساب اور تفویض کو یکجا کرتے ہیں۔

| Operator | Equivalent to | Example |
|----------|--------------|---------|
| `=` | plain assignment | `x = 5` |
| `+=` | `x = x + n` | `x += 3` |
| `-=` | `x = x - n` | `x -= 2` |
| `*=` | `x = x * n` | `x *= 4` |
| `/=` | `x = x / n` | `x /= 2` |
| `%=` | `x = x % n` | `x %= 3` |
| `**=` | `x = x ** n` | `x **= 2` |
| `&&=` | `x = x && n` | `x &&= y` |
| `\|\|=` | `x = x \|\| n` | `x \|\|= y` |
| `??=` | `x = x ?? n` | `x ??= y` |

```urdu
متغیر رقم = 100;

رقم += 50;
لکھو(رقم);    // 150

رقم -= 30;
لکھو(رقم);    // 120

رقم *= 2;
لکھو(رقم);    // 240

رقم /= 4;
لکھو(رقم);    // 60

رقم %= 7;
لکھو(رقم);    // 4

رقم **= 3;
لکھو(رقم);    // 64
```

```urdu
// Logical assignment
متغیر صارف_نام = غیر_معرف;
صارف_نام ??= "مہمان";
لکھو(صارف_نام);    // مہمان

متغیر ترتیب = { رنگ: "" };
ترتیب.رنگ ||= "نیلا";   // "" is falsy → assign
لکھو(ترتیب.رنگ);         // نیلا
```

---

## Comparison Operators — موازنہ آپریٹرز

Comparison operators return `سچ` or `جھوٹ`.

> **اردو:** موازنہ آپریٹرز `سچ` یا `جھوٹ` واپس کرتے ہیں۔

| Operator | Meaning |
|----------|---------|
| `==` | Loose equality (type coercion) |
| `!=` | Loose inequality |
| `===` | Strict equality (no coercion) |
| `!==` | Strict inequality |
| `<` | Less than |
| `>` | Greater than |
| `<=` | Less than or equal |
| `>=` | Greater than or equal |

### Loose vs strict equality — ڈھیلی بمقابلہ سخت برابری

`==` coerces types before comparing; `===` requires identical types.

> **اردو:** `==` موازنے سے پہلے اقسام بدل دیتا ہے؛ `===` کو ایک جیسی اقسام درکار ہیں۔

```urdu
لکھو(5 == "5");     // true   (string coerced to number)
لکھو(5 === "5");    // false  (different types)

لکھو(0 == جھوٹ);    // true
لکھو(0 === جھوٹ);   // false

لکھو(خالی == غیر_معرف);    // true
لکھو(خالی === غیر_معرف);   // false
```

> **Best practice:** Always use `===` and `!==` to avoid unexpected coercion behaviour.

> **اردو:** بہترین عمل: غیر متوقع قسم تبدیلی سے بچنے کے لیے ہمیشہ `===` اور `!==` استعمال کریں۔

```urdu
متغیر الف = 10;
متغیر ب = 20;

لکھو(الف < ب);      // true
لکھو(الف > ب);      // false
لکھو(الف <= 10);    // true
لکھو(ب >= 20);      // true
لکھو(الف !== ب);    // true
```

### String comparison — سٹرنگ موازنہ

Strings are compared lexicographically (Unicode code point order).

> **اردو:** سٹرنگز کا موازنہ لغوی ترتیب سے کیا جاتا ہے (یونیکوڈ کوڈ پوائنٹ ترتیب)۔

```urdu
لکھو("احمد" < "علی");    // true   (alphabetic order)
لکھو("ب" > "الف");       // depends on Unicode values
لکھو("abc" === "abc");   // true
لکھو("ABC" === "abc");   // false
```

---

## Logical Operators — منطقی آپریٹرز

Logical operators work with boolean (or truthy/falsy) values.

> **اردو:** منطقی آپریٹرز بولین (یا سچ/جھوٹ جیسی) قدروں کے ساتھ کام کرتے ہیں۔

| Operator | Urdu keyword | Meaning |
|----------|-------------|---------|
| `&&` | `اور` | Logical AND |
| `\|\|` | `یا` | Logical OR |
| `!` | `نہیں` | Logical NOT |

Both the symbol form and the Urdu keyword form are accepted.

> **اردو:** علامتی شکل اور اردو کلیدی لفظ دونوں قابل قبول ہیں۔

```urdu
// AND — اور
لکھو(سچ اور سچ);      // true
لکھو(سچ اور جھوٹ);    // false
لکھو(جھوٹ اور سچ);    // false

// OR — یا
لکھو(سچ یا جھوٹ);     // true
لکھو(جھوٹ یا جھوٹ);   // false

// NOT — نہیں
لکھو(نہیں سچ);         // false
لکھو(نہیں جھوٹ);       // true
لکھو(نہیں 0);           // true
لکھو(نہیں "");           // true
```

### Short-circuit evaluation — مختصر سرکٹ تشخیص

`&&` stops at the first falsy value. `||` stops at the first truthy value. This enables elegant defaults and guards.

> **اردو:** `&&` پہلی جھوٹ قدر پر رک جاتا ہے۔ `||` پہلی سچ قدر پر رک جاتا ہے۔ اس سے خوبصورت ڈیفالٹس اور محافظ ممکن ہوتے ہیں۔

```urdu
// && guard
متغیر صارف = { نام: "علی" };
متغیر نتیجہ = صارف اور صارف.نام;
لکھو(نتیجہ);    // علی

متغیر خالی_صارف = خالی;
لکھو(خالی_صارف اور خالی_صارف.نام);    // null  (short-circuited)
```

```urdu
// || default value
فنکشن سلام(نام) {
    نام = نام یا "دوست";
    لکھو(`مرحبا، ${نام}!`);
}

سلام("احمد");    // مرحبا، احمد!
سلام();          // مرحبا، دوست!
```

```urdu
// Practical condition
متغیر عمر = 20;
متغیر شناختی_کارڈ = سچ;

اگر (عمر >= 18 اور شناختی_کارڈ) {
    لکھو("داخلہ جائز ہے");
} ورنہ {
    لکھو("داخلہ ممنوع ہے");
}
```

---

## Bitwise Operators — بٹ آپریٹرز

Bitwise operators treat operands as 32-bit integers and work at the binary level.

> **اردو:** بٹ آپریٹرز آپرینڈز کو 32-بٹ اعداد صحیح کے طور پر سمجھتے ہیں اور بائنری سطح پر کام کرتے ہیں۔

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `&` | AND | `5 & 3` | `1` |
| `\|` | OR | `5 \| 3` | `7` |
| `^` | XOR | `5 ^ 3` | `6` |
| `~` | NOT | `~5` | `-6` |
| `<<` | Left shift | `5 << 1` | `10` |
| `>>` | Right shift (signed) | `20 >> 2` | `5` |
| `>>>` | Right shift (unsigned) | `-1 >>> 0` | `4294967295` |

```urdu
متغیر الف = 0b1101;   // 13
متغیر ب  = 0b1010;   // 10

لکھو(الف & ب);    // 8   (0b1000)
لکھو(الف | ب);    // 15  (0b1111)
لکھو(الف ^ ب);    // 7   (0b0111)
لکھو(~الف);       // -14
لکھو(الف << 2);   // 52  (0b110100)
لکھو(الف >> 1);   // 6   (0b0110)
```

### Practical bitwise use cases — بٹ آپریٹرز کے عملی استعمال

> **اردو:** بٹ آپریٹرز کے عملی استعمال کی مثالیں:

```urdu
// Check if a number is even or odd
فنکشن جفت_ہے(n) {
    واپس (n & 1) === 0;
}
لکھو(جفت_ہے(8));    // true
لکھو(جفت_ہے(7));    // false

// Fast floor using double NOT
لکھو(~~3.9);    // 3
لکھو(~~-3.9);   // -3

// Bit flags
مستقل پڑھ_سکتا = 0b001;   // 1
مستقل لکھ_سکتا = 0b010;   // 2
مستقل چلا_سکتا = 0b100;   // 4

متغیر اجازت = پڑھ_سکتا | لکھ_سکتا;   // 3

لکھو(!!(اجازت & پڑھ_سکتا));   // true
لکھو(!!(اجازت & چلا_سکتا));   // false
```

---

## Special Operators — خصوصی آپریٹرز

### Nullish coalescing `??` — خالی ادغام

Returns the right-hand value only when the left side is `خالی` or `غیر_معرف` (not just any falsy value).

> **اردو:** دائیں طرف کی قدر صرف اس وقت واپس کرتا ہے جب بائیں طرف `خالی` یا `غیر_معرف` ہو (کوئی بھی جھوٹ قدر نہیں)۔

```urdu
لکھو(خالی ?? "پہلے سے طے");          // پہلے سے طے
لکھو(غیر_معرف ?? "پہلے سے طے");      // پہلے سے طے
لکھو(0 ?? "پہلے سے طے");             // 0      ← 0 is NOT null/undefined
لکھو("" ?? "پہلے سے طے");            // ""     ← empty string is NOT null/undefined
لکھو(جھوٹ ?? "پہلے سے طے");          // false  ← false is NOT null/undefined
```

### Optional chaining `?.` — اختیاری زنجیر

Safely accesses nested properties. Returns `غیر_معرف` instead of throwing if an intermediate value is `خالی` or `غیر_معرف`.

> **اردو:** گھونسلے دار خاصیات تک محفوظ طریقے سے رسائی۔ اگر درمیانی قدر `خالی` یا `غیر_معرف` ہو تو غلطی پھینکنے کی بجائے `غیر_معرف` واپس کرتا ہے۔

```urdu
مستقل صارف = {
    نام: "زید",
    پتہ: { شہر: "پشاور" }
};

لکھو(صارف.پتہ?.شہر);           // پشاور
لکھو(صارف.فون?.نمبر);          // undefined  (no error)
لکھو(صارف.پتہ?.شہر?.لمبائی);  // 6

// Optional method call
لکھو(صارف.تعارف?.());          // undefined  (method doesn't exist — no crash)
```

```urdu
// Chained with ??
مستقل شہر = صارف.پتہ?.شہر ?? "نامعلوم شہر";
لکھو(شہر);    // پشاور
```

### Spread operator `...` — پھیلاؤ آپریٹر

Expands an iterable (array, string, object) in place.

> **اردو:** ایک تکرار پذیر (فہرست، سٹرنگ، شے) کو جگہ پر پھیلا دیتا ہے۔

```urdu
// Spread in array
مستقل اعداد_1 = [1, 2, 3];
مستقل اعداد_2 = [4, 5, 6];
مستقل سب = [...اعداد_1, ...اعداد_2];
لکھو(سب);    // [1, 2, 3, 4, 5, 6]

// Clone array (shallow)
مستقل اصل = [10, 20, 30];
مستقل کاپی = [...اصل];
کاپی.شامل(40);
لکھو(اصل);    // [10, 20, 30]     ← unchanged
لکھو(کاپی);   // [10, 20, 30, 40]
```

```urdu
// Spread in object
مستقل بنیادی = { نام: "علی", عمر: 25 };
مستقل توسیع = { ...بنیادی, شہر: "ملتان", عمر: 26 };
لکھو(توسیع);
// { نام: "علی", عمر: 26, شہر: "ملتان" }
```

```urdu
// Spread in function call
فنکشن جمع(الف, ب, ج) {
    واپس الف + ب + ج;
}
مستقل قدریں = [1, 2, 3];
لکھو(جمع(...قدریں));    // 6
```

### typeof operator — قسم

Returns the type of a value as a string.

> **اردو:** کسی قدر کی قسم بطور سٹرنگ واپس کرتا ہے۔

```urdu
لکھو(قسم(42));           // "عدد"
لکھو(قسم("اردو"));       // "متن"
لکھو(قسم(سچ));           // "بولین"
لکھو(قسم(غیر_معرف));     // "خالی"
لکھو(قسم(خالی));         // "خالی"
لکھو(قسم({}));            // "شے"
لکھو(قسم([]));            // "فہرست"
لکھو(قسم(فنکشن() {}));   // "فنکشن"
```

### instanceof operator — مثال

Checks the prototype chain.

> **اردو:** پروٹو ٹائپ زنجیر جانچتا ہے۔

```urdu
// مثال صرف صارف کی بنائی کلاسوں کے ساتھ کام کرتا ہے
// مثال (instanceof) only works with user-defined classes

کلاس جانور {}
کلاس کتا توسیع جانور {}

متغیر ک = نیا کتا();
لکھو(ک مثال کتا);     // true
لکھو(ک مثال جانور);   // true
```

### delete operator — حذف

Removes a property from an object.

> **اردو:** کسی شے سے خاصیت ہٹاتا ہے۔

```urdu
متغیر شے = { الف: 1, ب: 2, ج: 3 };
لکھو(شے);         // { الف: 1, ب: 2, ج: 3 }

حذف شے.ب;
لکھو(شے);         // { الف: 1, ج: 3 }
لکھو(شے.ب);       // undefined
```

---

## Increment and Decrement — اضافہ اور کمی

`++` adds 1 and `--` subtracts 1. The position (prefix vs postfix) matters.

> **اردو:** `++` ایک جوڑتا ہے اور `--` ایک گھٹاتا ہے۔ پوزیشن (پہلے یا بعد) کا فرق پڑتا ہے۔

| Form | Effect | Returns |
|------|--------|---------|
| `++x` | Increment first | New value |
| `x++` | Return first | Old value |
| `--x` | Decrement first | New value |
| `x--` | Return first | Old value |

```urdu
متغیر گنتی = 5;

لکھو(گنتی++);    // 5   (returns old, then increments)
لکھو(گنتی);      // 6

لکھو(++گنتی);    // 7   (increments first, then returns)
لکھو(گنتی);      // 7

لکھو(گنتی--);    // 7
لکھو(گنتی);      // 6

لکھو(--گنتی);    // 5
لکھو(گنتی);      // 5
```

### Practical increment in a loop — حلقے میں عملی اضافہ

> **اردو:** حلقے میں اضافے کی عملی مثال:

```urdu
متغیر i = 0;
جبکہ (i < 5) {
    لکھو(`قدم ${i + 1}`);
    i++;
}
```

---

## Ternary Operator — تثلیثی آپریٹر

The ternary operator `? :` is a compact if/else in a single expression.

> **اردو:** تثلیثی آپریٹر `? :` ایک واحد اظہار میں مختصر if/else ہے۔

**Syntax:**
```
شرط ? قدر_اگر_سچ : قدر_اگر_جھوٹ
```

```urdu
متغیر عمر = 20;
متغیر حیثیت = عمر >= 18 ? "بالغ" : "نابالغ";
لکھو(حیثیت);    // بالغ
```

```urdu
// Nested ternary
متغیر نمبر = 75;
متغیر درجہ = نمبر >= 90 ? "A"
           : نمبر >= 80 ? "B"
           : نمبر >= 70 ? "C"
           : نمبر >= 60 ? "D"
           : "F";
لکھو(درجہ);    // C
```

```urdu
// Inline function call
فنکشن مطلق_قدر(n) {
    واپس n >= 0 ? n : -n;
}
لکھو(مطلق_قدر(-7));    // 7
لکھو(مطلق_قدر(3));     // 3
```

```urdu
// In template literal
متغیر اشیاء = 1;
لکھو(`${اشیاء} ${اشیاء === 1 ? "شے" : "اشیاء"} ملی`);
// 1 شے ملی
```

---

## Operator Precedence — آپریٹر ترجیح

Higher precedence means the operator binds more tightly. Operators on the same row have equal precedence and are evaluated left-to-right (or right-to-left where noted).

> **اردو:** زیادہ ترجیح کا مطلب ہے کہ آپریٹر زیادہ مضبوطی سے باندھتا ہے۔ ایک ہی سطر کے آپریٹرز برابر ترجیح رکھتے ہیں اور بائیں سے دائیں (یا جہاں بتایا گیا دائیں سے بائیں) تشخیص ہوتے ہیں۔

| Level | Operators | Associativity |
|-------|-----------|--------------|
| 20 | `()` grouping | n/a |
| 19 | `.` `?.` `[]` `()` calls `new` | left-to-right |
| 17 | `++` `--` (postfix) | n/a |
| 16 | `!` `~` `+` `-` (unary) `++` `--` (prefix) `قسم` `حذف` | right-to-left |
| 15 | `**` | right-to-left |
| 14 | `*` `/` `%` | left-to-right |
| 13 | `+` `-` | left-to-right |
| 12 | `<<` `>>` `>>>` | left-to-right |
| 11 | `<` `<=` `>` `>=` `مثال` | left-to-right |
| 10 | `==` `!=` `===` `!==` | left-to-right |
| 9 | `&` | left-to-right |
| 8 | `^` | left-to-right |
| 7 | `\|` | left-to-right |
| 6 | `&&` `اور` | left-to-right |
| 5 | `\|\|` `یا` | left-to-right |
| 4 | `??` | left-to-right |
| 3 | `? :` (ternary) | right-to-left |
| 2 | `=` `+=` `-=` `*=` `/=` `%=` `**=` `&&=` `\|\|=` `??=` | right-to-left |
| 1 | `...` (spread/rest) | n/a |

### Precedence examples — ترجیح کی مثالیں

> **اردو:** آپریٹر ترجیح کی عملی مثالیں:

```urdu
// Arithmetic before comparison
لکھو(2 + 3 * 4);       // 14  (not 20)
لکھو((2 + 3) * 4);     // 20

// Comparison before logical
لکھو(1 + 2 === 3 اور 4 > 2);    // true
// Equivalent to: ((1+2) === 3) && (4 > 2)

// && before ||
لکھو(سچ یا جھوٹ اور جھوٹ);    // true
// Equivalent to: true || (false && false)  → true || false → true

// Exponentiation is right-to-left
لکھو(2 ** 3 ** 2);    // 512  (2 ** 9, not 8 ** 2)

// Nullish coalescing vs OR — same-level, use parentheses to mix
// لکھو(سچ || undefined ?? "default");  // غلطی پیدا کر سکتا ہے
لکھو((سچ یا غیر_معرف) ?? "default");   // true
```

> **Tip:** When in doubt, use parentheses `()` to make the intended evaluation order explicit. This is always safer and more readable than relying on precedence rules.

> **اردو:** مشورہ: جب شک ہو تو مطلوبہ تشخیص ترتیب واضح کرنے کے لیے قوسین `()` استعمال کریں۔ یہ ترجیح قواعد پر انحصار سے ہمیشہ محفوظ اور زیادہ پڑھنے کے قابل ہے۔
