# 3. HTTP Client — کرل

**Difficulty:** Advanced — اعلیٰ  
**Time:** ~25 minutes

---

## Importing — درآمد

```urdu
درآمد { کرل, کرل_حاصل, بھیجو_کرو, تازہ_کرو, جزوی_تازہ_کرو, مٹاؤ_کرو } سے "اردو/کرل";
```

> **اردو:** `کرل` HTTP مؤکل ہے۔ تمام طریقے `غیر_متزامن` (async) ہیں — `انتظار` کے ساتھ استعمال کریں۔

---

## GET Request — ڈیٹا حاصل کریں

All HTTP methods are **async** — they must be called inside an `async` function with `انتظار`:

```urdu
غیر_متزامن فنکشن مرکزی() {
    متغیر جواب = انتظار کرل_حاصل("https://httpbin.org/get");
    لکھو(جواب.حالت);    // 200
    لکھو(جواب.ٹھیک);    // True  (2xx = success)
    لکھو(جواب.متن);     // full response body
}

انتظار مرکزی();
```

**With query params — پیرامیٹر کے ساتھ:**

```urdu
غیر_متزامن فنکشن مرکزی() {
    متغیر جواب = انتظار کرل_حاصل(
        "https://httpbin.org/get",
        پیرامیٹر={ q: "اردو", صفحہ: 1 }
    );
    لکھو(جواب.حالت);    // 200
    لکھو(جواب.ربط);     // shows full URL with query string
}

انتظار مرکزی();
```

---

## Response Properties — جواب کی خصوصیات

| Property | Type | Description |
|----------|------|-------------|
| `.حالت` | int | HTTP status code (200, 404, …) |
| `.ٹھیک` | bool | `سچ` if status < 400 |
| `.متن` | str | Response body as text |
| `.مواد` | bytes | Response body as raw bytes |
| `.سرخط` | dict | Response headers |
| `.ربط` | str | Final URL (after redirects) |
| `.جے_سون()` | obj/list | Parse JSON body |

---

## JSON API Calls — جے سان API

```urdu
غیر_متزامن فنکشن صارف_حاصل(شناخت) {
    متغیر جواب = انتظار کرل_حاصل(
        `https://jsonplaceholder.typicode.com/users/${شناخت}`
    );
    اگر (نہیں جواب.ٹھیک) {
        لکھو(`غلطی: ${جواب.حالت}`);
        واپس خالی;
    }
    متغیر ڈیٹا = جواب.جے_سون();
    لکھو(`نام: ${ڈیٹا.name}`);
    لکھو(`ای میل: ${ڈیٹا.email}`);
    واپس ڈیٹا;
}

انتظار صارف_حاصل(1);
```

---

## POST Request — ڈیٹا بھیجیں

Pass a dict — it's automatically sent as JSON:

```urdu
غیر_متزامن فنکشن نئی_پوسٹ_بنائیں() {
    متغیر جواب = انتظار بھیجو_کرو(
        "https://jsonplaceholder.typicode.com/posts",
        { عنوان: "اردو ٹیسٹ", مواد: "یہ ایک پوسٹ ہے", userId: 1 }
    );
    لکھو(جواب.حالت);      // 201
    لکھو(جواب.جے_سون());
}

انتظار نئی_پوسٹ_بنائیں();
```

---

## PUT and PATCH — تازہ کاری

```urdu
غیر_متزامن فنکشن تازہ_کاری() {
    // Full replace (PUT)
    متغیر جواب_پ = انتظار تازہ_کرو(
        "https://jsonplaceholder.typicode.com/posts/1",
        { عنوان: "نیا عنوان", مواد: "نیا مواد", userId: 1 }
    );
    لکھو(جواب_پ.حالت);    // 200

    // Partial update (PATCH)
    متغیر جواب_ج = انتظار جزوی_تازہ_کرو(
        "https://jsonplaceholder.typicode.com/posts/1",
        { عنوان: "صرف عنوان بدلا" }
    );
    لکھو(جواب_ج.حالت);    // 200
}

انتظار تازہ_کاری();
```

---

## DELETE Request — حذف کریں

```urdu
غیر_متزامن فنکشن حذف_کریں(شناخت) {
    متغیر جواب = انتظار مٹاؤ_کرو(
        `https://jsonplaceholder.typicode.com/posts/${شناخت}`
    );
    لکھو(جواب.حالت);      // 200
    لکھو(جواب.ٹھیک);      // True
}

انتظار حذف_کریں(1);
```

---

## کرل Class — Advanced Use

For multiple requests, create a `کرل` instance to share headers, auth, and base URL:

```urdu
متغیر کلائنٹ = نیا کرل({
    بنیادی_url: "https://api.example.com",
    سرخط: { "Content-Type": "application/json" },
    ختمی: 15
});

غیر_متزامن فنکشن استعمال() {
    متغیر جواب = انتظار کلائنٹ.حاصل("/users");
    لکھو(جواب.حالت);
    کلائنٹ.سیشن_بند();
}

انتظار استعمال();
```

### Authentication — توثیق

```urdu
// Bearer token
کلائنٹ.ٹوکن_مقرر("your-jwt-token-here");

// Basic auth
کلائنٹ.بنیادی_توثیق("صارف_نام", "پاس_ورڈ");

// API key header
کلائنٹ.کلید_توثیق("X-API-Key", "your-api-key");

// Custom header
کلائنٹ.سرخط_مقرر("Accept", "application/json");
```

### Custom Headers Per Request — درخواست کے مخصوص سرخط

```urdu
غیر_متزامن فنکشن مرکزی() {
    متغیر جواب = انتظار کلائنٹ.حاصل(
        "/data",
        سرخط={ "X-Request-ID": "abc123" }
    );
    لکھو(جواب.حالت);
}

انتظار مرکزی();
```

---

## File Upload & Download — فائل اپلوڈ و ڈاؤن لوڈ

```urdu
// Upload
غیر_متزامن فنکشن اپلوڈ() {
    متغیر جواب = انتظار کلائنٹ.فائل_بھیجو(
        "/upload",
        "تصویر.png",
        خانہ="image"
    );
    لکھو(جواب.حالت);
}

// Download
غیر_متزامن فنکشن ڈاؤن لوڈ() {
    متغیر جواب = انتظار کلائنٹ.فائل_حاصل(
        "/report.pdf",
        "رپورٹ.pdf"
    );
    لکھو(`محفوظ ہوگیا: ${جواب.ٹھیک}`);
}

انتظار اپلوڈ();
انتظار ڈاؤن لوڈ();
```

---

## Practical Example: JSON API Client — عملی مثال

```urdu
درآمد { کرل } سے "اردو/کرل";

متغیر API = نیا کرل({ بنیادی_url: "https://jsonplaceholder.typicode.com" });

غیر_متزامن فنکشن پوسٹیں_حاصل(صفحہ = 1) {
    متغیر جواب = انتظار API.حاصل("/posts", پیرامیٹر={ _page: صفحہ, _limit: 5 });
    اگر (نہیں جواب.ٹھیک) {
        پھینکو نیا غلطی(`HTTP ${جواب.حالت}`);
    }
    واپس جواب.جے_سون();
}

غیر_متزامن فنکشن مرکزی() {
    کوشش {
        متغیر پوسٹیں = انتظار پوسٹیں_حاصل(1);
        کے_لیے (متغیر پوسٹ میں پوسٹیں) {
            لکھو(`[${پوسٹ.id}] ${پوسٹ.title}`);
        }
    } پکڑو (غلطی_م) {
        لکھو(`غلطی: ${غلطی_م.message}`);
    } آخر {
        API.سیشن_بند();
    }
}

انتظار مرکزی();
```

---

## Quick Reference — فوری حوالہ

| Function / Method | Description |
|-------------------|-------------|
| `کرل_حاصل(url, پیرامیٹر=)` | Quick GET |
| `بھیجو_کرو(url, ڈیٹا)` | Quick POST with JSON body |
| `تازہ_کرو(url, ڈیٹا)` | Quick PUT |
| `جزوی_تازہ_کرو(url, ڈیٹا)` | Quick PATCH |
| `مٹاؤ_کرو(url)` | Quick DELETE |
| `کرل.حاصل(url)` | GET on instance |
| `کرل.بھیجو(url, dict)` | POST JSON on instance |
| `کرل.فائل_بھیجو(url, path)` | Multipart file upload |
| `کرل.فائل_حاصل(url, path)` | Stream download to file |
| `کرل.ٹوکن_مقرر(token)` | Set Bearer token |
| `کرل.بنیادی_توثیق(u, p)` | Set Basic auth |
| `کرل.سیشن_بند()` | Close session |

---

[← Previous: Algorithms](02-algorithms.md) | [Next: Cryptography →](04-cryptography.md)
