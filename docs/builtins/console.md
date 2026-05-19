# Console Object — کنسول

The `کنسول` object (also accessible as `console`) provides methods for printing structured output to the terminal. It is available globally in every Urdu program — no import required.

All output methods support Urdu (Arabic-script) text and apply Unicode BiDi markers automatically, so mixed Urdu-English text renders in the correct direction in modern terminals.

> **اردو:** `کنسول` شے (جسے `console` کے نام سے بھی استعمال کیا جا سکتا ہے) ٹرمینل پر منظم آؤٹ پٹ پرنٹ کرنے کے طریقے فراہم کرتی ہے۔ یہ ہر اردو پروگرام میں عالمی طور پر دستیاب ہے — کسی درآمد کی ضرورت نہیں۔ تمام آؤٹ پٹ طریقے اردو متن کی حمایت کرتے ہیں اور یونیکوڈ BiDi نشانات خود بخود لگاتے ہیں۔

---

## Quick Overview — فوری جائزہ

> **اردو:** کنسول کے تمام طریقوں کا فوری جائزہ:

```urdu
کنسول.لکھو("السلام علیکم!");         // عام پیغام
کنسول.غلطی("کچھ غلط ہوا");          // خطا پیغام
کنسول.انتباہ("خبردار رہیں");         // انتباہ
کنسول.معلومات("ورژن 1.0.0");         // معلومات
کنسول.ڈیبگ("قدر ہے:", 42);          // ڈیبگ
```

---

## Method Reference — طریقوں کا حوالہ

### `کنسول.لکھو(*args)` / `console.log(*args)`

Print one or more values to standard output (stdout). This is the general-purpose logging method. Multiple arguments are space-separated.

**Behavior:** Outputs to `stdout`. No prefix character.

> **اردو:** ایک یا زیادہ قدریں معیاری آؤٹ پٹ (stdout) پر پرنٹ کریں۔ یہ عام مقصد کا لاگنگ طریقہ ہے۔ کئی دلائل کے درمیان خالی جگہ ہوتی ہے۔

**Examples**

```urdu
کنسول.لکھو("السلام علیکم!");
// السلام علیکم!

متغیر نام = "احمد";
متغیر عمر = 25;
کنسول.لکھو("نام:", نام, "— عمر:", عمر);
// نام: احمد — عمر: 25

کنسول.لکھو("اعداد:", [1, 2, 3]);
// اعداد: [1, 2, 3]
```

---

### `کنسول.غلطی(*args)` / `console.error(*args)`

Print an error message to standard error (stderr). Prefixed with `✗` to visually distinguish errors. Use this for fatal errors, exceptions, or anything that indicates a failure.

**Behavior:** Outputs to `stderr`. Prefixed with `✗`.

> **اردو:** معیاری خطا (stderr) پر خطا پیغام پرنٹ کریں۔ `✗` سے شروع ہوتا ہے تاکہ غلطیاں بصری طور پر ممتاز ہوں۔ مہلک غلطیوں، استثناءات، یا ناکامی کی نشاندہی کرنے والی کسی بھی چیز کے لیے استعمال کریں۔

**Examples**

```urdu
کنسول.غلطی("ڈیٹا بیس سے رابطہ ناکام ہوا");
// ✗ ڈیٹا بیس سے رابطہ ناکام ہوا

کوشش {
    پھینکو نیا غلطی("فائل نہیں ملی");
} پکڑو (غ) {
    کنسول.غلطی("خطا:", غ.پیغام);
    // ✗ خطا: فائل نہیں ملی
}
```

---

### `کنسول.انتباہ(*args)` / `console.warn(*args)`

Print a warning message to standard error. Prefixed with `⚠`. Use this for non-fatal issues, deprecated features, or unusual (but recoverable) conditions.

**Behavior:** Outputs to `stderr`. Prefixed with `⚠`.

> **اردو:** معیاری خطا پر انتباہ پیغام پرنٹ کریں۔ `⚠` سے شروع ہوتا ہے۔ غیر مہلک مسائل، پرانی خصوصیات، یا غیر معمولی (لیکن قابل بحالی) حالات کے لیے استعمال کریں۔

**Examples**

```urdu
کنسول.انتباہ("یہ فنکشن پرانا ہو گیا ہے");
// ⚠ یہ فنکشن پرانا ہو گیا ہے

اگر (درجہ_حرارت > 90) {
    کنسول.انتباہ("درجہ حرارت بہت زیادہ ہے:", درجہ_حرارت);
}
```

---

### `کنسول.معلومات(*args)` / `console.info(*args)`

Print an informational message to standard output. Prefixed with `ℹ`. Use this for progress updates, startup messages, or status reports.

**Behavior:** Outputs to `stdout`. Prefixed with `ℹ`.

> **اردو:** معیاری آؤٹ پٹ پر معلوماتی پیغام پرنٹ کریں۔ `ℹ` سے شروع ہوتا ہے۔ پیشرفت کی اپڈیٹس، شروعاتی پیغامات، یا حیثیت رپورٹس کے لیے استعمال کریں۔

**Examples**

```urdu
کنسول.معلومات("پروگرام شروع ہو رہا ہے...");
// ℹ پروگرام شروع ہو رہا ہے...

کنسول.معلومات("ورژن: 1.0.0 | پلیٹ فارم: Windows");
// ℹ ورژن: 1.0.0 | پلیٹ فارم: Windows
```

---

### `کنسول.ڈیبگ(*args)` / `console.debug(*args)`

Print a debug message to standard output. Prefixed with `🔍`. Use this during development to trace variable values, control flow, or internal state.

**Behavior:** Outputs to `stdout`. Prefixed with `🔍`.

> **اردو:** معیاری آؤٹ پٹ پر ڈیبگ پیغام پرنٹ کریں۔ `🔍` سے شروع ہوتا ہے۔ ترقی کے دوران متغیر قدروں، کنٹرول بہاؤ، یا داخلی حالت کا سراغ لگانے کے لیے استعمال کریں۔

**Examples**

```urdu
متغیر x = 42;
کنسول.ڈیبگ("x کی قدر:", x);
// 🔍 x کی قدر: 42

فنکشن جمع(ا, ب) {
    کنسول.ڈیبگ("جمع کہا گیا:", ا, "+", ب);
    واپس ا + ب;
}
```

---

### `کنسول.جدول(data)` / `console.table(data)`

Display structured data (a list or dictionary) in a table-like format. Each row is printed on its own line with the index or key shown as a prefix.

**Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `data` | list, tuple, dict | The data to display. |

- **List/tuple:** Prints `[index]  value` for each element.
- **Dictionary:** Prints `  key: value` for each entry.

> **اردو:** منظم ڈیٹا (فہرست یا لغت) کو جدول نما فارمیٹ میں دکھائیں۔ ہر قطار اپنی لائن پر پرنٹ ہوتی ہے، انڈیکس یا کلید سابقے کے طور پر۔

**Examples**

```urdu
// فہرست سے جدول
متغیر طلباء = ["احمد", "فاطمہ", "علی", "زینب"];
کنسول.جدول(طلباء);
// [0] احمد
// [1] فاطمہ
// [2] علی
// [3] زینب
```

```urdu
// لغت سے جدول
متغیر نمبرات = { احمد: 90, فاطمہ: 95, علی: 85 };
کنسول.جدول(نمبرات);
//   احمد: 90
//   فاطمہ: 95
//   علی: 85
```

```urdu
// اشیاء کی فہرست
متغیر ریکارڈ = [
    { نام: "احمد", عمر: 20 },
    { نام: "فاطمہ", عمر: 22 }
];
کے_لیے (متغیر [i, ر] کا گنو(ریکارڈ)) {
    کنسول.لکھو(`[${i}]`, JSON_لکھو(ر));
}
```

---

### `کنسول.صاف()` / `console.clear()`

Clear the terminal screen. Sends the ANSI escape sequence `\033[2J\033[H` which moves the cursor to the top-left and clears the visible buffer. Has no effect in environments that do not support ANSI codes.

> **اردو:** ٹرمینل اسکرین صاف کریں۔ ANSI ایسکیپ ترتیب بھیجتا ہے جو کرسر کو اوپر بائیں منتقل کرتی ہے اور نظر آنے والا بفر صاف کرتی ہے۔ ANSI کوڈز کی حمایت نہ کرنے والے ماحول میں کوئی اثر نہیں۔

**Examples**

```urdu
کنسول.صاف();
لکھو("صاف اسکرین پر خوش آمدید!");
```

---

### `کنسول.گروپ(label)` / `console.group(label)`

Print a group header with a `▼` prefix. Use to visually organize related log messages. Combine with `کنسول.گروپ_ختم()` to mark the end of the group.

> Note: In the current runtime, `گروپ` only prints the header — it does not visually indent subsequent lines. Use manual indentation in your `لکھو()` calls if you need visual nesting.

> **اردو:** `▼` سابقے کے ساتھ گروپ ہیڈر پرنٹ کریں۔ متعلقہ لاگ پیغامات کو بصری طور پر منظم کرنے کے لیے استعمال کریں۔ نوٹ: موجودہ رن ٹائم میں `گروپ` صرف ہیڈر پرنٹ کرتا ہے، بعد کی سطروں کو بصری طور پر دانت نہیں لگاتا۔

**Examples**

```urdu
کنسول.گروپ("طالب علم کی معلومات");
کنسول.لکھو("  نام: احمد");
کنسول.لکھو("  درجہ: دسواں");
کنسول.لکھو("  نمبر: 95");
کنسول.گروپ_ختم();
// ▼ طالب علم کی معلومات
//   نام: احمد
//   درجہ: دسواں
//   نمبر: 95
```

```urdu
// نتائج گروپ
کنسول.گروپ("جانچ کے نتائج");
کنسول.لکھو("  ✓ فنکشن الف");
کنسول.لکھو("  ✓ فنکشن ب");
کنسول.لکھو("  ✗ فنکشن ج");
کنسول.گروپ_ختم();
```

---

### `کنسول.گروپ_ختم()` / `console.groupEnd()`

Mark the end of a group started with `کنسول.گروپ()`. In the current runtime this is a no-op (placeholder for API compatibility).

> **اردو:** `کنسول.گروپ()` سے شروع ہونے والے گروپ کا اختتام نشان زد کریں۔ موجودہ رن ٹائم میں یہ کوئی عمل نہیں کرتا (API ہم آہنگی کے لیے موجود ہے)۔

---

### `کنسول.وقت_شروع(label)` / `console.time(label)`

Start a named timer. Records the current high-resolution time under the given `label`. Call `کنسول.وقت_ختم(label)` with the same label to stop the timer and print the elapsed time in milliseconds.

Multiple independent timers can be active simultaneously as long as they have different labels.

**Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `label` | str | A name identifying this timer. Defaults to `""`. |

> **اردو:** نامزد ٹائمر شروع کریں۔ دیے گئے `label` کے تحت موجودہ اعلی ریزولیوشن وقت ریکارڈ کرتا ہے۔ ٹائمر روکنے کے لیے ایک ہی لیبل کے ساتھ `کنسول.وقت_ختم(label)` کہیں۔ مختلف لیبلز کے ساتھ کئی ٹائمر بیک وقت فعال ہو سکتے ہیں۔

**Examples**

```urdu
کنسول.وقت_شروع("حساب");
متغیر جمع = مجموع(حد(1, 1000001));
کنسول.وقت_ختم("حساب");
// حساب: 0.83ms
```

---

### `کنسول.وقت_ختم(label)` / `console.timeEnd(label)`

Stop the timer identified by `label` and print the elapsed time in milliseconds with two decimal places. If `label` was never started, the elapsed time reported will be near zero.

**Output format:** `label: X.XXms`

> **اردو:** `label` سے پہچانا گیا ٹائمر روکیں اور گزرا ہوا وقت ملی سیکنڈ میں پرنٹ کریں۔ آؤٹ پٹ فارمیٹ: `label: X.XXms`

**Examples**

```urdu
کنسول.وقت_شروع("ترتیب");
متغیر ترتیب_شدہ = ترتیب(حد(1000, 0, -1));
کنسول.وقت_ختم("ترتیب");
// ترتیب: 1.45ms

// متعدد ٹائمر
کنسول.وقت_شروع("ٹائمر-الف");
کنسول.وقت_شروع("ٹائمر-ب");
// ... کام ...
کنسول.وقت_ختم("ٹائمر-الف");
کنسول.وقت_ختم("ٹائمر-ب");
```

---

## Complete Practical Example — مکمل عملی مثال

> **اردو:** کنسول شے کا مکمل استعمال دکھانے والی ایک جامع مثال:

```urdu
// ═══════════════════════════════════════════
// کنسول آبجیکٹ کا مکمل استعمال
// ═══════════════════════════════════════════

کنسول.گروپ("پروگرام شروع");
کنسول.معلومات("اردو پروگرامنگ لینگویج — ورژن 1.0.0");
کنسول.گروپ_ختم();

// وقت ماپنا
کنسول.وقت_شروع("کل وقت");

// ڈیٹا پروسیسنگ
کنسول.گروپ("ڈیٹا پروسیسنگ");
متغیر ڈیٹا = حد(1, 1001);
کنسول.ڈیبگ("اندراجات:", لمبائی(فہرست(ڈیٹا)));

کوشش {
    متغیر نتیجہ = مجموع(ڈیٹا);
    کنسول.لکھو("مجموع:", نتیجہ);
    کنسول.انتباہ("یہ صرف جانچ کا ڈیٹا ہے");
} پکڑو (غ) {
    کنسول.غلطی("حساب میں خرابی:", غ.پیغام);
}
کنسول.گروپ_ختم();

// جدول
کنسول.گروپ("نمبرات جدول");
کنسول.جدول({ احمد: 90, فاطمہ: 95, علی: 85, زینب: 92 });
کنسول.گروپ_ختم();

کنسول.وقت_ختم("کل وقت");
// کل وقت: 1.23ms
```

---

## Output Destination Summary — آؤٹ پٹ منزل کا خلاصہ

| Method | Prefix | Destination |
|--------|--------|-------------|
| `کنسول.لکھو()` | (none) | stdout |
| `کنسول.معلومات()` | `ℹ` | stdout |
| `کنسول.ڈیبگ()` | `🔍` | stdout |
| `کنسول.انتباہ()` | `⚠` | stderr |
| `کنسول.غلطی()` | `✗` | stderr |
| `کنسول.جدول()` | (none) | stdout |
| `کنسول.گروپ()` | `▼` | stdout |
| `کنسول.صاف()` | (ANSI) | stdout |

> **اردو:** ہر طریقے کی آؤٹ پٹ منزل اور سابقے کا خلاصہ۔ stdout عام آؤٹ پٹ ہے، stderr غلطی اور انتباہ آؤٹ پٹ ہے۔

---

*اردو پروگرامنگ لینگویج — Console Object Reference — Mohammed Zahid Wadiwale*
