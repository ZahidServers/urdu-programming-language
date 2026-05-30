# 15. Threading — دھاگے

**Difficulty:** Intermediate — متوسط  
**Time:** ~30 minutes

---

## Importing — درآمد

```urdu
درآمد {
    دھاگہ, دھاگہ_تالاب, تالہ, واقعہ,
    سیمافور, قطار, ترجیحی_قطار,
    ٹائمر, وقفہ_ٹائمر, مقامی_ذخیرہ
} سے "اردو/دھاگہ";
درآمد { نیند } سے "اردو/تاریخ";
```

> **اردو:** `"اردو/دھاگہ"` میں تمام کثیر-دھاگہ اوزار ہیں۔ `نیند` کے لیے `"اردو/تاریخ"` سے درآمد کریں۔

---

## Basic Thread — بنیادی دھاگہ

`نیا دھاگہ(کام)` creates a thread. `.شروع()` starts it. `.انتظار()` waits for it to finish.

```urdu
فنکشن سلام() {
    لکھو("دھاگہ: سلام!");
}

متغیر د = نیا دھاگہ(سلام);
د.شروع();
د.انتظار();    // wait until thread finishes
لکھو("مکمل");
```

**With arguments — دلائل کے ساتھ:**

```urdu
فنکشن عنوان(نام) {
    لکھو(`دھاگہ: ${نام}`);
}

متغیر د = نیا دھاگہ(عنوان, "احمد");
د.شروع();
د.انتظار();
// Output: دھاگہ: احمد
```

**Thread info — دھاگہ معلومات:**

```urdu
لکھو(دھاگہ.گنتی());      // active thread count
لکھو(د.چل_رہا());         // False (finished)
```

> **اردو:** `نیا دھاگہ(فنکشن, دلیل1, دلیل2)` — فنکشن اور دلائل پاس کریں۔ `.شروع()` دھاگہ چالو کرتا ہے، `.انتظار()` اس کے ختم ہونے کا انتظار کرتا ہے۔

---

## Multiple Threads — کئی دھاگے

```urdu
فنکشن کام(شناخت) {
    لکھو(`دھاگہ ${شناخت} چل رہا ہے`);
}

متغیر دھاگے = [];
متغیر ا = 0;
جبکہ (ا < 3) {
    متغیر د = نیا دھاگہ(کام, ا + 1);
    دھاگے.شامل(د);
    د.شروع();
    ا = ا + 1;
}

// Wait for all
کے_لیے (متغیر د میں دھاگے) {
    د.انتظار();
}
لکھو("سب مکمل");
```

---

## Lock — تالہ (Mutual Exclusion)

Use `تالہ` when multiple threads share mutable data. Without a lock, updates can interleave and produce wrong results.

```urdu
متغیر شمار = [0];    // use list for mutable shared state
متغیر ل = نیا تالہ();

فنکشن بڑھاؤ() {
    متغیر ا = 0;
    جبکہ (ا < 100) {
        ل.قبضہ();         // acquire lock
        شمار[0] = شمار[0] + 1;
        ل.چھوڑو();         // release lock
        ا = ا + 1;
    }
}

متغیر د1 = نیا دھاگہ(بڑھاؤ);
متغیر د2 = نیا دھاگہ(بڑھاؤ);
د1.شروع(); د2.شروع();
د1.انتظار(); د2.انتظار();

لکھو(شمار[0]);    // 200 (always correct with lock)
```

> **اردو:** `.قبضہ()` تالہ لیتا ہے، `.چھوڑو()` چھوڑتا ہے۔ مشترکہ ڈیٹا کو ہمیشہ تالے سے محفوظ کریں۔

> **Note:** Shared mutable variables must be wrapped in a list (`[0]`) due to how Urdu closures work — you cannot reassign an outer variable directly from inside an inner function.

---

## Queue — قطار (Thread-Safe Messaging)

`قطار` is the standard way to pass data between threads safely:

| Method | Description |
|--------|-------------|
| `.ڈالو(آئٹم)` | Add item (blocks if full) |
| `.نکالو()` | Remove item (blocks until available) |
| `.نکالو_نہ_رکو()` | Remove item without blocking (returns `خالی` if empty) |
| `.خالی()` | Returns `سچ` if queue is empty |
| `.لمبائی()` | Current item count |

**Producer-consumer pattern — پیدا_کار/صارف:**

```urdu
متغیر ق = نیا قطار();
متغیر نتائج = [];

فنکشن پیدا_کار() {
    متغیر ا = 0;
    جبکہ (ا < 3) {
        ق.ڈالو(ا + 1);
        ا = ا + 1;
    }
    ق.ڈالو(خالی);    // signal: no more items
}

فنکشن صارف() {
    جبکہ (سچ) {
        متغیر آئٹم = ق.نکالو();
        اگر (آئٹم == خالی) { ٹوٹنا; }
        نتائج.شامل(آئٹم * 10);
    }
}

متغیر د_پ = نیا دھاگہ(پیدا_کار);
متغیر د_ص = نیا دھاگہ(صارف);
د_پ.شروع(); د_ص.شروع();
د_پ.انتظار(); د_ص.انتظار();

لکھو(نتائج);    // [10, 20, 30]
```

---

## Priority Queue — ترجیحی قطار

Items are dequeued in priority order (lowest number = highest priority):

```urdu
متغیر ترق = نیا ترجیحی_قطار();
ترق.ڈالو(3, "کم اہم");
ترق.ڈالو(1, "اہم");
ترق.ڈالو(2, "درمیانی");

لکھو(ترق.نکالو());    // (1, 'اہم')
لکھو(ترق.نکالو());    // (2, 'درمیانی')
لکھو(ترق.نکالو());    // (3, 'کم اہم')
```

> **اردو:** `ترجیحی_قطار` میں `.ڈالو(عدد, آئٹم)` — پہلا عدد ترجیح ہے (چھوٹا نمبر پہلے نکلے گا)۔

---

## Event — واقعہ (Thread Signaling)

`واقعہ` lets one thread signal another. The waiting thread blocks until the event is set.

```urdu
متغیر واق = نیا واقعہ();
متغیر پیغام = [""];

فنکشن منتظر_کام() {
    واق.انتظار(5.0);    // wait up to 5 seconds
    لکھو(`پیغام ملا: ${پیغام[0]}`);
}

فنکشن بھیجنے_والا() {
    نیند(0.5);
    پیغام[0] = "آمادہ";
    واق.مقرر();    // signal the event
}

متغیر د_م = نیا دھاگہ(منتظر_کام);
متغیر د_ب = نیا دھاگہ(بھیجنے_والا);
د_م.شروع(); د_ب.شروع();
د_م.انتظار(); د_ب.انتظار();
// Output: پیغام ملا: آمادہ
```

**Event methods — واقعہ کے طریقے:**

```urdu
واق.مقرر();           // set the event (unblocks all waiters)
واق.صاف();            // reset to un-set
واق.لگا_ہوا();        // True if set
واق.انتظار(5.0);      // block until set or timeout
```

---

## Semaphore — سیمافور (Limit Concurrency)

`سیمافور` limits how many threads can run a section simultaneously:

```urdu
متغیر س = نیا سیمافور(2);    // allow 2 at a time

فنکشن محدود_کام(شناخت) {
    س.حاصل();                  // acquire one slot
    لکھو(`دھاگہ ${شناخت} فعال`);
    نیند(0.1);
    لکھو(`دھاگہ ${شناخت} مکمل`);
    س.چھوڑو();                  // release slot
}

متغیر دھاگے = [];
متغیر ب = 0;
جبکہ (ب < 4) {
    متغیر د = نیا دھاگہ(محدود_کام, ب + 1);
    دھاگے.شامل(د);
    د.شروع();
    ب = ب + 1;
}
کے_لیے (متغیر د میں دھاگے) { د.انتظار(); }
```

Only 2 threads run at once, even though 4 were started.

---

## Thread Pool — دھاگہ تالاب

`دھاگہ_تالاب` runs many tasks efficiently using a worker pool:

### Map — نقشہ

```urdu
فنکشن مربع(ن) { واپس ن * ن; }

متغیر تالاب = نیا دھاگہ_تالاب(4);    // 4 worker threads
متغیر نتائج = تالاب.نقشہ(مربع, [1, 2, 3, 4, 5]);
لکھو(نتائج);    // [1, 4, 9, 16, 25]
تالاب.بند();
```

### Future — مستقبل

Submit a single task and retrieve its result later:

```urdu
متغیر تالاب = نیا دھاگہ_تالاب(2);

متغیر م = تالاب.جمع_کرو_مستقبل(مربع, 7);
لکھو(م.مکمل());       // False (may still be running)
لکھو(م.نتیجہ());      // 49   (blocks until done)
لکھو(م.مکمل());       // True

تالاب.بند();
```

**Future methods — مستقبل کے طریقے:**

| Method | Description |
|--------|-------------|
| `.نتیجہ(وقفہ=خالی)` | Block and return result |
| `.مکمل()` | `سچ` if finished or cancelled |
| `.چل_رہا()` | `سچ` if currently executing |
| `.منسوخ()` | Cancel if not yet started |
| `.غلطی()` | Exception raised, or `خالی` |

---

## Timer — ٹائمر (One-Shot)

Run a function once after a delay:

```urdu
متغیر ہوا = [جھوٹ];

فنکشن کال_بیک() {
    ہوا[0] = سچ;
    لکھو("ٹائمر چلا!");
}

متغیر ٹ = نیا ٹائمر(1.0, کال_بیک);    // fire after 1 second
ٹ.شروع();

نیند(1.5);
لکھو(ہوا[0]);    // True
```

Cancel before it fires: `ٹ.منسوخ()`

---

## Repeating Timer — وقفہ ٹائمر

Fire a function repeatedly at a fixed interval:

```urdu
متغیر گنتی = [0];

فنکشن دہرائیں() {
    گنتی[0] = گنتی[0] + 1;
    لکھو(`دھڑکن ${گنتی[0]}`);
}

متغیر وٹ = نیا وقفہ_ٹائمر(0.5, دہرائیں);
وٹ.شروع();
نیند(1.8);
وٹ.روکو();    // stop the repeating timer
لکھو(`کل: ${گنتی[0]}`);    // 3
```

---

## Thread-Local Storage — مقامی ذخیرہ

Each thread gets its own independent value:

```urdu
متغیر ذخیرہ = نیا مقامی_ذخیرہ();

فنکشن کام(نام) {
    ذخیرہ.مقرر("صارف", نام);
    نیند(0.05);
    لکھو(`${نام}: ${ذخیرہ.حاصل("صارف")}`);
}

متغیر د1 = نیا دھاگہ(کام, "احمد");
متغیر د2 = نیا دھاگہ(کام, "فاطمہ");
د1.شروع(); د2.شروع();
د1.انتظار(); د2.انتظار();
// Each thread sees only its own value
```

---

## Practical Example: Parallel Downloads — موازی ڈاؤن لوڈ

```urdu
درآمد { دھاگہ_تالاب } سے "اردو/دھاگہ";

فنکشن فائل_ڈاؤن_لوڈ(فائل_نام) {
    // simulate work
    درآمد { نیند } سے "اردو/تاریخ";
    نیند(0.1);
    واپس `${فائل_نام} مکمل`;
}

متغیر فائلیں = ["دستاویز.pdf", "تصویر.png", "ڈیٹا.json", "رپورٹ.xlsx"];

متغیر تالاب = نیا دھاگہ_تالاب(4);
متغیر نتائج = تالاب.نقشہ(فائل_ڈاؤن_لوڈ, فائلیں);
تالاب.بند();

کے_لیے (متغیر ن میں نتائج) {
    لکھو(ن);
}
```

---

## Threading Tips — اہم نکات

**Shared state — مشترکہ حالت:**
- Wrap mutable shared values in a list: `[0]` not `0`
- Always protect with `تالہ` when multiple threads write

**Use the right tool:**
- `دھاگہ` — for a single background task
- `دھاگہ_تالاب + نقشہ` — for applying one function to many inputs
- `دھاگہ_تالاب + جمع_کرو_مستقبل` — when you need the result later
- `قطار` — for passing work items between threads
- `واقعہ` — for signaling "something happened"
- `سیمافور` — to cap how many threads do something at once

---

## Quick Reference — فوری حوالہ

| Class | Purpose |
|-------|---------|
| `دھاگہ(کام, *دلائل)` | Single thread |
| `دھاگہ_تالاب(n)` | Worker pool |
| `تالہ()` | Mutual exclusion |
| `واقعہ()` | Thread signaling |
| `سیمافور(n)` | Limit concurrency |
| `قطار()` | Thread-safe FIFO queue |
| `ترجیحی_قطار()` | Priority-ordered queue |
| `ٹائمر(t, fn)` | One-shot delayed call |
| `وقفہ_ٹائمر(t, fn)` | Repeating interval call |
| `مقامی_ذخیرہ()` | Per-thread storage |

---

[← Previous: Type Conversion](14-type-conversion.md) | [Next: Intermediate Index →](index.md)
