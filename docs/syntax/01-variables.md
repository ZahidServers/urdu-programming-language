# Variables and Constants — متغیرات اور مستقلات

This document covers how to declare, assign, and work with variables and constants in the Urdu Programming Language.

> **اردو:** یہ دستاویز اردو پروگرامنگ لینگویج میں متغیرات اور مستقلات کو ڈکلیئر کرنے، اسائن کرنے اور استعمال کرنے کا طریقہ بیان کرتی ہے۔

---

## Table of Contents

1. [متغیر — Variables](#متغیر--variables)
2. [مستقل — Constants](#مستقل--constants)
3. [Naming Rules](#naming-rules)
4. [Multiple Assignment](#multiple-assignment)
5. [Destructuring Assignment — Objects](#destructuring-assignment--objects)
6. [Destructuring Assignment — Arrays](#destructuring-assignment--arrays)
7. [Default Values in Destructuring](#default-values-in-destructuring)
8. [Nested Destructuring](#nested-destructuring)
9. [Swap Variables](#swap-variables)
10. [Practical Examples](#practical-examples)

---

## متغیر — Variables

The keyword `متغیر` declares a variable. Variables declared with `متغیر` can be reassigned at any time. They are block-scoped.

> **اردو:** `متغیر` کلیدی لفظ متغیر ڈکلیئر کرتا ہے۔ `متغیر` سے بنائے گئے متغیرات کو کسی بھی وقت دوبارہ اسائن کیا جا سکتا ہے۔ یہ بلاک سکوپڈ ہوتے ہیں — یعنی صرف اس بلاک میں دستیاب ہوتے ہیں جہاں بنائے گئے۔

**Syntax:**

```urdu
متغیر نام = قدر;
```

**Basic examples:**

```urdu
متغیر عمر = 25;
متغیر نام = "احمد";
متغیر قیمت = 99.5;
متغیر فعال = سچ;
متغیر خالی_قدر = خالی;

لکھو(عمر);      // 25
لکھو(نام);      // احمد
لکھو(قیمت);    // 99.5
لکھو(فعال);    // true
لکھو(خالی_قدر); // null
```

**Reassigning a variable:**

```urdu
متغیر گنتی = 0;
لکھو(گنتی);   // 0

گنتی = 10;
لکھو(گنتی);   // 10

گنتی = گنتی + 5;
لکھو(گنتی);   // 15
```

> **اردو:** متغیر کو کسی بھی وقت نئی قدر دی جا سکتی ہے۔ پہلے صفر ہے، پھر 10، پھر 15 ہو گیا۔

**Declaring without an initial value:**

A variable declared without a value is `غیر_معرف` (undefined) until assigned.

```urdu
متغیر رنگ;
لکھو(رنگ);    // undefined

رنگ = "نیلا";
لکھو(رنگ);    // نیلا
```

> **اردو:** اگر متغیر بناتے وقت قدر نہ دیں تو وہ `غیر_معرف` (undefined) ہوتا ہے۔ بعد میں جب چاہیں قدر دے سکتے ہیں۔

---

## مستقل — Constants

The keyword `مستقل` declares a constant. Once assigned, a constant cannot be reassigned. It is also block-scoped.

> **اردو:** `مستقل` کلیدی لفظ مستقل ڈکلیئر کرتا ہے۔ ایک بار قدر دینے کے بعد اسے تبدیل نہیں کیا جا سکتا۔ یہ بھی بلاک سکوپڈ ہے۔

**Syntax:**

```urdu
مستقل نام = قدر;
```

**Basic examples:**

```urdu
مستقل پائی = 3.14159;
مستقل زبان = "اردو";
مستقل سال = 2024;

لکھو(پائی);   // 3.14159
لکھو(زبان);   // اردو
لکھو(سال);    // 2024
```

> **Note:** Attempting to reassign a constant will throw a `TypeError` at runtime.
>
> ```urdu
> مستقل حد = 100;
> حد = 200;  // غلطی: cannot reassign constant
> ```

> **اردو:** **نوٹ:** مستقل کو دوبارہ اسائن کرنے کی کوشش کرنے پر پروگرام چلتے وقت `TypeError` غلطی آئے گی۔

**Constants with objects and arrays:**

The reference is constant, but the contents of objects and arrays can still be mutated.

```urdu
مستقل شخص = { نام: "فاطمہ", عمر: 30 };
شخص.عمر = 31;           // جائز — object contents changed
لکھو(شخص.عمر);          // 31

مستقل اعداد = [1, 2, 3];
اعداد.شامل(4);           // جائز — array contents changed
لکھو(اعداد);            // [1, 2, 3, 4]
```

> **اردو:** مستقل کے ساتھ شے (object) یا فہرست (array) کی صورت میں — حوالہ مستقل ہے، لیکن اندر کا مواد تبدیل ہو سکتا ہے۔ یعنی `شخص.عمر` تبدیل کر سکتے ہیں، لیکن `شخص` کو بالکل نئی شے نہیں دے سکتے۔

---

## Naming Rules — نام رکھنے کے قواعد

Variable and constant names follow these rules:

| Rule | Details |
|------|---------|
| **Urdu identifiers** | Names can be written entirely in Urdu script |
| **Latin identifiers** | Standard ASCII letters, digits, `_` are also allowed |
| **Mixed** | Mixing Urdu and ASCII characters is allowed |
| **Start character** | Must start with a letter (Urdu or Latin) or `_`; not a digit |
| **Reserved words** | Language keywords (e.g., `اگر`, `جبکہ`) cannot be used as names |
| **Case sensitive** | `نام` and `نام2` are different; `x` and `X` are different |

> **اردو:** متغیر اور مستقل کے نام رکھنے کے قواعد: نام مکمل اردو میں، مکمل لاطینی میں یا دونوں ملا کر لکھ سکتے ہیں۔ نام کا پہلا حرف ہمیشہ حرف (اردو یا لاطینی) یا `_` ہونا چاہیے — عدد سے شروع نہیں ہو سکتا۔ زبان کے کلیدی الفاظ (جیسے `اگر`، `جبکہ`) نام کے طور پر نہیں ہو سکتے۔ بڑے اور چھوٹے حروف الگ الگ سمجھے جاتے ہیں۔

**Valid names:**

```urdu
متغیر نام_طالب_علم = "زینب";
متغیر _وقت = 0;
متغیر رقم1 = 500;
متغیر totalPrice = 1200;
متغیر قیمت_کل = 1200;
متغیر userName = "admin";
متغیر کاؤنٹر = 0;
```

**Invalid names (will cause errors):**

```urdu
// متغیر 3رنگ = "سرخ";    // غلط — starts with digit
// متغیر اگر = 5;          // غلط — reserved keyword
// متغیر نام رنگ = "سبز";  // غلط — space in name
```

> **اردو:** اوپر کے درست نام قابلِ قبول ہیں — اردو، انگریزی یا ملے جلے۔ نیچے کے غلط نام: عدد سے شروع، کلیدی لفظ، یا نام میں خالی جگہ — یہ سب غلطی دیں گے۔

---

## Multiple Assignment — متعدد اسائنمنٹ

You can declare multiple variables on a single line or assign the same value to multiple variables.

> **اردو:** ایک ہی لائن میں کئی متغیرات ڈکلیئر کر سکتے ہیں یا ایک ہی قدر کئی متغیرات کو دے سکتے ہیں۔

**Multiple declarations:**

```urdu
متغیر الف = 1, ب = 2, ج = 3;
لکھو(الف, ب, ج);   // 1 2 3
```

**Chained assignment:**

```urdu
متغیر x, y, z;
x = y = z = 10;
لکھو(x, y, z);    // 10 10 10
```

**Declaring multiple constants:**

```urdu
مستقل چوڑائی = 800, اونچائی = 600;
مستقل رنگ_پس_منظر = "سفید", رنگ_سرخی = "#FF0000";
لکھو(چوڑائی, اونچائی);
```

> **اردو:** زنجیری اسائنمنٹ میں `x = y = z = 10` سے تینوں متغیرات ایک ساتھ 10 ہو جاتے ہیں۔

---

## Destructuring Assignment — Objects — شے سے توڑنا

Object destructuring extracts properties from an object into named variables. The variable names must match the property keys.

> **اردو:** شے سے توڑنا (object destructuring) کسی شے کی خاصیتوں کو نامدار متغیرات میں نکالتا ہے۔ متغیرات کے نام شے کی کلیدوں سے ملنے چاہیں۔

> **Note:** Object destructuring (`متغیر { نام } = شے`) is currently not supported. Use bracket notation instead: `متغیر نام = شے["نام"]`.

> **اردو:** **نوٹ:** شے توڑنا (`متغیر { نام } = شے`) فی الحال سپورٹ نہیں ہے۔ اس کی بجائے بریکٹ نوٹیشن استعمال کریں: `متغیر نام = شے["نام"]`۔

**Basic object destructuring:**

```urdu
مستقل شخص = { نام: "عمر", عمر: 28, شہر: "کراچی" };

متغیر { نام, عمر, شہر } = شخص;
لکھو(نام);    // عمر
لکھو(عمر);   // 28
لکھو(شہر);   // کراچی
```

**Rename while destructuring (aliasing):**

```urdu
مستقل ملازم = { نام: "سارہ", عہدہ: "مینیجر" };

متغیر { نام: ملازم_نام, عہدہ: ملازم_عہدہ } = ملازم;
لکھو(ملازم_نام);    // سارہ
لکھو(ملازم_عہدہ);   // مینیجر
```

> **اردو:** نام بدل کر توڑنے میں `نام: ملازم_نام` کا مطلب ہے: شے سے `نام` نکالو اور اسے `ملازم_نام` متغیر میں رکھو۔

**Destructuring in function parameters:**

```urdu
فنکشن تعارف({ نام, عمر }) {
    لکھو(`میرا نام ${نام} ہے اور عمر ${عمر} سال ہے`);
}

تعارف({ نام: "حسن", عمر: 22 });
// میرا نام حسن ہے اور عمر 22 سال ہے
```

**Collecting remaining properties with rest:**

```urdu
مستقل گاڑی = { برانڈ: "ٹویوٹا", ماڈل: "کورولا", رنگ: "سفید", سال: 2022 };

متغیر { برانڈ, ماڈل, ...باقی } = گاڑی;
لکھو(برانڈ);   // ٹویوٹا
لکھو(ماڈل);    // کورولا
لکھو(باقی);    // { رنگ: "سفید", سال: 2022 }
```

> **اردو:** `...باقی` سے شے کی بچی ہوئی تمام خاصیتیں ایک نئی شے میں جمع ہو جاتی ہیں۔

---

## Destructuring Assignment — Arrays — فہرست سے توڑنا

Array destructuring extracts elements by position.

> **اردو:** فہرست سے توڑنا عناصر کو ان کی جگہ (position) کے حساب سے نکالتا ہے۔

**Basic array destructuring:**

```urdu
مستقل رنگ = ["سرخ", "سبز", "نیلا"];

متغیر [پہلا, دوسرا, تیسرا] = رنگ;
لکھو(پہلا);    // سرخ
لکھو(دوسرا);   // سبز
لکھو(تیسرا);   // نیلا
```

**Skip elements:**

```urdu
مستقل اعداد = [10, 20, 30, 40, 50];

متغیر [پہلا, , تیسرا, , پانچواں] = اعداد;
لکھو(پہلا);      // 10
لکھو(تیسرا);     // 30
لکھو(پانچواں);   // 50
```

> **اردو:** درمیانی خانہ خالی چھوڑ کر عناصر چھوڑ سکتے ہیں — `[پہلا, , تیسرا]` میں دوسرا عنصر نظرانداز ہو گیا۔

**Rest element in arrays:**

```urdu
مستقل فہرست = [1, 2, 3, 4, 5];

متغیر [سر, ...دم] = فہرست;
لکھو(سر);    // 1
لکھو(دم);    // [2, 3, 4, 5]
```

**Destructuring from a function return:**

```urdu
فنکشن حدود() {
    واپس [0, 100];
}

متغیر [کم, زیادہ] = حدود();
لکھو(کم);      // 0
لکھو(زیادہ);   // 100
```

> **اردو:** فنکشن سے فہرست واپس کرنے پر اسے سیدھا توڑ کر الگ متغیرات میں رکھ سکتے ہیں — بہت صاف طریقہ!

---

## Default Values in Destructuring — توڑنے میں پہلے سے طے قدریں

If a property or element is missing or `غیر_معرف`, a default value is used.

> **اردو:** اگر کوئی خاصیت یا عنصر موجود نہ ہو یا `غیر_معرف` ہو تو پہلے سے طے قدر (default value) استعمال ہوتی ہے۔

**Object destructuring with defaults:**

```urdu
مستقل ترتیبات = { تھیم: "گہرا" };

متغیر { تھیم = "روشن", زبان = "اردو", سائز = 14 } = ترتیبات;
لکھو(تھیم);    // گہرا      (موجود تھا)
لکھو(زبان);    // اردو      (پہلے سے طے)
لکھو(سائز);    // 14        (پہلے سے طے)
```

**Array destructuring with defaults:**

```urdu
مستقل رنگ = ["سرخ"];

متغیر [پہلا = "کالا", دوسرا = "سفید"] = رنگ;
لکھو(پہلا);    // سرخ   (موجود تھا)
لکھو(دوسرا);   // سفید  (پہلے سے طے)
```

**Combined alias and default:**

```urdu
مستقل ڈیٹا = { قدر: خالی };

متغیر { قدر: نتیجہ = "ناپید" } = ڈیٹا;
لکھو(نتیجہ);   // null  (خالی موجود تھا — default only applies to undefined)
```

> **Note:** Default values apply only when the value is `غیر_معرف`. If the value is `خالی` (null), the default is NOT used.

> **اردو:** **نوٹ:** پہلے سے طے قدر صرف اس وقت استعمال ہوتی ہے جب قدر `غیر_معرف` (undefined) ہو۔ اگر قدر `خالی` (null) ہو تو پہلے سے طے قدر **نہیں** لگتی — `خالی` وہاں رہتا ہے۔

---

## Nested Destructuring — گہرا توڑنا

Destructuring can be nested to extract values from deeply nested structures.

> **اردو:** توڑنے کو ایک دوسرے کے اندر لگا کر گہرے ڈھانچوں سے قدریں نکالی جا سکتی ہیں۔

**Nested object destructuring:**

```urdu
مستقل کمپنی = {
    نام: "ٹیک لیب",
    پتہ: {
        شہر: "لاہور",
        ملک: "پاکستان"
    }
};

متغیر { نام, پتہ: { شہر, ملک } } = کمپنی;
لکھو(نام);    // ٹیک لیب
لکھو(شہر);   // لاہور
لکھو(ملک);   // پاکستان
```

**Nested array destructuring:**

```urdu
مستقل میٹرکس = [[1, 2], [3, 4], [5, 6]];

متغیر [[الف, ب], [ج, د]] = میٹرکس;
لکھو(الف, ب);   // 1 2
لکھو(ج, د);     // 3 4
```

**Mixed nested destructuring:**

```urdu
مستقل صارف = {
    نام: "علی",
    پتہ: { شہر: "اسلام آباد" },
    ہنر: ["پروگرامنگ", "ڈیزائن"]
};

متغیر {
    نام: صارف_نام,
    پتہ: { شہر },
    ہنر: [پہلا_ہنر]
} = صارف;

لکھو(صارف_نام);     // علی
لکھو(شہر);         // اسلام آباد
لکھو(پہلا_ہنر);    // پروگرامنگ
```

> **اردو:** گہرا توڑنا بہت طاقتور ہے — شے، فہرست اور ملے جلے ڈھانچے سب کو ایک ہی بار میں توڑا جا سکتا ہے۔

---

## Swap Variables — متغیرات بدلنا

Array destructuring makes swapping two variables concise without a temporary variable.

> **اردو:** فہرست توڑنا دو متغیرات کی قدریں بدلنے کا بہت آسان طریقہ ہے — کسی عارضی متغیر کی ضرورت نہیں!

```urdu
متغیر الف = "پہلا";
متغیر ب = "دوسرا";

لکھو(الف, ب);    // پہلا دوسرا

[الف, ب] = [ب, الف];

لکھو(الف, ب);    // دوسرا پہلا
```

**Rotating three variables:**

```urdu
متغیر x = 1, y = 2, z = 3;
[x, y, z] = [y, z, x];
لکھو(x, y, z);   // 2 3 1
```

> **اردو:** تین متغیرات کو گھمانا بھی اتنا ہی آسان — ایک ہی لائن میں سب بدل جاتے ہیں۔

---

## Practical Examples — عملی مثالیں

**Storing user profile data:**

```urdu
مستقل صارف = {
    نام: "مریم",
    ای_میل: "maryam@example.com",
    عمر: 27,
    فعال: سچ
};

متغیر { نام, ای_میل, عمر, فعال } = صارف;
لکھو(`صارف: ${نام}`);
لکھو(`ای میل: ${ای_میل}`);
لکھو(`عمر: ${عمر}`);
لکھو(`فعال: ${فعال}`);
```

> **اردو:** صارف کا ڈیٹا شے میں رکھ کر توڑنے سے صاف اور پڑھنے میں آسان کوڈ بنتا ہے۔

**Configuration with defaults:**

```urdu
فنکشن ترتیب_دو(اختیارات = {}) {
    متغیر {
        میزبان = "localhost",
        بندرگاہ = 3000,
        محفوظ = جھوٹ,
        ٹائم_آؤٹ = 5000
    } = اختیارات;

    لکھو(`${محفوظ ? "https" : "http"}://${میزبان}:${بندرگاہ}`);
    لکھو(`ٹائم آؤٹ: ${ٹائم_آؤٹ}ms`);
}

ترتیب_دو({ میزبان: "example.com", محفوظ: سچ });
// https://example.com:3000
// ٹائم آؤٹ: 5000ms
```

> **اردو:** یہ ایک عام نمونہ ہے — ترتیبات کی شے پاس کریں، جو نہ دی ہو وہ پہلے سے طے قدر استعمال کرے۔

**Processing a list of students:**

```urdu
مستقل طلباء = [
    { نام: "احمد", نمبر: 85 },
    { نام: "بیا",  نمبر: 92 },
    { نام: "ثمر",  نمبر: 78 }
];

کے_لیے (متغیر { نام, نمبر } کا طلباء) {
    متغیر درجہ = نمبر >= 90 ? "A" : نمبر >= 80 ? "B" : "C";
    لکھو(`${نام}: ${نمبر} (${درجہ})`);
}
// احمد: 85 (B)
// بیا: 92 (A)
// ثمر: 78 (C)
```

**Coordinate unpacking:**

```urdu
فنکشن مرکز_حاصل_کرو(شکل) {
    مستقل { x = 0, y = 0, چوڑائی = 100, اونچائی = 100 } = شکل;
    واپس [x + چوڑائی / 2, y + اونچائی / 2];
}

متغیر [مرکز_x, مرکز_y] = مرکز_حاصل_کرو({ x: 50, y: 50, چوڑائی: 200, اونچائی: 100 });
لکھو(`مرکز: (${مرکز_x}, ${مرکز_y})`);
// مرکز: (150, 100)
```

> **اردو:** یہ آخری مثال دکھاتی ہے کہ شے توڑنا (پہلے سے طے قدروں کے ساتھ) اور فہرست توڑنا دونوں ایک ساتھ کیسے استعمال ہوتے ہیں — ایک نقطے کا مرکز نکالنا بہت آسان ہو گیا۔
