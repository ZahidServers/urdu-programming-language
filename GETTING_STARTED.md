<div dir="rtl" align="right">

# شروع کریں — اردو پروگرامنگ لینگویج

نصب کامیاب! اب آپ اردو میں کوڈ لکھ سکتے ہیں۔

</div>

# Getting Started — اردو پروگرامنگ لینگویج

Welcome! You have successfully installed the **Urdu Programming Language**. This guide will walk you through your first steps.

---

## Step 1 — Verify Installation

Open a terminal and run:

```
urdu version
```

You should see output like:

```
اردو پروگرامنگ لینگویج — نسخہ 1.0.0
Urdu Programming Language — Version 1.0.0
Author: Mohammed Zahid Wadiwale
```

---

## Step 2 — Your First Program

Create a file called `hello.urdu` and write:

```urdu
لکھو("السلام علیکم، دنیا!")
```

Run it:

```
urdu run hello.urdu
```

Output:

```
السلام علیکم، دنیا!
```

**Congratulations — you just ran your first Urdu program!**

---

## Step 3 — Try the Interactive REPL

The REPL (Read-Eval-Print Loop) lets you type and run Urdu code one line at a time — great for experimenting.

```
urdu repl
```

Try typing these lines:

```urdu
لکھو("مرحبا!")
متغیر عدد = 42
لکھو(عدد * 2)
```

Type `خروج` or press `Ctrl+C` to exit the REPL.

---

## Step 4 — Core Language Concepts

### Variables

```urdu
متغیر نام = "احمد"
مستقل پائی = 3.14159
لکھو(`${نام} کو خوش آمدید!`)
```

### User Input

```urdu
متغیر نام = پڑھو("آپ کا نام کیا ہے؟ ")
لکھو(`خوش آمدید، ${نام}!`)
```

### Conditions

```urdu
متغیر عمر = 20

اگر (عمر >= 18) {
    لکھو("آپ بالغ ہیں")
} ورنہ {
    لکھو("آپ نابالغ ہیں")
}
```

### Loops

```urdu
کے_لیے (متغیر i کا حد(1, 6)) {
    لکھو(i)
}
```

### Functions

```urdu
فنکشن خوش_آمدید(نام) {
    واپس `السلام علیکم، ${نام}!`
}

لکھو(خوش_آمدید("فاطمہ"))
```

### Lists and Objects

```urdu
متغیر پھل = ["آم", "کیلا", "سیب"]

کے_لیے (متغیر ف کا پھل) {
    لکھو(ف)
}

متغیر شخص = { نام: "علی", عمر: 25 }
لکھو(شخص.نام)
```

---

## Step 5 — Check a File for Errors

Before running, you can check syntax:

```
urdu check myfile.urdu
```

---

## Step 6 — Compile to Python

To see the generated Python code:

```
urdu compile myfile.urdu
```

This is useful for debugging or learning how the language works internally.

---

## Step 7 — Install Additional Libraries

The Urdu Programming Language supports many built-in library modules. Some require Python packages to be installed first.

Install packages using:

```
urdu نصب fastapi uvicorn
urdu نصب requests beautifulsoup4
urdu نصب scikit-learn pandas numpy
```

Or use pip directly:

```
pip install fastapi uvicorn
```

---

## Available Libraries

| Import | Use Case |
|--------|---------|
| `اردو/ویب` | FastAPI, Flask web servers |
| `اردو/ڈیٹا_بیس` | MySQL, PostgreSQL, MongoDB, SQLite |
| `اردو/فائلیں` | Files, CSV, JSON, Excel, PDF |
| `اردو/رمز` | Encryption and cryptography |
| `اردو/ذہین` | Machine learning, data science |
| `اردو/کھرچنی` | Web scraping |
| `اردو/دھاگہ` | Threads and async tasks |
| `اردو/تاریخ` | Dates and times |
| `اردو/کرل` | HTTP client |
| `اردو/لاگ` | Logging |

**Example — importing a library:**

```urdu
درآمد { فاسٹ_اے_پی_آئی } سے "اردو/ویب"

متغیر ایپ = نیا فاسٹ_اے_پی_آئی({ عنوان: "میری API" })

@ایپ.حاصل("/")
فنکشن جڑ() {
    واپس { "پیغام": "السلام علیکم!" }
}

ایپ.چلائیں({ پورٹ: 8000 })
```

---

## CLI Quick Reference

| Command | What it does |
|---------|-------------|
| `urdu run file.urdu` | Run a program |
| `urdu repl` | Start interactive shell |
| `urdu compile file.urdu` | Transpile to Python |
| `urdu check file.urdu` | Check syntax only |
| `urdu version` | Show version |
| `urdu مدد` | Urdu help |
| `urdu نصب <package>` | Install a package |

---

## Next Steps

- Read the full **[Syntax Reference](docs/syntax/)** to learn all language features
- Browse **[Examples](docs/examples/)** for real programs you can run
- Explore **[Library Reference](docs/libraries/)** for web, database, ML, and more
- Try the **[Quick Start Guide](docs/quick-start.md)** for a structured tutorial

---

## Getting Help

- Run `urdu مدد` in your terminal for Urdu-language help
- Full documentation: [`docs/`](docs/) folder
- Report issues: https://github.com/ZahidServers/urdu-programming-language/issues
- Contact the author: zahid.wadiwale1234@gmail.com

---

<div dir="rtl" align="right">

## اگلا قدم

مکمل دستاویزات کے لیے [`docs/`](docs/) فولڈر دیکھیں۔  
سوال ہو تو: zahid.wadiwale1234@gmail.com

**تخلیق کار:** محمد زاہد وڈیوالے  
یہ پروجیکٹ اردو بولنے والوں کو پروگرامنگ کے قابل بنانے کے لیے بنایا گیا ہے۔

</div>
