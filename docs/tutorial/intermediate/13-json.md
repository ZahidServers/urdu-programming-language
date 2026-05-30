# 13. JSON — جے سان

**Difficulty:** Intermediate — متوسط  
**Time:** ~20 minutes

---

## What is JSON? — جے سان کیا ہے؟

JSON (JavaScript Object Notation) is a text format for storing and sending structured data. Urdu PL has **built-in** JSON support — no import needed.

> **اردو:** JSON ڈیٹا کو متن کے طور پر محفوظ کرنے اور بھیجنے کا طریقہ ہے۔ اردو PL میں یہ بلٹ-ان ہے — درآمد کی ضرورت نہیں۔

---

## Object to JSON — شے سے جے سان

`JSON_لکھو()` converts any object/list to a JSON string:

```urdu
متغیر شخص = { نام: "احمد", عمر: 25, شہر: "کراچی" };
لکھو(JSON_لکھو(شخص));
// {"نام": "احمد", "عمر": 25, "شہر": "کراچی"}

// List to JSON
لکھو(JSON_لکھو([1, 2, 3, "اردو"]));
// [1, 2, 3, "اردو"]

// Booleans and null
لکھو(JSON_لکھو({ فعال: سچ, قدر: خالی }));
// {"فعال": true, "قدر": null}
```

---

## Pretty Print — صاف فارمیٹ

Pass an indent number for readable output:

```urdu
متغیر ڈیٹا = {
    طلباء: [
        { نام: "احمد",  نمبر: 85 },
        { نام: "فاطمہ", نمبر: 92 }
    ],
    مجموع: 2
};

لکھو(JSON_لکھو(ڈیٹا, 2));
```

Output:
```json
{
  "طلباء": [
    {
      "نام": "احمد",
      "نمبر": 85
    },
    {
      "نام": "فاطمہ",
      "نمبر": 92
    }
  ],
  "مجموع": 2
}
```

> **اردو:** `JSON_لکھو(ڈیٹا, 2)` — دوسرا پیرامیٹر انڈینٹ (space count) ہے۔ بغیر انڈینٹ ایک سطر میں آتا ہے۔

---

## JSON to Object — جے سان سے شے

`JSON_پڑھو()` parses a JSON string back to an object:

```urdu
متغیر json_م = "{\"نام\": \"علی\", \"عمر\": 30}";
متغیر آبجیکٹ = JSON_پڑھو(json_م);
لکھو(آبجیکٹ["نام"]);    // علی
لکھو(آبجیکٹ["عمر"]);    // 30
```

> **اردو:** `JSON_پڑھو()` JSON متن کو واپس شے یا فہرست میں بدلتا ہے۔

---

## Round-Trip — آمد و رفت

```urdu
متغیر اصل = {
    زبان: "اردو",
    نسخہ: 1,
    خصوصیات: ["متغیر", "فنکشن", "کلاس"]
};

// Serialize
متغیر json_s = JSON_لکھو(اصل);
لکھو(json_s);

// Deserialize
متغیر بحال = JSON_پڑھو(json_s);
لکھو(بحال["زبان"]);
لکھو(بحال["خصوصیات"][0]);    // متغیر
```

---

## JSON with Files — جے سان اور فائلیں

Save and load JSON data from disk:

```urdu
درآمد { فائل_لکھو, فائل_پڑھو } سے "اردو/فائلیں";

// Save to file
متغیر ترتیبات = { زبان: "اردو", تھیم: "تاریک", فونٹ: 14 };
فائل_لکھو("ترتیبات.json", JSON_لکھو(ترتیبات, 2));

// Load from file
متغیر لوڈ = JSON_پڑھو(فائل_پڑھو("ترتیبات.json"));
لکھو(لوڈ["تھیم"]);    // تاریک
```

---

## JSON Type Mapping — اقسام کا تبادلہ

| JSON Type | Urdu PL |
|-----------|---------|
| `string` | `متن` |
| `number` | `عدد` |
| `boolean true` | `سچ` |
| `boolean false` | `جھوٹ` |
| `null` | `خالی` |
| `array [...]` | `فہرست` |
| `object {...}` | `شے` |

---

## Practical Example: Student Records — عملی مثال: طلباء کا ریکارڈ

```urdu
درآمد { فائل_لکھو, فائل_پڑھو, فائل_موجود } سے "اردو/فائلیں";

فنکشن ریکارڈ_محفوظ(فائل_ر, ریکارڈ) {
    فائل_لکھو(فائل_ر, JSON_لکھو(ریکارڈ, 2));
}

فنکشن ریکارڈ_لوڈ(فائل_ر) {
    اگر (نہیں فائل_موجود(فائل_ر)) { واپس []; }
    واپس JSON_پڑھو(فائل_پڑھو(فائل_ر));
}

متغیر طلباء = [
    { نام: "احمد",  نمبر: 85 },
    { نام: "فاطمہ", نمبر: 92 }
];

ریکارڈ_محفوظ("طلباء.json", طلباء);
متغیر لوڈ = ریکارڈ_لوڈ("طلباء.json");
لکھو(`${لوڈ[0].نام}: ${لوڈ[0].نمبر}`);    // احمد: 85
```

---

## Key Points — اہم نکات

- `JSON_لکھو(شے)` — object/list → JSON string (built-in, no import)
- `JSON_لکھو(شے, 2)` — pretty-print with 2-space indent
- `JSON_پڑھو(متن)` — JSON string → object/list
- `سچ` → `true`, `جھوٹ` → `false`, `خالی` → `null` in JSON
- Combine with `فائل_لکھو/پڑھو` to persist data to disk

> **اردو:** `JSON_لکھو` شے کو متن میں، `JSON_پڑھو` متن کو شے میں بدلتا ہے — کوئی درآمد نہیں چاہیے۔

---

[← Previous: Math](12-math.md) | [Next: Type Conversion →](14-type-conversion.md)
