# Cryptography Library — اردو/رمز

The `اردو/رمز` library provides hashing, symmetric encryption (Fernet and AES-256-GCM), and asymmetric encryption (RSA) — all with Urdu-named methods.

> **اردو:** `اردو/رمز` لائبریری ہیش (hash)، یکطرفہ خفیہ کاری (Fernet / AES-256-GCM)، اور دو کلیدی خفیہ کاری (RSA) اردو ناموں کے ساتھ فراہم کرتی ہے۔

**Import:**

```urdu
درآمد { ہیش, متناسق, AES, غیر_متناسق } سے "اردو/رمز"
```

**Backend:** Python `hashlib`, `hmac`, `cryptography` package.

---

## Table of Contents — فہرست مضامین

1. [Hashing — ہیش](#hashing--ہیش)
2. [Symmetric Encryption — متناسق (Fernet)](#symmetric-encryption--متناسق-fernet)
3. [AES-256-GCM — AES](#aes-256-gcm--AES)
4. [RSA — غیر_متناسق](#rsa--غیر_متناسق)
5. [Examples](#examples)

---

## Hashing — ہیش

All methods are **static** — call directly on the class without `نیا`.

> **اردو:** ہیش (hash) ڈیٹا کا ایک یک طرفہ خلاصہ ہے۔ تمام طریقے جامد (static) ہیں — `نیا` کے بغیر کلاس پر براہ راست کال کریں۔

| Method | Urdu alias | Returns | Description |
|--------|-----------|---------|-------------|
| `ہیش.sha256(ڈیٹا)` | `ہیش.ہیش_256(ڈیٹا)` | hex string | SHA-256 hash |
| `ہیش.sha512(ڈیٹا)` | `ہیش.ہیش_512(ڈیٹا)` | hex string | SHA-512 hash |
| `ہیش.md5(ڈیٹا)` | `ہیش.ایم_ڈی_5(ڈیٹا)` | hex string | MD5 hash (not for security) |
| `ہیش.blake2b(ڈیٹا, digest_size=32)` | `ہیش.بلیک_2بی(ڈیٹا)` | hex string | BLAKE2b hash |
| `ہیش.hmac(ڈیٹا, کلید, الگورتھم="sha256")` | `ہیش.ہمیک(ڈیٹا, کلید)` | hex string | HMAC authentication code |
| `ہیش.pbkdf2(پاسورڈ, نمک, دور=100000, طول=32)` | `ہیش.کلید_استخراج(پاسورڈ, نمک)` | hex string | PBKDF2 key derivation |

**Input:** `ڈیٹا` can be a string or bytes. Strings are encoded as UTF-8 automatically.

### Hashing examples — ہیش کی مثالیں

```urdu
درآمد { ہیش } سے "اردو/رمز"

// SHA-256
متغیر h = ہیش.sha256("السلام علیکم")
لکھو("SHA-256:", h)

// SHA-512 (Urdu alias)
متغیر h512 = ہیش.ہیش_512("اردو پروگرامنگ")
لکھو("SHA-512:", h512)

// MD5 — صرف checksums کے لیے، پاسورڈ کے لیے نہیں
متغیر md5 = ہیش.md5("test")
لکھو("MD5:", md5)

// BLAKE2b — تیز اور محفوظ
متغیر b2 = ہیش.بلیک_2بی("میرا ڈیٹا")
لکھو("BLAKE2b:", b2)

// HMAC — پیغام کی صداقت جانچنا
متغیر سر = ہیش.ہمیک("پیغام متن", "خفیہ_کلید")
لکھو("HMAC:", سر)

// PBKDF2 — پاسورڈ سے کلید بنانا
متغیر نمک = "تصادفی_نمک_123"
متغیر کلید = ہیش.کلید_استخراج("میرا_پاسورڈ", نمک)
لکھو("PBKDF2:", کلید)
```

---

## Symmetric Encryption — متناسق (Fernet)

Fernet guarantees that a message encrypted with a given key cannot be manipulated or read without that key. Uses AES-128-CBC + HMAC-SHA256.

> **اردو:** متناسق (symmetric) خفیہ کاری میں ایک ہی کلید سے ڈیٹا خفیہ کرنا (encrypt) اور ظاہر کرنا (decrypt) ممکن ہے۔ Fernet، AES-128-CBC اور HMAC-SHA256 استعمال کرتا ہے۔

```urdu
متغیر enc = نیا متناسق(کلید_یا_خالی)
```

- Pass `خالی` to auto-generate a new key.
- Pass an existing key string to reuse it.

| Method / Property | Returns | Description |
|-------------------|---------|-------------|
| `متناسق.نئی_کلید()` | string | **Static.** Generate a new Fernet key |
| `enc.کلید` | string | The current encryption key |
| `enc.خفیہ_کریں(پیغام)` | string | Encrypt a plaintext string → ciphertext |
| `enc.ظاہر_کریں(خفیہ)` | string | Decrypt ciphertext → plaintext |

### Example — Fernet encryption

> **اردو:** مثال — Fernet سے پیغام خفیہ کرنا اور ظاہر کرنا

```urdu
درآمد { متناسق } سے "اردو/رمز"

// نئی کلید بنائیں
متغیر کلید = متناسق.نئی_کلید()
لکھو("کلید:", کلید)

متغیر enc = نیا متناسق(کلید)

متغیر اصل_پیغام = "یہ خفیہ پیغام ہے — صرف آپ کے لیے"
متغیر خفیہ    = enc.خفیہ_کریں(اصل_پیغام)
لکھو("خفیہ:", خفیہ)

متغیر واضح = enc.ظاہر_کریں(خفیہ)
لکھو("واضح:", واضح)

// تصدیق
لکھو("مماثل:", واضح == اصل_پیغام)
```

---

## AES-256-GCM — AES

AES-256 in GCM (Galois/Counter Mode) provides authenticated encryption with optional additional data (AAD).

> **اردو:** AES-256-GCM توثیق شدہ خفیہ کاری فراہم کرتا ہے۔ یہ ڈیٹا خفیہ کرنے کے ساتھ سالمیت بھی جانچتا ہے۔

```urdu
متغیر aes = نیا AES(کلید_یا_خالی)
```

Pass `خالی` to auto-generate a 256-bit key.

| Method / Property | Returns | Description |
|-------------------|---------|-------------|
| `aes.کلید` | string | The AES key (hex or base64) |
| `aes.خفیہ_کریں(پیغام, اضافی=null)` | string | Encrypt; optionally bind additional data |
| `aes.ظاہر_کریں(خفیہ)` | string | Decrypt and authenticate |

```urdu
درآمد { AES } سے "اردو/رمز"

متغیر aes = نیا AES(خالی)     // نئی کلید خودکار بنائیں
لکھو("AES کلید:", aes.کلید)

متغیر خفیہ = aes.خفیہ_کریں("حساس ڈیٹا: اکاؤنٹ نمبر 12345")
لکھو("خفیہ:", خفیہ)

متغیر واضح = aes.ظاہر_کریں(خفیہ)
لکھو("واضح:", واضح)

// کلید دوبارہ استعمال
متغیر aes2 = نیا AES(aes.کلید)
لکھو("دوبارہ خفیہ:", aes2.ظاہر_کریں(خفیہ))
```

---

## RSA — غیر_متناسق

Asymmetric (public-key) encryption and digital signatures using RSA.

> **اردو:** غیر متناسق (asymmetric) خفیہ کاری میں دو کلیدیں ہوتی ہیں — عوامی کلید سے خفیہ کریں (encrypt) اور نجی کلید سے ظاہر کریں (decrypt)۔ RSA دستخط (digital signature) کے لیے بھی استعمال ہوتا ہے۔

```urdu
متغیر rsa = نیا غیر_متناسق(بٹ=2048)
```

Default key size is 2048 bits. Use 4096 for extra security.

| Property / Method | Returns | Description |
|-------------------|---------|-------------|
| `rsa.عوامی_کلید` | string | PEM-encoded public key |
| `rsa.نجی_کلید` | string | PEM-encoded private key |
| `rsa.خفیہ_کریں(پیغام)` | string | Encrypt with **public key** |
| `rsa.ظاہر_کریں(خفیہ)` | string | Decrypt with **private key** |
| `rsa.دستخط(ڈیٹا)` | string | Sign data with **private key** |
| `rsa.تصدیق(ڈیٹا, دستخط)` | bool | Verify signature with **public key** |

```urdu
درآمد { غیر_متناسق } سے "اردو/رمز"

// نئی RSA کلیدیں بنائیں
متغیر rsa = نیا غیر_متناسق(2048)
لکھو("عوامی کلید:\n", rsa.عوامی_کلید)

// خفیہ کاری
متغیر خفیہ = rsa.خفیہ_کریں("یہ خفیہ پیغام ہے")
لکھو("\nخفیہ:", خفیہ.substring(0, 60) + "...")

متغیر واضح = rsa.ظاہر_کریں(خفیہ)
لکھو("واضح:", واضح)

// دستخط اور تصدیق
متغیر ڈیٹا = "یہ اہم دستاویز ہے"
متغیر دستخط = rsa.دستخط(ڈیٹا)
لکھو("\nدستخط:", دستخط.substring(0, 60) + "...")

متغیر درست = rsa.تصدیق(ڈیٹا, دستخط)
لکھو("تصدیق:", درست)   // سچ
```

---

## Examples — مثالیں

### Example 1 — Password storage with PBKDF2

> **اردو:** مثال ۱ — PBKDF2 سے پاسورڈ محفوظ طریقے سے ذخیرہ کرنا

```urdu
درآمد { ہیش } سے "اردو/رمز"

// ═══════════════════════════════════════
// محفوظ پاسورڈ ذخیرہ کاری
// ═══════════════════════════════════════

فنکشن پاسورڈ_محفوظ_کریں(پاسورڈ) {
    متغیر نمک = "rand_" + Date.now().toString();
    متغیر ہیش_قدر = ہیش.کلید_استخراج(پاسورڈ, نمک, دور=200000);
    واپس { نمک, ہیش: ہیش_قدر };
}

فنکشن پاسورڈ_جانچیں(درج_شدہ_پاسورڈ, محفوظ) {
    متغیر جانچ_ہیش = ہیش.کلید_استخراج(
        درج_شدہ_پاسورڈ,
        محفوظ.نمک,
        دور=200000
    );
    واپس جانچ_ہیش == محفوظ.ہیش;
}

// استعمال
متغیر محفوظ_پاسورڈ = پاسورڈ_محفوظ_کریں("MyP@ssw0rd!")
لکھو("محفوظ ہیش:", محفوظ_پاسورڈ.ہیش)

لکھو("درست پاسورڈ:", پاسورڈ_جانچیں("MyP@ssw0rd!", محفوظ_پاسورڈ))   // سچ
لکھو("غلط پاسورڈ:",  پاسورڈ_جانچیں("wrongpassword", محفوظ_پاسورڈ))  // جھوٹ
```

### Example 2 — File integrity check

> **اردو:** مثال ۲ — SHA-256 ہیش سے فائل (file) کی سالمیت جانچنا

```urdu
درآمد { ہیش } سے "اردو/رمز"
درآمد { فائل_پڑھو } سے "اردو/نظام_فائل"

فنکشن فائل_ہیش(راستہ) {
    متغیر مواد = فائل_پڑھو(راستہ, "bytes");
    واپس ہیش.sha256(مواد);
}

فنکشن سالمیت_جانچیں(راستہ, متوقع_ہیش) {
    متغیر اصل_ہیش = فائل_ہیش(راستہ);
    اگر (اصل_ہیش == متوقع_ہیش) {
        لکھو("✓ فائل سالم ہے:", راستہ);
        واپس سچ;
    } ورنہ {
        لکھو("✗ فائل تبدیل ہو گئی ہے!", راستہ);
        واپس جھوٹ;
    }
}

// ڈاؤن لوڈ کے بعد تصدیق
متغیر متوقع = "a3f5b9c2d8e1f4a7b0c3d6e9f2a5b8c1d4e7f0a3b6c9d2e5f8a1b4c7d0e3f6a9"
سالمیت_جانچیں("ڈاؤن لوڈ.zip", متوقع)
```

### Example 3 — Encrypted configuration file

> **اردو:** مثال ۳ — Fernet سے ترتیب فائل (config file) خفیہ کرنا اور ظاہر کرنا

```urdu
درآمد { متناسق } سے "اردو/رمز"
درآمد { فائل_پڑھو, فائل_لکھو } سے "اردو/نظام_فائل"

// ═══════════════════════════════════════
// خفیہ config فائل — لکھنا اور پڑھنا
// ═══════════════════════════════════════

مستقل کلید_فائل = "encryption.key"
مستقل config_فائل = "config.enc"

فنکشن config_محفوظ_کریں(config_ڈکشنری) {
    متغیر کلید;
    کوشش {
        کلید = فائل_پڑھو(کلید_فائل);
    } پکڑو (غ) {
        کلید = متناسق.نئی_کلید();
        فائل_لکھو(کلید_فائل, کلید);
        لکھو("نئی کلید بنائی:", کلید_فائل);
    }

    متغیر enc = نیا متناسق(کلید);
    متغیر json_متن = JSON.stringify(config_ڈکشنری, خالی, 2);
    متغیر خفیہ = enc.خفیہ_کریں(json_متن);
    فائل_لکھو(config_فائل, خفیہ);
    لکھو("config محفوظ:", config_فائل);
}

فنکشن config_لوڈ_کریں() {
    متغیر کلید = فائل_پڑھو(کلید_فائل);
    متغیر enc = نیا متناسق(کلید);
    متغیر خفیہ = فائل_پڑھو(config_فائل);
    متغیر json_متن = enc.ظاہر_کریں(خفیہ);
    واپس JSON.parse(json_متن);
}

// استعمال
config_محفوظ_کریں({
    db_host:     "localhost",
    db_password: "S3cr3tP@ss!",
    api_key:     "sk-abc123xyz",
    admin_pin:   "9876"
})

متغیر config = config_لوڈ_کریں()
لکھو("DB:", config.db_host)
لکھو("API کلید:", config.api_key)
```

### Example 4 — JWT-like signed token

> **اردو:** مثال ۴ — HMAC-SHA256 دستخط شدہ ٹوکن بنانا اور جانچنا

```urdu
درآمد { ہیش } سے "اردو/رمز"

// ═══════════════════════════════════════
// HMAC-SHA256 دستخط شدہ ٹوکن
// ═══════════════════════════════════════

مستقل خفیہ_کلید = "super-secret-key-do-not-share"

فنکشن ٹوکن_بنائیں(صارف_ڈیٹا) {
    متغیر payload = JSON.stringify({
        ڈیٹا: صارف_ڈیٹا,
        وقت: Date.now(),
        میعاد: Date.now() + (60 * 60 * 1000)  // 1 گھنٹہ
    });
    متغیر payload_b64 = btoa(payload);
    متغیر دستخط = ہیش.ہمیک(payload_b64, خفیہ_کلید);
    واپس `${payload_b64}.${دستخط}`;
}

فنکشن ٹوکن_جانچیں(ٹوکن) {
    کوشش {
        متغیر [payload_b64, ملا_دستخط] = ٹوکن.split(".");
        متغیر متوقع_دستخط = ہیش.ہمیک(payload_b64, خفیہ_کلید);

        اگر (ملا_دستخط != متوقع_دستخط) {
            واپس { درست: جھوٹ, غلطی: "دستخط غلط" };
        }

        متغیر payload = JSON.parse(atob(payload_b64));

        اگر (Date.now() > payload.میعاد) {
            واپس { درست: جھوٹ, غلطی: "ٹوکن میعاد ختم" };
        }

        واپس { درست: سچ, ڈیٹا: payload.ڈیٹا };

    } پکڑو (ے) {
        واپس { درست: جھوٹ, غلطی: ے.message };
    }
}

// استعمال
متغیر ٹوکن = ٹوکن_بنائیں({ id: 42, نام: "احمد", کردار: "admin" })
لکھو("ٹوکن:", ٹوکن.substring(0, 60) + "...")

متغیر نتیجہ = ٹوکن_جانچیں(ٹوکن)
لکھو("درست:", نتیجہ.درست)
لکھو("صارف:", نتیجہ.ڈیٹا.نام)

// تبدیل شدہ ٹوکن جانچیں
متغیر نتیجہ2 = ٹوکن_جانچیں(ٹوکن + "tampered")
لکھو("تبدیل شدہ ٹوکن:", نتیجہ2.غلطی)
```

### Example 5 — RSA key exchange for secure channel

> **اردو:** مثال ۵ — RSA اور Fernet ملا کر محفوظ مواصلاتی چینل بنانا۔ RSA سے Fernet کلید خفیہ کریں (encrypt) اور Fernet سے ڈیٹا خفیہ کریں۔

```urdu
درآمد { غیر_متناسق, متناسق } سے "اردو/رمز"

// ═══════════════════════════════════════
// RSA + Fernet ملا کر محفوظ چینل
// ═══════════════════════════════════════

// - RSA سے Fernet کلید بھیجیں
// - Fernet سے ڈیٹا خفیہ کریں

// الف: RSA کلیدیں بنائیں
متغیر rsa = نیا غیر_متناسق(2048)
لکھو("RSA کلیدیں بنائی گئیں")

// ب: Fernet کلید بنائیں (sessions کی کلید)
متغیر fernet_کلید = متناسق.نئی_کلید()

// ج: Fernet کلید کو RSA عوامی کلید سے خفیہ کریں
متغیر خفیہ_fernet_کلید = rsa.خفیہ_کریں(fernet_کلید)
لکھو("Fernet کلید RSA سے خفیہ ہوئی")

// د: وصول کنندہ RSA نجی کلید سے Fernet کلید حاصل کرے
متغیر بحال_fernet_کلید = rsa.ظاہر_کریں(خفیہ_fernet_کلید)

// ہـ: اب Fernet سے ڈیٹا خفیہ کریں
متغیر enc = نیا متناسق(بحال_fernet_کلید)
متغیر خفیہ_ڈیٹا = enc.خفیہ_کریں("بینک اکاؤنٹ: 1234-5678-9012")
لکھو("ڈیٹا خفیہ ہوا")

// و: ڈیکرپٹ کریں
متغیر واضح_ڈیٹا = enc.ظاہر_کریں(خفیہ_ڈیٹا)
لکھو("واضح ڈیٹا:", واضح_ڈیٹا)
```

---

*Previous: [File Utilities →](files.md) | Next: [Date & Time →](datetime.md)*
