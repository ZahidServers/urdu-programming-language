"""اردو/الگورتھم — Algorithms Library for Urdu Programming Language."""

from __future__ import annotations
import heapq as _heapq
import math as _math


# ─── Sorting ─────────────────────────────────────────────────────────────────

def بلبلہ_ترتیب(فہرست: list) -> list:
    """Bubble Sort — O(n²)"""
    فہرست = list(فہرست)
    ن = len(فہرست)
    for i in range(ن):
        تبادلہ = False
        for j in range(0, ن - i - 1):
            if فہرست[j] > فہرست[j + 1]:
                فہرست[j], فہرست[j + 1] = فہرست[j + 1], فہرست[j]
                تبادلہ = True
        if not تبادلہ:
            break
    return فہرست


def انتخاب_ترتیب(فہرست: list) -> list:
    """Selection Sort — O(n²)"""
    فہرست = list(فہرست)
    ن = len(فہرست)
    for i in range(ن):
        کم = i
        for j in range(i + 1, ن):
            if فہرست[j] < فہرست[کم]:
                کم = j
        فہرست[i], فہرست[کم] = فہرست[کم], فہرست[i]
    return فہرست


def اندراج_ترتیب(فہرست: list) -> list:
    """Insertion Sort — O(n²), efficient for small / nearly-sorted data"""
    فہرست = list(فہرست)
    for i in range(1, len(فہرست)):
        کلید = فہرست[i]
        j = i - 1
        while j >= 0 and فہرست[j] > کلید:
            فہرست[j + 1] = فہرست[j]
            j -= 1
        فہرست[j + 1] = کلید
    return فہرست


def ضم_ترتیب(فہرست: list) -> list:
    """Merge Sort — O(n log n), stable"""
    if len(فہرست) <= 1:
        return list(فہرست)
    وسط = len(فہرست) // 2
    بایاں = ضم_ترتیب(فہرست[:وسط])
    دایاں = ضم_ترتیب(فہرست[وسط:])
    return _ضم(بایاں, دایاں)


def _ضم(الف, ب):
    نتیجہ, i, j = [], 0, 0
    while i < len(الف) and j < len(ب):
        if الف[i] <= ب[j]:
            نتیجہ.append(الف[i]); i += 1
        else:
            نتیجہ.append(ب[j]); j += 1
    نتیجہ.extend(الف[i:])
    نتیجہ.extend(ب[j:])
    return نتیجہ


def تیز_ترتیب(فہرست: list) -> list:
    """Quick Sort — O(n log n) average"""
    if len(فہرست) <= 1:
        return list(فہرست)
    محور = فہرست[len(فہرست) // 2]
    کم    = [x for x in فہرست if x < محور]
    برابر = [x for x in فہرست if x == محور]
    زیادہ = [x for x in فہرست if x > محور]
    return تیز_ترتیب(کم) + برابر + تیز_ترتیب(زیادہ)


def ڈھیر_ترتیب(فہرست: list) -> list:
    """Heap Sort — O(n log n)"""
    فہرست = list(فہرست)
    _heapq.heapify(فہرست)
    return [_heapq.heappop(فہرست) for _ in range(len(فہرست))]


# ─── Searching ────────────────────────────────────────────────────────────────

def خطی_تلاش(فہرست: list, قدر) -> int:
    """Linear Search — O(n); پہلا اشاریہ یا -1"""
    for i, v in enumerate(فہرست):
        if v == قدر:
            return i
    return -1


def دوئی_تلاش(فہرست: list, قدر) -> int:
    """Binary Search on sorted list — O(log n); اشاریہ یا -1"""
    بایاں, دایاں = 0, len(فہرست) - 1
    while بایاں <= دایاں:
        وسط = (بایاں + دایاں) // 2
        if فہرست[وسط] == قدر:
            return وسط
        elif فہرست[وسط] < قدر:
            بایاں = وسط + 1
        else:
            دایاں = وسط - 1
    return -1


# ─── Hash Table ───────────────────────────────────────────────────────────────

class ہیش_جدول:
    """Chaining hash table — ہیش جدول
    استعمال: ج = ہیش_جدول();  ج["نام"] = "علی";  لکھو(ج["نام"])"""

    def __init__(self, گنجائش: int = 16):
        self._گنجائش = گنجائش
        self._بالٹی: list = [[] for _ in range(گنجائش)]
        self._تعداد = 0

    def _idx(self, کلید) -> int:
        return hash(کلید) % self._گنجائش

    def مقرر_کریں(self, کلید, قدر):
        i = self._idx(کلید)
        for k, (j, (ک, ق)) in enumerate([(n, p) for n, p in enumerate(self._بالٹی[i])]):
            if ک == کلید:
                self._بالٹی[i][j] = (کلید, قدر)
                return
        self._بالٹی[i].append((کلید, قدر))
        self._تعداد += 1
        if self._تعداد > self._گنجائش * 0.75:
            self._وسعت()

    def حاصل_کریں(self, کلید, ڈیفالٹ=None):
        for ک, ق in self._بالٹی[self._idx(کلید)]:
            if ک == کلید:
                return ق
        return ڈیفالٹ

    def نکالیں(self, کلید):
        i = self._idx(کلید)
        self._بالٹی[i] = [(ک, ق) for ک, ق in self._بالٹی[i] if ک != کلید]

    def موجود_ہے(self, کلید) -> bool:
        return any(ک == کلید for ک, _ in self._بالٹی[self._idx(کلید)])

    def کلیدیں(self) -> list:
        return [ک for b in self._بالٹی for ک, _ in b]

    def قدریں(self) -> list:
        return [ق for b in self._بالٹی for _, ق in b]

    def اشیاء(self) -> list:
        return [(ک, ق) for b in self._بالٹی for ک, ق in b]

    def _وسعت(self):
        پرانی = self.اشیاء()
        self._گنجائش *= 2
        self._بالٹی = [[] for _ in range(self._گنجائش)]
        self._تعداد = 0
        for ک, ق in پرانی:
            self.مقرر_کریں(ک, ق)

    def __setitem__(self, k, v):
        self.مقرر_کریں(k, v)

    def __getitem__(self, k):
        for ک, ق in self._بالٹی[self._idx(k)]:
            if ک == k:
                return ق
        raise KeyError(k)

    def __contains__(self, k):
        return self.موجود_ہے(k)

    def __len__(self):
        return self._تعداد

    def __repr__(self):
        return f"ہیش_جدول({dict(self.اشیاء())!r})"


# ─── Mathematics ─────────────────────────────────────────────────────────────

def اعظم_مشترک_قاسم(الف: int, ب: int) -> int:
    """Greatest Common Divisor"""
    return _math.gcd(الف, ب)


def اقل_مشترک_ضرب(الف: int, ب: int) -> int:
    """Least Common Multiple"""
    return abs(الف * ب) // _math.gcd(الف, ب) if الف and ب else 0


def فیبوناچی(ن: int) -> int:
    """nth Fibonacci number (0-indexed)"""
    if ن < 0:
        raise ValueError("ن منفی نہیں ہو سکتا")
    if ن < 2:
        return ن
    الف, ب = 0, 1
    for _ in range(2, ن + 1):
        الف, ب = ب, الف + ب
    return ب


def فیبوناچی_سلسلہ(ن: int) -> list:
    """First n Fibonacci numbers"""
    if ن <= 0:
        return []
    نتیجہ = [0] * ن
    if ن > 1:
        نتیجہ[1] = 1
    for i in range(2, ن):
        نتیجہ[i] = نتیجہ[i-1] + نتیجہ[i-2]
    return نتیجہ


def فیکٹوریل(ن: int) -> int:
    """Factorial — ن!"""
    if ن < 0:
        raise ValueError("ن منفی نہیں ہو سکتا")
    نتیجہ = 1
    for i in range(2, ن + 1):
        نتیجہ *= i
    return نتیجہ


def عدد_زائی_ہے(ن: int) -> bool:
    """Is prime check"""
    if ن < 2:
        return False
    if ن < 4:
        return True
    if ن % 2 == 0 or ن % 3 == 0:
        return False
    i = 5
    while i * i <= ن:
        if ن % i == 0 or ن % (i + 2) == 0:
            return False
        i += 6
    return True


def اعداد_زائیہ(ن: int) -> list:
    """Sieve of Eratosthenes — n تک تمام اعداد زائیہ"""
    if ن < 2:
        return []
    چھلنی = bytearray([1]) * (ن + 1)
    چھلنی[0] = چھلنی[1] = 0
    for i in range(2, int(ن**0.5) + 1):
        if چھلنی[i]:
            چھلنی[i*i::i] = bytearray(len(چھلنی[i*i::i]))
    return [i for i in range(2, ن + 1) if چھلنی[i]]


def قوت(بنیاد: int, گھات: int, ماڈیولس: int = None) -> int:
    """Fast exponentiation"""
    return pow(بنیاد, گھات, ماڈیولس)


def اعداد_زائیہ_عوامل(ن: int) -> list:
    """Prime factorization"""
    عوامل, d = [], 2
    while d * d <= ن:
        while ن % d == 0:
            عوامل.append(d)
            ن //= d
        d += 1
    if ن > 1:
        عوامل.append(ن)
    return عوامل


def ترتیب(فہرست: list, *, الٹا: bool = False, کلید=None) -> list:
    """General sort wrapper — Python sorted()"""
    return sorted(فہرست, reverse=الٹا, key=کلید)


# ─── String Algorithms ────────────────────────────────────────────────────────

def لمبی_مشترک_ذیل_ترتیب(الف: str, ب: str) -> str:
    """Longest Common Subsequence"""
    m, n = len(الف), len(ب)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if الف[i-1] == ب[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    نتیجہ, i, j = [], m, n
    while i > 0 and j > 0:
        if الف[i-1] == ب[j-1]:
            نتیجہ.append(الف[i-1]); i -= 1; j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(نتیجہ))


def لیوینشٹین_فاصلہ(الف: str, ب: str) -> int:
    """Levenshtein edit distance"""
    m, n = len(الف), len(ب)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        پچھلا = dp[:]
        dp[0] = i
        for j in range(1, n + 1):
            dp[j] = پچھلا[j-1] if الف[i-1] == ب[j-1] else 1 + min(پچھلا[j], dp[j-1], پچھلا[j-1])
    return dp[n]


def کے_ایم_پی_تلاش(نمونہ: str, متن: str) -> list:
    """KMP pattern matching — تمام مطابقت کی جگہیں (0-indexed)"""
    if not نمونہ:
        return []
    ناکامی = [0] * len(نمونہ)
    j = 0
    for i in range(1, len(نمونہ)):
        while j > 0 and نمونہ[i] != نمونہ[j]:
            j = ناکامی[j-1]
        if نمونہ[i] == نمونہ[j]:
            j += 1
        ناکامی[i] = j
    نتیجہ, j = [], 0
    for i in range(len(متن)):
        while j > 0 and متن[i] != نمونہ[j]:
            j = ناکامی[j-1]
        if متن[i] == نمونہ[j]:
            j += 1
        if j == len(نمونہ):
            نتیجہ.append(i - len(نمونہ) + 1)
            j = ناکامی[j-1]
    return نتیجہ


# ─── English aliases ──────────────────────────────────────────────────────────

bubble_sort      = بلبلہ_ترتیب
selection_sort   = انتخاب_ترتیب
insertion_sort   = اندراج_ترتیب
merge_sort       = ضم_ترتیب
quick_sort       = تیز_ترتیب
heap_sort        = ڈھیر_ترتیب
sort             = ترتیب
linear_search    = خطی_تلاش
binary_search    = دوئی_تلاش
HashTable        = ہیش_جدول
gcd              = اعظم_مشترک_قاسم
lcm              = اقل_مشترک_ضرب
fibonacci        = فیبوناچی
fibonacci_series = فیبوناچی_سلسلہ
factorial        = فیکٹوریل
is_prime         = عدد_زائی_ہے
primes           = اعداد_زائیہ
fast_power       = قوت
prime_factors    = اعداد_زائیہ_عوامل
lcs              = لمبی_مشترک_ذیل_ترتیب
edit_distance    = لیوینشٹین_فاصلہ
kmp_search       = کے_ایم_پی_تلاش

__all__ = [
    "بلبلہ_ترتیب", "انتخاب_ترتیب", "اندراج_ترتیب", "ضم_ترتیب",
    "تیز_ترتیب", "ڈھیر_ترتیب", "ترتیب",
    "خطی_تلاش", "دوئی_تلاش",
    "ہیش_جدول",
    "اعظم_مشترک_قاسم", "اقل_مشترک_ضرب", "فیبوناچی", "فیبوناچی_سلسلہ",
    "فیکٹوریل", "عدد_زائی_ہے", "اعداد_زائیہ", "قوت", "اعداد_زائیہ_عوامل",
    "لمبی_مشترک_ذیل_ترتیب", "لیوینشٹین_فاصلہ", "کے_ایم_پی_تلاش",
    "bubble_sort", "selection_sort", "insertion_sort", "merge_sort",
    "quick_sort", "heap_sort", "sort",
    "linear_search", "binary_search",
    "HashTable",
    "gcd", "lcm", "fibonacci", "fibonacci_series",
    "factorial", "is_prime", "primes", "fast_power", "prime_factors",
    "lcs", "edit_distance", "kmp_search",
]
