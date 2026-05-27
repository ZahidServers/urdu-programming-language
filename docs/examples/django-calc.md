# Django Calculator App — اردو حساب دان

A real-time calculator built with Django and Socket.IO. Demonstrates programmatic Django setup (no manage.py), Socket.IO event handlers over WSGI/werkzeug, SQLite calculation history, search, and server-side pagination — all in a dark-themed RTL Urdu UI.

> **اردو:** Django اور Socket.IO سے بنا ایک حقیقی وقت کا حساب دان جو SQLite میں حسابات کی تاریخ محفوظ کرتا ہے۔ یہ مثال Django کا پروگرامی آغاز، Socket.IO ایونٹ ہینڈلرز، تلاش اور صفحہ بندی ظاہر کرتی ہے۔

---

## چلانے کا طریقہ / How to Run

```bash
pip install django python-socketio werkzeug
cd examples/DJANGO_CALC_APP
urdu run app.urdu
```

Then open: **http://localhost:8000**

---

## Features

| Feature | Description |
|---------|-------------|
| Real-time calculation | Socket.IO sends the expression, server evaluates it and emits the result |
| Calculation history | Every computation is saved to SQLite with timestamp and error flag |
| History search | Filter history by expression or result string |
| Pagination | 8 results per page; page links with active highlight |
| Error handling | Division by zero, invalid syntax — all caught and stored with `is_error=1` |
| Safe eval | `eval()` runs with a restricted `__builtins__=None` — only math functions allowed |
| Django programmatic setup | No `manage.py` or `settings.py` files — configured entirely in code |
| Urdu Django templates | `بنیاد.html`, `کیلکولیٹر.html`, `تاریخ.html` using Urdu block/for/if keywords |

---

## Architecture

```
Browser (Socket.IO JS client)
        ↕  Socket.IO over HTTP / polling
socketio.WSGIApp
        ├─ /socket.io/  →  Socket.IO server (threading mode)
        └─  all other   →  Django WSGI app
                werkzeug run_simple (threaded=True)
```

`socketio.WSGIApp` wraps Django's WSGI callable. Regular HTTP requests (`/` and `/تاریخ/`) go to Django; Socket.IO handshakes and events go to the Socket.IO server.

---

## File Structure

```
examples/DJANGO_CALC_APP/
  app.urdu               ← main application (server + routes + sockets)
  templates/
    بنیاد.html           ← base layout (nav, dark theme CSS)
    کیلکولیٹر.html       ← calculator UI + Socket.IO JS client
    تاریخ.html           ← history page with search + pagination table
  حساب.db               ← SQLite database (auto-created on first run)
```

---

## Code Walkthrough

### 1. Imports and SQLite Setup

```urdu
درآمد { ڈجانگو, ڈجانگو_سانچہ } سے "اردو/ویب";
درآمد { ساکٹ_آئی_او } سے "اردو/ویب";
درآمد * بطور sqlite3 سے "sqlite3";
درآمد * بطور os سے "os";

متغیر _بنیاد     = os.path.dirname(os.path.abspath(__file__));
متغیر ڈی_بی_راستہ = `${_بنیاد}/حساب.db`;
متغیر ڈی_بی       = sqlite3.connect(ڈی_بی_راستہ, check_same_thread=جھوٹ);
ڈی_بی.execute("CREATE TABLE IF NOT EXISTS calculations (...)");
ڈی_بی.commit();
```

`os.path.abspath(__file__)` resolves the script's own directory — critical because `urdu run` may be invoked from any working directory. `__file__` is set by the Urdu runtime to the path of the `.urdu` file.

`check_same_thread=False` allows `sqlite3.connect` to be used from the worker threads that werkzeug spawns per request.

**Why not `اردو/ڈیٹا_بیس`?** The `ایس_کیو_لائٹ` wrapper is async. This app uses werkzeug threading mode (sync), so raw `sqlite3` is simpler and more direct.

---

### 2. Programmatic Django Setup

```urdu
متغیر سانچہ_ڈائریکٹری = `${_بنیاد}/templates`;
متغیر ایپ = نیا ڈجانگو({ "سانچہ_فولڈر": [سانچہ_ڈائریکٹری], "ڈیبگ": سچ });
ایپ.ترتیب_دیں();
```

`ڈجانگو` calls `django.conf.settings.configure(...)` internally — no separate `settings.py` file is needed. The config dict accepts:

| Key | Description |
|-----|-------------|
| `سانچہ_فولڈر` | List of absolute paths to search for templates |
| `ڈیبگ` | Enable Django debug mode |
| `خفیہ_کلید` | Django `SECRET_KEY` (defaults to a dev key) |
| `ڈیٹا_بیس` | Database config dict or SQLite path string |
| `ایپس` | Additional `INSTALLED_APPS` entries |

The `UrduFilesystemLoader` is wired in automatically — it preprocesses Urdu template tags (`{% اگر %}`, `{% کے_لیے %}`, `{% بلاک %}`) before Django's template engine sees them.

---

### 3. URL Registration

```urdu
فنکشن گھر(req) {
    واپس ڈجانگو_سانچہ(req, "کیلکولیٹر.html", {});
}
ایپ.راستہ("", گھر);

فنکشن تاریخ_دیکھیں(req) { ... }
ایپ.راستہ("تاریخ/", تاریخ_دیکھیں);
```

`ایپ.راستہ(url, view_fn)` calls Django's `path()` and appends to the dynamic URL module (`__urdu_urls__`). Django resolves `/` → `""` and `/تاریخ/` → `"تاریخ/"`.

---

### 4. History — Search and Pagination

```urdu
فنکشن تاریخ_دیکھیں(req) {
    متغیر تلاش  = req.GET.get("تلاش", "").strip();
    متغیر صفحہ  = int(req.GET.get("صفحہ", "1"));
    متغیر ازاچہ = (صفحہ - 1) * فی_صفحہ;

    اگر (len(تلاش) > 0) {
        متغیر مثل   = `%${تلاش}%`;
        متغیر کرسر  = ڈی_بی.execute(
            "SELECT ... WHERE expression LIKE ? OR result LIKE ? LIMIT ? OFFSET ?",
            [مثل, مثل, فی_صفحہ, ازاچہ]);
        متغیر گنتی  = ڈی_بی.execute(
            "SELECT COUNT(*) FROM calculations WHERE expression LIKE ? OR result LIKE ?",
            [مثل, مثل]).fetchone();
    } ورنہ {
        // all results, no filter
    }

    متغیر کل_صفحات = کل > 0 ? int(ریاضی.چھت(کل / فی_صفحہ)) : 1;
    ...
    واپس ڈجانگو_سانچہ(req, "تاریخ.html", سیاق);
}
```

The history page assembles the context dict with `حسابات` (list of row dicts), pagination state, and the search term. The template uses these directly in Urdu variable expressions.

---

### 5. Socket.IO Event Handlers

```urdu
@sio.پر_جڑنا()
فنکشن جڑنا(sid, environ) {
    لکھو(`جڑت: ${sid}`);
}

@sio.پر("حساب")
فنکشن حساب_کریں(sid, data) {
    متغیر اظہار = data.get("اظہار", "").strip();

    کوشش {
        متغیر امن_گلوبلز = {
            "__builtins__": خالی,
            "abs": abs, "round": round, "int": int, "float": float,
            "max": max, "min": min, "pow": pow
        };
        متغیر جواب = eval(اظہار, امن_گلوبلز);
        نتیجہ = str(جواب);
    } پکڑو (e) {
        نتیجہ = str(e);
        خطا = 1;
    }

    ڈی_بی.execute("INSERT INTO calculations ...", [اظہار, نتیجہ, خطا]);
    ڈی_بی.commit();
    sio._sio.emit("نتیجہ", { "اظہار": اظہار, "نتیجہ": نتیجہ, "خطا": خطا }, room=sid);
}
```

**Safe eval:** passing `{"__builtins__": None}` as the globals dict to `eval()` removes access to all Python built-ins. Only the explicitly whitelisted names (`abs`, `round`, etc.) are available. Expressions like `__import__('os').system(...)` will fail with `NameError`.

**Sync emit:** in threading mode (WSGI), `sio._sio` is a `socketio.Server` object. `.emit()` is synchronous — `await` is not needed.

---

### 6. WSGI Integration and Server Startup

```urdu
درآمد { run_simple } سے "werkzeug.serving";
متغیر wsgi_یکجا = sio.wsgi_ایپ(ایپ);
run_simple("0.0.0.0", 8000, wsgi_یکجا, threaded=سچ, passthrough_errors=سچ);
```

`sio.wsgi_ایپ(ایپ)` creates `socketio.WSGIApp(sio._sio, django_wsgi_callable)`.
`threaded=True` is required for Socket.IO threading mode — without it the server deadlocks because the Socket.IO polling transport needs concurrent request handling.

---

### 7. Urdu Django Templates

Templates extend `بنیاد.html` using Urdu block keywords:

```html
{% توسیع "بنیاد.html" %}
{% بلاک عنوان %}کیلکولیٹر — اردو حساب دان{% بلاک_ختم %}

{% بلاک مواد %}
...
{% بلاک_ختم %}
```

The history table iterates with `{% کے_لیے %}` and applies conditional CSS via `{% اگر %}`:

```html
{% کے_لیے ح کا حسابات %}
<tr>
  <td>{{ ح.expression }}</td>
  <td {% اگر ح.is_error %}class="خطا_متن"{% ورنہ %}class="کامیاب_متن"{% اگر_ختم %}>
    {{ ح.result }}
  </td>
</tr>
{% کے_لیے_ختم %}
```

---

### 8. Browser-Side Socket.IO (JavaScript)

```javascript
var socket = io();

function حساب_کریں() {
  var expr = document.getElementById('اظہار').value.trim();
  socket.emit('حساب', { 'اظہار': expr });
}

socket.on('نتیجہ', function(data) {
  if (data['خطا']) {
    box.innerHTML = 'غلطی: ' + data['نتیجہ'];
  } else {
    box.innerHTML = data['اظہار'] + ' = ' + data['نتیجہ'];
  }
});
```

Urdu key names (`اظہار`, `نتیجہ`, `خطا`) are used as plain JavaScript strings — they match the server-side event payload keys exactly.

---

## Event Flow

```
User types "2 ** 10" → Enter
    → browser: socket.emit('حساب', { اظہار: '2 ** 10' })
        → server: حساب_کریں(sid, { اظہار: '2 ** 10' })
            → eval('2 ** 10', امن_گلوبلز)  →  1024
            → INSERT INTO calculations (expression='2 ** 10', result='1024', is_error=0)
            → sio._sio.emit('نتیجہ', { اظہار: '2 ** 10', نتیجہ: '1024', خطا: 0 }, room=sid)
                → browser: نتیجہ handler updates #نتیجہ_باکس
```

---

## Known Limitations

| Limitation | Reason | Workaround |
|------------|--------|------------|
| No user sessions | Single shared history | Add Django auth and filter `WHERE user_id = ?` |
| `eval()` with whitelist | Only math — no custom functions | Extend `امن_گلوبلز` carefully; never restore `__builtins__` |
| SQLite with threading | `check_same_thread=False` + one writer at a time | Fine for development; use PostgreSQL + connection pool for production |
| No delete history | Read-only history | Add a DELETE endpoint and AJAX call |

### Compiled-exe note — `urdu.exe` میں نوٹ

`django.contrib.auth` and `django.contrib.contenttypes` are **not** included in the default `INSTALLED_APPS` when using the `ڈجانگو` wrapper. Those apps transitively import `django.core.management`, which is excluded from the compiled standalone exe (`--nofollow-import-to=django.core.management`).

If your app needs Django's auth system or content types framework, add them explicitly:

```urdu
متغیر ایپ = نیا ڈجانگو({
    "سانچہ_فولڈر": [سانچہ_ڈائریکٹری],
    "ایپس": ["django.contrib.contenttypes", "django.contrib.auth"],
    "ڈیبگ": سچ
});
```

> **Note:** If you add `django.contrib.auth` or `django.contrib.contenttypes`, remove `--nofollow-import-to=django.core.management` from `build.py` and rebuild — otherwise Django's app registry will fail during `django.setup()`.

This calculator app does **not** use Django auth, so it works with the default settings in both source mode and the compiled exe.

---

## Next Steps

- Add delete endpoint: `ایپ.راستہ("حذف/<int:cid>/", حذف_کریں)`
- Export history to CSV: `اردو/فائلیں`
- Add user authentication with Django's built-in `django.contrib.auth`
- Deploy with gunicorn + gevent for production Socket.IO: `gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker`
- Add a graph of recent calculations using Chart.js on the history page
