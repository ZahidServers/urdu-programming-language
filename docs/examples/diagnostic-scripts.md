# Diagnostic Scripts — تشخیصی اسکرپٹ

These three short scripts in the `examples/` folder are **internal diagnostic tests**, not end-user examples. They verify that specific runtime dependencies (ctypes, asyncio, uvicorn) work correctly inside the compiled `urdu.exe` — particularly after a Nuitka standalone build where DLL bundling can be tricky.

> **اردو:** `examples/` فولڈر میں یہ تین مختصر اسکرپٹ **اندرونی تشخیصی جانچ** ہیں، نہ کہ صارف کی مثالیں۔ یہ تصدیق کرتے ہیں کہ مخصوص رن ٹائم انحصارات (ctypes، asyncio، uvicorn) مرتب شدہ `urdu.exe` کے اندر صحیح طور پر کام کرتے ہیں — خاص طور پر Nuitka تعمیر کے بعد جہاں DLL بنڈلنگ مشکل ہو سکتی ہے۔

---

## test_ctypes.urdu

**Full source:**

```urdu
لکھو("ctypes ٹیسٹ شروع...");
لکھو("asyncio ٹیسٹ...");
درآمد { غیر_متزامن_چلائیں } سے "اردو/دھاگہ";
لکھو("تمام ٹھیک ہے!");
```

### Line-by-line explanation — سطر بہ سطر وضاحت

| Line | Code | What it does |
|------|------|--------------|
| 1 | `لکھو("ctypes ٹیسٹ شروع...")` | Prints a start marker to confirm the script is running at all. If this fails, the interpreter itself is broken. |
| 2 | `لکھو("asyncio ٹیسٹ...")` | Checkpoint before the import — confirms execution reaches this point. |
| 3 | `درآمد { غیر_متزامن_چلائیں } سے "اردو/دھاگہ"` | Imports `غیر_متزامن_چلائیں` (the async runner) from `اردو/دھاگہ`. Internally this triggers `import asyncio` and `import concurrent.futures`. In a Nuitka build, asyncio requires `_asyncio.pyd` to be bundled — this line fails if that extension module is missing. |
| 4 | `لکھو("تمام ٹھیک ہے!")` | Prints only if the import succeeded. The absence of this line in the output means line 3 crashed. |

> **اردو:** یہ اسکرپٹ `اردو/دھاگہ` درآمد کر کے جانچتا ہے کہ `asyncio` اور `_asyncio.pyd` صحیح طور پر بنڈل ہوئے ہیں۔ اگر آخری سطر پرنٹ ہو تو سب ٹھیک ہے۔

**How to run:**

```
urdu run examples/test_ctypes.urdu
```

**Expected output:**

```
ctypes ٹیسٹ شروع...
asyncio ٹیسٹ...
تمام ٹھیک ہے!
```

---

## test_ctypes2.urdu

**Full source:**

```urdu
لکھو("شروع");
لکھو("sys درآمد...");
درآمد { چلائیں_پائیتھن } سے "اردو/پل";
لکھو("چلا رہے ہیں...");
چلائیں_پائیتھن("import ctypes; print('ctypes ok:', ctypes.__version__)");
لکھو("ختم");
```

### Line-by-line explanation — سطر بہ سطر وضاحت

| Line | Code | What it does |
|------|------|--------------|
| 1 | `لکھو("شروع")` | Start marker — confirms the script begins executing. |
| 2 | `لکھو("sys درآمد...")` | Checkpoint before the import. |
| 3 | `درآمد { چلائیں_پائیتھن } سے "اردو/پل"` | Imports `چلائیں_پائیتھن` (run-Python helper) from `اردو/پل`. This module exposes `exec()` and `eval()` in a controlled way for direct Python evaluation inside an Urdu program. |
| 4 | `لکھو("چلا رہے ہیں...")` | Checkpoint before the `ctypes` test. |
| 5 | `چلائیں_پائیتھن("import ctypes; print('ctypes ok:', ctypes.__version__)")` | Runs a raw Python string via `exec()`. Imports `ctypes` (the C foreign function library) and prints its version. In a Nuitka build this requires `_ctypes.pyd` and `libffi` to be present. If this line fails, ctypes is missing from the bundle. |
| 6 | `لکھو("ختم")` | Prints only if `چلائیں_پائیتھن` did not raise an exception. |

> **اردو:** یہ اسکرپٹ `ctypes` ماڈیول کو براہ راست پائتھن کوڈ کے ذریعے آزماتا ہے۔ `ctypes.__version__` کامیابی سے پرنٹ ہونا اس بات کی تصدیق کرتا ہے کہ C فارن فنکشن لائبریری بنڈل میں موجود ہے۔

**How to run:**

```
urdu run examples/test_ctypes2.urdu
```

**Expected output:**

```
شروع
sys درآمد...
چلا رہے ہیں...
ctypes ok: <version>
ختم
```

---

## test_uvicorn.urdu

**Full source:**

```urdu
درآمد { فاسٹ_اے_پی_آئی } سے "اردو/ویب";
متغیر ایپ = نیا فاسٹ_اے_پی_آئی({});
@ایپ.حاصل("/")
فنکشن جڑ() {
    واپس { "حال": "ٹھیک" };
}
لکھو("uvicorn شروع...");
ایپ.چلائیں(پورٹ=9999);
```

### Line-by-line explanation — سطر بہ سطر وضاحت

| Line | Code | What it does |
|------|------|--------------|
| 1 | `درآمد { فاسٹ_اے_پی_آئی } سے "اردو/ویب"` | Imports the FastAPI wrapper. Internally requires `fastapi`, `starlette`, `uvicorn`, `anyio`, `h11`, and `pydantic` — all must be present in the bundle. |
| 2 | `متغیر ایپ = نیا فاسٹ_اے_پی_آئی({})` | Creates a FastAPI application instance with an empty config dict (uses all defaults: title "اردو API", version "1.0.0"). |
| 3–5 | `@ایپ.حاصل("/") فنکشن جڑ() { ... }` | Registers a GET route at `/` using a decorator. The route function returns a JSON-serialisable dict `{"حال": "ٹھیک"}` (status: ok). This tests that the decorator transpilation and FastAPI route registration work correctly. |
| 6 | `لکھو("uvicorn شروع...")` | Prints before the blocking `چلائیں()` call, confirming all setup code executed without error. |
| 7 | `ایپ.چلائیں(پورٹ=9999)` | Starts the uvicorn ASGI server on port 9999 (not 8000, to avoid conflicts with other running servers). This is a **blocking call** — the script stays running until you press Ctrl+C. |

> **اردو:** یہ اسکرپٹ FastAPI سرور کو پورٹ 9999 پر شروع کرتا ہے۔ اگر `http://localhost:9999/` پر `{"حال": "ٹھیک"}` ملے تو اس کا مطلب ہے کہ FastAPI، uvicorn، اور ASGI اسٹیک درست طریقے سے بنڈل ہوئے ہیں۔

**How to run:**

```
urdu run examples/test_uvicorn.urdu
```

**Expected output:**

```
uvicorn شروع...
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9999 (Press CTRL+C to quit)
```

Then visit **http://localhost:9999/** to confirm the response:

```json
{"حال": "ٹھیک"}
```

Press **Ctrl+C** to stop the server.

---

## When to run these — کب چلائیں

Run all three after a fresh `python build.py` to confirm the standalone `urdu.exe` has all required native extensions:

```powershell
# From the dist\urdu.dist\ folder:
.\urdu.exe run examples\test_ctypes.urdu
.\urdu.exe run examples\test_ctypes2.urdu
.\urdu.exe run examples\test_uvicorn.urdu
```

If any script fails, the missing native extension (`_asyncio.pyd`, `_ctypes.pyd`, or a uvicorn dependency DLL) was not included in the Nuitka bundle. Add the missing DLL from the Anaconda `Library\bin` folder (which the post-build step in `build.py` copies automatically).

> **اردو:** یہ تینوں اسکرپٹ تازہ Nuitka تعمیر کے بعد چلائیں تاکہ یہ یقین ہو کہ `urdu.exe` میں تمام ضروری نیٹو ایکسٹینشنز شامل ہیں۔ اگر کوئی اسکرپٹ ناکام ہو تو `build.py` میں پوسٹ بلڈ مرحلے کا Anaconda DLL کاپی کوڈ جانچیں۔
