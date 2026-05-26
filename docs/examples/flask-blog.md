# Flask Blog App — اردو بلاگ

A complete multi-page blog application built with Flask and Urdu Jinja2 templates. Demonstrates template inheritance, Urdu template keywords, form handling, GET/POST routes, and RTL Urdu UI.

> **اردو:** Flask اور اردو Jinja2 سانچوں سے بنی ایک مکمل بلاگ ایپلیکیشن۔ یہ مثال سانچہ وراثت، اردو ٹیگ کلیدی الفاظ، فارم ہینڈلنگ، GET/POST راستے اور اردو RTL UI ظاہر کرتی ہے۔

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
| Urdu Jinja2 templates | All `.html` files use Urdu tag keywords (`{% اگر %}`, `{% کے_لیے %}`, `{% توسیع %}`) |
| Template inheritance | `گھر.html`, `پوسٹ.html`, `نئی_پوسٹ.html` all extend `بنیاد.html` |
| Home page | Lists all posts with 3-line excerpt (CSS clamp) and post count via `\|طول` filter |
| Post detail | Full post view at `/پوسٹ/<id>` |
| New post form | Write and publish a post at `/نئی_پوسٹ` |
| In-memory storage | Posts stored in a list — resets on restart |
| RTL Urdu UI | Full right-to-left layout with Urdu CSS class names |

---

## File Structure

```
examples/FLASK_BLOG_App/
  app.urdu                ← main application
  templates/
    بنیاد.html            ← base layout (nav, CSS)
    گھر.html              ← home page: list all posts
    پوسٹ.html             ← single post view
    نئی_پوسٹ.html         ← new post form
```

---

## Code Walkthrough

### 1. Imports and App Setup

```urdu
درآمد { فلاسک, فلاسک_سانچہ, فلاسک_جواب, فلاسک_رجوع } سے "اردو/ویب";
درآمد { فلاسک_درخواست } سے "اردو/ویب";

متغیر ایپ = نیا فلاسک();
```

- `فلاسک` — Flask app wrapper; automatically enables Urdu Jinja2 template preprocessing
- `فلاسک_سانچہ(template, **ctx)` — render a Jinja2 template from `templates/`
- `فلاسک_رجوع(url)` — HTTP redirect (302)
- `فلاسک_درخواست()` — returns the current Flask request object

---

### 2. In-Memory Data Store

```urdu
متغیر حالت = { "اگلا": 1 };
متغیر پوسٹیں = [];

فنکشن پوسٹ_شامل(عنوان, متن, مصنف) {
    متغیر شناخت = حالت["اگلا"];
    پوسٹیں.append({ "شناخت": شناخت, "عنوان": عنوان, "متن": متن, "مصنف": مصنف });
    حالت["اگلا"] = حالت["اگلا"] + 1;
}
```

**Why a dict for the counter?** Inside a function, assigning to a plain variable creates a local copy. Mutating a dict value (`حالت["اگلا"] = ...`) modifies the global dict in-place — no `global` keyword needed.

---

### 3. Base Template — `بنیاد.html`

```html
<!DOCTYPE html>
<html dir="rtl" lang="ur">
<head>
  <title>{% بلاک عنوان %}اردو بلاگ{% بلاک_ختم %}</title>
  <style>
    body { direction: rtl; }
    .کارڈ { border-right: 4px solid #e74c3c; }
    ...
  </style>
</head>
<body>
<nav>
  <span class="لوگو">اردو بلاگ</span>
  <a href="/">گھر</a>
  <a href="/نئی_پوسٹ">+ نئی پوسٹ</a>
</nav>
<div class="کنٹینر">
  {% بلاک مواد %}{% بلاک_ختم %}
</div>
</body>
</html>
```

- `{% بلاک عنوان %}` / `{% بلاک مواد %}` — named blocks that child templates override
- `{% بلاک_ختم %}` — closes a block (`{% endblock %}`)
- Urdu words are valid CSS class names (`.کارڈ`, `.لوگو`, `.کنٹینر`)

---

### 4. Home Template — `گھر.html`

```html
{% توسیع "بنیاد.html" %}
{% بلاک عنوان %}گھر — اردو بلاگ{% بلاک_ختم %}

{% بلاک مواد %}
<h1>تازہ پوسٹیں</h1>

{% اگر پوسٹیں %}
<p class="شمار">کل {{ پوسٹیں|طول }} پوسٹیں</p>

{% کے_لیے پ کا پوسٹیں %}
<div class="کارڈ">
  <h2><a href="/پوسٹ/{{ پ.شناخت }}">{{ پ.عنوان }}</a></h2>
  <div class="میٹا">✍ {{ پ.مصنف }}</div>
  <p class="متن">{{ پ.متن }}</p>
  <a href="/پوسٹ/{{ پ.شناخت }}" class="بٹن">مزید پڑھیں</a>
</div>
{% کے_لیے_ختم %}

{% ورنہ %}
<div class="خالی">
  <p>ابھی کوئی پوسٹ نہیں۔</p>
  <a href="/نئی_پوسٹ" class="بٹن">پہلی پوسٹ لکھیں</a>
</div>
{% اگر_ختم %}
{% بلاک_ختم %}
```

**Key Urdu template keywords used:**

| کلیدی لفظ | کام |
|-----------|-----|
| `{% توسیع "..." %}` | inherit from base template |
| `{% بلاک نام %}` | define/override a named block |
| `{% بلاک_ختم %}` | end a block |
| `{% اگر پوسٹیں %}` | conditional — truthy check |
| `{% ورنہ %}` | else branch |
| `{% اگر_ختم %}` | end if |
| `{% کے_لیے پ کا پوسٹیں %}` | for loop |
| `{% کے_لیے_ختم %}` | end for |
| `{{ پوسٹیں\|طول }}` | `length` filter |

---

### 5. Route Handlers

```urdu
// گھر — تمام پوسٹیں
@ایپ.حاصل("/")
فنکشن گھر() {
    واپس فلاسک_سانچہ("گھر.html", پوسٹیں=پوسٹیں);
}

// پوسٹ دیکھیں
@ایپ.حاصل("/پوسٹ/<pid>")
فنکشن پوسٹ_دیکھیں(pid) {
    متغیر نمبر = int(pid);
    متغیر پوسٹ = خالی;
    کے_لیے (متغیر پ کا پوسٹیں) {
        اگر (پ["شناخت"] == نمبر) {
            پوسٹ = پ;
        }
    }
    اگر (پوسٹ == خالی) {
        واپس فلاسک_جواب("پوسٹ نہیں ملی", 404, "text/plain; charset=utf-8");
    }
    واپس فلاسک_سانچہ("پوسٹ.html", پوسٹ=پوسٹ);
}

// نئی پوسٹ فارم
@ایپ.حاصل("/نئی_پوسٹ")
فنکشن نئی_فارم() {
    واپس فلاسک_سانچہ("نئی_پوسٹ.html");
}

// نئی پوسٹ محفوظ
@ایپ.بھیجیں("/نئی_پوسٹ")
فنکشن نئی_محفوظ() {
    متغیر درخواست = فلاسک_درخواست();
    متغیر عنوان = درخواست.form.get("عنوان", "بے عنوان");
    متغیر متن = درخواست.form.get("متن", "");
    متغیر مصنف = درخواست.form.get("مصنف", "گمنام");
    اگر (len(متن) > 0) {
        پوسٹ_شامل(عنوان, متن, مصنف);
    }
    واپس فلاسک_رجوع("/");
}
```

- `فلاسک_سانچہ("گھر.html", پوسٹیں=پوسٹیں)` — renders `templates/گھر.html`; keyword arguments become template variables
- `فلاسک_درخواست().form.get(key, default)` — reads submitted form fields
- Flask URL route params must use ASCII names (e.g. `<pid>`); Urdu inside `< >` causes a Werkzeug error

---

### 6. Run the Server

```urdu
ایپ.چلائیں(پورٹ=5000, ڈیبگ=جھوٹ);
```

`ڈیبگ=سچ` enables Flask's auto-reloader and error pages in the browser.

---

## Known Limitations

| Limitation | Reason | Workaround |
|------------|--------|------------|
| URL route params must be ASCII | Werkzeug rejects non-ASCII inside `< >` | Use `<pid>`, `<id>`, etc. |
| No persistence | In-memory storage only | Integrate `اردو/ڈیٹا_بیس` for SQLite |
| Template files use `.html` extension | Jinja2 finds files by name | Name templates with Urdu filenames — both work |

---

## Next Steps

- Add a delete post route (`@ایپ.بھیجیں("/حذف/<pid>")`)
- Connect to a real database using `اردو/ڈیٹا_بیس`
- Add user authentication with sessions (`فلاسک_نشست`)
- Add pagination using `لوپ.اشاریہ` and Jinja2 slice filters
