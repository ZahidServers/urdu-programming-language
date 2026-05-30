# 5. Databases — ڈیٹا بیس

**Difficulty:** Advanced — اعلیٰ  
**Time:** ~30 minutes

---

## Importing — درآمد

```urdu
// SQLite — no extra install needed
درآمد { ایس_کیو_لائٹ } سے "اردو/ڈیٹا_بیس";

// MySQL
درآمد { مائی_ایس_کیو_ایل } سے "اردو/ڈیٹا_بیس";

// PostgreSQL
درآمد { پوسٹ_گریس } سے "اردو/ڈیٹا_بیس";

// MongoDB
درآمد { مونگو_ڈی_بی } سے "اردو/ڈیٹا_بیس";
```

> **اردو:** تمام ڈیٹا بیس طریقے `غیر_متزامن` (async) ہیں — `انتظار` کے ساتھ استعمال کریں۔

---

## SQLite — ایس کیو لائٹ (No Install Needed)

SQLite is built into Python — perfect for local apps, testing, and small projects.

```urdu
درآمد { ایس_کیو_لائٹ } سے "اردو/ڈیٹا_بیس";

غیر_متزامن فنکشن مرکزی() {
    // In-memory database (lost when program ends)
    متغیر ڈب = نیا ایس_کیو_لائٹ(":memory:");

    // File-based database (persists to disk)
    // متغیر ڈب = نیا ایس_کیو_لائٹ("میرا_ڈیٹا.db");

    انتظار ڈب.جوڑیں();

    // Create table
    انتظار ڈب.چلائیں("CREATE TABLE طلباء (شناخت INTEGER PRIMARY KEY, نام TEXT, نمبر INTEGER)");

    // Insert rows — use ? for parameters (prevents SQL injection)
    انتظار ڈب.چلائیں("INSERT INTO طلباء (نام, نمبر) VALUES (?, ?)", ["احمد", 85]);
    انتظار ڈب.چلائیں("INSERT INTO طلباء (نام, نمبر) VALUES (?, ?)", ["فاطمہ", 92]);
    انتظار ڈب.چلائیں("INSERT INTO طلباء (نام, نمبر) VALUES (?, ?)", ["علی", 78]);

    // SELECT all rows
    متغیر صفوف = انتظار ڈب.سوال("SELECT * FROM طلباء");
    لکھو(لمبائی(صفوف));        // 3

    // Access columns by name using dot notation
    لکھو(صفوف[0].نام);         // احمد
    لکھو(صفوف[1].نمبر);        // 92

    // SELECT with WHERE
    متغیر بہترین = انتظار ڈب.سوال("SELECT * FROM طلباء WHERE نمبر > ?", [80]);
    لکھو(لمبائی(بہترین));      // 2

    // UPDATE
    انتظار ڈب.چلائیں("UPDATE طلباء SET نمبر = ? WHERE نام = ?", [95, "احمد"]);

    // DELETE
    انتظار ڈب.چلائیں("DELETE FROM طلباء WHERE نمبر < 80");

    انتظار ڈب.منقطع();
}

انتظار مرکزی();
```

### جدول بنائیں Shortcut — SQLite only

```urdu
انتظار ڈب.جدول_بنائیں("کورسز", {
    شناخت: "INTEGER PRIMARY KEY",
    عنوان: "TEXT NOT NULL",
    کریڈٹ: "INTEGER DEFAULT 3"
});
```

---

## Core Methods — بنیادی طریقے

All database classes share the same interface:

| Method | Returns | Description |
|--------|---------|-------------|
| `انتظار .جوڑیں()` | self | Open connection |
| `انتظار .منقطع()` | — | Close connection |
| `انتظار .سوال(sql, params=[])` | list | SELECT — returns rows with dot-access |
| `انتظار .چلائیں(sql, params=[])` | int | INSERT/UPDATE/DELETE — returns row count |

> **اردو:** `.سوال()` SELECT کے لیے، `.چلائیں()` INSERT/UPDATE/DELETE کے لیے۔ ہمیشہ `?` پیرامیٹر استعمال کریں — SQL انجیکشن سے بچاؤ ہوگا۔

---

## Transactions — لین دین

Group multiple operations so they all succeed or all fail together:

```urdu
غیر_متزامن فنکشن بینک_منتقلی(ڈب, بھیجنے_والا, پانے_والا, رقم) {
    انتظار ڈب.لین_دین_شروع();
    کوشش {
        انتظار ڈب.چلائیں(
            "UPDATE کھاتے SET رقم = رقم - ? WHERE شناخت = ?",
            [رقم, بھیجنے_والا]
        );
        انتظار ڈب.چلائیں(
            "UPDATE کھاتے SET رقم = رقم + ? WHERE شناخت = ?",
            [رقم, پانے_والا]
        );
        انتظار ڈب.کمٹ();
        لکھو("منتقلی مکمل");
    } پکڑو (غلطی_م) {
        انتظار ڈب.واپسی();    // undo everything on error
        لکھو(`منتقلی ناکام: ${غلطی_م.message}`);
    }
}
```

**Auto-transaction helper:**

```urdu
غیر_متزامن فنکشن کام() {
    انتظار ڈب.داخل("logs", { پیغام: "شروع" });
    انتظار ڈب.چلائیں("UPDATE stats SET گنتی = گنتی + 1");
}

انتظار ڈب.لین_دین(کام);    // auto commit or rollback
```

---

## MySQL — مائی ایس کیو ایل

Requires: `pip install mysql-connector-python`

```urdu
درآمد { مائی_ایس_کیو_ایل } سے "اردو/ڈیٹا_بیس";

غیر_متزامن فنکشن مرکزی() {
    متغیر ڈب = نیا مائی_ایس_کیو_ایل({
        میزبان: "localhost",
        صارف: "root",
        پاس_ورڈ: "میراپاس",
        ڈیٹا_بیس: "اسکول",
        پورٹ: 3306
    });

    انتظار ڈب.جوڑیں();

    // Convenience insert — auto-builds the SQL
    انتظار ڈب.داخل("طلباء", { نام: "احمد", نمبر: 85 });

    متغیر صفوف = انتظار ڈب.سوال("SELECT * FROM طلباء WHERE نمبر > %s", [80]);
    کے_لیے (متغیر صف میں صفوف) {
        لکھو(`${صف.نام}: ${صف.نمبر}`);
    }

    انتظار ڈب.منقطع();
}

انتظار مرکزی();
```

> **اردو:** MySQL میں `.داخل(جدول, شے)` shortcut دستیاب ہے۔ پیرامیٹر کے لیے `?` استعمال کریں۔

---

## PostgreSQL — پوسٹ گریس

Requires: `pip install psycopg2-binary`

```urdu
درآمد { پوسٹ_گریس } سے "اردو/ڈیٹا_بیس";

غیر_متزامن فنکشن مرکزی() {
    متغیر ڈب = نیا پوسٹ_گریس({
        میزبان: "localhost",
        صارف: "postgres",
        پاس_ورڈ: "میراپاس",
        ڈیٹا_بیس: "اسکول",
        پورٹ: 5432
    });

    انتظار ڈب.جوڑیں();

    // Convenience insert
    انتظار ڈب.داخل("طلباء", { نام: "فاطمہ", نمبر: 92 });

    متغیر صفوف = انتظار ڈب.سوال("SELECT * FROM طلباء ORDER BY نمبر DESC LIMIT 5");
    لکھو(لمبائی(صفوف));

    انتظار ڈب.منقطع();
}

انتظار مرکزی();
```

---

## MongoDB — مونگو ڈی بی

Requires: `pip install pymongo`

```urdu
درآمد { مونگو_ڈی_بی } سے "اردو/ڈیٹا_بیس";

غیر_متزامن فنکشن مرکزی() {
    متغیر ڈب = نیا مونگو_ڈی_بی({
        میزبان: "localhost",
        پورٹ: 27017,
        ڈیٹا_بیس: "اسکول"
    });

    انتظار ڈب.جوڑیں();

    // Get collection
    متغیر طلباء = ڈب.مجموعہ("طلباء");

    // Insert one
    متغیر شناخت = انتظار طلباء.داخل({ نام: "احمد", نمبر: 85, شہر: "کراچی" });
    لکھو(شناخت);    // ObjectId string

    // Insert many
    انتظار طلباء.بہت_داخل([
        { نام: "فاطمہ", نمبر: 92 },
        { نام: "علی", نمبر: 78 }
    ]);

    // Find all
    متغیر سب = انتظار طلباء.تلاش();
    لکھو(لمبائی(سب));

    // Find with filter
    متغیر بہترین = انتظار طلباء.تلاش({ نمبر: { "$gt": 80 } });
    لکھو(لمبائی(بہترین));

    // Find one
    متغیر ایک = انتظار طلباء.ایک_تلاش({ نام: "احمد" });
    لکھو(ایک.نام);

    // Update
    انتظار طلباء.تازہ_کاری({ نام: "احمد" }, { نمبر: 95 });

    // Delete
    انتظار طلباء.حذف({ نمبر: { "$lt": 80 } });

    انتظار ڈب.منقطع();
}

انتظار مرکزی();
```

**MongoDB Collection Methods:**

| Method | Description |
|--------|-------------|
| `.تلاش(فلٹر={}, حد=0)` | Find all matching documents |
| `.ایک_تلاش(فلٹر)` | Find one document |
| `.داخل(دستاویز)` | Insert one, returns id |
| `.بہت_داخل(فہرست)` | Insert many |
| `.تازہ_کاری(فلٹر, تازہ_قدر)` | Update matching docs |
| `.حذف(فلٹر)` | Delete matching docs |

---

## Practical Example: Student Records — عملی مثال

```urdu
درآمد { ایس_کیو_لائٹ } سے "اردو/ڈیٹا_بیس";

غیر_متزامن فنکشن ڈیٹا_بیس_شروع(ڈب) {
    انتظار ڈب.چلائیں("""
        CREATE TABLE IF NOT EXISTS طلباء (
            شناخت INTEGER PRIMARY KEY AUTOINCREMENT,
            نام TEXT NOT NULL,
            نمبر INTEGER,
            کورس TEXT
        )
    """);
}

غیر_متزامن فنکشن طالب_شامل(ڈب, نام, نمبر, کورس) {
    انتظار ڈب.چلائیں(
        "INSERT INTO طلباء (نام, نمبر, کورس) VALUES (?, ?, ?)",
        [نام, نمبر, کورس]
    );
}

غیر_متزامن فنکشن اوسط_نمبر(ڈب, کورس) {
    متغیر نتیجہ = انتظار ڈب.سوال(
        "SELECT AVG(نمبر) as اوسط FROM طلباء WHERE کورس = ?",
        [کورس]
    );
    واپس نتیجہ[0].اوسط;
}

غیر_متزامن فنکشن مرکزی() {
    متغیر ڈب = نیا ایس_کیو_لائٹ("طلباء.db");
    انتظار ڈب.جوڑیں();
    انتظار ڈیٹا_بیس_شروع(ڈب);

    انتظار طالب_شامل(ڈب, "احمد", 85, "کمپیوٹر");
    انتظار طالب_شامل(ڈب, "فاطمہ", 92, "کمپیوٹر");
    انتظار طالب_شامل(ڈب, "علی", 78, "ریاضی");

    متغیر اوسط = انتظار اوسط_نمبر(ڈب, "کمپیوٹر");
    لکھو(`کمپیوٹر کا اوسط: ${گول(اوسط, 1)}`);    // 88.5

    انتظار ڈب.منقطع();
}

انتظار مرکزی();
```

---

## Connection Config Keys — ترتیب کی کلیدیں

| Key | Description | Default |
|-----|-------------|---------|
| `میزبان` | Host / server address | `localhost` |
| `صارف` | Username | `root` / `postgres` |
| `پاس_ورڈ` | Password | `""` |
| `ڈیٹا_بیس` | Database name | — |
| `پورٹ` | Port number | MySQL: 3306, PG: 5432 |

---

[← Previous: Cryptography](04-cryptography.md) | [Next: GUI →](06-gui.md)
