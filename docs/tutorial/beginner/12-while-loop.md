# 12. While Loop — جبکہ لوپ

**Difficulty:** Beginner — مبتدی  
**Time:** ~20 minutes

---

## Basic While — بنیادی جبکہ

A `جبکہ` loop repeats a block of code as long as a condition is true:

```urdu
متغیر گنتی = 1;
جبکہ (گنتی <= 5) {
    لکھو(گنتی);
    گنتی += 1;
}
```

Output:
```
1
2
3
4
5
```

**Pattern:**
```
جبکہ (شرط) {
    // code to repeat
}
```

> **اردو:** `جبکہ` لوپ تب تک چلتا رہتا ہے جب تک شرط سچ رہے۔ ہر چکر میں شرط دوبارہ جانچی جاتی ہے۔ شرط جھوٹ ہو جائے تو لوپ رک جاتا ہے۔

---

## The Counter Pattern — گنتی کا طریقہ

The most common while loop pattern uses a counter:

```urdu
متغیر ن = 0;
جبکہ (ن < 3) {
    لکھو(`چکر نمبر: ${ن}`);
    ن += 1;    // ← must update the counter!
}
```

Output:
```
چکر نمبر: 0
چکر نمبر: 1
چکر نمبر: 2
```

> **اردو:** کاؤنٹر لوپ تین حصے: شروع (`متغیر ن = 0`)، شرط (`ن < 3`)، تبدیلی (`ن += 1`)۔ تبدیلی نہ لکھیں تو لوپ ہمیشہ چلتا رہے گا (انفینٹ لوپ)۔

---

## Infinite Loop with Break — بے انتہا لوپ ٹوٹنا سے

Sometimes you don't know in advance when to stop. Use `جبکہ (سچ)` and break when ready:

```urdu
متغیر ن = 0;
جبکہ (سچ) {
    ن += 1;
    اگر (ن >= 3) {
        ٹوٹنا;
    }
}
لکھو(`ٹوٹا: ${ن}`);    // ٹوٹا: 3
```

> **اردو:** `جبکہ (سچ)` بے انتہا لوپ ہے۔ `ٹوٹنا` سے باہر نکلیں۔ جب شرط لوپ کے درمیان جانچنی ہو یہ طریقہ مناسب ہے۔

---

## Skip Iterations with Continue — جاری سے چھوڑنا

`جاری` skips the rest of the current iteration and jumps back to the condition check:

```urdu
متغیر ج = 0;
جبکہ (ج < 10) {
    ج += 1;
    اگر (ج % 2 == 0) {
        جاری;    // skip even numbers — جفت اعداد چھوڑیں
    }
    لکھو(ج);
}
```

Output: `1  3  5  7  9`

> **اردو:** `جاری` اس چکر کا بقیہ کوڈ چھوڑ دیتا ہے اور اگلے چکر پر جاتا ہے۔ `ٹوٹنا` لوپ باہر نکالتا ہے، `جاری` صرف چکر چھوڑتا ہے۔

---

## Do-While — کرو جبکہ

A `کرو...جبکہ` loop always executes **at least once**, then checks the condition:

```urdu
متغیر د = 1;
کرو {
    لکھو(`کرو: ${د}`);
    د += 1;
} جبکہ (د <= 3);
```

Output:
```
کرو: 1
کرو: 2
کرو: 3
```

Even if the condition is false from the start, the body still runs once:

```urdu
متغیر ے = 10;
کرو {
    لکھو("کم از کم ایک بار چلا");
} جبکہ (ے < 5);    // false immediately
```

Output: `کم از کم ایک بار چلا`

> **اردو:** `کرو...جبکہ` پہلے کوڈ چلاتا ہے، پھر شرط جانچتا ہے۔ `جبکہ` پہلے شرط جانچتا ہے — اس لیے شرط پہلے سے جھوٹ ہو تو `جبکہ` بالکل نہیں چلتا لیکن `کرو...جبکہ` ایک بار ضرور چلتا ہے۔

---

## Practical Example: Input Validation — عملی مثال: ان پٹ جانچ

```urdu
متغیر عمر;
جبکہ (سچ) {
    متغیر ان_پٹ = پڑھو("آپ کی عمر (1-120): ");
    عمر = عدد(ان_پٹ);
    اگر (عمر >= 1 اور عمر <= 120) {
        ٹوٹنا;
    }
    لکھو("غلط عمر — دوبارہ لکھیں");
}
لکھو(`عمر قبول: ${عمر}`);
```

> **اردو:** یہ عام طریقہ ہے: `جبکہ (سچ)` میں ان پٹ لو، جانچو، درست ہو تو `ٹوٹنا`، ورنہ پھر پوچھو۔

---

## Common Mistakes — عام غلطیاں

**Infinite loop — بے انتہا لوپ:**
```urdu
متغیر ن = 1;
جبکہ (ن <= 10) {
    لکھو(ن);
    // ← forgot ن += 1 — loop runs forever!
}
```

**Off-by-one — ایک کم زیادہ:**
```urdu
// To print 1 through 5:
متغیر ن = 1;
جبکہ (ن < 5) {     // ← wrong: prints 1,2,3,4 only
    لکھو(ن);
    ن += 1;
}

متغیر ن = 1;
جبکہ (ن <= 5) {    // ← correct: prints 1,2,3,4,5
    لکھو(ن);
    ن += 1;
}
```

---

## Key Points — اہم نکات

- `جبکہ (شرط) { ... }` — repeats while condition is true
- Always update the counter to avoid infinite loops
- `ٹوٹنا` exits the loop immediately
- `جاری` skips to the next iteration
- `کرو { ... } جبکہ (شرط)` — runs at least once

> **اردو:** `جبکہ` شرط سچ رہے تو چلتا ہے۔ `ٹوٹنا` باہر نکلتا ہے، `جاری` اگلے چکر پر جاتا ہے۔ `کرو...جبکہ` پہلے چلتا ہے پھر شرط جانچتا ہے۔

---

[← Previous: Switch / Case](11-switch-case.md) | [Next: For Loop →](13-for-loop.md)
