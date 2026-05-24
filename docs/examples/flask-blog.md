# Flask Blog App — اردو بلاگ

A complete multi-page blog application built with Flask. Demonstrates HTML responses, form handling, GET/POST routes, in-memory data storage, and RTL Urdu UI.

> **اردو:** Flask سے بنی ایک مکمل بلاگ ایپلیکیشن۔ یہ مثال HTML جوابات، فارم ہینڈلنگ، GET/POST راستے، ان میموری ڈیٹا اسٹوریج، اور اردو RTL UI ظاہر کرتی ہے۔

---

## چلانے کا طریقہ / How to Run

```bash
pip install flask
cd examples/FLASK_BLOG_App
urdu run app.urdu
```

Then open: **http://localhost:5000**

---

## Features

| Feature | Description |
|---------|-------------|
| Home page | Lists all posts with 3-line excerpt (CSS clamp) |
| Post detail | Full post view at `/پوسٹ/<id>` |
| New post form | Write and publish a post at `/نئی_پوسٹ` |
| In-memory storage | Posts stored in a list — resets on restart |
| RTL Urdu UI | Full right-to-left layout with Urdu CSS class names |

---

## Code Walkthrough

### 1. Imports and App Setup

```urdu
درآمد { فلاسک, فلاسک_جواب, فلاسک_رجوع } سے "اردو/ویب";
درآمد { فلاسک_درخواست } سے "اردو/ویب";

متغیر ایپ = نیا فلاسک();
```

- `فلاسک` — Flask app wrapper
- `فلاسک_جواب(html, status, mime)` — build a custom HTTP response
- `فلاسک_رجوع(url)` — HTTP redirect (302)
- `فلاسک_درخواست()` — returns the current Flask request object (for form data, query params)

---

### 2. In-Memory Data Store

```urdu
// شمار کو dict میں رکھا تاکہ فنکشن میں بھی تبدیل ہو
متغیر حالت = { "اگلا": 1 };
متغیر پوسٹیں = [];

فنکشن پوسٹ_شامل(عنوان, متن, مصنف) {
    متغیر شناخت = حالت["اگلا"];
    پوسٹیں.append({ "شناخت": شناخت, "عنوان": عنوان, "متن": متن, "مصنف": مصنف });
    حالت["اگلا"] = حالت["اگلا"] + 1;
}
```

**Why a dict for the counter?**  
Inside a function, assigning to a plain variable (`اگلا = اگلا + 1`) would create a local variable and not update the global. Mutating a dict value (`حالت["اگلا"] = ...`) modifies the global dict in-place — no `global` keyword needed.

**Why `list.append()`?**  
Urdu PL transpiles to Python, so all Python list and dict methods work directly on runtime objects.

---

### 3. Base HTML Layout Function

```urdu
متغیر طرز = `<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { direction: rtl; ... }
  .کارڈ { border-right: 4px solid #e74c3c; ... }
  ...
</style>`;

فنکشن بیس(عنوان_صفحہ, مواد) {
    واپس `<!DOCTYPE html>
<html dir="rtl" lang="ur">
<head>
  <title>${عنوان_صفحہ} — اردو بلاگ</title>
  ${طرز}
</head>
<body>
  <nav>...</nav>
  <div class="کنٹینر">${مواد}</div>
</body>
</html>`;
}
```

**Key points:**
- Template literals (backtick strings) support multi-line HTML
- `${variable}` is the interpolation syntax
- CSS `{` and `}` characters are handled automatically by the transpiler
- `dir="rtl"` and `direction: rtl` for right-to-left Urdu text
- Urdu words are valid CSS class names (`.کارڈ`, `.بٹن`, `.میٹا`)

---

### 4. Home Page Route

```urdu
@ایپ.حاصل("/")
فنکشن گھر() {
    متغیر کارڈز = "";
    کے_لیے (متغیر پ کا پوسٹیں) {
        متغیر شناخت = پ["شناخت"];
        متغیر عنوان = پ["عنوان"];
        متغیر مصنف = پ["مصنف"];
        متغیر خلاصہ = پ["متن"];
        کارڈز = کارڈز + `<div class="کارڈ">
  <h2><a href="/پوسٹ/${شناخت}">${عنوان}</a></h2>
  <div class="میٹا">✍ ${مصنف}</div>
  <p class="متن">${خلاصہ}</p>
  <a href="/پوسٹ/${شناخت}" class="بٹن">مزید پڑھیں</a>
</div>`;
    }
    متغیر مواد = `<h1>تازہ پوسٹیں</h1>${کارڈز}`;
    واپس فلاسک_جواب(بیس("گھر", مواد), 200, "text/html; charset=utf-8");
}
```

**Excerpt truncation:** Instead of string slicing (Urdu PL's parser does not support `[start:end]` slice notation), the CSS property `-webkit-line-clamp: 3` is used to visually truncate long posts to 3 lines with an ellipsis.

---

### 5. Post Detail Route

```urdu
@ایپ.حاصل("/پوسٹ/<pid>")
فنکشن پوسٹ_دیکھیں(pid) {
    متغیر نمبر = int(pid);
    متغیر ملی = جھوٹ;
    متغیر پ_عنوان = "";
    متغیر پ_متن = "";
    متغیر پ_مصنف = "";
    کے_لیے (متغیر پ کا پوسٹیں) {
        اگر (پ["شناخت"] == نمبر) {
            پ_عنوان = پ["عنوان"];
            پ_متن = پ["متن"];
            پ_مصنف = پ["مصنف"];
            ملی = سچ;
        }
    }
    اگر (ملی == جھوٹ) {
        واپس فلاسک_جواب(بیس("غلطی", مواد_خطا), 404, "text/html; charset=utf-8");
    }
    ...
}
```

**Important:** Flask's URL route parameters must use ASCII names (e.g. `<pid>`). Urdu characters inside `< >` cause a Werkzeug "malformed url rule" error. The ASCII parameter is then used normally inside the function body.

---

### 6. New Post: GET Form + POST Save

```urdu
// ─── فارم دکھائیں ─────────────────────────────────
@ایپ.حاصل("/نئی_پوسٹ")
فنکشن نئی_فارم() {
    متغیر مواد = `<form method="POST" action="/نئی_پوسٹ" class="فارم">
    <label for="عنوان">عنوان</label>
    <input type="text" name="عنوان" required />
    <label for="متن">پوسٹ</label>
    <textarea name="متن" required></textarea>
    <button type="submit" class="بٹن">شائع کریں</button>
</form>`;
    واپس فلاسک_جواب(بیس("نئی پوسٹ", مواد), 200, "text/html; charset=utf-8");
}

// ─── فارم محفوظ کریں ──────────────────────────────
@ایپ.بھیجیں("/نئی_پوسٹ")
فنکشن نئی_محفوظ() {
    متغیر درخواست = فلاسک_درخواست();
    متغیر عنوان = درخواست.form.get("عنوان", "بے عنوان");
    متغیر متن   = درخواست.form.get("متن", "");
    متغیر مصنف  = درخواست.form.get("مصنف", "گمنام");
    اگر (len(متن) > 0) {
        پوسٹ_شامل(عنوان, متن, مصنف);
    }
    واپس فلاسک_رجوع("/");
}
```

- `@ایپ.حاصل` → GET route
- `@ایپ.بھیجیں` → POST route
- `فلاسک_درخواست()` returns Flask's `request` proxy; `.form.get(key, default)` reads submitted form fields
- `فلاسک_رجوع("/")` redirects back to the home page after saving

---

### 7. Run the Server

```urdu
ایپ.چلائیں(پورٹ=5000, ڈیبگ=جھوٹ);
```

`ڈیبگ=جھوٹ` disables Flask's debug/reloader. Set `ڈیبگ=سچ` during development to see errors in the browser.

---

## Known Limitations

| Limitation | Reason | Workaround |
|------------|--------|------------|
| Slice notation `[0:130]` unsupported | Urdu PL parser treats `:` inside `[]` as syntax error | Use CSS `-webkit-line-clamp` for visual truncation |
| URL route params must be ASCII | Werkzeug rejects non-ASCII inside `< >` | Use `<pid>`, `<id>`, etc. |
| No persistence | In-memory storage only | Integrate `اردو/ڈیٹا_بیس` for SQLite/PostgreSQL |

---

## File Structure

```
examples/FLASK_BLOG_App/
  app.urdu     ← main application (this file)
```

---

## Next Steps

- Add a delete post route (`@ایپ.بھیجیں("/حذف/<pid>")`)
- Connect to a real database using `اردو/ڈیٹا_بیس`
- Add user authentication with sessions (`فلاسک_نشست`)
- Move HTML to Jinja2 templates using `فلاسک_سانچہ`
