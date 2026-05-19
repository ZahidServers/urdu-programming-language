# Operators Reference — آپریٹر حوالہ

A complete reference for all operators available in the Urdu Programming Language. Operators follow JavaScript/Python semantics. Urdu keyword forms and symbol forms are interchangeable wherever both are listed.

> **اردو:** اردو پروگرامنگ زبان کے تمام آپریٹرز کا مکمل حوالہ۔ جہاں دونوں موجود ہوں، اردو کلیدی لفظ اور علامتی شکل آپس میں بدلی جا سکتی ہیں۔

---

## Table of Contents — فہرست مضامین

- [Arithmetic Operators](#arithmetic-operators)
- [Assignment Operators](#assignment-operators)
- [Comparison Operators](#comparison-operators)
- [Logical Operators](#logical-operators)
- [Bitwise Operators](#bitwise-operators)
- [Special Operators](#special-operators)
- [Operator Precedence](#operator-precedence)

---

## Arithmetic Operators — ریاضی آپریٹر

Used to perform mathematical calculations.

> **اردو:** ریاضی آپریٹر عددی حسابات کے لیے استعمال ہوتے ہیں۔ `+` جمع، `-` تفریق، `*` ضرب، `/` تقسیم، `%` باقی، `**` طاقت۔ منزل تقسیم (floor division) کے لیے `عدد(a / b)` استعمال کریں۔

| Operator | Name | Example | Result | Notes |
|----------|------|---------|--------|-------|
| `+` | جمع (Addition) | `5 + 3` | `8` | Also concatenates strings: `"الف" + "ب"` → `"الفب"` |
| `-` | تفریق (Subtraction) | `10 - 4` | `6` | Unary minus: `-x` negates |
| `*` | ضرب (Multiplication) | `6 * 7` | `42` | Also repeats strings: `"ا" * 3` → `"ااا"` |
| `/` | تقسیم (Division) | `10 / 4` | `2.5` | Always returns float |
| `%` | باقی (Modulo) | `10 % 3` | `1` | Remainder after integer division |
| `**` | طاقت (Exponentiation) | `2 ** 8` | `256` | Right-associative: `2 ** 3 ** 2` → `512` |
| `++` | اضافہ (Increment) | `i++` | `i = i + 1` | Postfix only in most contexts |
| `--` | کمی (Decrement) | `i--` | `i = i - 1` | Postfix only in most contexts |

> **Note:** `//` is the line **comment** operator, not floor division. Use `عدد(a / b)` or `ریاضی.فرش(a / b)` for floor (integer) division.

**Examples**

```urdu
متغیر ا = 17;
لکھو(ا % 5);          // 2
لکھو(عدد(ا / 5));     // 3  (floor division)
لکھو(ا / 5);          // 3.4

// مربع
لکھو(2 ** 10);  // 1024

// متن ضرب
لکھو("-" * 20);  // --------------------

// اضافہ اور کمی
متغیر گنتی = 0;
گنتی++;
گنتی++;
لکھو(گنتی);   // 2
گنتی--;
لکھو(گنتی);   // 1
```

---

## Assignment Operators — تفویض آپریٹر

Used to assign or update variable values.

> **اردو:** تفویض آپریٹر متغیر کو قدر دینے یا اپ ڈیٹ کرنے کے لیے ہیں۔ `=` بنیادی تفویض، `+=` جمع کر کے تفویض، وغیرہ۔

| Operator | Name | Equivalent To | Example |
|----------|------|---------------|---------|
| `=` | تفویض (Assignment) | — | `x = 5` |
| `+=` | جمع تفویض (Add-assign) | `x = x + y` | `x += 3` |
| `-=` | تفریق تفویض (Sub-assign) | `x = x - y` | `x -= 2` |
| `*=` | ضرب تفویض (Mul-assign) | `x = x * y` | `x *= 4` |
| `/=` | تقسیم تفویض (Div-assign) | `x = x / y` | `x /= 2` |
| `%=` | باقی تفویض (Mod-assign) | `x = x % y` | `x %= 3` |
| `**=` | طاقت تفویض (Pow-assign) | `x = x ** y` | `x **= 2` |
| `&&=` | اور تفویض (And-assign) | `x = x && y` | `x &&= y` |
| `\|\|=` | یا تفویض (Or-assign) | `x = x \|\| y` | `x \|\|= y` |
| `??=` | خالی تفویض (Nullish-assign) | `x = x ?? y` | `x ??= y` |
| `&=` | بٹ اور تفویض (Bitand-assign) | `x = x & y` | `x &= 0xFF` |
| `\|=` | بٹ یا تفویض (Bitor-assign) | `x = x \| y` | `x \|= 0x01` |

**Examples**

```urdu
متغیر رقم = 1000;
رقم += 200;    // 1200
رقم -= 50;     // 1150
رقم *= 2;      // 2300
رقم /= 4;      // 575.0
رقم **= 2;     // 330625.0
رقم %= 1000;   // 625.0
```

```urdu
// nullish assign — صرف اس وقت تفویض کریں جب قدر خالی ہو
متغیر نام = خالی;
نام ??= "مہمان";
لکھو(نام);    // مہمان

متغیر نام2 = "احمد";
نام2 ??= "مہمان";
لکھو(نام2);   // احمد  (نہیں بدلا)
```

```urdu
// یا تفویض — فالبیک قدر
متغیر ترتیب = {};
ترتیب.رنگ ||= "نیلا";
لکھو(ترتیب.رنگ);   // نیلا
```

---

## Comparison Operators — موازنہ آپریٹر

Compare two values and return a boolean (`سچ` or `جھوٹ`).

> **اردو:** موازنہ آپریٹر دو قدروں کا موازنہ کرتے ہیں اور بولین (`سچ` یا `جھوٹ`) واپس کرتے ہیں۔ `===` سخت مساوات (قسم اور قدر دونوں) جانچتا ہے۔

| Operator | Name | Description | Example | Result |
|----------|------|-------------|---------|--------|
| `==` | برابر (Equal) | Loose equality — coerces types | `"5" == 5` | `True` |
| `!=` | نہ برابر (Not equal) | Loose inequality | `"5" != 6` | `True` |
| `===` | سخت برابر (Strict equal) | Exact equality — no type coercion | `"5" === 5` | `False` |
| `!==` | سخت نہ برابر (Strict not equal) | Exact inequality | `5 !== 5` | `False` |
| `<` | کم (Less than) | Strictly less | `3 < 5` | `True` |
| `>` | زیادہ (Greater than) | Strictly greater | `5 > 3` | `True` |
| `<=` | کم یا برابر (Less or equal) | Less than or equal | `5 <= 5` | `True` |
| `>=` | زیادہ یا برابر (Greater or equal) | Greater than or equal | `6 >= 5` | `True` |

> **`==` vs `===`:** The strict equality operator `===` checks both value and type and is generally preferred. Use `==` only when intentional type coercion is desired.

> **اردو:** `===` سخت مساوات قدر اور قسم (type) دونوں جانچتا ہے اور عموماً ترجیح دی جاتی ہے۔ `==` صرف اس وقت استعمال کریں جب جان بوجھ کر قسم کی تبدیلی مطلوب ہو۔

**Examples**

```urdu
لکھو(10 == "10");     // True   (قسم تبدیل ہوتی ہے)
لکھو(10 === "10");    // False  (قسم مختلف)
لکھو(10 !== 10);      // False
لکھو(خالی == غیر_معرف);   // True  (دونوں None ہیں)
```

```urdu
// درجہ بندی
متغیر نمبر = 75;
اگر (نمبر >= 90) {
    لکھو("ممتاز");
} ورنہ_اگر (نمبر >= 75) {
    لکھو("اچھا");
} ورنہ_اگر (نمبر >= 50) {
    لکھو("اوسط");
} ورنہ {
    لکھو("ناکام");
}
// اچھا
```

---

## Logical Operators — منطقی آپریٹر

Combine or invert boolean expressions. Both symbol and Urdu keyword forms are supported.

> **اردو:** منطقی آپریٹر بولین اظہارات کو جوڑتے یا الٹاتے ہیں۔ `&&`/`اور`، `||`/`یا`، `!`/`نہیں` — دونوں شکلیں قابل استعمال ہیں۔

| Symbol | Urdu Keyword | Name | Description |
|--------|-------------|------|-------------|
| `&&` | `اور` | اور (AND) | `سچ` if **both** operands are truthy. Short-circuits: returns first falsy value, or last value. |
| `\|\|` | `یا` | یا (OR) | `سچ` if **at least one** operand is truthy. Short-circuits: returns first truthy value, or last value. |
| `!` | `نہیں` | نہیں (NOT) | Inverts truthiness. `!سچ` → `جھوٹ`. |
| `??` | — | خالی_فالبیک (Nullish coalescing) | Returns right operand only when left is `خالی` or `غیر_معرف`. |

**Short-circuit evaluation:** `&&` stops at the first falsy value; `||` stops at the first truthy value. This is useful for default values and conditional execution.

**Examples**

```urdu
// اور — AND
لکھو(سچ && سچ);          // True
لکھو(سچ && جھوٹ);        // False
لکھو(5 > 3 && 10 < 20);  // True

// یا — OR
لکھو(جھوٹ || سچ);        // True
لکھو(جھوٹ || جھوٹ);      // False

// نہیں — NOT
لکھو(!سچ);               // False
لکھو(!0);                // True
لکھو(!"");               // True
لکھو(!"اردو");           // False
```

```urdu
// شارٹ سرکٹ — فالبیک قدر
متغیر نام = "" || "مہمان";
لکھو(نام);    // مہمان

متغیر قدر = خالی ?? "پہلے سے موجود";
لکھو(قدر);    // پہلے سے موجود

// محفوظ رسائی
متغیر صارف = خالی;
متغیر نتیجہ = صارف && صارف.نام;
لکھو(نتیجہ);  // None (null) — کوئی خطا نہیں
```

```urdu
// Urdu keyword form
اگر (عمر >= 18 اور ملک == "پاکستان") {
    لکھو("اہل");
}
اگر (نہیں لاگ_ان یا وقت_ختم) {
    لکھو("براہ کرم دوبارہ لاگ ان کریں");
}
```

---

## Bitwise Operators — بٹ آپریٹر

Operate on the individual binary bits of integers.

> **اردو:** بٹ آپریٹر عدد کے انفرادی بائنری بٹوں پر عمل کرتے ہیں۔

| Operator | Name | Description | Example | Result |
|----------|------|-------------|---------|--------|
| `&` | بٹ اور (Bitwise AND) | 1 only where both bits are 1 | `0b1100 & 0b1010` | `8` (`0b1000`) |
| `\|` | بٹ یا (Bitwise OR) | 1 where either bit is 1 | `0b1100 \| 0b1010` | `14` (`0b1110`) |
| `^` | بٹ ایکس اور (Bitwise XOR) | 1 where bits differ | `0b1100 ^ 0b1010` | `6` (`0b0110`) |
| `~` | بٹ نہیں (Bitwise NOT) | Flips all bits (two's complement) | `~5` | `-6` |
| `<<` | بائیں شفٹ (Left shift) | Shift bits left, fill with 0 | `1 << 4` | `16` |
| `>>` | دائیں شفٹ (Right shift) | Shift bits right, sign-fill | `16 >> 2` | `4` |
| `>>>` | بغیر علامت دائیں شفٹ (Unsigned right shift) | Shift right, fill with 0 | `−1 >>> 0` | `4294967295` |

**Examples**

```urdu
// پرچم بٹ (permission flags)
مستقل پڑھنا  = 0b001;   // 1
مستقل لکھنا  = 0b010;   // 2
مستقل چلانا = 0b100;   // 4

متغیر اجازت = پڑھنا | لکھنا;   // 3
لکھو(اجازت & پڑھنا != 0);      // True — پڑھنے کی اجازت ہے
لکھو(اجازت & چلانا != 0);      // False — چلانے کی نہیں

// بٹ شفٹ بطور ضرب/تقسیم (2 کی طاقت)
لکھو(1 << 8);    // 256
لکھو(256 >> 4);  // 16

// XOR سے قدریں بدلنا
متغیر الف = 5;
متغیر ب   = 9;
الف = الف ^ ب;
ب   = الف ^ ب;
الف = الف ^ ب;
لکھو(الف, ب);   // 9 5
```

---

## Special Operators — خاص آپریٹر

### Optional Chaining `?.`

Safely access a property or call a method on a value that might be `خالی` or `غیر_معرف`. Returns `خالی` instead of throwing an error when the left side is nullish.

> **اردو:** اختیاری زنجیر بندی `?.` اس وقت `خالی` واپس کرتا ہے جب بائیں جانب کی قدر `خالی` یا `غیر_معرف` ہو — خطا نہیں آتی۔

```urdu
متغیر صارف = {
    نام: "احمد",
    پتہ: { شہر: "کراچی" }
};

لکھو(صارف?.نام);            // احمد
لکھو(صارف?.فون?.نمبر);      // None  (کوئی خطا نہیں)
لکھو(صارف?.پتہ?.شہر);       // کراچی

// خالی شے
متغیر غیر_موجود = خالی;
لکھو(غیر_موجود?.نام);       // None  (خطا نہیں آتی)
```

---

### Nullish Coalescing `??`

Return the right operand only when the left operand is `خالی` (`null`) or `غیر_معرف` (`undefined`). Unlike `||`, it does **not** treat `0`, `""`, or `جھوٹ` as nullish.

> **اردو:** خالی فالبیک `??` صرف اس وقت دائیں قدر واپس کرتا ہے جب بائیں قدر `خالی` یا `غیر_معرف` ہو۔ `||` کے برعکس، `0`، `""` اور `جھوٹ` کو خالی نہیں مانتا۔

```urdu
متغیر عمر = 0;
لکھو(عمر || 18);    // 18   (غلط! 0 کو falsy مانتا ہے)
لکھو(عمر ?? 18);    // 0    (صحیح — صرف null/undefined پر فالبیک)

متغیر رنگ = خالی;
لکھو(رنگ ?? "نیلا");   // نیلا
```

---

### Spread Operator `...`

Expand an iterable (list, string) into individual elements, or collect multiple arguments into a list.

> **اردو:** پھیلاؤ آپریٹر `...` سے فہرست کو پھیلائیں یا متعدد دلائل کو فہرست میں اکٹھا کریں۔

```urdu
// فہرست پھیلانا
متغیر ا = [1, 2, 3];
متغیر ب = [4, 5, 6];
متغیر ج = [...ا, ...ب];
لکھو(ج);   // [1, 2, 3, 4, 5, 6]

// فنکشن میں پھیلانا
فنکشن جمع(x, y, z) { واپس x + y + z; }
متغیر اعداد = [1, 2, 3];
لکھو(جمع(...اعداد));   // 6

// باقی پیرامیٹر
فنکشن سب_کچھ(پہلا, ...باقی) {
    لکھو("پہلا:", پہلا);
    لکھو("باقی:", باقی);
}
سب_کچھ(1, 2, 3, 4);
// پہلا: 1
// باقی: [2, 3, 4]
```

---

### Arrow Function `=>`

Shorthand for defining anonymous functions. The `=>` operator (also written as `->`) separates parameters from the function body.

> **اردو:** تیر فنکشن `=>` گمنام فنکشن کی مختصر شکل ہے۔ ایک لائن میں `واپس` ضمنی ہے۔

```urdu
// ایک لائن — واپس ضمنی ہے
مستقل مربع = x => x * x;
لکھو(مربع(5));    // 25

// متعدد پیرامیٹر
مستقل جمع = (ا, ب) => ا + ب;
لکھو(جمع(3, 4));  // 7

// بلاک باڈی — واپس صریح ہے
مستقل مطلق = x => {
    اگر (x < 0) واپس -x;
    واپس x;
};

// نقشہ / فلٹر میں استعمال
متغیر دگنا = نقشہ(x => x * 2, [1, 2, 3, 4, 5]);
لکھو(دگنا);   // [2, 4, 6, 8, 10]
```

---

### Increment / Decrement `++` / `--`

> **اردو:** `i++` پہلے پرانی قدر استعمال کرے پھر بڑھائے، `++i` پہلے بڑھائے پھر استعمال کرے۔

| Form | Name | Effect |
|------|------|--------|
| `i++` | postfix increment | Use current value of `i`, then add 1 |
| `++i` | prefix increment | Add 1 to `i`, then use new value |
| `i--` | postfix decrement | Use current value of `i`, then subtract 1 |
| `--i` | prefix decrement | Subtract 1 from `i`, then use new value |

```urdu
متغیر ن = 5;
لکھو(ن++);   // 5  (پرانی قدر)
لکھو(ن);     // 6
لکھو(++ن);   // 7  (نئی قدر)
لکھو(ن--);   // 7
لکھو(ن);     // 6
```

---

### Ternary (Conditional) Operator `? :`

A shorthand if-else expression: `condition ? value_if_true : value_if_false`

> **اردو:** ٹرنری آپریٹر مختصر if-else ہے: `شرط ? سچ_قدر : جھوٹ_قدر`

```urdu
متغیر عمر = 20;
متغیر حالت = (عمر >= 18) ? "بالغ" : "نابالغ";
لکھو(حالت);   // بالغ

// زنجیر
متغیر گریڈ = 82;
متغیر نتیجہ = گریڈ >= 90 ? "A"
            : گریڈ >= 80 ? "B"
            : گریڈ >= 70 ? "C"
            : "F";
لکھو(نتیجہ);   // B
```

---

### `typeof` — `قسم`

Return the type of a value as a string. See the [keywords reference](keywords.md#type-and-meta-operators--قسم-آپریٹر) for details.

> **اردو:** `قسم` آپریٹر قدر کی نوعیت بطور متن واپس کرتا ہے۔

```urdu
لکھو(قسم(42));         // "عدد"
لکھو(قسم("اردو"));     // "متن"
لکھو(قسم(سچ));         // "بولین"
لکھو(قسم(خالی));       // "خالی"
لکھو(قسم([]));          // "فہرست"
لکھو(قسم({}));          // "شے"
```

---

### `instanceof` — `مثال`

Test whether an object is an instance of a class.

> **اردو:** `مثال` آپریٹر جانچتا ہے کہ آیا کوئی شے کسی کلاس (class) کا نمونہ ہے۔

```urdu
// صرف صارف کی بنائی کلاسوں کے ساتھ کام کرتا ہے
کلاس جانور {}
کلاس کتا بڑھاؤ جانور {}

متغیر ک = نیا کتا();
لکھو(ک مثال کتا);      // True
لکھو(ک مثال جانور);    // True

متغیر ج = نیا جانور();
لکھو(ج مثال کتا);      // False
```

> **نوٹ:** `مثال` صرف صارف کی تعریف کردہ کلاسوں کے ساتھ کام کرتا ہے۔ بلٹ ان اقسام (`list`, `str`, `int`) کے ساتھ استعمال نہ کریں۔

---

### `in` / `میں_ہے`

Test whether a key or value exists in a collection.

> **اردو:** `میں_ہے` آپریٹر جانچتا ہے کہ آیا کوئی کلید یا قدر مجموعے میں موجود ہے۔

```urdu
متغیر ڈکشنری = { ا: 1, ب: 2, ج: 3 };
لکھو("ا" میں_ہے ڈکشنری);    // True
لکھو("د" میں_ہے ڈکشنری);    // False

متغیر فہرست = [10, 20, 30];
لکھو(20 میں فہرست);          // True
```

---

### `delete` — `حذف`

Remove a property from an object.

> **اردو:** `حذف` آپریٹر کسی شے سے خاصیت (property) ہٹاتا ہے۔

```urdu
متغیر شے = { ا: 1, ب: 2, ج: 3 };
حذف شے.ب;
لکھو(شے.مفاتیح(شے));   // ['ا', 'ج']
```

---

## Operator Precedence — آپریٹر ترجیح

Operators are evaluated in the order shown below — highest precedence first (evaluated first). When operators have the same precedence, associativity determines the order (left-to-right unless noted).

> **اردو:** آپریٹر ترجیح کا مطلب ہے کون پہلے چلتا ہے۔ اوپر والے پہلے چلتے ہیں۔ جب شک ہو تو قوسین `()` استعمال کریں کیونکہ گروپنگ سب سے زیادہ ترجیح رکھتی ہے۔

| Level | Operators | Name | Associativity |
|-------|-----------|------|---------------|
| 18 | `()` | Grouping | — |
| 17 | `?.` `[]` `.` `()` | Member access, call, optional chain | Left |
| 16 | `new` (with args) | Object creation | Right |
| 15 | `i++` `i--` | Postfix increment/decrement | Left |
| 14 | `!` `~` `+x` `-x` `++i` `--i` `قسم` `خلاء` `حذف` | Unary operators | Right |
| 13 | `**` | Exponentiation | **Right** |
| 12 | `*` `/` `%` `//` | Multiplicative | Left |
| 11 | `+` `-` | Additive | Left |
| 10 | `<<` `>>` `>>>` | Bitwise shift | Left |
| 9 | `<` `<=` `>` `>=` `میں` `میں_ہے` `مثال` | Relational | Left |
| 8 | `==` `!=` `===` `!==` | Equality | Left |
| 7 | `&` | Bitwise AND | Left |
| 6 | `^` | Bitwise XOR | Left |
| 5 | `\|` | Bitwise OR | Left |
| 4 | `&&` / `اور` | Logical AND | Left |
| 3 | `\|\|` / `یا` | Logical OR | Left |
| 2 | `??` | Nullish coalescing | Left |
| 1.5 | `? :` | Ternary conditional | **Right** |
| 1 | `=` `+=` `-=` `*=` `/=` `%=` `**=` `&&=` `\|\|=` `??=` `&=` `\|=` | Assignment | **Right** |
| 0 | `,` | Comma (sequence) | Left |

> **Rule of thumb:** When in doubt, use parentheses `()` to make the intended evaluation order explicit. Grouping is always at the highest precedence.

**Precedence Examples**

```urdu
// بغیر قوسین — طاقت پہلے، پھر ضرب
لکھو(2 + 3 * 4);       // 14  (نہیں 20)
لکھو((2 + 3) * 4);     // 20

// یاد رکھیں: ** دائیں سے بائیں ہے
لکھو(2 ** 3 ** 2);     // 512  (= 2 ** (3 ** 2) = 2 ** 9)
لکھو((2 ** 3) ** 2);   // 64

// منطقی آپریٹر کی ترتیب
لکھو(سچ || جھوٹ && جھوٹ);   // True  (&& پہلے چلتا ہے)
لکھو((سچ || جھوٹ) && جھوٹ); // False

// مقایسہ پہلے، پھر منطق
لکھو(5 > 3 && 10 < 20);    // True
لکھو(!(5 > 3) || 1 == 1);  // True

// nullish coalescing
متغیر الف = خالی ?? "فالبیک";
لکھو(الف);   // فالبیک

// تفویض دائیں سے بائیں
متغیر x, y, z;
x = y = z = 0;   // سب صفر
```

---

## Quick Cheat Sheet — فوری حوالہ

> **اردو:** عام آپریٹرز کی فوری یاد دہانی۔

```urdu
// ریاضی
5 + 3      // 8
10 - 4     // 6
3 * 7      // 21
10 / 4     // 2.5
10 % 3     // 1
2 ** 10    // 1024
عدد(10 / 3)    // 3  (floor division)

// مقایسہ
5 == 5     // True
5 === "5"  // False
5 != 6     // True
5 < 10     // True
5 >= 5     // True

// منطق
سچ && جھوٹ     // False
سچ || جھوٹ     // True
!سچ             // False
خالی ?? "اے"   // "اے"

// تفویض
x = 5
x += 3          // 8
x -= 2          // 6
x *= 3          // 18
x /= 6          // 3.0
x **= 2         // 9.0
x ??= "قدر"    // 9.0 (نہیں بدلا — خالی نہیں)

// خاص
شے?.خاصیت       // محفوظ رسائی
ا ?? ب          // خالی فالبیک
...فہرست        // پھیلانا
x => x * 2     // تیر فنکشن
شرط ? ا : ب    // ٹرنری
```

---

*اردو پروگرامنگ لینگویج — Operators Reference — Mohammed Zahid Wadiwale*
