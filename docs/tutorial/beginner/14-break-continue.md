# 14. Break & Continue — ٹوٹنا اور جاری

**Difficulty:** Beginner — مبتدی  
**Time:** ~15 minutes

---

## Break — ٹوٹنا

`ٹوٹنا` immediately exits the loop. No more iterations run.

```urdu
کے_لیے (متغیر i میں حد(10)) {
    اگر (i == 5) {
        ٹوٹنا;
    }
    لکھو(i);
}
```

Output: `0  1  2  3  4`

When `i` reaches 5, `ٹوٹنا` exits the loop. The value 5 and everything after is skipped.

> **اردو:** `ٹوٹنا` لوپ سے فوری باہر نکلتا ہے۔ باقی چکر اور شرط جانچنا سب بند — لوپ کے بعد کا کوڈ چلتا ہے۔

**Break in while:**

```urdu
متغیر ن = 0;
جبکہ (سچ) {
    لکھو(ن);
    ن += 1;
    اگر (ن == 4) {
        ٹوٹنا;
    }
}
```

Output: `0  1  2  3`

---

## Continue — جاری

`جاری` skips the rest of the **current iteration** and jumps straight to the next one:

```urdu
کے_لیے (متغیر i میں حد(10)) {
    اگر (i % 2 == 0) {
        جاری;    // skip even numbers
    }
    لکھو(i);
}
```

Output: `1  3  5  7  9`

> **اردو:** `جاری` صرف اس چکر کا بقیہ کوڈ چھوڑتا ہے اور اگلے چکر پر جاتا ہے — لوپ ختم نہیں ہوتا۔ `ٹوٹنا` لوپ باہر نکالتا ہے، `جاری` صرف چکر چھوڑتا ہے۔

**Continue in while:**

```urdu
متغیر م = 0;
جبکہ (م < 8) {
    م += 1;
    اگر (م % 3 == 0) {
        جاری;    // skip multiples of 3
    }
    لکھو(م);
}
```

Output: `1  2  4  5  7  8`

---

## Break vs Continue — فرق

| | `ٹوٹنا` | `جاری` |
|--|---------|--------|
| Effect | Exits the loop entirely | Skips current iteration |
| Remaining iterations | None — loop ends | Yes — loop keeps going |
| Code after loop | Runs next | Runs after all iterations |

```urdu
لکھو("--- ٹوٹنا ---");
کے_لیے (متغیر i میں حد(5)) {
    اگر (i == 3) { ٹوٹنا; }
    لکھو(i);
}
لکھو("لوپ کے بعد");
// Output: 0  1  2
//         لوپ کے بعد

لکھو("--- جاری ---");
کے_لیے (متغیر i میں حد(5)) {
    اگر (i == 3) { جاری; }
    لکھو(i);
}
لکھو("لوپ کے بعد");
// Output: 0  1  2  4
//         لوپ کے بعد
```

---

## Practical Example: Search — عملی مثال: تلاش

```urdu
فنکشن تلاش(فہرست, ہدف) {
    کے_لیے (متغیر [i, قدر] میں گنو(فہرست)) {
        اگر (قدر == ہدف) {
            واپس i;    // found — ملا
        }
    }
    واپس -1;    // not found — نہیں ملا
}

متغیر نام = ["احمد", "فاطمہ", "علی", "زینب"];
لکھو(تلاش(نام, "علی"));     // 2
لکھو(تلاش(نام, "حسن"));    // -1
```

> **اردو:** فہرست میں تلاش کے لیے لوپ اور `ٹوٹنا` (یا `واپس`) کا استعمال۔ `واپس` فنکشن سے نکلتا ہے — لوپ بھی خودبخود رک جاتا ہے۔

---

## Practical Example: Filter — عملی مثال: فلٹر

```urdu
متغیر تمام_نمبر = [1, 5, 3, 8, 2, 9, 4, 7, 6];
متغیر بڑے = [];

کے_لیے (متغیر ن میں تمام_نمبر) {
    اگر (ن < 5) {
        جاری;    // skip small numbers
    }
    بڑے.شامل(ن);
}

لکھو(بڑے);    // [5, 8, 9, 7, 6]
```

> **اردو:** `جاری` سے ناپسندیدہ عناصر چھوڑیں اور باقی فہرست میں جمع کریں۔

---

## Key Points — اہم نکات

- `ٹوٹنا` — exits the loop immediately; works in `جبکہ` and `کے_لیے`
- `جاری` — skips the rest of the current iteration; loop continues
- Both work in all loop types: `جبکہ`, `کرو...جبکہ`, `کے_لیے`
- `ٹوٹنا` in a `منتخب` case prevents fallthrough (covered in chapter 11)

> **اردو:** `ٹوٹنا` لوپ باہر نکالتا ہے۔ `جاری` چکر چھوڑتا ہے۔ دونوں `جبکہ` اور `کے_لیے` میں کام کرتے ہیں۔

---

[← Previous: For Loop](13-for-loop.md) | [Next: Functions Basics →](15-functions-basics.md)
