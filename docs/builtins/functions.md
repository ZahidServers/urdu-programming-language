# Built-in Functions — اردو پروگرامنگ لینگویج

All built-in functions listed below are available in every Urdu program without any import. They are injected into the global namespace automatically at startup.

> **اردو:** نیچے درج تمام بنا بنایا فنکشنز ہر اردو پروگرام میں بغیر کسی درآمد کے دستیاب ہیں۔ یہ شروع ہونے پر خود بخود عالمی نام فضا میں شامل ہو جاتے ہیں۔

---

## Table of Contents

- [Input / Output](#inputoutput)
- [Type Conversion](#type-conversion)
- [Collections](#collections)
- [Sequence and Iteration](#sequence-and-iteration)
- [Aggregation](#aggregation)
- [Math](#math)
- [String Utilities](#string-utilities)
- [JSON](#json)
- [Time](#time)
- [Random](#random)
- [Type Checking](#type-checking)
- [Advanced Execution](#advanced-execution)
- [Parsing Utilities](#parsing-utilities)
- [Global Constants](#global-constants)

---

## Input/Output — ان پٹ/آؤٹ پٹ

### `لکھو(*args, sep=" ", end="\n")`

Print one or more values to the console. Fully supports Urdu (Arabic-script) text and mixed bidirectional output via Unicode BiDi markers, so Urdu text renders correctly in modern terminals (Windows Terminal, VS Code, xterm).

> **اردو:** ایک یا زیادہ قدریں کنسول پر پرنٹ کریں۔ اردو (عربی رسم الخط) متن کو مکمل حمایت حاصل ہے اور یونیکوڈ BiDi نشانات کے ذریعے جدید ٹرمینلز میں صحیح طور پر ظاہر ہوتا ہے۔

**Parameters**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `*args`   | —       | One or more values to print. Each is converted to a string automatically. |
| `sep`     | `" "`   | Separator string inserted between arguments. |
| `end`     | `"\n"`  | String appended after the last argument. |

**Returns:** `خالی` (nothing)

**Examples**

```urdu
// سادہ پیغام
لکھو("السلام علیکم، دنیا!");
```

```urdu
// کئی قدریں ایک ساتھ
متغیر نام = "احمد";
متغیر عمر = 25;
لکھو("نام:", نام, "— عمر:", عمر);
// نام: احمد — عمر: 25
```

```urdu
// sep اور end بدلنا
لکھو("ایک", "دو", "تین", sep=" | ", end=" ۔\n");
// ایک | دو | تین ۔
```

---

### `پڑھو(prompt="")`

Read a line of text from the user (standard input). The optional `prompt` string is displayed before waiting — it is also BiDi-safe so Urdu prompts display correctly.

> **اردو:** صارف سے (معیاری ان پٹ سے) متن کی ایک سطر پڑھیں۔ اختیاری `prompt` سٹرنگ انتظار سے پہلے دکھائی جاتی ہے۔

**Parameters**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `prompt`  | `""`    | Text shown to the user before input. |

**Returns:** `متن` — the user's input as a string (newline stripped)

**Examples**

```urdu
متغیر نام = پڑھو("اپنا نام لکھیں: ");
لکھو("خوش آمدید، " + نام + "!");
```

```urdu
متغیر عمر_متن = پڑھو("آپ کی عمر کیا ہے؟ ");
متغیر عمر = عدد(عمر_متن);
لکھو("آپ " + متن(عمر + 1) + " سال میں ہوں گے۔");
```

---

## Type Conversion — قسم تبدیلی

### `عدد(x) → int`

Convert a value to an integer. Equivalent to Python's `int(x)`.

Returns `نان` (NaN) if conversion fails rather than raising an exception.

> **اردو:** قدر کو صحیح عدد میں تبدیل کریں۔ تبدیلی ناکام ہونے پر استثناء اٹھانے کی بجائے `نان` واپس کرتا ہے۔

**Examples**

```urdu
لکھو(عدد("42"));      // 42
لکھو(عدد(3.9));       // 3  (truncates, does not round)
لکھو(عدد("abc"));     // nan
```

---

### `اعشاریہ(x) → float`

Convert a value to a floating-point number. Equivalent to Python's `float(x)`.

Returns `نان` on failure.

> **اردو:** قدر کو اعشاری عدد میں تبدیل کریں۔ ناکامی پر `نان` واپس کرتا ہے۔

**Examples**

```urdu
لکھو(اعشاریہ("3.14"));    // 3.14
لکھو(اعشاریہ(5));         // 5.0
لکھو(اعشاریہ("abc"));     // nan
```

---

### `متن(x) → str`

Convert any value to its string representation. Equivalent to Python's `str(x)`.

> **اردو:** کسی بھی قدر کو اس کی سٹرنگ نمائندگی میں تبدیل کریں۔

**Examples**

```urdu
لکھو(متن(100));           // "100"
لکھو(متن(3.14));          // "3.14"
لکھو(متن(سچ));            // "True"
```

---

### `بولین(x) → bool`

Convert a value to a boolean. Equivalent to Python's `bool(x)`.

Falsy values: `0`, `""`, `[]`, `{}`, `خالی`, `جھوٹ`.  
Everything else is truthy.

> **اردو:** قدر کو بولین میں تبدیل کریں۔ جھوٹ قدریں: `0`، `""`، `[]`، `{}`، `خالی`، `جھوٹ`۔ باقی سب سچ ہیں۔

**Examples**

```urdu
لکھو(بولین(0));        // False
لکھو(بولین("اردو"));   // True
لکھو(بولین([]));       // False
```

---

## Collections — مجموعے

### `فہرست(*args) → list`

Create a list.

- `فہرست()` — empty list
- `فہرست(iterable)` — list from an iterable
- `فہرست(a, b, c, ...)` — list from multiple arguments

> **اردو:** فہرست بنائیں۔ خالی فہرست، کسی تکرار پذیر سے، یا کئی دلائل سے بنائی جا سکتی ہے۔

**Examples**

```urdu
متغیر خالی_فہرست = فہرست();
لکھو(خالی_فہرست);            // []

متغیر حروف = فہرست("اردو");
لکھو(حروف);                  // ['ا', 'ر', 'د', 'و']

متغیر اعداد = فہرست(1, 2, 3, 4, 5);
لکھو(اعداد);                  // [1, 2, 3, 4, 5]
```

---

### `ٹپل(*args) → tuple`

Create a tuple (immutable sequence).

- `ٹپل()` — empty tuple
- `ٹپل(iterable)` — tuple from an iterable
- `ٹپل(a, b, c, ...)` — tuple from arguments

> **اردو:** ٹپل بنائیں (ناقابل تبدیل ترتیب)۔ فہرست کے برعکس ٹپل کو بعد میں تبدیل نہیں کیا جا سکتا۔

**Examples**

```urdu
متغیر نقطہ = ٹپل(10, 20);
لکھو(نقطہ);            // (10, 20)

متغیر ت = ٹپل([1, 2, 3]);
لکھو(ت);               // (1, 2, 3)
```

---

### `لغت(*args, **kwargs) → dict`

Create a dictionary (object). Returns an `_UrduObj` that supports both `obj["key"]` and `obj.key` access.

> **اردو:** لغت (شے) بنائیں۔ ایک `_UrduObj` واپس کرتا ہے جو `obj["key"]` اور `obj.key` دونوں طریقوں سے رسائی کی حمایت کرتا ہے۔

**Examples**

```urdu
متغیر طالب = لغت();
طالب["نام"] = "فاطمہ";
طالب["درجہ"] = "دسواں";
لکھو(طالب["نام"]);      // فاطمہ
```

```urdu
// براہ راست لٹریل نحو بھی کام کرتی ہے
متغیر شخص = { نام: "علی", عمر: 30 };
لکھو(شخص.نام);          // علی
```

---

### `مجموعہ(*args) → set`

Create a set (unique unordered values).

- `مجموعہ()` — empty set
- `مجموعہ(iterable)` — set from iterable
- `مجموعہ(a, b, c, ...)` — set from arguments

> **اردو:** مجموعہ بنائیں (منفرد غیر ترتیب شدہ قدریں)۔ مجموعے میں ہر قدر صرف ایک بار ہو سکتی ہے۔

**Examples**

```urdu
متغیر منفرد = مجموعہ([1, 2, 2, 3, 3, 3]);
لکھو(منفرد);     // {1, 2, 3}

متغیر پھل = مجموعہ("سیب", "کیلا", "سیب");
لکھو(لمبائی(پھل));   // 2
```

---

## Sequence and Iteration — ترتیب اور تکرار

### `لمبائی(x) → int`

Return the number of items in a string, list, tuple, dictionary, or set. Equivalent to Python's `len(x)`.

> **اردو:** سٹرنگ، فہرست، ٹپل، لغت، یا مجموعے میں اشیاء کی تعداد واپس کریں۔

**Examples**

```urdu
لکھو(لمبائی("اردو"));          // 4
لکھو(لمبائی([10, 20, 30]));    // 3
لکھو(لمبائی({ ا: 1, ب: 2 })); // 2
```

---

### `حد(stop)` / `حد(start, stop)` / `حد(start, stop, step) → range`

Generate a sequence of integers. Equivalent to Python's `range()`.

> **اردو:** اعداد صحیح کی ترتیب بنائیں۔ حلقوں میں بہت استعمال ہوتی ہے۔

| Form | Behavior |
|------|----------|
| `حد(n)` | `0, 1, 2, ..., n-1` |
| `حد(start, stop)` | `start, start+1, ..., stop-1` |
| `حد(start, stop, step)` | with custom step |

**Examples**

```urdu
// 0 سے 4 تک
کے_لیے (متغیر i کا حد(5)) {
    لکھو(i);
}
```

```urdu
// 1 سے 10 تک فرد اعداد
کے_لیے (متغیر n کا حد(1, 11, 2)) {
    لکھو(n);   // 1 3 5 7 9
}
```

```urdu
// الٹی گنتی
کے_لیے (متغیر i کا حد(5, 0, -1)) {
    لکھو(i);   // 5 4 3 2 1
}
```

---

### `گنو(iterable, start=0) → enumerate`

Iterate over an iterable and yield `(index, value)` pairs. Equivalent to Python's `enumerate()`.

> **اردو:** کسی تکرار پذیر پر تکرار کریں اور `(انڈیکس، قدر)` جوڑے پیدا کریں۔ جب آپ کو قدر کے ساتھ اس کا نمبر بھی چاہیے تو مفید ہے۔

**Examples**

```urdu
متغیر پھل = ["سیب", "کیلا", "آم"];
کے_لیے (متغیر [i, ف] میں گنو(پھل)) {
    لکھو(i, ":", ف);
}
// 0 : سیب
// 1 : کیلا
// 2 : آم
```

```urdu
// شروع 1 سے کریں
کے_لیے (متغیر [ن, ق] میں گنو(["الف", "ب", "ج"], 1)) {
    لکھو(ن, ".", ق);
}
// 1. الف   2. ب   3. ج
```

---

### `زپ(*iterables) → zip`

Combine multiple iterables element-by-element. Stops at the shortest iterable. Equivalent to Python's `zip()`.

> **اردو:** کئی تکرار پذیروں کو عنصر بہ عنصر یکجا کریں۔ سب سے چھوٹی پر رک جاتا ہے۔

**Examples**

```urdu
متغیر نام = ["احمد", "فاطمہ", "علی"];
متغیر عمر = [20, 22, 19];
کے_لیے (متغیر [ن, ع] میں زپ(نام, عمر)) {
    لکھو(ن, "—", ع, "سال");
}
```

```urdu
// تین فہرستیں جوڑنا
متغیر الف = [1, 2, 3];
متغیر ب   = [4, 5, 6];
متغیر ج   = [7, 8, 9];
لکھو(فہرست(زپ(الف, ب, ج)));
// [(1,4,7), (2,5,8), (3,6,9)]
```

---

### `نقشہ(func, *iterables) → list`

Apply a function to every element of one or more iterables, returning a list of results. Equivalent to Python's `list(map(...))`.

> **اردو:** ایک یا زیادہ تکرار پذیروں کے ہر عنصر پر فنکشن لاگو کریں اور نتائج کی فہرست واپس کریں۔

**Examples**

```urdu
متغیر اعداد = [1, 2, 3, 4, 5];
متغیر مربع = نقشہ(x => x * x, اعداد);
لکھو(مربع);    // [1, 4, 9, 16, 25]
```

```urdu
متغیر متون = ["  احمد  ", "  فاطمہ  "];
متغیر صاف = نقشہ(s => s.trim(), متون);
لکھو(صاف);    // ['احمد', 'فاطمہ']
```

---

### `فلٹر(func, iterable) → list`

Return only those elements of `iterable` for which `func(element)` is truthy. Equivalent to Python's `list(filter(...))`.

Pass `خالی` as the function to filter out all falsy values.

> **اردو:** `iterable` کے صرف وہ عناصر واپس کریں جن کے لیے `func(element)` سچ ہو۔ تمام جھوٹ قدریں ہٹانے کے لیے فنکشن کی جگہ `خالی` دیں۔

**Examples**

```urdu
متغیر اعداد = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
متغیر جفت = فلٹر(x => x % 2 == 0, اعداد);
لکھو(جفت);    // [2, 4, 6, 8, 10]
```

```urdu
// خالی نہ ہوں
متغیر الفاظ = ["اردو", "", "پاکستان", "", "زبان"];
متغیر بھرے = فلٹر(خالی, الفاظ);
لکھو(بھرے);   // ['اردو', 'پاکستان', 'زبان']
```

---

### `ترتیب(iterable, *, کلید=None, الٹا=False) → list`

Return a new sorted list from an iterable. Does not modify the original. Equivalent to Python's `sorted()`.

> **اردو:** کسی تکرار پذیر سے ترتیب شدہ نئی فہرست واپس کریں۔ اصل کو تبدیل نہیں کرتا۔

**Parameters**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `iterable` | —      | Any iterable to sort. |
| `کلید`     | `None`  | A function applied to each element before comparing (key function). |
| `الٹا`     | `False` | If `True`, sort in descending order. |

**Examples**

```urdu
لکھو(ترتیب([3, 1, 4, 1, 5, 9, 2, 6]));
// [1, 1, 2, 3, 4, 5, 6, 9]

لکھو(ترتیب([3, 1, 4, 1, 5], الٹا=سچ));
// [5, 4, 3, 1, 1]
```

```urdu
// لمبائی کے مطابق ترتیب
متغیر الفاظ = ["کیلا", "آم", "انگور", "سیب"];
لکھو(ترتیب(الفاظ, کلید=x => لمبائی(x)));
// ['آم', 'سیب', 'کیلا', 'انگور']
```

---

### `ریورس(iterable) → list`

Return a new list with elements in reverse order. Equivalent to Python's `list(reversed(...))`.

> **اردو:** الٹی ترتیب میں عناصر کے ساتھ نئی فہرست واپس کریں۔

**Examples**

```urdu
لکھو(ریورس([1, 2, 3, 4, 5]));   // [5, 4, 3, 2, 1]
لکھو(ریورس("اردو"));            // ['و', 'د', 'ر', 'ا']
```

---

## Aggregation — جمع بندی

### `مجموع(iterable, start=0) → number`

Return the sum of all elements, starting from `start`. Equivalent to Python's `sum()`.

> **اردو:** تمام عناصر کا مجموع واپس کریں، `start` سے شروع کر کے۔

**Examples**

```urdu
لکھو(مجموع([1, 2, 3, 4, 5]));          // 15
لکھو(مجموع([10, 20, 30], 100));         // 160
لکھو(مجموع(حد(1, 101)));               // 5050
```

---

### `کم(iterable or *args, کلید=None) → value`

Return the minimum value. Accepts either an iterable or multiple arguments. Equivalent to Python's `min()`.

> **اردو:** کم از کم قدر واپس کریں۔ تکرار پذیر یا کئی دلائل قبول کرتا ہے۔

**Examples**

```urdu
لکھو(کم([5, 3, 8, 1, 9]));        // 1
لکھو(کم(10, 20, 5, 15));          // 5

// لمبائی کم
متغیر الفاظ = ["کیلا", "آم", "انگور"];
لکھو(کم(الفاظ, کلید=لمبائی));    // آم
```

---

### `زیادہ(iterable or *args, کلید=None) → value`

Return the maximum value. Equivalent to Python's `max()`.

> **اردو:** زیادہ سے زیادہ قدر واپس کریں۔

**Examples**

```urdu
لکھو(زیادہ([5, 3, 8, 1, 9]));    // 9
لکھو(زیادہ(10, 20, 5, 15));      // 20

// سب سے لمبا لفظ
متغیر الفاظ = ["کیلا", "آم", "انگور"];
لکھو(زیادہ(الفاظ, کلید=لمبائی)); // انگور
```

---

## Math — ریاضی

### `مطلق(x) → number`

Return the absolute (non-negative) value of a number. Equivalent to Python's `abs(x)`.

> **اردو:** عدد کی مطلق (غیر منفی) قدر واپس کریں۔

**Examples**

```urdu
لکھو(مطلق(-7));     // 7
لکھو(مطلق(3.14));   // 3.14
لکھو(مطلق(0));      // 0
```

---

### `گول(x, n=0) → number`

Round `x` to `n` decimal places. If `n` is omitted, rounds to the nearest integer. Equivalent to Python's `round()`.

> **اردو:** `x` کو `n` اعشاری مقامات تک گول کریں۔ `n` چھوڑنے پر قریب ترین صحیح عدد پر گول کرتا ہے۔

**Examples**

```urdu
لکھو(گول(3.7));         // 4
لکھو(گول(3.14159, 2));  // 3.14
لکھو(گول(2.5));         // 2  (Python banker's rounding)
```

---

### `طاقت(x, y) → number`

Raise `x` to the power of `y`. Equivalent to Python's `pow(x, y)`.

> **اردو:** `x` کو `y` کی قوت تک بڑھائیں۔

**Examples**

```urdu
لکھو(طاقت(2, 10));   // 1024
لکھو(طاقت(9, 0.5));  // 3.0
لکھو(طاقت(3, 3));    // 27
```

---

## String Utilities — سٹرنگ مددگار

### `ربط(separator, iterable) → str`

Join elements of an iterable into a single string, with `separator` between each element. Non-string elements are converted to strings automatically. Equivalent to Python's `str.join()`.

> **اردو:** کسی تکرار پذیر کے عناصر کو ایک سٹرنگ میں جوڑیں، ہر عنصر کے درمیان `separator` رکھیں۔ غیر سٹرنگ عناصر خود بخود تبدیل ہو جاتے ہیں۔

**Examples**

```urdu
لکھو(ربط(", ", ["احمد", "فاطمہ", "علی"]));
// احمد, فاطمہ, علی

لکھو(ربط(" — ", [1, 2, 3]));
// 1 — 2 — 3

لکھو(ربط("", ["ا", "ر", "د", "و"]));
// اردو
```

---

### `تقسیم(string, sep=None) → list`

Split a string into a list of substrings. If `sep` is `None` (or omitted), splits on any whitespace and removes empty strings. Equivalent to Python's `str.split()`.

> **اردو:** سٹرنگ کو ذیلی سٹرنگز کی فہرست میں تقسیم کریں۔ `sep` نہ دینے پر کسی بھی خالی جگہ پر تقسیم کرتا ہے۔

**Examples**

```urdu
لکھو(تقسیم("احمد فاطمہ علی"));
// ['احمد', 'فاطمہ', 'علی']

لکھو(تقسیم("ایک,دو,تین", ","));
// ['ایک', 'دو', 'تین']
```

---

### `شامل(string, sub) → bool`

Return `True` if `sub` is found inside `string`. Equivalent to Python's `in` operator for strings.

> **اردو:** اگر `sub` `string` کے اندر ملے تو `True` واپس کریں۔

**Examples**

```urdu
لکھو(شامل("اردو پروگرامنگ", "پروگرامنگ"));   // True
لکھو(شامل("اردو پروگرامنگ", "جاوا"));         // False
لکھو(شامل([1, 2, 3, 4], 3));                   // True
```

---

## JSON

### `JSON_پڑھو(s) → object`

Parse a JSON string and return the corresponding Urdu/Python object (dict, list, number, string, bool, or `None`). Equivalent to JavaScript's `JSON.parse()` or Python's `json.loads()`.

Raises an exception if the string is not valid JSON.

> **اردو:** JSON سٹرنگ کو پارس کریں اور متعلقہ اردو/Python شے واپس کریں۔ اگر سٹرنگ درست JSON نہ ہو تو استثناء اٹھاتا ہے۔

**Examples**

```urdu
متغیر ڈیٹا = JSON_پڑھو('{"نام": "احمد", "عمر": 25}');
لکھو(ڈیٹا["نام"]);    // احمد
```

```urdu
متغیر فہرست = JSON_پڑھو('[1, 2, 3, 4, 5]');
لکھو(مجموع(فہرست));   // 15
```

---

### `JSON_لکھو(obj, indent=None) → str`

Serialize an object to a JSON string. Non-ASCII characters (including Urdu) are preserved as-is (not escaped to `\uXXXX`). Equivalent to JavaScript's `JSON.stringify()` or Python's `json.dumps()`.

Pass `indent` (e.g., `4`) for pretty-printed output.

> **اردو:** شے کو JSON سٹرنگ میں سیریلائز کریں۔ اردو سمیت غیر ASCII حروف جوں کے توں محفوظ رہتے ہیں۔ خوبصورت آؤٹ پٹ کے لیے `indent` دیں۔

**Examples**

```urdu
متغیر شخص = { نام: "فاطمہ", عمر: 22 };
لکھو(JSON_لکھو(شخص));
// {"نام": "فاطمہ", "عمر": 22}

لکھو(JSON_لکھو(شخص, 4));
// {
//     "نام": "فاطمہ",
//     "عمر": 22
// }
```

---

## Time — وقت

### `وقت() → float`

Return the current time as milliseconds since the Unix epoch (1 January 1970 UTC). Equivalent to JavaScript's `Date.now()`.

> **اردو:** Unix epoch (یکم جنوری 1970 UTC) سے اب تک کا وقت ملی سیکنڈ میں واپس کریں۔ وقت ناپنے کے لیے مفید ہے۔

**Examples**

```urdu
متغیر شروع = وقت();
// ... کچھ کام ...
متغیر گزرا = وقت() - شروع;
لکھو("وقت لگا:", گول(گزرا, 2), "ms");
```

---

### `تاریخ() → datetime`

Return the current date and time as a Python `datetime.datetime` object.

> **اردو:** موجودہ تاریخ اور وقت Python `datetime.datetime` شے کے طور پر واپس کریں۔

**Examples**

```urdu
متغیر ابھی = تاریخ();
لکھو(ابھی);
// 2026-05-19 14:30:00.123456
```

---

### `تاخیر(ms) → awaitable`

Return an awaitable that resolves after `ms` milliseconds. Must be used with `انتظار` inside a `غیر_متزامن` function. Equivalent to JavaScript's `setTimeout` (Promise-style) or Python's `asyncio.sleep(ms/1000)`.

> **اردو:** ایک awaitable واپس کریں جو `ms` ملی سیکنڈ بعد حل ہو۔ `غیر_متزامن` فنکشن کے اندر `انتظار` کے ساتھ استعمال کرنا ضروری ہے۔

**Examples**

```urdu
غیر_متزامن فنکشن مثال() {
    لکھو("شروع...");
    انتظار تاخیر(1000);   // 1 سیکنڈ انتظار
    لکھو("ایک سیکنڈ بعد!");
}
انتظار مثال();
```

---

## Random — اتفاقی

### `اتفاقی(a=0, b=1) → float`

Return a random floating-point number between `a` and `b` (inclusive). Equivalent to Python's `random.uniform(a, b)`.

> **اردو:** `a` اور `b` کے درمیان (شامل) اتفاقی اعشاری عدد واپس کریں۔

**Examples**

```urdu
لکھو(اتفاقی());         // e.g. 0.7234...
لکھو(اتفاقی(0, 100));   // e.g. 57.8...
لکھو(اتفاقی(-1, 1));    // e.g. -0.3...
```

---

### `اتفاقی_عدد(a, b) → int`

Return a random integer between `a` and `b` inclusive. Equivalent to Python's `random.randint(a, b)`.

> **اردو:** `a` اور `b` کے درمیان (شامل) اتفاقی صحیح عدد واپس کریں۔

**Examples**

```urdu
لکھو(اتفاقی_عدد(1, 6));       // پانسہ: 1 تا 6
لکھو(اتفاقی_عدد(0, 100));     // 0 تا 100
لکھو(اتفاقی_عدد(-10, 10));    // -10 تا 10
```

---

## Type Checking — قسم جانچ

### `قسم(x) → str`

Return the Urdu type name of a value as a string.

> **اردو:** کسی قدر کا اردو قسم نام بطور سٹرنگ واپس کریں۔

| Value type | Returns |
|------------|---------|
| Integer, float | `"عدد"` |
| String | `"متن"` |
| List, tuple | `"فہرست"` |
| Dictionary / object | `"شے"` |
| Callable (function) | `"فنکشن"` |
| Boolean | `"بولین"` |
| `None` / `خالی` | `"خالی"` |

> Note: The raw Python type name is returned when no Urdu mapping exists (e.g., `"set"`, `"datetime"`). Use the internal helper `_urdu_typeof` for the strict Urdu typeset.

> **اردو:** نوٹ: جب کوئی اردو میپنگ موجود نہ ہو تو Python کا خام قسم نام واپس کیا جاتا ہے۔

**Examples**

```urdu
لکھو(قسم(42));           // "عدد"
لکھو(قسم("اردو"));       // "متن"
لکھو(قسم([1,2,3]));      // "فہرست"
لکھو(قسم(سچ));           // "بولین"
لکھو(قسم(خالی));         // "خالی"
لکھو(قسم(غیر_معرف));     // "خالی"
لکھو(قسم({}));            // "شے"
لکھو(قسم(فنکشن() {}));   // "فنکشن"
```

---

### `نمونہ(cls, obj) → bool`

Check whether `obj` is an instance of `cls`. Equivalent to Python's `isinstance(obj, cls)`.

> **اردو:** جانچیں کہ آیا `obj` `cls` کا نمونہ ہے۔

**Examples**

```urdu
لکھو(نمونہ(str, "اردو"));      // True
لکھو(نمونہ(int, 3.14));        // False
لکھو(نمونہ(list, [1, 2, 3])); // True
```

---

## Advanced Execution — جدید عملدرآمد

### `متحرک_چلاؤ(code, env=None) → dict`

Execute a string of Urdu or Python code dynamically at runtime, returning the resulting scope (variable namespace) as a dictionary.

- If `code` contains Urdu characters, it is first transpiled to Python, then executed.
- If `code` is pure Python (no Urdu), it is executed directly.
- `env` (optional) — a dictionary used as the execution scope. Pass an existing dict to share variables. Urdu built-ins are always available inside the executed code.

**Returns:** The scope dictionary after execution (contains all variables defined in the executed code).

> **اردو:** رن ٹائم میں اردو یا Python کوڈ کی سٹرنگ متحرک طور پر چلائیں اور نتیجے کی گنجائش (متغیر نام فضا) لغت کے طور پر واپس کریں۔ اگر کوڈ میں اردو حروف ہوں تو پہلے Python میں تبدیل ہو کر چلتا ہے۔

**Examples**

```urdu
متغیر دائرہ = متحرک_چلاؤ('
    متغیر رداس = 5
    متغیر رقبہ = ریاضی.پائی * رداس * رداس
');
لکھو(دائرہ["رقبہ"]);   // 78.539...
```

```urdu
// مشترک ماحول
متغیر ماحول = { "x": 10 };
متحرک_چلاؤ("x = x * 2", ماحول);
لکھو(ماحول["x"]);    // 20
```

---

## Parsing Utilities — پارسنگ مددگار

### `صحیح_پارس(s, base=10) → int`

Parse a string as an integer. Equivalent to JavaScript's `parseInt()` or Python's `int(str, base)`.

Returns `نان` if the string cannot be parsed.

> **اردو:** سٹرنگ کو صحیح عدد کے طور پر پارس کریں۔ نہ پارس ہونے پر `نان` واپس کرتا ہے۔

**Examples**

```urdu
لکھو(صحیح_پارس("42"));       // 42
لکھو(صحیح_پارس("ff", 16));   // 255  (hex)
لکھو(صحیح_پارس("1010", 2));  // 10   (binary)
لکھو(صحیح_پارس("abc"));      // nan
```

---

### `اعشاریہ_پارس(s) → float`

Parse a string as a floating-point number. Equivalent to JavaScript's `parseFloat()`.

Returns `نان` on failure.

> **اردو:** سٹرنگ کو اعشاری عدد کے طور پر پارس کریں۔ ناکامی پر `نان` واپس کرتا ہے۔

**Examples**

```urdu
لکھو(اعشاریہ_پارس("3.14"));    // 3.14
لکھو(اعشاریہ_پارس("1e5"));     // 100000.0
لکھو(اعشاریہ_پارس("xyz"));     // nan
```

---

### `نان_ہے(x) → bool`

Return `True` if `x` is Not a Number (NaN). Equivalent to JavaScript's `isNaN()`.

> **اردو:** اگر `x` نان (نہ عدد) ہو تو `True` واپس کریں۔

**Examples**

```urdu
لکھو(نان_ہے(نان));             // True
لکھو(نان_ہے(عدد("abc")));      // True
لکھو(نان_ہے(42));              // False
```

---

### `محدود_ہے(x) → bool`

Return `True` if `x` is a finite number (not NaN, not Infinity). Equivalent to JavaScript's `isFinite()`.

> **اردو:** اگر `x` محدود عدد ہو (نہ نان، نہ لامحدود) تو `True` واپس کریں۔

**Examples**

```urdu
لکھو(محدود_ہے(42));           // True
لکھو(محدود_ہے(لامحدود));      // False
لکھو(محدود_ہے(نان));          // False
```

---

## Global Constants — عالمی مستقلات

These constants are pre-defined in every Urdu program's global scope.

> **اردو:** یہ مستقلات ہر اردو پروگرام کی عالمی گنجائش میں پہلے سے متعین ہیں۔

| Urdu Name | English Alias | Value | Description |
|-----------|---------------|-------|-------------|
| `نان` | `NaN` | `float("nan")` | Not a Number — result of invalid numeric operations |
| `لامحدود` | `Infinity` | `float("inf")` | Positive infinity |
| `غیر_معرف` | `undefined` | `None` | Undefined / absent value |
| `سچ` | `True` | `True` | Boolean true |
| `جھوٹ` | `False` | `False` | Boolean false |
| `خالی` | `None` / `null` | `None` | Null / empty value |

**Examples**

```urdu
متغیر نتیجہ = 1 / 0;
لکھو(نتیجہ == لامحدود);    // True

متغیر قدر = عدد("abc");
لکھو(نان_ہے(قدر));         // True

متغیر کچھ_نہیں = خالی;
لکھو(کچھ_نہیں == غیر_معرف); // True  (both are None)
```

---

*اردو پروگرامنگ لینگویج — Built-in Functions Reference — Mohammed Zahid Wadiwale*
