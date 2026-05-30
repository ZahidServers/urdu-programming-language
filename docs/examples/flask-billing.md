# Flask Billing App — اردو بلنگ سسٹم

A multi-page billing system built with Flask and SQLite. Demonstrates async Flask route handlers, multi-table SQL joins, dashboard aggregates, invoice line-item entry, and one-click payment status updates.

> **اردو:** Flask اور SQLite سے بنا ایک مکمل بلنگ سسٹم جو گاہک انتظام، بل سازی، اشیاء کی فہرست اور ادائیگی ٹریکنگ کا احاطہ کرتا ہے۔ یہ مثال غیر_متزامن فنکشن، کثیر جدول SQL، ڈیش بورڈ اور فارم ہینڈلنگ ظاہر کرتی ہے۔

---

## چلانے کا طریقہ / How to Run

```bash
pip install flask
cd examples/FLASK_BILLING_APP
urdu run app.urdu
```

Then open: **http://localhost:5000**

---

## Features

| Feature | Description |
|---------|-------------|
| Dashboard | Totals for customers, invoices, pending amount, and paid amount |
| Customer management | List, add, and view customers with phone and email |
| Invoice creation | Multi-line item invoices with quantity × price |
| Invoice detail | Full view with line items and total |
| Pay invoice | One-click status change from `pending` to `paid` |
| Async DB helpers | `انتظار` throughout — non-blocking SQLite via `اردو/ڈیٹا_بیس` |
| Auto schema | Tables are created on first run; no migrations needed |

---

## File Structure

```
examples/FLASK_BILLING_APP/
  app.urdu           ← main application
  templates/
    dashboard.html   ← home page: totals + recent invoices
    customers.html   ← customer list
    customer_form.html ← add customer form
    invoices.html    ← invoice list with status badge
    invoice_form.html ← new invoice form (dynamic line items)
    invoice.html     ← invoice detail + pay button
```

---

## Code Walkthrough

### 1. Imports and Database Helpers

```urdu
درآمد { فلاسک, فلاسک_سانچہ, فلاسک_رجوع, فلاسک_درخواست } سے "اردو/ویب";
درآمد { ایس_کیو_لائٹ } سے "اردو/ڈیٹا_بیس";

// query — returns rows
غیر_متزامن فنکشن dq(sql, p) {
    متغیر تجارت = نیا ایس_کیو_لائٹ("billing.db");
    انتظار تجارت.جوڑیں();
    واپس انتظار تجارت.سوال(sql, p);
}

// execute — no return
غیر_متزامن فنکشن dx(sql, p) {
    متغیر تجارت = نیا ایس_کیو_لائٹ("billing.db");
    انتظار تجارت.جوڑیں();
    انتظار تجارت.چلائیں(sql, p);
}

// execute + last insert id
غیر_متزامن فنکشن dxi(sql, p) {
    متغیر تجارت = نیا ایس_کیو_لائٹ("billing.db");
    انتظار تجارت.جوڑیں();
    انتظار تجارت.چلائیں(sql, p);
    واپس (انتظار تجارت.سوال("SELECT last_insert_rowid() as id", []))[0]["id"];
}
```

Three thin helper functions avoid repeating the connect/execute pattern everywhere.

| Helper | Use |
|--------|-----|
| `dq(sql, p)` | SELECT — returns list of row dicts |
| `dx(sql, p)` | INSERT / UPDATE / DELETE — returns nothing |
| `dxi(sql, p)` | INSERT — returns the new row's `id` |

---

### 2. Schema Creation (top-level `انتظار`)

```urdu
انتظار dx("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT DEFAULT '', email TEXT DEFAULT '')", []);
انتظار dx("CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL, date TEXT NOT NULL, status TEXT DEFAULT 'pending', notes TEXT DEFAULT '')", []);
انتظار dx("CREATE TABLE IF NOT EXISTS invoice_items (id INTEGER PRIMARY KEY AUTOINCREMENT, invoice_id INTEGER NOT NULL, description TEXT NOT NULL, qty REAL NOT NULL DEFAULT 1, price REAL NOT NULL DEFAULT 0)", []);
```

`انتظار` at the top level works because the Urdu transpiler detects any `غیر_متزامن` / `انتظار` usage in the file and wraps the whole script in an `async def _اردو_main()` block, executed via `asyncio.run()`.

---

### 3. Dashboard — Multi-Table Aggregates

```urdu
@ایپ.حاصل("/")
غیر_متزامن فنکشن گھر() {
    متغیر gc   = (انتظار dq("SELECT COUNT(*) as n FROM customers", []))[0]["n"];
    متغیر pnd  = (انتظار dq("SELECT COALESCE(SUM(ii.qty * ii.price), 0) as t
                              FROM invoices inv
                              LEFT JOIN invoice_items ii ON ii.invoice_id = inv.id
                              WHERE inv.status = 'pending'", []))[0]["t"];
    متغیر paid = (انتظار dq("...WHERE inv.status = 'paid'", []))[0]["t"];
    متغیر recent = انتظار dq("SELECT ... GROUP BY inv.id ORDER BY inv.id DESC LIMIT 5", []);
    واپس فلاسک_سانچہ("dashboard.html", customers=gc, pending=pnd, paid=paid, recent=recent);
}
```

`COALESCE(SUM(...), 0)` guards against `NULL` when there are no matching rows. The `LEFT JOIN` means invoices without any items are still included (with a total of 0).

---

### 4. New Invoice — Dynamic Line Items

```urdu
@ایپ.بھیجیں("/invoices/new")
غیر_متزامن فنکشن بل_محفوظ() {
    متغیر req    = فلاسک_درخواست();
    متغیر bid    = انتظار dxi("INSERT INTO invoices (customer_id, date, notes) VALUES (?, ?, ?)",
                               [cid, dt, notes]);

    // repeated fields: item_name[], item_qty[], item_price[]
    متغیر names  = req.form.getlist("item_name");
    متغیر qtys   = req.form.getlist("item_qty");
    متغیر prices = req.form.getlist("item_price");

    متغیر idx = 0;
    کے_لیے (متغیر nm کا names) {
        اگر (len(nm) > 0) {
            انتظار dx("INSERT INTO invoice_items (...) VALUES (?, ?, ?, ?)",
                       [bid, nm, qtys[idx], prices[idx]]);
        }
        idx = idx + 1;
    }
    واپس فلاسک_رجوع("/invoices");
}
```

The HTML form uses repeated `name="item_name"` / `name="item_qty"` / `name="item_price"` fields. `req.form.getlist()` returns all values for a given field name as a list, which are then zipped by index with a manual counter.

---

### 5. Pay Invoice — Status Update

```urdu
@ایپ.بھیجیں("/invoices/<bid>/pay")
غیر_متزامن فنکشن بل_ادا(bid) {
    انتظار dx("UPDATE invoices SET status = 'paid' WHERE id = ?", [عدد(bid)]);
    واپس فلاسک_رجوع("/invoices/" + bid);
}
```

A simple POST-only route. The "Pay" button in the template submits a form to this URL. After updating, it redirects back to the invoice detail page.

`عدد(bid)` converts the URL string parameter to an integer — `عدد` is the Urdu built-in for `int()`.

---

### 6. Run the Server

```urdu
ایپ.چلائیں(پورٹ=5000, ڈیبگ=جھوٹ);
```

---

## Database Schema

```
customers
  id, name, phone, email

invoices
  id, customer_id → customers.id
  date, status ('pending' | 'paid'), notes

invoice_items
  id, invoice_id → invoices.id
  description, qty, price
```

Invoice total = `SUM(qty × price)` across all `invoice_items` for a given `invoice_id`.

---

## Stopping the Server — سرور بند کرنا

> ⚠️ **Ctrl+C does not stop this server.** Flask/werkzeug's threaded mode keeps worker threads alive after the signal. Kill the process from another terminal:
>
> ```
> taskkill /F /IM urdu.exe        # CMD / PowerShell
> Stop-Process -Name urdu -Force  # PowerShell
> ```
>
> **اردو:** `Ctrl+C` Flask/werkzeug تھریڈڈ موڈ میں سرور نہیں روکتا — اوپر دی گئی کمانڈ استعمال کریں۔

---

## Known Limitations

| Limitation | Reason | Workaround |
|------------|--------|------------|
| No authentication | Simple demo app | Add Flask-Login or JWT sessions |
| No edit / delete | CRUD is create + read + pay only | Add PUT/DELETE routes |
| SQLite concurrency | Single-writer under async | Fine for small loads; switch to PostgreSQL for production |
| No print/PDF | Browser-only | Add `weasyprint` or `reportlab` for PDF export |

---

## Next Steps

- Add delete route: `@ایپ.بھیجیں("/invoices/<bid>/delete")`
- Add customer edit form at `/customers/<cid>/edit`
- Export invoice to PDF with `weasyprint`
- Add authentication: `فلاسک_نشست` for session-based login
- Switch to PostgreSQL: `درآمد { PostgreSQL } سے "اردو/ڈیٹا_بیس"`
