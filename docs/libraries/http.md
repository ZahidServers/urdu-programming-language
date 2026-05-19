# HTTP Client Library — اردو/کرل

The `اردو/کرل` library provides an async HTTP client for making web requests — GET, POST, file uploads, REST APIs, and more — using Urdu-named methods.

> **اردو:** `اردو/کرل` لائبریری اردو نام والے طریقوں سے ویب درخواستیں (GET، POST، فائل اپلوڈ، REST APIs) بھیجنے کے لیے ایک غیر متزامن HTTP کلائنٹ فراہم کرتی ہے۔

**Import:**

```urdu
درآمد { کرل } سے "اردو/کرل"
```

---

## Table of Contents

1. [Constructor and Configuration](#constructor-and-configuration)
2. [Request Methods](#request-methods)
3. [Response Object — _کرل_جواب](#response-object--_کرل_جواب)
4. [Examples](#examples)

---

## Constructor and Configuration — تعمیر کنندہ اور ترتیب

```urdu
متغیر http = نیا کرل(ترتیب)
```

> **اردو:** تعمیر کنندہ ایک اختیاری ترتیب آبجیکٹ قبول کرتا ہے۔ آپ پہلے سے طے شدہ سرخیاں، ختمی مدت (seconds میں)، بنیادی URL، SSL بندی، پراکسی اور خودکار ری ڈائریکٹ ترتیب دے سکتے ہیں۔

All configuration keys are optional:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `سرخط` | dict | `{}` | Default headers sent with every request |
| `ختمی` | int | `30` | Timeout in seconds |
| `بنیادی_url` | string | `""` | Base URL prepended to all paths |
| `تصدیق_نہ_کرو` | bool | `جھوٹ` | Disable SSL certificate verification |
| `پراکسی` | string | `null` | Proxy URL, e.g. `"http://proxy:8080"` |
| `ری_ڈائریکٹ` | bool | `سچ` | Follow HTTP redirects automatically |

**Basic client:**

```urdu
متغیر http = نیا کرل()
```

**Client with base URL and default headers:**

```urdu
متغیر http = نیا کرل({
    بنیادی_url: "https://api.example.com",
    سرخط: {
        "Content-Type": "application/json",
        "Accept": "application/json"
    },
    ختمی: 15
})
```

---

## Request Methods — درخواست طریقے

All methods are **async** — use `انتظار` inside an `غیر_متزامن` function, or at the top level of an async script.

> **اردو:** تمام طریقے غیر متزامن ہیں — `غیر_متزامن` فنکشن کے اندر `انتظار` استعمال کریں۔ GET سے ڈیٹا حاصل کریں، POST سے بھیجیں، PUT سے تبدیل کریں، DELETE سے مٹائیں اور `فائل_بھیجو` سے ملٹی پارٹ فائل اپلوڈ کریں۔

| Method | HTTP verb | Description |
|--------|-----------|-------------|
| `http.حاصل(url, پیرامیٹر={}, سرخط={})` | GET | Fetch a resource |
| `http.بھیجو(url, ڈیٹا={}, سرخط={})` | POST | Send JSON body |
| `http.فارم_بھیجو(url, ڈیٹا={})` | POST | Send form-encoded body |
| `http.تازہ(url, ڈیٹا={})` | PUT | Replace a resource |
| `http.جزوی_تازہ(url, ڈیٹا={})` | PATCH | Partially update a resource |
| `http.مٹاؤ(url)` | DELETE | Delete a resource |
| `http.سر(url)` | HEAD | Fetch headers only |
| `http.اختیارات(url)` | OPTIONS | Fetch allowed methods |
| `http.فائل_بھیجو(url, فائل_راستہ, خانہ="file", اضافی_ڈیٹا={})` | POST multipart | Upload a file |

---

## Response Object — _کرل_جواب — جواب آبجیکٹ

Every request method returns a `_کرل_جواب` object.

> **اردو:** ہر درخواست طریقہ ایک `_کرل_جواب` آبجیکٹ واپس کرتا ہے۔ `.حالت` سے HTTP حالت رمز، `.متن` سے جواب متن، `.جے_سون()` سے JSON پارس کریں اور `.ٹھیک` سے جانچیں کہ درخواست کامیاب تھی یا نہیں۔

| Property / Method | Type | Description |
|-------------------|------|-------------|
| `.حالت` | int | HTTP status code (e.g. `200`, `404`) |
| `.متن` | string | Response body as text |
| `.مواد` | bytes | Response body as raw bytes |
| `.سرخط` | dict | Response headers |
| `.ٹھیک` | bool | `سچ` when status code < 400 |
| `.ربط` | string | Final URL after redirects |
| `.جے_سون()` | any | Parse body as JSON → object/list |

---

## Examples — مثالیں

### Example 1 — Simple GET request and JSON parsing — سادہ GET درخواست

> **اردو:** یہ مثال سادہ GET درخواست اور JSON پارسنگ دکھاتی ہے۔ `http.حاصل()` سے URL پر GET درخواست بھیجیں، پھر `.جے_سون()` سے جواب کو JSON میں بدلیں۔

```urdu
درآمد { کرل } سے "اردو/کرل"

متغیر http = نیا کرل()

غیر_متزامن فنکشن مرکزی() {
    متغیر جواب = انتظار http.حاصل("https://jsonplaceholder.typicode.com/posts/1");

    اگر (جواب.ٹھیک) {
        متغیر ڈیٹا = جواب.جے_سون();
        لکھو("عنوان:", ڈیٹا.title);
        لکھو("متن:",   ڈیٹا.body);
        لکھو("شناخت:", ڈیٹا.id);
    } ورنہ {
        لکھو("غلطی:", جواب.حالت);
    }
}

انتظار مرکزی();
```

### Example 2 — GET with query parameters — سوال پیرامیٹرز کے ساتھ GET

> **اردو:** GET درخواست میں `پیرامیٹر: {...}` دیں تاکہ سوال پیرامیٹرز URL میں شامل ہوں۔ مثلاً GitHub API پر ذخیرے تلاش کرنا۔

```urdu
درآمد { کرل } سے "اردو/کرل"

متغیر http = نیا کرل()

غیر_متزامن فنکشن تلاش_کریں(عبارت) {
    متغیر جواب = انتظار http.حاصل(
        "https://api.github.com/search/repositories",
        پیرامیٹر: { q: عبارت, sort: "stars", per_page: 5 }
    );

    متغیر نتیجہ = جواب.جے_سون();
    لکھو(`"${عبارت}" کے لیے ${نتیجہ.total_count} ذخیرے ملے:`);

    کے_لیے (متغیر ریپو کا نتیجہ.items) {
        لکھو(`  ★ ${ریپو.stargazers_count}  ${ریپو.full_name}`);
    }
}

انتظار تلاش_کریں("اردو پروگرامنگ");
```

### Example 3 — POST with JSON body — JSON باڈی کے ساتھ POST

> **اردو:** JSON باڈی کے ساتھ POST درخواست بھیجنے کے لیے `http.بھیجو(url, ڈیٹا: {...})` استعمال کریں۔ سرور سے `201 Created` جواب ملنے پر نیا ریکارڈ کامیابی سے بنا۔

```urdu
درآمد { کرل } سے "اردو/کرل"

متغیر http = نیا کرل({
    سرخط: { "Content-Type": "application/json" }
})

غیر_متزامن فنکشن نئی_پوسٹ_بنائیں() {
    متغیر پیغام = {
        title:  "اردو پروگرامنگ کا تعارف",
        body:   "یہ زبان اردو میں کوڈ لکھنے کی سہولت دیتی ہے۔",
        userId: 1
    };

    متغیر جواب = انتظار http.بھیجو(
        "https://jsonplaceholder.typicode.com/posts",
        ڈیٹا: پیغام
    );

    اگر (جواب.حالت == 201) {
        متغیر بنائی_گئی = جواب.جے_سون();
        لکھو("نئی پوسٹ ID:", بنائی_گئی.id);
    } ورنہ {
        لکھو("بنانے میں ناکامی، کوڈ:", جواب.حالت);
    }
}

انتظار نئی_پوسٹ_بنائیں();
```

### Example 4 — Authenticated API calls — تصدیق شدہ API کالز

> **اردو:** تصدیق شدہ API کالز کے لیے ٹوکن کو پہلے سے طے شدہ سرخیوں میں `Authorization` کے طور پر رکھیں۔ پھر تمام درخواستیں خودبخود یہ سرخی لے جائیں گی۔

```urdu
درآمد { کرل } سے "اردو/کرل"

مستقل ٹوکن = "Bearer ghp_xxxxxxxxxxxxxxxxxxxx"

متغیر http = نیا کرل({
    بنیادی_url: "https://api.github.com",
    سرخط: {
        "Authorization": ٹوکن,
        "Accept": "application/vnd.github+json"
    }
})

غیر_متزامن فنکشن صارف_معلومات() {
    متغیر جواب = انتظار http.حاصل("/user");
    متغیر صارف = جواب.جے_سون();
    لکھو("صارف نام:", صارف.login);
    لکھو("نام:",      صارف.name);
    لکھو("ای میل:",  صارف.email);
}

غیر_متزامن فنکشن ذخیرے_دیکھیں() {
    متغیر جواب = انتظار http.حاصل("/user/repos", پیرامیٹر: { per_page: 10 });
    کے_لیے (متغیر ذخیرہ کا جواب.جے_سون()) {
        لکھو(`  📁 ${ذخیرہ.full_name} (${ذخیرہ.stargazers_count} ستارے)`);
    }
}

انتظار صارف_معلومات();
انتظار ذخیرے_دیکھیں();
```

### Example 5 — File upload — فائل اپلوڈ

> **اردو:** فائل اپلوڈ کرنے کے لیے `http.فائل_بھیجو()` استعمال کریں۔ فائل کا راستہ، خانے کا نام اور اضافی ڈیٹا دیں۔ ختمی مدت `60` سیکنڈ رکھیں کیونکہ بڑی فائلیں زیادہ وقت لیتی ہیں۔

```urdu
درآمد { کرل } سے "اردو/کرل"

متغیر http = نیا کرل({ ختمی: 60 })

غیر_متزامن فنکشن تصویر_اپلوڈ(فائل_راستہ) {
    لکھو("فائل اپلوڈ ہو رہی ہے:", فائل_راستہ);

    متغیر جواب = انتظار http.فائل_بھیجو(
        "https://api.example.com/upload",
        فائل_راستہ,
        خانہ: "image",
        اضافی_ڈیٹا: { عنوان: "میری تصویر", الگورتھم: "اردو" }
    );

    اگر (جواب.ٹھیک) {
        متغیر نتیجہ = جواب.جے_سون();
        لکھو("اپلوڈ کامیاب!");
        لکھو("URL:", نتیجہ.url);
    } ورنہ {
        لکھو("اپلوڈ ناکام:", جواب.حالت, جواب.متن);
    }
}

انتظار تصویر_اپلوڈ("تصاویر/پروفائل.jpg");
```

### Example 6 — Full REST API CRUD — مکمل REST API CRUD

> **اردو:** یہ مثال مکمل CRUD عمل دکھاتی ہے: `بھیجو` سے بنانا، `حاصل` سے پڑھنا، `جزوی_تازہ` سے جزوی تازہ کاری اور `مٹاؤ` سے حذف کرنا — سب `بنیادی_url` کے ساتھ مختصر راستوں پر۔

```urdu
درآمد { کرل } سے "اردو/کرل"

// ═══════════════════════════════════════════════
// REST API — Todo فہرست کا مکمل انتظام
// ═══════════════════════════════════════════════

مستقل API = "https://jsonplaceholder.typicode.com"

متغیر http = نیا کرل({
    بنیادی_url: API,
    سرخط: { "Content-Type": "application/json" }
})

// CREATE — نئی todo شامل کریں
غیر_متزامن فنکشن todo_بنائیں(عنوان) {
    متغیر جواب = انتظار http.بھیجو("/todos", ڈیٹا: {
        title:     عنوان,
        completed: جھوٹ,
        userId:    1
    });
    متغیر todo = جواب.جے_سون();
    لکھو("بنائی گئی todo ID:", todo.id);
    واپس todo;
}

// READ — تمام todos پڑھیں
غیر_متزامن فنکشن todos_پڑھیں() {
    متغیر جواب = انتظار http.حاصل("/todos", پیرامیٹر: { _limit: 5 });
    کے_لیے (متغیر todo کا جواب.جے_سون()) {
        متغیر علامت = todo.completed ? "✓" : "○";
        لکھو(`  ${علامت} [${todo.id}] ${todo.title}`);
    }
}

// UPDATE — todo مکمل کریں
غیر_متزامن فنکشن todo_مکمل_کریں(id) {
    متغیر جواب = انتظار http.جزوی_تازہ(`/todos/${id}`, ڈیٹا: {
        completed: سچ
    });
    متغیر todo = جواب.جے_سون();
    لکھو(`Todo ${id} مکمل:`, todo.completed);
}

// DELETE — todo مٹائیں
غیر_متزامن فنکشن todo_مٹائیں(id) {
    متغیر جواب = انتظار http.مٹاؤ(`/todos/${id}`);
    اگر (جواب.ٹھیک) {
        لکھو(`Todo ${id} مٹا دیا گیا`);
    } ورنہ {
        لکھو("مٹانے میں ناکامی");
    }
}

// ── چلائیں ──────────────────────────────────

غیر_متزامن فنکشن مرکزی() {
    لکھو("=== Todo مینیجر ===\n");

    لکھو("موجودہ todos:");
    انتظار todos_پڑھیں();

    لکھو("\nنئی todo بنا رہے ہیں...");
    متغیر نئی = انتظار todo_بنائیں("اردو پروگرامنگ سیکھنا");

    لکھو("\nTodo مکمل کر رہے ہیں...");
    انتظار todo_مکمل_کریں(1);

    لکھو("\nTodo مٹا رہے ہیں...");
    انتظار todo_مٹائیں(2);
}

انتظار مرکزی();
```

### Example 7 — Parallel requests — متوازی درخواستیں

> **اردو:** `Promise.all([...])` سے متعدد درخواستیں بیک وقت بھیجیں۔ یہ ترتیب وار بھیجنے سے بہت تیز ہے — تمام درخواستیں ایک ساتھ چلتی ہیں اور سب کا انتظار ایک بار ہوتا ہے۔

```urdu
درآمد { کرل } سے "اردو/کرل"

متغیر http = نیا کرل()

غیر_متزامن فنکشن ڈیٹا_اکٹھا_کریں() {
    // تمام درخواستیں بیک وقت بھیجیں
    متغیر [صارفین_ج, پوسٹس_ج, تبصرے_ج] = انتظار Promise.all([
        http.حاصل("https://jsonplaceholder.typicode.com/users"),
        http.حاصل("https://jsonplaceholder.typicode.com/posts?_limit=5"),
        http.حاصل("https://jsonplaceholder.typicode.com/comments?_limit=3")
    ]);

    لکھو("صارفین:",  صارفین_ج.جے_سون().length);
    لکھو("پوسٹیں:", پوسٹس_ج.جے_سون().length);
    لکھو("تبصرے:",  تبصرے_ج.جے_سون().length);
}

انتظار ڈیٹا_اکٹھا_کریں();
```

### Example 8 — Error handling — غلطی ہینڈلنگ

> **اردو:** درخواست میں غلطیاں `کوشش/پکڑو` سے سنبھالیں۔ `.حالت == 404` سے نہ ملنے کی جانچ کریں، `.ٹھیک` سے کامیابی جانچیں اور `timeout` غلطی کو علیحدہ پکڑیں۔ یہ نمونہ محفوظ اور مضبوط HTTP کالز کا بہترین طریقہ ہے۔

```urdu
درآمد { کرل } سے "اردو/کرل"

متغیر http = نیا کرل({ ختمی: 5 })

غیر_متزامن فنکشن محفوظ_درخواست(url) {
    کوشش {
        متغیر جواب = انتظار http.حاصل(url);

        اگر (جواب.حالت == 404) {
            لکھو("صفحہ نہیں ملا:", url);
            واپس خالی;
        }

        اگر (نہیں (جواب.ٹھیک)) {
            لکھو(`HTTP غلطی ${جواب.حالت}:`, جواب.متن);
            واپس خالی;
        }

        واپس جواب.جے_سون();

    } پکڑو (غلطی) {
        اگر (غلطی.message.includes("timeout")) {
            لکھو("مدت ختم — سرور جواب نہیں دے رہا");
        } ورنہ {
            لکھو("نیٹ ورک غلطی:", غلطی.message);
        }
        واپس خالی;
    }
}

متغیر نتیجہ = انتظار محفوظ_درخواست("https://httpstat.us/404");
لکھو("نتیجہ:", نتیجہ);
```

---

*Previous: [ML →](ml.md) | Next: [Web Scraper →](scraper.md)*
