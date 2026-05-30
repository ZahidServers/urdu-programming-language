# 2. Installation — نصب کرنا

**Difficulty:** Beginner — مبتدی  
**Time:** ~10 minutes

---

## Option A — Standalone Executable (Recommended) — قابل عمل فائل (تجویز کردہ)

The easiest way. No Python installation required.

> **اردو:** سب سے آسان طریقہ۔ Python نصب کرنے کی ضرورت نہیں۔

**Steps — اقدامات:**

1. Go to the [GitHub Releases page](https://github.com/ZahidServers/urdu-programming-language/releases)
2. Download the latest `urdu-windows-vX.X.X.zip`
3. Extract the ZIP — you get a folder called `urdu.dist`
4. Inside is `urdu.exe`

**Verify it works — تصدیق کریں:**

```powershell
.\urdu.exe نسخہ
```

Expected output — متوقع آؤٹ پٹ:
```
اردو پروگرامنگ لینگویج v1.0.1
```

**Add to PATH (optional) — PATH میں شامل کریں (اختیاری):**

```powershell
# Run as Administrator — بطور منتظم چلائیں
$env:PATH += ";C:\path\to\urdu.dist"
[Environment]::SetEnvironmentVariable("PATH", $env:PATH, "Machine")
```

After this, type `urdu` from any folder instead of `.\urdu.exe`.

> **اردو:** PATH میں شامل کرنے کے بعد کسی بھی فولڈر سے صرف `urdu` ٹائپ کر سکتے ہیں۔

---

## Option B — Python Source — Python سورس

For developers who want to contribute to the language or run from source.

> **اردو:** ان ڈویلپرز کے لیے جو زبان میں حصہ ڈالنا چاہتے ہیں یا سورس سے چلانا چاہتے ہیں۔

**Requirements — ضروریات:**
- Python 3.8 or later
- Git

**Steps — اقدامات:**

```bash
git clone https://github.com/ZahidServers/urdu-programming-language
cd urdu-programming-language
pip install -e .
```

**Verify — تصدیق:**

```bash
python -m urdu نسخہ
```

---

## Running Your First File — پہلی فائل چلانا

Create a file `hello.urdu` anywhere on your computer:

```urdu
لکھو("السلام علیکم!")
```

Run it — چلائیں:

```powershell
# With the executable — قابل عمل فائل سے
urdu run hello.urdu

# Or with Python source — یا Python سورس سے
python -m urdu run hello.urdu
```

Output — آؤٹ پٹ:
```
السلام علیکم!
```

---

## CLI Commands — کمانڈ لائن حکام

| Command | Description |
|---------|-------------|
| `urdu run file.urdu` | Run a `.urdu` file |
| `urdu repl` | Open the interactive REPL |
| `urdu نسخہ` | Show version |
| `urdu مدد` | Show help |

> **اردو:** `urdu run` کسی بھی `.urdu` فائل چلاتا ہے۔ `urdu repl` انٹرایکٹو REPL کھولتا ہے جہاں آپ فوری کوڈ لکھ کر آؤٹ پٹ دیکھ سکتے ہیں۔

---

## Interactive REPL — انٹرایکٹو REPL

The REPL (Read-Evaluate-Print Loop) lets you type code line-by-line and see results instantly.

```
urdu repl

اردو> لکھو("سلام")
سلام
اردو> متغیر ع = 5 * 5
اردو> لکھو(ع)
25
اردو> خروج
```

> **اردو:** REPL میں ایک ایک سطر لکھیں اور فوری نتیجہ دیکھیں۔ سیکھنے اور تجربہ کرنے کے لیے بہترین ٹول ہے۔ باہر نکلنے کے لیے `خروج` لکھیں۔

---

## Key Points — اہم نکات

- Option A (`.exe`) is the easiest — no Python needed, just extract and run
- Option B (Python source) requires `python -m urdu run` prefix
- File extension must be `.urdu`
- The REPL is great for quick experiments

> **اردو:** آسان طریقہ: `.exe` ڈاؤن لوڈ کریں۔ فائل ایکسٹینشن `.urdu` ہونی چاہیے۔ REPL تجربہ کے لیے بہترین ہے۔

---

[← Previous: Welcome](01-welcome.md) | [Next: Hello World →](03-hello-world.md)
