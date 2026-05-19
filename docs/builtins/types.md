# Type Helpers — قسم مددگار

The Urdu Programming Language provides three static helper objects — `Object`, `Array`, and `String` — plus a set of built-in error classes. All are available globally without any import.

> **اردو:** اردو پروگرامنگ لینگویج تین جامد مددگار اشیاء — `Object`، `Array`، اور `String` — اور بنا بنایا غلطی کلاسز کا ایک مجموعہ فراہم کرتی ہے۔ یہ سب کسی بھی درآمد کے بغیر عالمی طور پر دستیاب ہیں۔

---

## Table of Contents

- [Object Helper — شے](#object-helper--شے)
- [Array Helper — صف](#array-helper--صف)
- [String Helper — ڈور](#string-helper--ڈور)
- [Error Types](#error-types)

---

## Object Helper — شے

`شے` (also `Object`) provides utility methods for working with dictionaries and object instances.

> **اردو:** `شے` (یا `Object`) لغتوں اور شے نمونوں کے ساتھ کام کرنے کے لیے مددگار طریقے فراہم کرتی ہے۔

---

### `Object.مفاتیح(obj) → list`

Return a list of all keys of a dictionary. For non-dict objects, returns a list of public attribute names (excluding names that begin with `_`).

Equivalent to JavaScript's `Object.keys()` or Python's `list(dict.keys())`.

> **اردو:** لغت کی تمام کلیدوں کی فہرست واپس کریں۔ غیر لغت اشیاء کے لیے عوامی صفت ناموں کی فہرست واپس کرتا ہے (`_` سے شروع ہونے والے ناموں کے بغیر)۔

**Examples**

```urdu
متغیر شخص = { نام: "احمد", عمر: 25, شہر: "کراچی" };
لکھو(Object.مفاتیح(شخص));
// ['نام', 'عمر', 'شہر']
```

```urdu
متغیر خالی_لغت = {};
لکھو(Object.مفاتیح(خالی_لغت));   // []
```

```urdu
// کلیدوں پر لوپ
کے_لیے (متغیر کلید کا Object.مفاتیح(شخص)) {
    لکھو(کلید, "=", شخص[کلید]);
}
```

---

### `Object.اقدار(obj) → list`

Return a list of all values of a dictionary.

Equivalent to JavaScript's `Object.values()` or Python's `list(dict.values())`.

> **اردو:** لغت کی تمام قدروں کی فہرست واپس کریں۔

**Examples**

```urdu
متغیر نمبرات = { ریاضی: 90, اردو: 85, سائنس: 95 };
لکھو(Object.اقدار(نمبرات));
// [90, 85, 95]

لکھو(مجموع(Object.اقدار(نمبرات)));   // 270
```

---

### `Object.اندراج(obj) → list`

Return a list of `[key, value]` pairs (as tuples) from a dictionary.

Equivalent to JavaScript's `Object.entries()` or Python's `list(dict.items())`.

> **اردو:** لغت سے `[کلید، قدر]` جوڑوں (ٹپلز) کی فہرست واپس کریں۔

**Examples**

```urdu
متغیر مضامین = { ریاضی: 90, اردو: 85, سائنس: 95 };
کے_لیے (متغیر [مضمون, نمبر] کا Object.اندراج(مضامین)) {
    لکھو(مضمون, ":", نمبر);
}
// ریاضی : 90
// اردو : 85
// سائنس : 95
```

```urdu
// جدول بنانا
متغیر کل = مجموع(نقشہ(جوڑا => جوڑا[1], Object.اندراج(مضامین)));
لکھو("کل نمبر:", کل);   // 270
```

---

### `Object.تفویض(target, *sources) → dict`

Merge one or more source dictionaries into `target`. Properties from later sources overwrite earlier ones. Mutates and returns `target`.

Equivalent to JavaScript's `Object.assign()` or Python's `dict.update()`.

> **اردو:** ایک یا زیادہ ذریعہ لغتوں کو `target` میں ضم کریں۔ بعد کے ذرائع کی خاصیات پہلے والوں کو اوور رائٹ کرتی ہیں۔ `target` کو تبدیل کر کے واپس کرتا ہے۔

**Examples**

```urdu
متغیر بنیاد = { رنگ: "نیلا", سائز: "بڑا" };
متغیر اضافہ = { وزن: 1.5, رنگ: "سبز" };
Object.تفویض(بنیاد, اضافہ);
لکھو(بنیاد);
// {'رنگ': 'سبز', 'سائز': 'بڑا', 'وزن': 1.5}
```

```urdu
// ڈیفالٹ اقدار
متغیر ڈیفالٹ = { زبان: "اردو", تاریک_حالت: جھوٹ, فونٹ_سائز: 14 };
متغیر صارف = { فونٹ_سائز: 18 };
متغیر ترتیب = Object.تفویض({}, ڈیفالٹ, صارف);
لکھو(ترتیب.فونٹ_سائز);   // 18
لکھو(ترتیب.زبان);          // اردو
```

---

### `Object.منجمد(obj) → obj`

Mark an object as frozen (read-only). Returns the same object.

> Note: In the current runtime this is a no-op placeholder that returns the object unchanged (true immutability enforcement is not implemented). It is provided for API compatibility.

> **اردو:** شے کو منجمد (صرف پڑھنے کے قابل) نشان زد کریں۔ وہی شے واپس کرتا ہے۔ نوٹ: موجودہ رن ٹائم میں یہ کوئی عمل نہیں کرتا (API ہم آہنگی کے لیے موجود ہے)۔

**Examples**

```urdu
متغیر ثابت = Object.منجمد({ پائی: 3.14159 });
لکھو(ثابت.پائی);   // 3.14159
```

---

### `Object.بنا(**kwargs) → dict`

Create a new `_UrduObj` dictionary from keyword arguments. The resulting object supports both `obj.key` and `obj["key"]` access.

> **اردو:** کلیدی الفاظ کے دلائل سے نئی `_UrduObj` لغت بنائیں۔ نتیجہ `obj.key` اور `obj["key"]` دونوں طریقوں سے رسائی کی حمایت کرتا ہے۔

**Examples**

```urdu
متغیر نقطہ = Object.بنا(x=10, y=20, z=0);
لکھو(نقطہ.x, نقطہ.y);   // 10 20
```

---

## Array Helper — صف

`صف` (also `Array`) provides utility methods for working with sequences.

> **اردو:** `صف` (یا `Array`) ترتیبوں کے ساتھ کام کرنے کے لیے مددگار طریقے فراہم کرتی ہے۔

---

### `Array.سے(iterable) → list`

Convert any iterable (range, tuple, set, string, generator) to a list.

Equivalent to JavaScript's `Array.from()` or Python's `list(iterable)`.

> **اردو:** کسی بھی تکرار پذیر (حد، ٹپل، مجموعہ، سٹرنگ، جنریٹر) کو فہرست میں تبدیل کریں۔

**Examples**

```urdu
لکھو(Array.سے(حد(5)));
// [0, 1, 2, 3, 4]

لکھو(Array.سے("اردو"));
// ['ا', 'ر', 'د', 'و']

لکھو(Array.سے(مجموعہ([1, 2, 2, 3, 3])));
// [1, 2, 3]  (ترتیب مختلف ہو سکتی ہے)
```

```urdu
// زپ کو فہرست میں بدلنا
متغیر الف = [1, 2, 3];
متغیر ب   = [4, 5, 6];
لکھو(Array.سے(زپ(الف, ب)));
// [(1, 4), (2, 5), (3, 6)]
```

---

### `Array.ہے(x) → bool`

Return `True` if `x` is a list or tuple, otherwise `False`.

Equivalent to JavaScript's `Array.isArray()`.

> **اردو:** اگر `x` فہرست یا ٹپل ہو تو `True` واپس کریں، ورنہ `False`۔

**Examples**

```urdu
لکھو(Array.ہے([1, 2, 3]));        // True
لکھو(Array.ہے((1, 2, 3)));        // True
لکھو(Array.ہے("اردو"));           // False
لکھو(Array.ہے({ ک: "قدر" }));    // False
لکھو(Array.ہے(42));               // False
```

```urdu
// دفاعی پروگرامنگ
فنکشن جمع_کرو(ڈیٹا) {
    اگر (!Array.ہے(ڈیٹا)) {
        پھینکو نیا قسم_غلطی("فہرست درکار ہے");
    }
    واپس مجموع(ڈیٹا);
}
```

---

## String Helper — ڈور

`ڈور` (also `String`) provides character-level utilities for strings.

> **اردو:** `ڈور` (یا `String`) سٹرنگز کے لیے حرف سطح کی مددگار سہولتیں فراہم کرتی ہے۔

---

### `String.سے(x) → str`

Convert any value to its string representation. Equivalent to Python's `str(x)`.

> **اردو:** کسی بھی قدر کو اس کی سٹرنگ نمائندگی میں تبدیل کریں۔

**Examples**

```urdu
لکھو(String.سے(42));       // "42"
لکھو(String.سے(3.14));     // "3.14"
لکھو(String.سے([1,2,3]));  // "[1, 2, 3]"
لکھو(String.سے(سچ));       // "True"
```

---

### `String.کوڈ(s, i=0) → int`

Return the Unicode code point (integer) of the character at index `i` in string `s`. Equivalent to Python's `ord(s[i])`.

> **اردو:** سٹرنگ `s` میں انڈیکس `i` پر حرف کا یونیکوڈ کوڈ پوائنٹ (عدد صحیح) واپس کریں۔

**Examples**

```urdu
لکھو(String.کوڈ("A"));       // 65
لکھو(String.کوڈ("ا"));       // 1575  (Unicode U+0627)
لکھو(String.کوڈ("اردو", 1)); // 1585  (ر at index 1)
لکھو(String.کوڈ("0"));       // 48
```

---

### `String.حرف(code) → str`

Return the single character whose Unicode code point is `code`. Equivalent to Python's `chr(code)`.

> **اردو:** وہ واحد حرف واپس کریں جس کا یونیکوڈ کوڈ پوائنٹ `code` ہو۔

**Examples**

```urdu
لکھو(String.حرف(65));      // A
لکھو(String.حرف(1575));    // ا
لکھو(String.حرف(48));      // 0
```

```urdu
// ASCII جدول
کے_لیے (متغیر i کا حد(65, 91)) {
    لکھو(i, "=", String.حرف(i));
}
// 65 = A  66 = B  ... 90 = Z
```

---

## Error Types — غلطی کی اقسام

All error classes extend the base `غلطی` class, which in turn extends Python's `Exception`. Every error instance has a `.پیغام` (and `.message`) attribute containing the error description.

Errors are raised with `پھینکو` and caught with `پکڑو`.

> **اردو:** تمام غلطی کلاسز بنیادی `غلطی` کلاس سے وراثت لیتی ہیں، جو Python کی `Exception` کو وراثت میں لیتی ہے۔ ہر غلطی نمونے میں `.پیغام` (اور `.message`) صفت ہوتی ہے۔ غلطیاں `پھینکو` سے اٹھائی جاتی ہیں اور `پکڑو` سے پکڑی جاتی ہیں۔

---

### `غلطی` / `Error`

The base error class. Use for general-purpose errors when no more specific type applies.

> **اردو:** بنیادی غلطی کلاس۔ عام مقصد کی غلطیوں کے لیے استعمال کریں جب کوئی زیادہ مخصوص قسم موزوں نہ ہو۔

```urdu
کوشش {
    پھینکو نیا غلطی("کچھ غلط ہوا");
} پکڑو (غ) {
    لکھو("پکڑا:", غ.پیغام);   // پکڑا: کچھ غلط ہوا
}
```

---

### `قسم_غلطی` / `TypeError`

Raised when a value is of the wrong type for an operation (e.g., calling a non-function, adding incompatible types).

> **اردو:** جب کسی آپریشن کے لیے غلط قسم کی قدر ہو تو اٹھائی جاتی ہے (مثلاً غیر فنکشن کو کہنا، غیر موافق اقسام جوڑنا)۔

```urdu
فنکشن ضرب(ا, ب) {
    اگر (قسم(ا) != "عدد" || قسم(ب) != "عدد") {
        پھینکو نیا قسم_غلطی("صرف اعداد قبول ہیں");
    }
    واپس ا * ب;
}

کوشش {
    ضرب("پانچ", 3);
} پکڑو (غ) {
    لکھو("قسم_غلطی:", غ.پیغام);
}
```

---

### `حد_غلطی` / `IndexError` / `RangeError`

Raised when an index is out of bounds for a sequence.

> **اردو:** جب انڈیکس کسی ترتیب کی حد سے باہر ہو تو اٹھائی جاتی ہے۔

```urdu
متغیر فہرست = [1, 2, 3];
کوشش {
    لکھو(فہرست[10]);
} پکڑو (غ) {
    لکھو("حد سے باہر:", غ.پیغام);
}
```

---

### `حوالہ_غلطی` / `NameError` / `ReferenceError`

Raised when a name (variable or function) is used before it is defined, or does not exist in the current scope.

> **اردو:** جب کسی نام (متغیر یا فنکشن) کو تعریف سے پہلے استعمال کیا جائے، یا وہ موجودہ گنجائش میں موجود نہ ہو۔

```urdu
کوشش {
    لکھو(غیر_موجود_متغیر);
} پکڑو (غ) {
    لکھو("حوالہ_غلطی:", غ.پیغام);
}
```

---

### `نحو_غلطی` / `SyntaxError`

Raised when code cannot be parsed due to a syntax error. Usually generated by the transpiler pipeline rather than user code.

> **اردو:** جب نحو کی غلطی کی وجہ سے کوڈ پارس نہ ہو سکے۔ عام طور پر ٹرانسپائلر پائپ لائن سے پیدا ہوتی ہے نہ کہ صارف کے کوڈ سے۔

```urdu
کوشش {
    متحرک_چلاؤ("@@@ غلط نحو @@@");
} پکڑو (غ) {
    لکھو("نحو_غلطی:", غ.پیغام);
}
```

---

### `رینج_غلطی` / `ValueError` / `RangeError`

Raised when a value is of the correct type but falls outside an acceptable range (e.g., a negative number where only positives are accepted, or a string that cannot be parsed as a number).

> **اردو:** جب قدر درست قسم کی ہو لیکن قابل قبول حد سے باہر ہو (مثلاً جہاں صرف مثبت قبول ہو وہاں منفی عدد، یا ایسی سٹرنگ جو عدد کے طور پر پارس نہ ہو سکے)۔

```urdu
فنکشن جذر(x) {
    اگر (x < 0) {
        پھینکو نیا رینج_غلطی("منفی عدد کا جذر نہیں نکلتا");
    }
    واپس ریاضی.جذر(x);
}

کوشش {
    جذر(-4);
} پکڑو (غ) {
    لکھو("رینج_غلطی:", غ.پیغام);
}
```

---

### `نیٹ_غلطی` / `ConnectionError` / `NetworkError`

Raised for network and connectivity failures (e.g., HTTP request timeout, connection refused).

> **اردو:** نیٹ ورک اور رابطے کی ناکامیوں کے لیے اٹھائی جاتی ہے (مثلاً HTTP درخواست ٹائم آؤٹ، رابطہ مسترد)۔

```urdu
کوشش {
    // نیٹ ورک درخواست
    متغیر نتیجہ = http_درخواست("https://example.com");
} پکڑو (غ) {
    اگر (نمونہ(نیٹ_غلطی, غ)) {
        لکھو("نیٹ ورک خطا:", غ.پیغام);
    } ورنہ {
        پھینکو غ;
    }
}
```

---

### `فائل_غلطی` / `FileNotFoundError`

Raised when a file or directory operation fails because the path does not exist.

> **اردو:** جب فائل یا ڈائریکٹری کا آپریشن ناکام ہو کیونکہ راستہ موجود نہ ہو۔

```urdu
کوشش {
    // فائل کھولنا
    متغیر مواد = فائل_پڑھو("غیر_موجود.txt");
} پکڑو (غ) {
    اگر (نمونہ(فائل_غلطی, غ)) {
        لکھو("فائل نہیں ملی:", غ.پیغام);
    } ورنہ {
        پھینکو غ;
    }
}
```

---

## Error Class Hierarchy — غلطی کلاس درجہ بندی

> **اردو:** غلطی کلاسز کی درجہ بندی:

```
Exception (Python)
└── غلطی  (base Urdu error)
    ├── قسم_غلطی    (TypeError)
    ├── حد_غلطی     (IndexError)
    ├── حوالہ_غلطی  (NameError)
    ├── نحو_غلطی    (SyntaxError)
    ├── رینج_غلطی   (ValueError)
    ├── نیٹ_غلطی    (ConnectionError)
    └── فائل_غلطی   (FileNotFoundError)
```

All error classes can be used with `نمونہ()` for type-based catching:

> **اردو:** تمام غلطی کلاسز قسم پر مبنی پکڑنے کے لیے `نمونہ()` کے ساتھ استعمال کی جا سکتی ہیں:

```urdu
کوشش {
    // ... کوئی بھی کوڈ ...
} پکڑو (غ) {
    اگر (نمونہ(فائل_غلطی, غ)) {
        لکھو("فائل خطا");
    } ورنہ_اگر (نمونہ(نیٹ_غلطی, غ)) {
        لکھو("نیٹ ورک خطا");
    } ورنہ_اگر (نمونہ(قسم_غلطی, غ)) {
        لکھو("قسم کی غلطی");
    } ورنہ {
        لکھو("نامعلوم غلطی:", غ.پیغام);
    }
}
```

---

## Error Attributes — غلطی کی صفات

Every error instance exposes these attributes:

> **اردو:** ہر غلطی نمونہ یہ صفات ظاہر کرتا ہے:

| Attribute | Type | Description |
|-----------|------|-------------|
| `.پیغام` | str | The error message (Urdu alias) |
| `.message` | str | The error message (English alias) |

```urdu
متغیر غ = نیا غلطی("کچھ غلط ہوا");
لکھو(غ.پیغام);    // کچھ غلط ہوا
لکھو(غ.message);  // کچھ غلط ہوا
```

---

*اردو پروگرامنگ لینگویج — Type Helpers Reference — Mohammed Zahid Wadiwale*


