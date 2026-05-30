# 4. Cryptography — رمز نگاری

**Difficulty:** Advanced — اعلیٰ  
**Time:** ~25 minutes

---

## Importing — درآمد

```urdu
درآمد { ہیش, متناسق, AES, غیر_متناسق, پاس_ورڈ, تصادفی, بنیاد64 } سے "اردو/رمز";
```

---

## Hashing — ہیش

One-way functions to verify data integrity. The same input always produces the same output.

```urdu
// SHA-256 (most common)
لکھو(ہیش.sha256("اردو"));
// 234d81e4dcbe229b248be0e241fc76ab84f0aef878c3cfb8ca7eb46e729742d0

// Urdu alias
لکھو(ہیش.ہیش_256("اردو"));     // same result

// SHA-512
لکھو(ہیش.sha512("hello"));     // 128-char hex string

// MD5 (not for security — use for checksums only)
لکھو(ہیش.md5("hello"));
// 5d41402abc4b2a76b9719d911017c592
```

**HMAC — پیغام توثیقی کوڈ:**

Verifies that a message was not tampered with and came from the right sender.

```urdu
متغیر دستخط = ہیش.hmac("پیغام", "راز_کلید");
لکھو(دستخط);    // hex digest
```

| Method | Description |
|--------|-------------|
| `ہیش.sha256(م)` / `ہیش.ہیش_256(م)` | SHA-256 digest |
| `ہیش.sha512(م)` | SHA-512 digest |
| `ہیش.md5(م)` | MD5 (checksums only) |
| `ہیش.blake2b(م)` / `ہیش.بلیک_2بی(م)` | BLAKE2b |
| `ہیش.hmac(م, کلید)` / `ہیش.ہمیک(م, ک)` | HMAC-SHA256 |
| `ہیش.pbkdf2(پاس, نمک)` / `ہیش.کلید_استخراج(...)` | PBKDF2 key derivation |

> **اردو:** `sha256` یا `ہیش_256` — دونوں ایک ہیں۔ ہیش یک طرفہ ہے — ظاہر نہیں کیا جا سکتا۔

---

## Symmetric Encryption — متناسق خفیہ نگاری

One key for both encryption and decryption. Uses Fernet (AES-128-CBC + HMAC).

```urdu
// Auto-generate key
متغیر رمز = نیا متناسق();
متغیر کلید_م = رمز.کلید;         // save this to decrypt later!
لکھو(کلید_م);

متغیر خفیہ = رمز.خفیہ_کریں("راز پیغام");
لکھو(خفیہ);                       // encrypted string

متغیر اصل = رمز.ظاہر_کریں(خفیہ);
لکھو(اصل);                        // راز پیغام
```

**With saved key — محفوظ کلید کے ساتھ:**

```urdu
// First time: generate and save key
متغیر نئی_کلید = متناسق.نئی_کلید();
لکھو(نئی_کلید);    // store this safely

// Later: use saved key
متغیر رمز2 = نیا متناسق(نئی_کلید);
متغیر خفیہ2 = رمز2.خفیہ_کریں("ڈیٹا");
لکھو(رمز2.ظاہر_کریں(خفیہ2));     // ڈیٹا
```

> **اردو:** `.کلید` خاصیت محفوظ کریں — اس کے بغیر ظاہر نہیں کیا جا سکتا۔

---

## AES-256-GCM Encryption

Stronger encryption with authentication. Recommended for new projects.

```urdu
متغیر اے = نیا AES();
لکھو(اے.کلید);    // base64-encoded 256-bit key

متغیر خفیہ = اے.خفیہ_کریں("اردو پیغام");
لکھو(اے.ظاہر_کریں(خفیہ));    // اردو پیغام
```

---

## RSA Asymmetric Encryption — غیر متناسق

Two keys: public key for encryption/verification, private key for decryption/signing.

```urdu
// Generate key pair
متغیر آر_ایس_اے = نیا غیر_متناسق(2048);

لکھو(آر_ایس_اے.عوامی_کلید());    // PEM format
لکھو(آر_ایس_اے.نجی_کلید());      // PEM format — keep secret!

// Encrypt with public key, decrypt with private key
متغیر خفیہ = آر_ایس_اے.خفیہ_کریں("راز");
لکھو(آر_ایس_اے.ظاہر_کریں(خفیہ));    // راز

// Digital signature — دستخط
متغیر دستخط_م = آر_ایس_اے.دستخط("دستاویز متن");
لکھو(آر_ایس_اے.تصدیق("دستاویز متن", دستخط_م));    // True
لکھو(آر_ایس_اے.تصدیق("تبدیل شدہ", دستخط_م));      // False
```

> **اردو:** `غیر_متناسق` میں عوامی کلید دوسروں کو دیں، نجی کلید خفیہ رکھیں۔ دستخط سے ثابت کریں کہ پیغام آپ کا ہے اور بدلا نہیں گیا۔

---

## Password Hashing — پاس ورڈ ہیش

**Never store passwords as plain text.** Use `پاس_ورڈ` which uses bcrypt:

```urdu
// Hash a password (slow on purpose — makes brute force harder)
متغیر ہیش_شدہ = پاس_ورڈ.ہیش("میراپاس_ورڈ");
لکھو(ہیش_شدہ);    // $2b$12$...

// Verify later
لکھو(پاس_ورڈ.جانچیں("میراپاس_ورڈ", ہیش_شدہ));    // True
لکھو(پاس_ورڈ.جانچیں("غلط_پاس_ورڈ", ہیش_شدہ));    // False
```

> **اردو:** `پاس_ورڈ.ہیش()` جان بوجھ کر سست ہے تاکہ طاقت سے اندازہ مشکل ہو۔ ہر بار مختلف نتیجہ آتا ہے لیکن `.جانچیں()` صحیح کام کرتا ہے۔

---

## Secure Random — محفوظ تصادفی

`تصادفی` uses the OS's cryptographically secure random source:

```urdu
// Secure token (for session IDs, API keys)
لکھو(تصادفی.ٹوکن(32));           // 64-char hex string
لکھو(تصادفی.ٹوکن_url(32));       // URL-safe base64

// OTP (One-Time Password)
لکھو(تصادفی.OTP(6));             // 6-digit code e.g. "042891"
لکھو(تصادفی.یک_وقتی_پاس_ورڈ(4)); // 4-digit OTP

// Random number in range
لکھو(تصادفی.عدد(1, 100));        // cryptographically secure int

// Random choice from list
لکھو(تصادفی.انتخاب(["الف", "ب", "ج"]));
```

---

## Base64 — بنیاد 64

Encode binary data as text (e.g., for sending in JSON or URLs):

```urdu
// Standard Base64
متغیر کوڈ_شدہ = بنیاد64.کوڈ("اردو");
لکھو(کوڈ_شدہ);                    // 2KfYsdiv2Yg=
لکھو(بنیاد64.ڈی_کوڈ(کوڈ_شدہ));   // اردو

// URL-safe Base64
متغیر url_م = بنیاد64.ربط_کوڈ("hello/world");
لکھو(url_م);
لکھو(بنیاد64.ربط_ڈی_کوڈ(url_م));  // hello/world
```

---

## Practical Example: Secure Storage — عملی مثال: محفوظ ذخیرہ

```urdu
درآمد { متناسق, ہیش, تصادفی } سے "اردو/رمز";
درآمد { فائل_لکھو, فائل_پڑھو } سے "اردو/فائلیں";

// Encrypt and save sensitive data
فنکشن محفوظ_لکھو(فائل_م, ڈیٹا, کلید) {
    متغیر رمز = نیا متناسق(کلید);
    فائل_لکھو(فائل_م, رمز.خفیہ_کریں(ڈیٹا));
}

// Load and decrypt
فنکشن محفوظ_پڑھو(فائل_م, کلید) {
    متغیر رمز = نیا متناسق(کلید);
    واپس رمز.ظاہر_کریں(فائل_پڑھو(فائل_م));
}

// Generate key once and save separately
متغیر کلید_م = متناسق.نئی_کلید();
محفوظ_لکھو("راز.enc", "API_KEY=abc123", کلید_م);
لکھو(محفوظ_پڑھو("راز.enc", کلید_م));    // API_KEY=abc123
```

---

## Quick Reference — فوری حوالہ

| Class | Purpose |
|-------|---------|
| `ہیش` | SHA-256, SHA-512, MD5, HMAC, PBKDF2 |
| `متناسق` | Fernet symmetric encryption (AES-128) |
| `AES` | AES-256-GCM encryption |
| `غیر_متناسق` | RSA encryption + digital signatures |
| `پاس_ورڈ` | bcrypt password hashing |
| `تصادفی` | Cryptographically secure random |
| `بنیاد64` | Base64 encode/decode |

---

[← Previous: HTTP Client](03-http-client.md) | [Next: Databases →](05-databases.md)
