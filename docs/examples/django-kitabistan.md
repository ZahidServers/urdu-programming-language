# Django Kitabistan App — اردو کتابستان

A complete Django web application demonstrating the full ORM stack: two related models, CRUD views, search, form handling, a JSON API, middleware, and redirect — all in a single `.urdu` file with Urdu-keyword HTML templates.

> **اردو:** Django ORM کی مکمل مثال — دو ماڈل (ناشر + کتاب)، CRUD آپریشن، تلاش، فارم، JSON API، درمیانی پرت اور ری ڈائریکٹ — ایک `.urdu` فائل میں۔

---

## چلانے کا طریقہ / How to Run

```bash
pip install django
cd examples/DJANGO_KITABISTAN_APP
urdu run app.urdu
```

Then open: **http://localhost:8000**

---

## Features

| Feature | Description |
|---------|-------------|
| Django ORM models | `ناشر` (Publisher) and `کتاب` (Book) with FK relation |
| Auto table creation | `ایپ.میزیں_بنائیں()` creates tables on first run |
| Seed data guard | Sample data inserted only when DB is empty |
| CRUD — Books | List, search, create, edit, delete (`/کتابیں/`) |
| CRUD — Publishers | List, add, delete (`/ناشرین/`) |
| Search | `?q=` query param — filters by title using `icontains` |
| JSON API | `/api/کتابیں/`, `/api/ناشرین/`, `/api/کتاب/<id>/` |
| Redirect | `ڈجانگو_رجوع` after POST — PRG pattern |
| Middleware | `درخواست_لاگ` logs every request method + path |
| Urdu templates | All 4 templates use Urdu block/for/if keywords |
| File-based SQLite | Persists across server restarts (`کتابستان.db`) |

---

## File Structure

```
examples/DJANGO_KITABISTAN_APP/
  app.urdu               ← models, views, URLs, server (single file)
  کتابستان.db            ← SQLite database (auto-created on first run)
  templates/
    بنیاد.html           ← base layout (RTL CSS, navigation)
    گھر.html             ← home page with summary stats
    کتابیں.html          ← books list with search
    کتاب_فارم.html       ← new / edit book form
    ناشرین.html          ← publishers list + inline add form
```

---

## Code Walkthrough

### 1. Imports and App Setup

```urdu
درآمد {
    ڈجانگو, ڈجانگو_سانچہ, ڈجانگو_درمیانی,
    ڈجانگو_جواب, ڈجانگو_جیسن, ڈجانگو_رجوع,
    ڈجانگو_ماڈل,
    متن_خانہ, عدد_خانہ, اعشاریہ_خانہ, بولین_خانہ, غیر_ملکی_کلید,
    سب_حاصل, فلٹر, ایک_حاصل, بنائیں, حذف_کریں
} سے "اردو/ویب";

متغیر _بنیاد = os.path.dirname(os.path.abspath(__file__));

متغیر ایپ = نیا ڈجانگو({
    "ڈیٹا_بیس": `${_بنیاد}/کتابستان.db`,
    "ڈیبگ": سچ,
    "سانچہ_فولڈر": [`${_بنیاد}/templates`]
});
ایپ.ترتیب_دیں();
```

`"ڈیٹا_بیس"` accepts a SQLite file path string directly — it is passed as Django's `DATABASES["default"]["NAME"]`. Using a file path (instead of `:memory:`) means every HTTP request connection sees the same persisted data.

> **اردو:** `"ڈیٹا_بیس"` کو SQLite فائل راستہ دیں — `:memory:` استعمال نہ کریں کیونکہ ہر HTTP کنکشن ایک نئی `:memory:` DB کھولتا ہے اور جدول نہیں ملتے۔

---

### 2. ORM Models

```urdu
کلاس ناشر توسیع ڈجانگو_ماڈل {
    جامد نام  = متن_خانہ(100)
    جامد شہر  = متن_خانہ(80)
}

کلاس کتاب توسیع ڈجانگو_ماڈل {
    جامد عنوان       = متن_خانہ(200)
    جامد مصنف        = متن_خانہ(100)
    جامد قیمت        = اعشاریہ_خانہ(10, 2)
    جامد دستیاب      = بولین_خانہ(ڈیفالٹ=سچ)
    جامد ناشر_کتاب   = غیر_ملکی_کلید(ناشر, متعلقہ_نام="کتابیں")
}
```

**Key rules:**
- Extend `ڈجانگو_ماڈل` (not a plain `کلاس`).
- Declare every field as `جامد` — the Urdu transpiler emits class-level attributes, which is how Django's `ModelBase` metaclass discovers them.
- **Do not use `خالی=سچ`** in field constructors — `خالی` is a reserved word that transpiles to `None`, creating invalid syntax `متن_خانہ(None=True)`. Use the `اجازت=سچ` parameter instead.
- The `غیر_ملکی_کلید` `ON DELETE` behaviour defaults to `CASCADE`. Override with `حذف_پر=...` if needed.

After defining models, call:

```urdu
ایپ.میزیں_بنائیں();
```

This calls Django's schema editor to `CREATE TABLE IF NOT EXISTS` for each registered `ڈجانگو_ماڈل` subclass. Safe to call on every start — it skips tables that already exist.

---

### 3. Seed Data (first run only)

```urdu
اگر (سب_حاصل(ناشر).count() == 0) {
    متغیر ن1 = بنائیں(ناشر, نام="مکتبہ اردو", شہر="لاہور");
    بنائیں(کتاب, عنوان="آگ کا دریا", مصنف="قرۃ العین حیدر",
            قیمت=450, دستیاب=سچ, ناشر_کتاب=ن1);
    // ...
}
```

`بنائیں(Model, **kwargs)` wraps `Model.objects.create(**kwargs)`. The `count() == 0` guard prevents duplicate rows on server restart.

---

### 4. Middleware

```urdu
کلاس درخواست_لاگ توسیع ڈجانگو_درمیانی {
    قبل(req) {
        لکھو(`  ← ${req.method} ${req.path}`);
    }
    بعد(req, res) {
        واپس res;
    }
}
```

`ڈجانگو_درمیانی` provides a `قبل(req)` / `بعد(req, res)` interface. The class is auto-registered with Django's middleware stack — no extra wiring needed.

---

### 5. Views — List, Search, CRUD

**Home page:**

```urdu
فنکشن نظارہ_گھر(req) {
    واپس ڈجانگو_سانچہ(req, "گھر.html", {
        "کتب_تعداد":   سب_حاصل(کتاب).count(),
        "ناشر_تعداد":  سب_حاصل(ناشر).count(),
        "دستیاب_تعداد": فلٹر(کتاب, دستیاب=سچ).count()
    });
}
```

**Books list with search:**

```urdu
فنکشن نظارہ_کتابیں(req) {
    متغیر تلاش = req.GET.get("q", "");
    اگر (تلاش) {
        کتابیں_qs = کتاب.objects.filter(عنوان__icontains=تلاش);
    } ورنہ {
        کتابیں_qs = سب_حاصل(کتاب).select_related("ناشر_کتاب");
    }
    واپس ڈجانگو_سانچہ(req, "کتابیں.html", { "کتابیں": کتابیں_qs, "تلاش": تلاش });
}
```

`سب_حاصل(Model)` returns `Model.objects.all()`. For QuerySet methods beyond the Urdu helpers (`__icontains`, `select_related`, etc.), use Django's native `.objects.filter(...)` directly — the ORM object is a full Django QuerySet.

**Create (POST + redirect):**

```urdu
فنکشن نظارہ_کتاب_نئی(req) {
    اگر (req.method == "POST") {
        متغیر ن = ایک_حاصل(ناشر, id=عدد(req.POST.get("ناشر_id", 1)));
        بنائیں(کتاب,
            عنوان=req.POST.get("عنوان", ""),
            مصنف=req.POST.get("مصنف", ""),
            قیمت=اعشاریہ(req.POST.get("قیمت", "0")),
            دستیاب=(req.POST.get("دستیاب") == "on"),
            ناشر_کتاب=ن
        );
        واپس ڈجانگو_رجوع("/کتابیں/");
    }
    واپس ڈجانگو_سانچہ(req, "کتاب_فارم.html", {
        "عنوان": "نئی کتاب", "ناشرین": سب_حاصل(ناشر), "کتاب": {}
    });
}
```

`ڈجانگو_رجوع(url)` returns an `HttpResponseRedirect` — implements the Post/Redirect/Get pattern to prevent duplicate form submissions on browser refresh.

**Edit (fetch instance, update fields, save):**

```urdu
فنکشن نظارہ_کتاب_ترمیم(req, id) {
    متغیر ک = ایک_حاصل(کتاب, id=id);
    اگر (req.method == "POST") {
        ک.عنوان  = req.POST.get("عنوان", ک.عنوان);
        ک.قیمت   = اعشاریہ(req.POST.get("قیمت", متن(ک.قیمت)));
        ک.دستیاب = (req.POST.get("دستیاب") == "on");
        ک.save();
        واپس ڈجانگو_رجوع("/کتابیں/");
    }
    واپس ڈجانگو_سانچہ(req, "کتاب_فارم.html",
        { "عنوان": "ترمیم کریں", "ناشرین": سب_حاصل(ناشر), "کتاب": ک });
}
```

`ایک_حاصل(Model, **kwargs)` wraps `Model.objects.get(**kwargs)`. Edit the fields directly on the instance and call `.save()`.

**Delete:**

```urdu
فنکشن نظارہ_کتاب_حذف(req, id) {
    حذف_کریں(کتاب, id=id);
    واپس ڈجانگو_رجوع("/کتابیں/");
}
```

`حذف_کریں(Model, **kwargs)` looks up the object by the given kwargs and calls `.delete()`.

---

### 6. JSON API

```urdu
فنکشن api_کتابیں(req) {
    متغیر qs = سب_حاصل(کتاب).select_related("ناشر_کتاب");
    متغیر نتیجہ = [];
    کے_لیے (متغیر ک کا qs) {
        نتیجہ.شامل({
            "id": ک.id, "عنوان": ک.عنوان,
            "مصنف": ک.مصنف, "قیمت": متن(ک.قیمت),
            "دستیاب": ک.دستیاب, "ناشر": ک.ناشر_کتاب.نام
        });
    }
    واپس ڈجانگو_جیسن(نتیجہ);
}
```

`ڈجانگو_جیسن(data, status=200)` wraps Django's `JsonResponse`. Pass a list or dict and optionally a status code.

**Single-item with 404 fallback:**

```urdu
فنکشن api_کتاب_ایک(req, id) {
    کوشش {
        متغیر ک = ایک_حاصل(کتاب, id=id);
        واپس ڈجانگو_جیسن({ ... });
    } پکڑو (غ) {
        واپس ڈجانگو_جیسن({ "خطا": "کتاب نہیں ملی" }, 404);
    }
}
```

---

### 7. URL Registration and Server

```urdu
ایپ.راستہ("",                         نظارہ_گھر);
ایپ.راستہ("کتابیں/",                   نظارہ_کتابیں);
ایپ.راستہ("کتاب/نئی/",                 نظارہ_کتاب_نئی);
ایپ.راستہ("کتاب/<int:id>/ترمیم/",     نظارہ_کتاب_ترمیم);
ایپ.راستہ("کتاب/<int:id>/حذف/",       نظارہ_کتاب_حذف);
ایپ.راستہ("ناشرین/",                   نظارہ_ناشرین);
ایپ.راستہ("ناشر/<int:id>/حذف/",       نظارہ_ناشر_حذف);
ایپ.راستہ("api/کتابیں/",               api_کتابیں);
ایپ.راستہ("api/ناشرین/",               api_ناشرین);
ایپ.راستہ("api/کتاب/<int:id>/",        api_کتاب_ایک);

ایپ.چلائیں(پورٹ=8000);
```

`ایپ.چلائیں(پورٹ=8000)` starts Django's development server via `execute_from_command_line`. It passes `--noreload` by default — this prevents the auto-reloader from spawning a child process (which would lose the in-process setup and break with single-file Urdu apps). Pass `دوبارہ_لوڈ=سچ` to re-enable the reloader for development.

---

### 8. Urdu Templates

All four templates extend `بنیاد.html` using Urdu block keywords:

```html
{% توسیع "بنیاد.html" %}
{% بلاک عنوان %}کتابستان — کتابیں{% بلاک_ختم %}
{% بلاک مواد %}

{% اگر کتابیں %}
<table>
  {% کے_لیے ک کا کتابیں %}
  <tr>
    <td>{{ ک.عنوان }}</td>
    <td>{{ ک.مصنف }}</td>
    <td>{{ ک.ناشر_کتاب.نام }}</td>
    <td>{{ ک.قیمت }} روپے</td>
    <td>
      {% اگر ک.دستیاب %}
        <span class="badge badge-yes">دستیاب</span>
      {% ورنہ %}
        <span class="badge badge-no">نادستیاب</span>
      {% اگر_ختم %}
    </td>
  </tr>
  {% کے_لیے_ختم %}
</table>
{% ورنہ %}
<p>کوئی کتاب نہیں۔</p>
{% اگر_ختم %}

{% بلاک_ختم %}
```

The `UrduFilesystemLoader` preprocesses these Urdu template tags before Django's engine parses them — all standard Django template features (inheritance, context variables, filters) continue to work normally.

---

## API Endpoints

| URL | Method | Description |
|-----|--------|-------------|
| `/` | GET | Home — summary stats |
| `/کتابیں/` | GET | Books list (with optional `?q=` search) |
| `/کتاب/نئی/` | GET / POST | New book form / create |
| `/کتاب/<id>/ترمیم/` | GET / POST | Edit book form / update |
| `/کتاب/<id>/حذف/` | GET | Delete book and redirect |
| `/ناشرین/` | GET / POST | Publishers list / add publisher |
| `/ناشر/<id>/حذف/` | GET | Delete publisher and redirect |
| `/api/کتابیں/` | GET | JSON — all books |
| `/api/ناشرین/` | GET | JSON — all publishers with book counts |
| `/api/کتاب/<id>/` | GET | JSON — single book or 404 |

---

## ORM Query Helpers — Quick Reference

| Helper | Equivalent | Description |
|--------|------------|-------------|
| `سب_حاصل(Model)` | `Model.objects.all()` | All rows as QuerySet |
| `فلٹر(Model, **kw)` | `Model.objects.filter(**kw)` | Filtered QuerySet |
| `ایک_حاصل(Model, **kw)` | `Model.objects.get(**kw)` | Single row or exception |
| `بنائیں(Model, **kw)` | `Model.objects.create(**kw)` | Create and save new row |
| `حذف_کریں(Model, **kw)` | `Model.objects.get(**kw).delete()` | Delete a row |

All helpers return full Django ORM objects — `.save()`, `.delete()`, `.count()`, `.select_related()`, `__icontains`, `__gte`, etc. all work normally.

---

## Known Limitations

| Limitation | Reason | Workaround |
|------------|--------|------------|
| No CSRF protection | Django CSRF middleware not added by default | Add `CsrfViewMiddleware` via `ایپس` config, use `{% csrf_token %}` in forms |
| No user auth | Auth apps excluded by default | Add `django.contrib.auth` to `ایپس` config key |
| `--noreload` always on | Single-file script loses in-memory setup on child spawn | Use `دوبارہ_لوڈ=سچ` for development with file-based DB |
| `خالی=سچ` breaks | `خالی` is a reserved word → `None=True` invalid syntax | Use `اجازت=سچ` in field constructors |

---

## Next Steps

- Add pagination: pass `qs[start:end]` slices to the template
- Add Django auth: create a login-required decorator around CRUD views
- Serve as a production app: `gunicorn --workers 4 '__urdu_urls__:get_wsgi_application()'`
- Export books to Excel: `اردو/فائلیں` → `ایکسل_لکھو()`
