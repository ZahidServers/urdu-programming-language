# 10. Web Scraping — ویب کھرچنی

**Difficulty:** Advanced — اعلیٰ  
**Time:** ~25 minutes

---

## Importing — درآمد

```urdu
درآمد { صفحہ_بناؤ, کھرچو } سے "اردو/کھرچنی";
```

Requires: `pip install beautifulsoup4 requests`

---

## Parse HTML String — HTML تجزیہ

Use `صفحہ_بناؤ()` when you already have the HTML text:

```urdu
متغیر html = "<html><head><title>خوش آمدید</title></head>
<body>
  <h1 id='سرخی'>اردو پروگرامنگ</h1>
  <p class='info'>یہ اردو پروگرامنگ لینگویج ہے۔</p>
  <a href='/گھر'>گھر</a>
  <a href='/بارے'>بارے میں</a>
</body></html>";

متغیر ص = صفحہ_بناؤ(html);
لکھو(ص.عنوان);    // خوش آمدید
```

---

## Fetch a URL — URL سے ڈاؤن لوڈ

`کھرچو()` is async — fetches + parses in one step:

```urdu
غیر_متزامن فنکشن مرکزی() {
    متغیر ص = انتظار کھرچو("https://example.com");
    لکھو(ص.عنوان);
    لکھو(ص.صاف_متن.slice(0, 100));
}

انتظار مرکزی();
```

**Custom headers (e.g. to mimic a browser):**

```urdu
متغیر ص = انتظار کھرچو(
    "https://example.com",
    سرخط={ "User-Agent": "Mozilla/5.0" }
);
```

---

## Element Content — عنصر کا مواد

```urdu
متغیر ہیڈنگ = ص.تلاش("h1");

لکھو(ہیڈنگ.متن);        // all text (may include whitespace)
لکھو(ہیڈنگ.صاف_متن);   // text with whitespace stripped
لکھو(ہیڈنگ.اندرونی_html);  // inner HTML
لکھو(ہیڈنگ.بیرونی_html);  // outer HTML (including the tag itself)
لکھو(ہیڈنگ.خوبصورت);    // prettified / indented HTML
لکھو(ہیڈنگ.ٹیگ);        // "h1"
```

---

## Attributes — خصوصیات

```urdu
متغیر لنک = ص.تلاش("a");
لکھو(لنک["href"]);            // /گھر
لکھو(لنک["class"]);           // attribute value (or None)
لکھو(لنک.خصوصیات.href);      // dot-access on all attrs
```

---

## Finding Elements — عناصر تلاش

### `.تلاش()` — first match

```urdu
// By tag name
متغیر پیرا = ص.تلاش("p");

// By tag + attributes
متغیر خاص = ص.تلاش("div", { "class": "container" });
متغیر شناخت_م = ص.تلاش("section", { "id": "مضمون" });
```

### `.سب_تلاش()` — all matches

```urdu
// All <a> tags
متغیر لنکس = ص.سب_تلاش("a");
لکھو(لمبائی(لنکس));    // number of links

// First 5 paragraphs
متغیر پیراز = ص.سب_تلاش("p", حد=5);

// All elements with a class
متغیر کارڈز = ص.سب_تلاش("div", { "class": "card" });

// Iterate
کے_لیے (متغیر لنک میں لنکس) {
    لکھو(لنک["href"]);
    لکھو(لنک.صاف_متن);
}
```

### `.چنو()` — CSS selector

```urdu
// All <p> inside .article
متغیر پیراز = ص.چنو("article p");
لکھو(لمبائی(پیراز));

// By ID
متغیر اہم = ص.چنو("#اہم");

// By class
متغیر کارڈز = ص.چنو(".card");

// Nested
متغیر لنکس = ص.چنو("nav a");
```

### `.ایک_چنو()` — first CSS match

```urdu
متغیر ٹائٹل = ص.ایک_چنو("h1");
لکھو(ٹائٹل.صاف_متن);
```

---

## Navigation — عناصر کے درمیان

```urdu
// Children of an element
متغیر بچے_م = ص.بچے;
کے_لیے (متغیر بچہ میں بچے_م) {
    لکھو(بچہ.ٹیگ);
}

// Parent
متغیر والد_م = ہیڈنگ.والد;
لکھو(والد_م.ٹیگ);    // body

// Siblings
متغیر اگلا_م = ہیڈنگ.اگلا;     // next element sibling
متغیر پچھلا_م = ہیڈنگ.پچھلا;   // previous element sibling
```

---

## Practical Example: Scrape Links — عملی مثال

```urdu
درآمد { کھرچو } سے "اردو/کھرچنی";

غیر_متزامن فنکشن لنکس_نکالو(url) {
    کوشش {
        متغیر ص = انتظار کھرچو(url, سرخط={
            "User-Agent": "Mozilla/5.0 (compatible; UrdBot/1.0)"
        });

        لکھو(`عنوان: ${ص.عنوان}`);

        متغیر تمام_لنکس = ص.سب_تلاش("a");
        متغیر بیرونی = [];

        کے_لیے (متغیر لنک میں تمام_لنکس) {
            متغیر href = لنک["href"];
            اگر (href اور href.startsWith("http")) {
                بیرونی.شامل(href);
            }
        }

        لکھو(`کل لنکس: ${لمبائی(تمام_لنکس)}`);
        لکھو(`بیرونی لنکس: ${لمبائی(بیرونی)}`);
        واپس بیرونی;

    } پکڑو (غلطی_م) {
        لکھو(`غلطی: ${غلطی_م.message}`);
        واپس [];
    }
}

انتظار لنکس_نکالو("https://example.com");
```

---

## Practical Example: Parse Product List — مصنوعات کی فہرست

```urdu
درآمد { صفحہ_بناؤ } سے "اردو/کھرچنی";

متغیر html = "
<div class='پروڈکٹس'>
  <div class='پروڈکٹ' data-id='1'>
    <h2 class='نام'>اردو کا سفر</h2>
    <span class='قیمت'>500</span>
    <span class='دستیاب'>دستیاب</span>
  </div>
  <div class='پروڈکٹ' data-id='2'>
    <h2 class='نام'>پروگرامنگ گائیڈ</h2>
    <span class='قیمت'>750</span>
    <span class='دستیاب'>ختم</span>
  </div>
</div>
";

متغیر ص = صفحہ_بناؤ(html);
متغیر پروڈکٹس = ص.سب_تلاش("div", { "class": "پروڈکٹ" });

کے_لیے (متغیر پی میں پروڈکٹس) {
    متغیر نام_م = پی.تلاش("h2").صاف_متن;
    متغیر قیمت_م = پی.تلاش("span", { "class": "قیمت" }).صاف_متن;
    متغیر حالت_م = پی.تلاش("span", { "class": "دستیاب" }).صاف_متن;
    متغیر شناخت_م = پی["data-id"];
    لکھو(`[${شناخت_م}] ${نام_م} — ${قیمت_م} — ${حالت_م}`);
}
```

Output:
```
[1] اردو کا سفر — 500 — دستیاب
[2] پروگرامنگ گائیڈ — 750 — ختم
```

---

## Element Quick Reference — فوری حوالہ

| Property / Method | Description |
|-------------------|-------------|
| `.متن` | All text content |
| `.صاف_متن` | Text (whitespace stripped) |
| `.اندرونی_html` | Inner HTML |
| `.بیرونی_html` | Outer HTML |
| `.ٹیگ` | Tag name ("div", "p", …) |
| `.شناخت` | `id` attribute value |
| `.خصوصیات` | All attributes as object |
| `[attr]` | Get attribute by name |
| `.والد` | Parent element |
| `.بچے` | List of child elements |
| `.اگلا` | Next sibling element |
| `.پچھلا` | Previous sibling element |
| `.تلاش(tag, attrs)` | First matching descendant |
| `.سب_تلاش(tag, attrs, حد)` | All matching descendants |
| `.چنو(css)` | CSS selector — all matches |
| `.ایک_چنو(css)` | CSS selector — first match |

---

[← Previous: Text Processing](09-text-processing.md) | [↑ Advanced Index](index.md)
