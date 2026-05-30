# 3. Hello World — ہیلو ورلڈ

**Difficulty:** Beginner — مبتدی  
**Time:** ~10 minutes

---

## Your First Program — آپ کا پہلا پروگرام

Create a new file called `hello.urdu` and type exactly this:

```urdu
لکھو("السلام علیکم، دنیا!")
```

Run it:
```
urdu run hello.urdu
```

Output:
```
السلام علیکم، دنیا!
```

That is a complete, working program. Just one line.

> **اردو:** یہ ایک مکمل کام کرنے والا پروگرام ہے — صرف ایک سطر۔ `hello.urdu` فائل بنائیں، اوپر کا کوڈ لکھیں، اور `urdu run hello.urdu` سے چلائیں۔

---

## Breaking It Down — تجزیہ

```urdu
لکھو("السلام علیکم، دنیا!")
│     │                    │
│     └── The text to print (wrapped in double quotes — دہری قوسین میں متن)
└── The print function — پرنٹ فنکشن
```

- **`لکھو`** — This is the print function. It displays whatever you give it on the screen, then moves to the next line.
- **`"السلام علیکم، دنیا!"`** — This is a **string** (a piece of text). Strings are always wrapped in double quotes `"..."` or single quotes `'...'`.
- **`(` `)` parentheses** — Every function call requires parentheses around its arguments.
- **`;`** — The semicolon at the end of a statement is optional. Both `لکھو("سلام")` and `لکھو("سلام");` work.

> **اردو:**
> - `لکھو` — پرنٹ فنکشن ہے۔ جو کچھ دیں، اسکرین پر دکھاتا ہے۔
> - `"السلام علیکم، دنیا!"` — یہ ایک **متن** (string) ہے۔ متن ہمیشہ دہری قوسین `"..."` یا اکہری `'...'` میں لپیٹا جاتا ہے۔
> - `()` قوسین — ہر فنکشن کال میں قوسین ضروری ہیں۔
> - `;` — بیان کے آخر میں سیمی کولن اختیاری ہے۔

---

## Printing Multiple Things — کئی چیزیں پرنٹ کریں

`لکھو` accepts any number of arguments separated by commas:

```urdu
لکھو("نام:", "احمد");
لکھو("عمر:", 25);
لکھو("شہر:", "کراچی");
```

Output:
```
نام: احمد
عمر: 25
شہر: کراچی
```

```urdu
// Print three values on one line
لکھو("ایک", "دو", "تین");
```

Output:
```
ایک دو تین
```

> **اردو:** `لکھو` کو کاما سے جدا کر کے جتنی بھی قدریں دیں، وہ خالی جگہ سے جوڑ کر ایک سطر میں دکھاتا ہے۔

---

## Controlling Separator and End — جوڑنے والا اور آخری حرف

```urdu
// Custom separator — sep
لکھو("احمد", "فاطمہ", "علی", sep=", ");
// احمد, فاطمہ, علی

// No newline at end — end
لکھو("ایک", end=" ");
لکھو("دو", end=" ");
لکھو("تین");
// ایک دو تین
```

> **اردو:** `sep` سے قدروں کے درمیان جوڑنے والا حرف بدلیں۔ `end` سے آخر میں لگنے والا حرف بدلیں (پہلے سے طے: نئی سطر)۔

---

## Comments — تبصرے

Comments are notes for humans — the program ignores them completely.

```urdu
// یہ ایک تبصرہ ہے — This is a comment
لکھو("یہ چلے گا");   // یہ بھی تبصرہ ہے

/* یہ
   کئی سطروں کا
   تبصرہ ہے */
لکھو("یہ بھی چلے گا");
```

Output:
```
یہ چلے گا
یہ بھی چلے گا
```

> **اردو:** `//` سے ایک سطر کا تبصرہ شروع ہوتا ہے۔ `/* ... */` سے کئی سطروں کا تبصرہ لکھ سکتے ہیں۔ تبصرے پروگرام کے چلنے پر کوئی اثر نہیں ڈالتے۔

---

## Common Beginner Mistakes — عام ابتدائی غلطیاں

| Mistake | Wrong | Correct |
|---------|-------|---------|
| Forgetting quotes | `لکھو(سلام)` | `لکھو("سلام")` |
| Missing parentheses | `لکھو "سلام"` | `لکھو("سلام")` |
| Mixing quote types | `لکھو("سلام')` | `لکھو("سلام")` |

> **اردو:** سب سے عام غلطیاں: قوسین `"..."` بھول جانا، قوسین `()` نہ لکھنا، یا شروع اور آخر میں مختلف قوسین استعمال کرنا۔

---

## Practice Exercises — مشق

Try writing these programs yourself:

1. Print your own name
2. Print three lines: your name, your city, and your hobby
3. Print the numbers 1 through 5 on one line, separated by dashes

```urdu
// Exercise 1 — مشق 1
لکھو("میرا نام [آپ کا نام] ہے");

// Exercise 2 — مشق 2
لکھو("نام: [آپ کا نام]");
لکھو("شہر: [آپ کا شہر]");
لکھو("مشغلہ: [آپ کا مشغلہ]");

// Exercise 3 — مشق 3
لکھو(1, 2, 3, 4, 5, sep="-");
```

> **اردو:** مشق 1: اپنا نام پرنٹ کریں۔ مشق 2: تین سطریں پرنٹ کریں۔ مشق 3: 1 سے 5 تک ڈیش سے جوڑ کر پرنٹ کریں۔

---

## Key Points — اہم نکات

- `لکھو()` is the print function — it displays output on the screen
- Strings must be wrapped in `"..."` or `'...'`
- `لکھو` accepts multiple comma-separated arguments
- `//` starts a comment — the program ignores everything after it
- Semicolons `;` are optional

> **اردو:** `لکھو()` پرنٹ فنکشن ہے۔ متن `"..."` میں لپیٹیں۔ `//` تبصرے کا آغاز ہے۔ سیمی کولن اختیاری ہے۔

---

[← Previous: Installation](02-installation.md) | [Next: Variables →](04-variables.md)
