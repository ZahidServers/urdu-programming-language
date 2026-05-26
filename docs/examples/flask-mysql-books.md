# Flask MySQL Books App — اردو کتب خانہ

A library catalogue application built with Flask, MySQL, and Urdu Jinja2 templates. Demonstrates MySQL integration, search with LIKE queries, server-side pagination, Urdu template files, and seeded sample data from classical Urdu literature.

> **اردو:** Flask اور MySQL سے بنا ایک اردو کتب خانہ جس میں 20 کلاسیکی اردو کتابوں کا نمونہ ڈیٹا شامل ہے۔ یہ مثال MySQL انضمام، تلاش، صفحہ بندی، اردو Jinja2 سانچے اور فارم ہینڈلنگ ظاہر کرتی ہے۔

---

## چلانے کا طریقہ / How to Run

```bash
pip install flask mysql-connector-python
# MySQL server must be running at localhost:3306 with user root (empty password)
cd examples/FLASK_MYSQL_BOOKS_APP
urdu run app.urdu
```

Then open: **http://localhost:5000**

The app creates the `urdu_kutub` database and seeds 20 books automatically on first run.

---

## Features

| Feature | Description |
|---------|-------------|
| MySQL integration | Creates database, table, and seeds sample data on startup |
| Search | Full-text `LIKE` search across title and author |
| Pagination | 6 books per page with page links; clamps invalid page numbers |
| Book detail | Individual page at `/کتاب/<id>` |
| Add book | Form at `/شامل` to add a new entry |
| Urdu templates | All `.html` files use Urdu file names and Urdu Jinja2 tag keywords |
| Sample data | 20 classic Urdu books pre-loaded (Manto, Ghalib, Iqbal, Hyder, Faiz…) |

---

## File Structure

```
examples/FLASK_MYSQL_BOOKS_APP/
  app.urdu           ← main application
  templates/
    فہرست.html       ← book list with search bar and pagination
    کتاب.html        ← single book detail page
    شامل_کریں.html   ← add-new-book form
```

---

## Code Walkthrough

### 1. Imports and MySQL Connection

```urdu
درآمد { فلاسک, فلاسک_سانچہ, فلاسک_رجوع, فلاسک_درخواست, فلاسک_جواب } سے "اردو/ویب";
درآمد { MySQL } سے "اردو/ڈیٹا_بیس";

// Bootstrap: create database first (no database= arg)
متغیر بنیاد_ڈی_بی = نیا MySQL({ "میزبان": "localhost", "صارف": "root", "پاس_ورڈ": "", "پورٹ": 3306 });
انتظار بنیاد_ڈی_بی.چلائیں("CREATE DATABASE IF NOT EXISTS urdu_kutub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");

// App connection: connect to the created database
متغیر ڈی_بی = نیا MySQL({ "میزبان": "localhost", "صارف": "root", "پاس_ورڈ": "", "پورٹ": 3306, "ڈیٹا_بیس": "urdu_kutub" });
```

Two connections are needed: `بنیاد_ڈی_بی` (no database selected) creates the database, then `ڈی_بی` (with `"ڈیٹا_بیس": "urdu_kutub"`) connects to it for all subsequent queries.

**MySQL charset:** `utf8mb4` is required for Urdu text (standard `utf8` is limited to BMP characters and truncates Nastaliq glyphs).

---

### 2. Auto-Seeding Sample Data

```urdu
متغیر گنتی_نتائج = انتظار ڈی_بی.سوال("SELECT COUNT(*) AS n FROM books");
اگر (گنتی_نتائج[0]["n"] == 0) {
    متغیر نمونہ = [
        ["آگ کا دریا",  "قرۃ العین حیدر", 1959, "ناول",   "اردو ادب کا شاہکار ناول..."],
        ["دیوان غالب",  "مرزا غالب",       1841, "شاعری",  "اردو شاعری کا سب سے مشہور دیوان۔"],
        // ... 18 more rows
    ];
    کے_لیے (متغیر ک کا نمونہ) {
        انتظار ڈی_بی.چلائیں("INSERT INTO books (...) VALUES (%s, %s, %s, %s, %s)", ک);
    }
}
```

The seed block runs only once: `COUNT(*) == 0` means the table is empty. Each iteration inserts one row from the `نمونہ` list. MySQL uses `%s` placeholders (not `?` like SQLite).

---

### 3. Home Page — Search + Pagination

```urdu
@ایپ.حاصل("/")
غیر_متزامن فنکشن گھر() {
    متغیر req   = فلاسک_درخواست();
    متغیر تلاش = req.args.get("تلاش", "").strip();
    متغیر صفحہ = int(req.args.get("صفحہ", "1"));
    اگر (صفحہ < 1) { صفحہ = 1; }
    متغیر ازاچہ = (صفحہ - 1) * فی_صفحہ;

    اگر (len(تلاش) > 0) {
        متغیر مثل = `%${تلاش}%`;
        متغیر کتابیں   = انتظار ڈی_بی.سوال(
            "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s ORDER BY title LIMIT %s OFFSET %s",
            [مثل, مثل, فی_صفحہ, ازاچہ]);
        متغیر کل_نتائج = انتظار ڈی_بی.سوال(
            "SELECT COUNT(*) AS n FROM books WHERE title LIKE %s OR author LIKE %s",
            [مثل, مثل]);
    } ورنہ {
        متغیر کتابیں   = انتظار ڈی_بی.سوال(
            "SELECT * FROM books ORDER BY title LIMIT %s OFFSET %s",
            [فی_صفحہ, ازاچہ]);
        متغیر کل_نتائج = انتظار ڈی_بی.سوال("SELECT COUNT(*) AS n FROM books");
    }

    متغیر کل        = کل_نتائج[0]["n"];
    متغیر کل_صفحات = کل > 0 ? int(ریاضی.چھت(کل / فی_صفحہ)) : 1;
    اگر (صفحہ > کل_صفحات) { صفحہ = کل_صفحات; }

    واپس فلاسک_سانچہ("فہرست.html",
        کتابیں=کتابیں, تلاش=تلاش,
        صفحہ=صفحہ, کل_صفحات=کل_صفحات,
        کل=کل, فی_صفحہ=فی_صفحہ);
}
```

**Pagination formula:**
- `ازاچہ = (صفحہ - 1) × فی_صفحہ` — SQL `OFFSET`
- `کل_صفحات = ⌈کل ÷ فی_صفحہ⌉` — ceiling division via `ریاضی.چھت()`
- Page is clamped: `اگر (صفحہ > کل_صفحات) { صفحہ = کل_صفحات; }`

**Template literal for LIKE pattern:**
`` متغیر مثل = `%${تلاش}%`; `` produces `%search_term%` for the SQL `LIKE` operator.

---

### 4. Book Detail

```urdu
@ایپ.حاصل("/کتاب/<int:bid>")
غیر_متزامن فنکشن کتاب_دیکھیں(bid) {
    متغیر نتائج = انتظار ڈی_بی.سوال("SELECT * FROM books WHERE id = %s", [bid]);
    اگر (len(نتائج) == 0) {
        واپس فلاسک_جواب("کتاب نہیں ملی", 404, "text/plain; charset=utf-8");
    }
    واپس فلاسک_سانچہ("کتاب.html", کتاب=نتائج[0]);
}
```

`<int:bid>` is a Flask typed path parameter — it converts the URL segment to an integer before passing it to the function, so no manual `int()` conversion is needed. The route URL `/کتاب/<int:bid>` uses a mixed Urdu/ASCII path, which works correctly.

---

### 5. Urdu Jinja2 Templates

The template filenames are fully Urdu (`فہرست.html`, `کتاب.html`, `شامل_کریں.html`). Template tags use Urdu keywords:

```html
{% کے_لیے کتاب کا کتابیں %}
<div class="کارڈ">
  <h2><a href="/کتاب/{{ کتاب.id }}">{{ کتاب.title }}</a></h2>
  <p class="مصنف">{{ کتاب.author }}
    {% اگر کتاب.year %} — {{ کتاب.year }}{% اگر_ختم %}
  </p>
  <p>{{ کتاب.summary }}</p>
</div>
{% کے_لیے_ختم %}

{# Pagination links #}
{% کے_لیے ن کا صفحات %}
<a href="/?صفحہ={{ ن }}{% اگر تلاش %}&تلاش={{ تلاش }}{% اگر_ختم %}"
   {% اگر ن == صفحہ %}class="فعال"{% اگر_ختم %}>{{ ن }}</a>
{% کے_لیے_ختم %}
```

Urdu variable names passed from Flask (`کتابیں`, `صفحات`, `تلاش`, `صفحہ`) are used directly in template expressions.

---

### 6. Add Book Form

```urdu
@ایپ.حاصل("/شامل")
فنکشن شامل_فارم() {
    واپس فلاسک_سانچہ("شامل_کریں.html");
}

@ایپ.بھیجیں("/شامل")
غیر_متزامن فنکشن شامل_محفوظ() {
    متغیر req    = فلاسک_درخواست();
    متغیر عنوان = req.form.get("title", "").strip();
    متغیر مصنف  = req.form.get("author", "").strip();
    متغیر سنہ   = req.form.get("year", "").strip();

    اگر (len(عنوان) > 0 اور len(مصنف) > 0) {
        متغیر سنہ_عدد = خالی;
        اگر (len(سنہ) > 0) { سنہ_عدد = int(سنہ); }
        انتظار ڈی_بی.چلائیں(
            "INSERT INTO books (title, author, year, category, summary) VALUES (%s, %s, %s, %s, %s)",
            [عنوان, مصنف, سنہ_عدد, زمرہ, خلاصہ]);
    }
    واپس فلاسک_رجوع("/");
}
```

The year field is optional — `سنہ_عدد = خالی` (None) is inserted as SQL `NULL` when left blank. Validation requires at minimum a title and author.

---

## SQLite vs MySQL: Key Differences

| Aspect | SQLite (`اردو/ڈیٹا_بیس` ایس_کیو_لائٹ) | MySQL (`اردو/ڈیٹا_بیس` MySQL) |
|--------|----------------------------------------|-------------------------------|
| Placeholders | `?` | `%s` |
| Last insert ID | `SELECT last_insert_rowid()` | `cursor.lastrowid` |
| Connection | File path | Host/port/user/password |
| Charset | UTF-8 by default | Must specify `utf8mb4` explicitly |

---

## Known Limitations

| Limitation | Reason | Workaround |
|------------|--------|------------|
| Root with no password | Local dev default | Pass credentials via environment variables for production |
| No edit / delete | CRUD is create + read only | Add PUT `/کتاب/<id>/ترمیم` and DELETE routes |
| URL param `<int:bid>` is ASCII | Flask path typing syntax | Use `<int:bid>` — the Urdu prefix in the path still works |
| No category filter | Search only | Add `?زمرہ=ناول` query param and WHERE clause |

---

## Next Steps

- Add category filter: `WHERE category = %s` with a dropdown in the search bar
- Add edit form at `/کتاب/<int:bid>/ترمیم`
- Add delete at `/کتاب/<int:bid>/حذف` (POST with confirmation)
- Paginate without page links: use infinite scroll with `fetch()` and JSON endpoint
- Export book list to CSV using `اردو/فائلیں`
