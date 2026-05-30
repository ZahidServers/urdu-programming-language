# 1. Advanced Functions — اعلی فنکشنز

**Difficulty:** Intermediate — متوسط  
**Time:** ~25 minutes

---

## Rest Parameters — باقی پیرامیٹرز

Accept any number of arguments with `...`:

```urdu
فنکشن جمع_سب(...اعداد) {
    متغیر کل = 0;
    کے_لیے (متغیر ن میں اعداد) {
        کل += ن;
    }
    واپس کل;
}

لکھو(جمع_سب(1, 2, 3));           // 6
لکھو(جمع_سب(1, 2, 3, 4, 5));    // 15
```

> **اردو:** `...` سے باقی تمام دلائل ایک فہرست میں جمع ہو جاتے ہیں۔ آخری پیرامیٹر پر ہی استعمال ہو سکتا ہے۔

---

## Spread Operator — پھیلاؤ آپریٹر

`...` also **spreads** an array into individual values:

```urdu
متغیر الف = [1, 2, 3];
متغیر ب = [4, 5, 6];
متغیر ملا = [...الف, ...ب];
لکھو(ملا);    // [1, 2, 3, 4, 5, 6]

فنکشن جمع3(x, y, z) { واپس x + y + z; }
لکھو(جمع3(...الف));    // 6  (spreads list as arguments)
```

> **اردو:** `...فہرست` فہرست کو الگ الگ قدروں میں پھیلاتا ہے۔ یہ فہرستیں جوڑنے یا فنکشن کو فہرست سے دلائل دینے کے لیے مفید ہے۔

---

## Higher-Order Functions — اعلی درجے کے فنکشنز

A function that takes another function as an argument (or returns one):

### تبدیل — map

Apply a function to every element of a list:

```urdu
متغیر اعداد = [1, 2, 3, 4, 5];

فنکشن دوگنا(ن) { واپس ن * 2; }
متغیر دوگنے = اعداد.تبدیل(دوگنا);
لکھو(دوگنے);    // [2, 4, 6, 8, 10]
```

### چھانو — filter

Keep only elements where the function returns true:

```urdu
فنکشن بڑا_سے_تین(ن) { واپس ن > 3; }
متغیر بڑے = اعداد.چھانو(بڑا_سے_تین);
لکھو(بڑے);    // [4, 5]
```

### اکٹھا — reduce

Combine all elements into a single value:

```urdu
فنکشن جوڑو(کل, ن) { واپس کل + ن; }
متغیر مجموع = اعداد.اکٹھا(جوڑو, 0);
لکھو(مجموع);    // 15
```

> **اردو:** `.تبدیل()` ہر عنصر تبدیل کرتا ہے، `.چھانو()` شرط کے مطابق چھانتا ہے، `.اکٹھا()` سب کو ایک قدر میں ملاتا ہے۔ فنکشن کا نام (بغیر قوسین) بطور دلیل دیں۔

---

## Closures — بندش

A function that remembers the variables of the scope it was created in:

```urdu
فنکشن گنتی_بنائیں(شروع = 0) {
    متغیر حالت = [شروع];
    واپس فنکشن() {
        حالت[0] = حالت[0] + 1;
        واپس حالت[0];
    };
}

متغیر گنتی = گنتی_بنائیں();
لکھو(گنتی());    // 1
لکھو(گنتی());    // 2
لکھو(گنتی());    // 3
```

> **اردو:** بندش (closure) اندرونی فنکشن باہری فنکشن کے متغیر یاد رکھتا ہے۔ باہری قدر کو تبدیل کرنے کے لیے فہرست `[قدر]` کا چال استعمال کریں۔

---

## Function Composition — فنکشن ترکیب

Combine simple functions to build complex ones:

```urdu
فنکشن دوگنا(ن) { واپس ن * 2; }
فنکشن ایک_جمع(ن) { واپس ن + 1; }

فنکشن ترکیب(ف1, ف2) {
    واپس فنکشن(ن) {
        واپس ف1(ف2(ن));
    };
}

متغیر دوگنا_پھر_جمع = ترکیب(ایک_جمع, دوگنا);
لکھو(دوگنا_پھر_جمع(5));    // 11  (5×2=10, 10+1=11)
```

---

## Key Points — اہم نکات

- `...اعداد` collects remaining args into a list (rest params)
- `...فہرست` spreads a list into separate args
- `.تبدیل(f)`, `.چھانو(f)`, `.اکٹھا(f, init)` — list transformations
- Closures capture outer scope; use mutable container `[val]` to update
- Pass function names without `()` as arguments

> **اردو:** `...` آرام اور پھیلاؤ دونوں کام کرتا ہے۔ `.تبدیل/.چھانو/.اکٹھا` فہرست کو تبدیل کرتے ہیں۔ بندش باہری متغیر یاد رکھتی ہے۔

---

[← Beginner: Functions](../beginner/15-functions-basics.md) | [Next: Lists / Arrays →](02-lists-arrays.md)
