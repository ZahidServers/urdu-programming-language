# Complete Keyword Reference — مکمل کلیدی الفاظ

Every reserved keyword in the Urdu Programming Language is listed below. Keywords cannot be used as variable names or function names. They are processed directly by the lexer before parsing.

> **اردو:** اردو پروگرامنگ زبان کے تمام محفوظ کلیدی الفاظ نیچے درج ہیں۔ کلیدی الفاظ متغیر یا فنکشن کے نام کے طور پر استعمال نہیں کیے جا سکتے۔

---

## Variable Declarations — متغیرات

> **اردو:** متغیر قابل تبدیل قدر ذخیرہ کرتا ہے، مستقل ناقابل تبدیل قدر کے لیے ہے، اور چھوٹا بلاک دائرہ کار متغیر ہے۔

| Urdu Keyword | English Equivalent | Category | Description |
|-------------|-------------------|----------|-------------|
| `متغیر` | `var` / `let` | Declaration | Declare a mutable variable. Scope is function-level (hoisted like `var`) or block-level depending on context. |
| `مستقل` | `const` | Declaration | Declare a constant — its binding cannot be reassigned after initialization. |
| `چھوٹا` | `let` | Declaration | Alias for `متغیر`. Block-scoped variable declaration. |

**Examples**

```urdu
متغیر نام = "احمد";
مستقل پائی = 3.14159;
چھوٹا عارضی = وقت();
```

---

## Control Flow — بہاؤ کنٹرول

> **اردو:** بہاؤ کنٹرول کلیدی الفاظ پروگرام کی سمت اور لوپ کو قابو کرتے ہیں۔

| Urdu Keyword | English Equivalent | Category | Description |
|-------------|-------------------|----------|-------------|
| `اگر` | `if` | Conditional | Execute a block only when the condition is true. |
| `ورنہ` | `else` | Conditional | Execute a block when the preceding `اگر` condition is false. |
| `ورنہ_اگر` | `else if` | Conditional | Chain a second condition after a failing `اگر`. |
| `جبکہ` | `while` | Loop | Repeat a block as long as the condition is true. |
| `کرو` | `do` | Loop | Start a do-while loop — body executes at least once. |
| `کے_لیے` | `for` | Loop | C-style for loop (`for (init; cond; update)`) or for-in/for-of iteration. |
| `میں` | `in` | Loop / Operator | Iterate over keys (for-in), or test membership with `میں_ہے`. |
| `کا` | `of` | Loop | Iterate over values of an iterable (for-of). |
| `ٹوٹنا` | `break` | Loop control | Exit the nearest enclosing loop or `منتخب` block immediately. |
| `جاری` | `continue` | Loop control | Skip the rest of the current loop iteration and proceed to the next. |
| `واپس` | `return` | Function | Exit a function and optionally return a value to the caller. |

**Examples**

```urdu
اگر (عمر >= 18) {
    لکھو("بالغ");
} ورنہ_اگر (عمر >= 13) {
    لکھو("نوجوان");
} ورنہ {
    لکھو("بچہ");
}

جبکہ (x > 0) {
    x = x - 1;
}

کے_لیے (متغیر i = 0; i < 10; i++) {
    اگر (i == 5) ٹوٹنا;
    اگر (i % 2 == 0) جاری;
    لکھو(i);
}

کے_لیے (متغیر پھل کا ["سیب", "کیلا", "آم"]) {
    لکھو(پھل);
}
```

---

## Switch Statement — منتخب

> **اردو:** `منتخب` بیان ایک اظہار کو جانچتا ہے اور مناسب `صورت` پر جاتا ہے۔ اگر کوئی صورت نہ ملے تو `بصورت_دیگر` چلتا ہے۔

| Urdu Keyword | English Equivalent | Category | Description |
|-------------|-------------------|----------|-------------|
| `منتخب` | `switch` | Conditional | Evaluate an expression and jump to a matching case. |
| `صورت` | `case` | Conditional | A labeled branch inside `منتخب`. |
| `بصورت_دیگر` | `default` | Conditional | The fallback branch executed when no `صورت` matches. |

**Examples**

```urdu
منتخب (دن) {
    صورت "پیر":
        لکھو("ہفتہ شروع");
        ٹوٹنا;
    صورت "جمعہ":
        لکھو("ہفتہ ختم");
        ٹوٹنا;
    بصورت_دیگر:
        لکھو("درمیانی دن");
}
```

---

## Functions — فنکشن

> **اردو:** فنکشن (function) کوڈ کا ایک قابل استعمال بلاک ہے۔ `غیر_متزامن` کے ساتھ غیر متزامن فنکشن اور `پیداوار` سے جنریٹر بنائیں۔

| Urdu Keyword | English Equivalent | Category | Description |
|-------------|-------------------|----------|-------------|
| `فنکشن` | `function` | Function | Declare a named or anonymous function. |
| `واپس` | `return` | Function | Return a value from a function (shared with control flow). |
| `غیر_متزامن` | `async` | Async | Mark a function as asynchronous — it returns an awaitable. |
| `انتظار` | `await` | Async | Suspend execution inside a `غیر_متزامن` function until the awaitable resolves. |
| `پیداوار` | `yield` | Generator | Pause a generator function and produce a value. |

**Examples**

```urdu
فنکشن جمع(ا, ب) {
    واپس ا + ب;
}

// تیر نحو (arrow syntax)
مستقل مربع = x => x * x;

غیر_متزامن فنکشن ڈیٹا_لو() {
    متغیر نتیجہ = انتظار fetch_something();
    واپس نتیجہ;
}

// جنریٹر
فنکشن* گنتی() {
    پیداوار 1;
    پیداوار 2;
    پیداوار 3;
}
```

---

## Classes and OOP — کلاس اور OOP

> **اردو:** کلاس (class) ایک بلیو پرنٹ ہے۔ `توسیع` سے وراثت، `نیا` سے نمونہ، `یہ` سے موجودہ نمونہ، اور `سپر` سے والدین تک رسائی ممکن ہے۔

| Urdu Keyword | English Equivalent | Category | Description |
|-------------|-------------------|----------|-------------|
| `کلاس` | `class` | OOP | Declare a class. |
| `توسیع` | `extends` | OOP | Inherit from a parent class. |
| `تعمیر` | `constructor` | OOP | The special method called when a new instance is created with `نیا`. |
| `یہ` | `this` | OOP | Refer to the current class instance inside methods. |
| `سپر` | `super` | OOP | Call the parent class constructor or methods. |
| `نیا` | `new` | OOP | Create a new instance of a class. |
| `عوامی` | `public` | OOP | Mark a member as publicly accessible (default). |
| `نجی` | `private` | OOP | Mark a member as private (accessible only within the class). |
| `محفوظ` | `protected` | OOP | Mark a member as protected (accessible in the class and subclasses). |
| `جامد` | `static` | OOP | Declare a static method or property (belongs to the class, not instances). |
| `خاکہ` | `abstract` | OOP | Mark a class or method as abstract — cannot be instantiated directly. |
| `انٹرفیس` | `interface` | OOP | Declare an interface (type contract). |
| `نافذ` | `implements` | OOP | Declare that a class implements an interface. |
| `صرف_پڑھو` | `readonly` | OOP | Mark a property as read-only after construction. |
| `اوور_رائڈ` | `override` | OOP | Explicitly mark a method as overriding a parent class method. |
| `حاصل_کرو` | `get` | OOP | Define a getter accessor property. |
| `مقرر_کرو` | `set` | OOP | Define a setter accessor property. |

**Examples**

```urdu
کلاس جانور {
    تعمیر(نام) {
        یہ.نام = نام;
    }
    بولو() {
        واپس "...";
    }
}

کلاس کتا توسیع جانور {
    تعمیر(نام) {
        سپر(نام);
    }
    اوور_رائڈ بولو() {
        واپس "بھو بھو!";
    }
    حاصل_کرو معلومات() {
        واپس `${یہ.نام} ایک کتا ہے`;
    }
}

متغیر ر = نیا کتا("ٹومی");
لکھو(ر.بولو());      // بھو بھو!
لکھو(ر.معلومات);     // ٹومی ایک کتا ہے
```

---

## Exception Handling — استثناء

> **اردو:** `کوشش` بلاک میں خطرناک کوڈ ڈالیں، `پکڑو` سے غلطی پکڑیں، `آخر` ہمیشہ چلتا ہے، اور `پھینکو` سے غلطی اٹھائیں۔

| Urdu Keyword | English Equivalent | Category | Description |
|-------------|-------------------|----------|-------------|
| `کوشش` | `try` | Exception | Wrap code that may throw an error. |
| `پکڑو` | `catch` | Exception | Handle an error thrown inside the preceding `کوشش` block. |
| `آخر` | `finally` | Exception | A block that always runs after `کوشش`/`پکڑو`, regardless of success or failure. |
| `پھینکو` | `throw` | Exception | Raise (throw) an error. |

**Examples**

```urdu
کوشش {
    متغیر نتیجہ = خطرناک_کام();
} پکڑو (غ) {
    لکھو("خطا:", غ.پیغام);
} آخر {
    لکھو("صفائی مکمل");
}

// خود غلطی پھینکنا
فنکشن تصدیق(عمر) {
    اگر (عمر < 0) {
        پھینکو نیا رینج_غلطی("عمر منفی نہیں ہو سکتی");
    }
    واپس عمر;
}
```

---

## Modules — ماڈیول

> **اردو:** `درآمد` سے ماڈیول لائیں، `سے` سے ماخذ بتائیں، `برآمد` سے باہر بھیجیں، اور `بطور` سے نام بدلیں۔

| Urdu Keyword | English Equivalent | Category | Description |
|-------------|-------------------|----------|-------------|
| `درآمد` | `import` | Module | Import a module or specific exports from a module. |
| `سے` | `from` | Module | Specify the source module in an import statement. |
| `برآمد` | `export` | Module | Export a value, function, or class from the current module. |
| `ڈیفالٹ` | `default` | Module | The default export of a module. |
| `بطور` | `as` | Module | Rename an import or export. |

**Examples**

```urdu
// مکمل ماڈیول درآمد کریں
درآمد ریاضی_ماڈیول سے "اردو/ریاضی";

// مخصوص نام درآمد کریں
درآمد { جمع, ضرب } سے "./حساب";

// نام بدل کر درآمد کریں
درآمد { جمع بطور جوڑنا } سے "./حساب";

// برآمد
برآمد فنکشن سلام(نام) {
    واپس "خوش آمدید، " + نام;
}

برآمد ڈیفالٹ کلاس میرا_ٹول { }
```

---

## Boolean and Null Values — بولین اور خالی

> **اردو:** `سچ` درست قدر، `جھوٹ` غلط قدر، `خالی` جان بوجھ کر غائب قدر، اور `غیر_معرف` غیر تفویض کردہ قدر ہے۔

| Urdu Keyword | English Equivalent | Category | Description |
|-------------|-------------------|----------|-------------|
| `سچ` | `true` | Literal | Boolean true value. |
| `جھوٹ` | `false` | Literal | Boolean false value. |
| `خالی` | `null` | Literal | Null — the intentional absence of a value. |
| `غیر_معرف` | `undefined` | Literal | Undefined — a value that has not been assigned (maps to Python `None`). |

**Examples**

```urdu
متغیر لاگ_ان = سچ;
متغیر مکمل = جھوٹ;
متغیر پتہ = خالی;
متغیر نتیجہ = غیر_معرف;

اگر (لاگ_ان == سچ) {
    لکھو("آپ لاگ ان ہیں");
}
```

---

## Logical Operators (Keyword Form) — منطقی آپریٹر

> **اردو:** `اور` دونوں سچ ہوں تو سچ، `یا` کم از کم ایک سچ ہو تو سچ، `نہیں` سچ کو جھوٹ اور جھوٹ کو سچ کرتا ہے۔

| Urdu Keyword | Symbol Equivalent | Category | Description |
|-------------|------------------|----------|-------------|
| `اور` | `&&` | Logical | Logical AND — true if both operands are truthy. |
| `یا` | `\|\|` | Logical | Logical OR — true if at least one operand is truthy. |
| `نہیں` | `!` | Logical | Logical NOT — inverts truthiness. |

**Examples**

```urdu
اگر (عمر >= 18 اور ملک == "پاکستان") {
    لکھو("اہل ہیں");
}

اگر (نام == "" یا نام == خالی) {
    لکھو("نام لازمی ہے");
}

اگر (نہیں لاگ_ان) {
    لکھو("پہلے لاگ ان کریں");
}
```

---

## Type and Meta Operators — قسم آپریٹر

> **اردو:** `قسم` قدر کی نوعیت بتاتا ہے، `مثال` جانچتا ہے کہ آیا شے کسی کلاس کا نمونہ ہے، `حذف` خاصیت مٹاتا ہے، اور `میں_ہے` وجود جانچتا ہے۔

| Urdu Keyword | English Equivalent | Category | Description |
|-------------|-------------------|----------|-------------|
| `قسم` | `typeof` | Type | Return the type name of a value as a string. |
| `مثال` | `instanceof` | Type | Test whether an object is an instance of a class. |
| `حذف` | `delete` | Meta | Delete a property from an object. |
| `میں_ہے` | `in` (operator) | Meta | Test whether a key exists in an object or collection. |
| `خلاء` | `void` | Meta | Evaluate an expression and return `undefined`/`خالی`. |

**Examples**

```urdu
لکھو(قسم(42));             // "عدد"
لکھو(قسم("اردو"));         // "متن"
لکھو(قسم(سچ));             // "بولین"
لکھو(قسم(خالی));           // "خالی"
لکھو(قسم([]));             // "فہرست"
لکھو(قسم({}));             // "شے"

متغیر ش = { الف: 1 };
لکھو("الف" میں_ہے ش);    // True
حذف ش.الف;
لکھو("الف" میں_ہے ش);    // False

// مثال — صرف صارف کی کلاسوں کے ساتھ
کلاس جانور {}
متغیر ج = نیا جانور();
لکھو(ج مثال جانور);      // True
```

---

## Built-in Function Keywords — اندرونی فنکشن

These two built-in functions are recognized as keywords by the lexer, though they behave identically to their function counterparts:

> **اردو:** `لکھو` کنسول پر لکھتا ہے اور `پڑھو` معیاری ان پٹ سے ایک سطر پڑھتا ہے۔

| Urdu Keyword | English Equivalent | Category | Description |
|-------------|-------------------|----------|-------------|
| `لکھو` | `print` | I/O | Print values to the console (also a keyword shorthand). |
| `پڑھو` | `input` | I/O | Read a line from standard input (also a keyword shorthand). |

---

## Full Alphabetical Index — مکمل حروف تہجی فہرست

> **اردو:** تمام کلیدی الفاظ کی حروف تہجی ترتیب سے مکمل فہرست۔

| Urdu Keyword | English Equivalent | Category |
|-------------|-------------------|----------|
| `آخر` | `finally` | Exception |
| `اگر` | `if` | Conditional |
| `اور` | `&&` / `and` | Logical |
| `اوور_رائڈ` | `override` | OOP |
| `انتظار` | `await` | Async |
| `انٹرفیس` | `interface` | OOP |
| `برآمد` | `export` | Module |
| `بصورت_دیگر` | `default` (switch) | Switch |
| `بطور` | `as` | Module |
| `پڑھو` | `input` | I/O |
| `پیداوار` | `yield` | Generator |
| `پھینکو` | `throw` | Exception |
| `پکڑو` | `catch` | Exception |
| `تعمیر` | `constructor` | OOP |
| `توسیع` | `extends` | OOP |
| `جاری` | `continue` | Loop |
| `جامد` | `static` | OOP |
| `جبکہ` | `while` | Loop |
| `جھوٹ` | `false` | Literal |
| `حاصل_کرو` | `get` | OOP |
| `حذف` | `delete` | Meta |
| `خاکہ` | `abstract` | OOP |
| `خالی` | `null` | Literal |
| `خلاء` | `void` | Meta |
| `درآمد` | `import` | Module |
| `ڈیفالٹ` | `default` (export) | Module |
| `سچ` | `true` | Literal |
| `سپر` | `super` | OOP |
| `سے` | `from` | Module |
| `صرف_پڑھو` | `readonly` | OOP |
| `صورت` | `case` | Switch |
| `طور` | (part of `بطور`) | Module |
| `عوامی` | `public` | OOP |
| `غیر_متزامن` | `async` | Async |
| `غیر_معرف` | `undefined` | Literal |
| `فنکشن` | `function` | Function |
| `قسم` | `typeof` | Type |
| `کا` | `of` | Loop |
| `کرو` | `do` | Loop |
| `کلاس` | `class` | OOP |
| `کوشش` | `try` | Exception |
| `کے_لیے` | `for` | Loop |
| `لکھو` | `print` | I/O |
| `محفوظ` | `protected` | OOP |
| `مستقل` | `const` | Declaration |
| `مثال` | `instanceof` | Type |
| `مقرر_کرو` | `set` | OOP |
| `منتخب` | `switch` | Switch |
| `متغیر` | `var` / `let` | Declaration |
| `میں` | `in` | Loop |
| `میں_ہے` | `in` (operator) | Meta |
| `نافذ` | `implements` | OOP |
| `نجی` | `private` | OOP |
| `نہیں` | `!` / `not` | Logical |
| `نیا` | `new` | OOP |
| `ورنہ` | `else` | Conditional |
| `ورنہ_اگر` | `else if` | Conditional |
| `واپس` | `return` | Function |
| `یا` | `\|\|` / `or` | Logical |
| `یہ` | `this` | OOP |
| `چھوٹا` | `let` | Declaration |
| `ٹوٹنا` | `break` | Loop |

---

*اردو پروگرامنگ لینگویج — Keyword Reference — Mohammed Zahid Wadiwale*
