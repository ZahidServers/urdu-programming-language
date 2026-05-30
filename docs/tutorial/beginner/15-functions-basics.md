# 15. Functions — فنکشن

**Difficulty:** Beginner — مبتدی  
**Time:** ~25 minutes

---

## What Is a Function? — فنکشن کیا ہے؟

A function is a named block of code that you can run whenever you need it. Instead of writing the same code multiple times, write it once as a function and **call** it by name.

> **اردو:** فنکشن ایک بار لکھو، بار بار استعمال کرو۔ پروگرام کو حصوں میں توڑ کر سمجھنا اور ٹھیک کرنا آسان ہو جاتا ہے۔

---

## Defining a Function — فنکشن بنانا

```urdu
فنکشن سلام(نام) {
    لکھو(`السلام علیکم، ${نام}!`);
}
```

**Pattern:**
```
فنکشن نام(پیرامیٹر1, پیرامیٹر2, ...) {
    // function body
}
```

**Calling the function — فنکشن چلانا:**

```urdu
سلام("احمد");     // السلام علیکم، احمد!
سلام("فاطمہ");    // السلام علیکم، فاطمہ!
سلام("علی");      // السلام علیکم، علی!
```

> **اردو:** `فنکشن` لکھیں، پھر نام، پھر گول قوسین میں پیرامیٹرز (ان پٹ کے نام)، پھر گھنگریالے قوسین میں کوڈ۔

---

## Return Values — واپسی قدر

Use `واپس` to return a result from a function:

```urdu
فنکشن جمع(الف, ب) {
    واپس الف + ب;
}

متغیر نتیجہ = جمع(3, 4);
لکھو(نتیجہ);    // 7
لکھو(جمع(10, 20));    // 30
```

`واپس` immediately exits the function and sends the value back to the caller.

> **اردو:** `واپس` فنکشن سے قدر لوٹاتا ہے۔ فنکشن وہاں رک جاتا ہے جہاں `واپس` لکھا ہو۔ اگر `واپس` نہ ہو تو فنکشن `خالی` لوٹاتا ہے۔

---

## Default Parameters — ڈیفالٹ پیرامیٹرز

Give a parameter a default value so it's optional when calling:

```urdu
فنکشن پیغام(متن, بار = 1) {
    کے_لیے (متغیر i میں حد(بار)) {
        لکھو(متن);
    }
}

پیغام("سلام");        // prints once (default بار=1)
پیغام("سلام", 3);     // prints three times
```

Output:
```
سلام
سلام
سلام
سلام
```

> **اردو:** `پیرامیٹر = قدر` سے ڈیفالٹ قدر دیں۔ کال کرتے وقت وہ پیرامیٹر نہ دیں تو ڈیفالٹ استعمال ہوگا۔

---

## Recursive Functions — بازگشتی فنکشن

A function that calls itself:

```urdu
فنکشن فیکٹوریل(ن) {
    اگر (ن <= 1) {
        واپس 1;
    }
    واپس ن * فیکٹوریل(ن - 1);
}

لکھو(فیکٹوریل(5));    // 120  (5 × 4 × 3 × 2 × 1)
لکھو(فیکٹوریل(0));    // 1
```

> **اردو:** بازگشتی فنکشن خود کو بلاتا ہے۔ ہر بار چھوٹی قدر پر — جب تک بنیادی صورت (base case) تک نہ پہنچے۔ بغیر base case کے بے انتہا چلتا رہے گا۔

---

## Arrow Functions — تیر فنکشن

A shorter way to write simple functions:

```urdu
// Arrow function — one expression
متغیر دوگنا = (ن) => ن * 2;
لکھو(دوگنا(7));    // 14

// Arrow function — with block
متغیر مربع = (ن) => {
    واپس ن * ن;
};
لکھو(مربع(6));    // 36
```

> **اردو:** `=>` سے چھوٹے فنکشن بنائیں۔ ایک اظہار ہو تو بلاک کی ضرورت نہیں — نتیجہ خودبخود واپس آتا ہے۔

---

## Functions as Values — فنکشن بطور قدر

Functions are values — you can store them in variables:

```urdu
متغیر جوڑو = فنکشن(الف, ب) {
    واپس الف + ب;
};
لکھو(جوڑو(10, 20));    // 30
```

Or pass them to other functions:

```urdu
فنکشن چلاؤ(فنکشن_م, قدر) {
    واپس فنکشن_م(قدر);
}

لکھو(چلاؤ(دوگنا, 5));    // 10
```

> **اردو:** اردو PL میں فنکشن خود ایک قدر ہے — متغیر میں رکھا جا سکتا ہے یا دوسرے فنکشن کو دیا جا سکتا ہے۔

---

## Scope — دائرہ

Variables declared inside a function are **local** — they don't exist outside:

```urdu
فنکشن دائرہ_مثال() {
    متغیر مقامی = "میں فنکشن کے اندر ہوں";
    لکھو(مقامی);
}

دائرہ_مثال();
// لکھو(مقامی);    // ← ERROR: مقامی is not defined here
```

Variables declared outside are **global** and can be read (but not reassigned) inside:

```urdu
متغیر عالمی = "میں باہر ہوں";

فنکشن پڑھو_عالمی() {
    لکھو(عالمی);    // ✓ can read global
}

پڑھو_عالمی();    // میں باہر ہوں
```

> **اردو:** فنکشن کے اندر بنا متغیر صرف اندر ہے — باہر نہیں پہنچتا۔ باہر کا متغیر اندر سے پڑھا جا سکتا ہے۔

---

## Practical Example: Temperature Converter — عملی مثال: درجہ حرارت تبدیل

```urdu
فنکشن سیلسیس_سے_فارن(ص) {
    واپس (ص * 9 / 5) + 32;
}

فنکشن فارن_سے_سیلسیس(ف) {
    واپس (ف - 32) * 5 / 9;
}

لکھو(سیلسیس_سے_فارن(0));      // 32.0
لکھو(سیلسیس_سے_فارن(100));    // 212.0
لکھو(گول(فارن_سے_سیلسیس(98.6), 1));    // 37.0
```

---

## Key Points — اہم نکات

- `فنکشن نام(پیرامیٹرز) { ... }` — defines a function
- `نام(قدریں)` — calls the function
- `واپس قدر` — returns a value and exits the function
- `پیرامیٹر = ڈیفالٹ` — makes a parameter optional
- Arrow function: `(ن) => ن * 2` — short form for simple functions
- Functions are values — store in variables, pass to other functions
- Local variables live only inside the function

> **اردو:** `فنکشن` سے بنائیں، نام اور قوسین سے چلائیں، `واپس` سے نتیجہ دیں۔ ڈیفالٹ پیرامیٹرز اختیاری بناتے ہیں۔ `=>` مختصر فنکشن کے لیے۔

---

[← Previous: Break & Continue](14-break-continue.md) | [Next: Intermediate Section →](../intermediate/index.md)
