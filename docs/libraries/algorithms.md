# Algorithms — اردو/الگورتھم

The `اردو/الگورتھم` library provides sorting, searching, a hash table, math helpers, and classic string algorithms — all with Urdu names. No pip install needed.

> **اردو:** `اردو/الگورتھم` لائبریری ترتیب، تلاش، ہیش جدول، ریاضیاتی مددگار اور متن الگورتھم — سب اردو ناموں کے ساتھ۔ کوئی اضافی نصب ضروری نہیں۔

**Import:**

```urdu
درآمد {
    بلبلہ_ترتیب, انتخاب_ترتیب, اندراج_ترتیب,
    ضم_ترتیب, تیز_ترتیب, ڈھیر_ترتیب,
    خطی_تلاش, دوئی_تلاش,
    ہیش_جدول,
    اعظم_مشترک_قاسم, اقل_مشترک_ضرب,
    فیبوناچی, فیبوناچی_سلسلہ, فیکٹوریل,
    عدد_زائی_ہے, اعداد_زائیہ, قوت, اعداد_زائیہ_عوامل,
    لمبی_مشترک_ذیل_ترتیب, لیوینشٹین_فاصلہ, کے_ایم_پی_تلاش
} سے "اردو/الگورتھم"
```

---

## Sorting — ترتیب

All sort functions accept a list and return a **new sorted list** — the original is not modified.

```urdu
متغیر فہ = [64, 34, 25, 12, 22, 11, 90]

لکھو(بلبلہ_ترتیب(فہ))      // [11, 12, 22, 25, 34, 64, 90]
لکھو(انتخاب_ترتیب(فہ))     // [11, 12, 22, 25, 34, 64, 90]
لکھو(اندراج_ترتیب(فہ))     // [11, 12, 22, 25, 34, 64, 90]
لکھو(ضم_ترتیب(فہ))          // [11, 12, 22, 25, 34, 64, 90]
لکھو(تیز_ترتیب(فہ))         // [11, 12, 22, 25, 34, 64, 90]
لکھو(ڈھیر_ترتیب(فہ))       // [11, 12, 22, 25, 34, 64, 90]
```

| Function | Complexity | Notes |
|----------|-----------|-------|
| `بلبلہ_ترتیب(فہرست)` | O(n²) | Simple; early-exit optimisation |
| `انتخاب_ترتیب(فہرست)` | O(n²) | Minimum swaps |
| `اندراج_ترتیب(فہرست)` | O(n²) | Fast on nearly-sorted data |
| `ضم_ترتیب(فہرست)` | O(n log n) | Stable sort |
| `تیز_ترتیب(فہرست)` | O(n log n) avg | Median pivot; functional style |
| `ڈھیر_ترتیب(فہرست)` | O(n log n) | In-place heapq |

---

## Searching — تلاش

```urdu
متغیر فہ = [10, 20, 30, 40, 50]

لکھو(خطی_تلاش(فہ, 30))    // 2  (اشاریہ)
لکھو(خطی_تلاش(فہ, 99))    // -1

متغیر ترتیب_شدہ = [1, 3, 5, 7, 9, 11]
لکھو(دوئی_تلاش(ترتیب_شدہ, 7))    // 3
لکھو(دوئی_تلاش(ترتیب_شدہ, 4))    // -1
```

| Function | Complexity | Notes |
|----------|-----------|-------|
| `خطی_تلاش(فہرست, قدر)` | O(n) | Works on unsorted lists; returns index or `-1` |
| `دوئی_تلاش(فہرست, قدر)` | O(log n) | List **must be sorted**; returns index or `-1` |

---

## ہیش_جدول — Hash Table

Chaining hash table — supports string or any hashable key, dict-style `[]` access.

```urdu
متغیر ج = نیا ہیش_جدول()
ج["نام"]   = "علی"
ج["عمر"]   = 25
ج["شہر"]   = "لاہور"

لکھو(ج["نام"])              // "علی"
لکھو(ج.حاصل_کریں("عمر"))   // 25
لکھو(ج.موجود_ہے("شہر"))    // True
لکھو(ج.کلیدیں())            // ["نام", "عمر", "شہر"]
لکھو(ج.قدریں())              // ["علی", 25, "لاہور"]
ج.نکالیں("عمر")
لکھو(len(ج))                // 2
```

| Method | Description |
|--------|-------------|
| `ج[کلید] = قدر` | Set a key-value pair |
| `ج[کلید]` | Get by key — raises `KeyError` if missing |
| `.حاصل_کریں(کلید, ڈیفالٹ=None)` | Get with fallback |
| `.نکالیں(کلید)` | Remove a key |
| `.موجود_ہے(کلید)` | Membership test |
| `.کلیدیں()` | All keys as list |
| `.قدریں()` | All values as list |
| `.اشیاء()` | All `(key, value)` tuples |
| `len(ج)` | Number of entries |

---

## Math — ریاضی

```urdu
لکھو(اعظم_مشترک_قاسم(12, 8))      // 4   (GCD)
لکھو(اقل_مشترک_ضرب(4, 6))          // 12  (LCM)
لکھو(فیبوناچی(10))                  // 55
لکھو(فیبوناچی_سلسلہ(6))            // [0, 1, 1, 2, 3, 5]
لکھو(فیکٹوریل(5))                   // 120
لکھو(عدد_زائی_ہے(17))              // True
لکھو(عدد_زائی_ہے(15))              // False
لکھو(اعداد_زائیہ(20))              // [2, 3, 5, 7, 11, 13, 17, 19]
لکھو(قوت(2, 10))                    // 1024
لکھو(قوت(2, 10, 1000))             // 24  (modular exponentiation)
لکھو(اعداد_زائیہ_عوامل(60))        // [2, 2, 3, 5]
```

| Function | Description |
|----------|-------------|
| `اعظم_مشترک_قاسم(الف, ب)` | Greatest Common Divisor |
| `اقل_مشترک_ضرب(الف, ب)` | Least Common Multiple |
| `فیبوناچی(ن)` | nth Fibonacci number (0-indexed) |
| `فیبوناچی_سلسلہ(ن)` | First n Fibonacci numbers as list |
| `فیکٹوریل(ن)` | n! |
| `عدد_زائی_ہے(ن)` | Is n prime? |
| `اعداد_زائیہ(ن)` | All primes ≤ n (Sieve of Eratosthenes) |
| `قوت(بنیاد, گھات, ماڈیولس=None)` | Fast exponentiation — `pow(b, e, m)` |
| `اعداد_زائیہ_عوامل(ن)` | Prime factorisation |

---

## String Algorithms — متن الگورتھم

```urdu
لکھو(لمبی_مشترک_ذیل_ترتیب("ABCBDAB", "BDCAB"))   // "BCAB"  (LCS)
لکھو(لیوینشٹین_فاصلہ("کتاب", "کتابیں"))           // 3     (edit distance)
لکھو(کے_ایم_پی_تلاش("hello world", "world"))       // [6]   (KMP — list of start indices)
لکھو(کے_ایم_پی_تلاش("abababab", "abab"))           // [0, 2, 4]
```

| Function | Description |
|----------|-------------|
| `لمبی_مشترک_ذیل_ترتیب(الف, ب)` | Longest Common Subsequence — returns the LCS string |
| `لیوینشٹین_فاصلہ(الف, ب)` | Minimum edit distance (insert / delete / replace) |
| `کے_ایم_پی_تلاش(متن, نمونہ)` | KMP pattern search — returns list of all start indices |
