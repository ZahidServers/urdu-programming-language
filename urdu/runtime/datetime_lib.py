"""
Date and Time library for the Urdu Programming Language.
Supports: Gregorian, Hijri (Islamic), and standard Python datetime types.

Usage from Urdu:
    درآمد { تاریخ, وقت, تاریخ_وقت, مدت, ہجری } سے "اردو/تاریخ";
"""

from __future__ import annotations
import datetime as _dt
import time as _time
import math as _math

# ─── Urdu Month / Day Names ──────────────────────────────────────────────────

_GR_MONTHS = [
    "جنوری", "فروری", "مارچ", "اپریل", "مئی", "جون",
    "جولائی", "اگست", "ستمبر", "اکتوبر", "نومبر", "دسمبر",
]

_HIJRI_MONTHS = [
    "محرم", "صفر", "ربیع الاول", "ربیع الثانی",
    "جمادی الاول", "جمادی الثانی", "رجب", "شعبان",
    "رمضان", "شوال", "ذوالقعدہ", "ذوالحجہ",
]

_DAYS = ["پیر", "منگل", "بدھ", "جمعرات", "جمعہ", "ہفتہ", "اتوار"]

# ─── Hijri ↔ Gregorian Conversion (tabular algorithm) ───────────────────────

def _greg_to_hijri(g_year: int, g_month: int, g_day: int):
    """Gregorian → Hijri (tabular/arithmetic algorithm)."""
    a = (14 - g_month) // 12
    y = g_year + 4800 - a
    m = g_month + 12 * a - 3
    jdn = (g_day + (153 * m + 2) // 5 + 365 * y
           + y // 4 - y // 100 + y // 400 - 32045)

    l = jdn - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316 * (50 * l) // 17719
         + l // 5670 * (43 * l) // 15238)
    l = (l - (30 - j) // 15 * (17719 * j) // 50
         - j // 16 * (15238 * j) // 43 + 29)
    h_month = (24 * l) // 709
    h_day   = l - (709 * h_month) // 24
    h_year  = 30 * n + j - 30
    return h_year, h_month, h_day


def _hijri_to_greg(h_year: int, h_month: int, h_day: int):
    """Hijri → Gregorian (tabular/arithmetic algorithm)."""
    jdn = (h_day
           + (11 * h_year + 3) // 30
           + 354 * h_year
           + 30 * h_month
           - (h_month - 1) // 2
           + 1948440 - 385)

    l = jdn + 68569
    n = (4 * l) // 146097
    l = l - (146097 * n + 3) // 4
    i = (4000 * (l + 1)) // 1461001
    l = l - (1461 * i) // 4 + 31
    j = (80 * l) // 2447
    g_day   = l - (2447 * j) // 80
    l       = j // 11
    g_month = j + 2 - 12 * l
    g_year  = 100 * (n - 49) + i + l
    return g_year, g_month, g_day


# ─── مدت (Duration / timedelta) ─────────────────────────────────────────────

class مدت:
    """Represents a duration (timedelta) — دن, گھنٹے, منٹ, سیکنڈ."""

    def __init__(self, دن=0, گھنٹے=0, منٹ=0, سیکنڈ=0, ہفتے=0):
        if isinstance(دن, _dt.timedelta):
            self._td = دن
        else:
            self._td = _dt.timedelta(
                weeks=int(ہفتے),
                days=int(دن),
                hours=int(گھنٹے),
                minutes=int(منٹ),
                seconds=int(سیکنڈ),
            )

    @classmethod
    def _from_td(cls, td: _dt.timedelta) -> "مدت":
        obj = cls.__new__(cls)
        obj._td = td
        return obj

    # ── Properties ────────────────────────────────────────────────────────────
    @property
    def دن(self):          return self._td.days
    @property
    def سیکنڈ(self):       return self._td.seconds
    @property
    def کل_سیکنڈ(self):   return int(self._td.total_seconds())
    @property
    def کل_منٹ(self):     return int(self._td.total_seconds() / 60)
    @property
    def کل_گھنٹے(self):  return int(self._td.total_seconds() / 3600)
    @property
    def کل_دن(self):      return int(self._td.total_seconds() / 86400)

    # ── Arithmetic ────────────────────────────────────────────────────────────
    def __add__(self, other):
        if isinstance(other, مدت):
            return مدت._from_td(self._td + other._td)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, مدت):
            return مدت._from_td(self._td - other._td)
        return NotImplemented

    def __mul__(self, scalar):
        return مدت._from_td(self._td * scalar)

    def __neg__(self):
        return مدت._from_td(-self._td)

    def __abs__(self):
        return مدت._from_td(abs(self._td))

    # ── Comparison ────────────────────────────────────────────────────────────
    def __eq__(self, other):  return isinstance(other, مدت) and self._td == other._td
    def __lt__(self, other):  return self._td < other._td
    def __le__(self, other):  return self._td <= other._td
    def __gt__(self, other):  return self._td > other._td
    def __ge__(self, other):  return self._td >= other._td

    def __repr__(self):  return f"مدت(دن={self._td.days}, سیکنڈ={self._td.seconds})"
    def __str__(self):   return str(self._td)


# ─── تاریخ (Gregorian Date) ─────────────────────────────────────────────────

class تاریخ:
    """Gregorian calendar date — سال, مہینہ, دن."""

    def __init__(self, سال=None, مہینہ=None, دن=None):
        if isinstance(سال, _dt.datetime):
            self._date = سال.date()
        elif isinstance(سال, _dt.date):
            self._date = سال
        elif سال is None:
            self._date = _dt.date.today()
        else:
            self._date = _dt.date(int(سال), int(مہینہ), int(دن))

    # ── Class methods ─────────────────────────────────────────────────────────
    @classmethod
    def آج(cls) -> "تاریخ":
        return cls(_dt.date.today())

    @classmethod
    def پارس(cls, متن: str, نمونہ: str = "%Y-%m-%d") -> "تاریخ":
        return cls(_dt.datetime.strptime(متن, نمونہ).date())

    @classmethod
    def مہر_سے(cls, مہر) -> "تاریخ":
        return cls(_dt.date.fromtimestamp(float(مہر)))

    # ── Properties ────────────────────────────────────────────────────────────
    @property
    def سال(self):         return self._date.year
    @property
    def مہینہ(self):       return self._date.month
    @property
    def دن(self):          return self._date.day
    @property
    def دن_ہفتہ(self):    return self._date.weekday()   # 0 = پیر
    @property
    def دن_نام(self):      return _DAYS[self._date.weekday()]
    @property
    def مہینہ_نام(self):   return _GR_MONTHS[self._date.month - 1]
    @property
    def کبیسہ(self) -> bool:
        y = self._date.year
        return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
    @property
    def ہفتے_کا_دن(self):  return self._date.isoweekday()  # 1=Mon … 7=Sun

    # ── Formatting ────────────────────────────────────────────────────────────
    def فارمیٹ(self, نمونہ: str = "%Y-%m-%d") -> str:
        return self._date.strftime(نمونہ)

    def اردو_فارمیٹ(self) -> str:
        return f"{self._date.day} {_GR_MONTHS[self._date.month - 1]} {self._date.year}"

    # ── Calendar conversion ───────────────────────────────────────────────────
    def ہجری_میں(self) -> "ہجری":
        y, m, d = _greg_to_hijri(self._date.year, self._date.month, self._date.day)
        return ہجری(y, m, d)

    # ── Arithmetic ────────────────────────────────────────────────────────────
    def __add__(self, other):
        if isinstance(other, مدت):
            return تاریخ(self._date + other._td)
        if isinstance(other, int):
            return تاریخ(self._date + _dt.timedelta(days=other))
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, تاریخ):
            return مدت._from_td(self._date - other._date)
        if isinstance(other, مدت):
            return تاریخ(self._date - other._td)
        if isinstance(other, int):
            return تاریخ(self._date - _dt.timedelta(days=other))
        return NotImplemented

    # ── Comparison ────────────────────────────────────────────────────────────
    def __eq__(self, other):  return isinstance(other, تاریخ) and self._date == other._date
    def __lt__(self, other):  return self._date < other._date
    def __le__(self, other):  return self._date <= other._date
    def __gt__(self, other):  return self._date > other._date
    def __ge__(self, other):  return self._date >= other._date

    def __repr__(self):  return f"تاریخ({self._date.year}, {self._date.month}, {self._date.day})"
    def __str__(self):   return self._date.isoformat()


# ─── وقت (Time) ──────────────────────────────────────────────────────────────

class وقت:
    """Time of day — گھنٹہ, منٹ, سیکنڈ."""

    def __init__(self, گھنٹہ=0, منٹ=0, سیکنڈ=0, مائیکرو=0):
        if isinstance(گھنٹہ, _dt.time):
            self._time = گھنٹہ
        else:
            self._time = _dt.time(int(گھنٹہ), int(منٹ), int(سیکنڈ), int(مائیکرو))

    @classmethod
    def ابھی(cls) -> "وقت":
        return cls(_dt.datetime.now().time())

    @classmethod
    def پارس(cls, متن: str, نمونہ: str = "%H:%M:%S") -> "وقت":
        return cls(_dt.datetime.strptime(متن, نمونہ).time())

    # ── Properties ────────────────────────────────────────────────────────────
    @property
    def گھنٹہ(self):   return self._time.hour
    @property
    def منٹ(self):    return self._time.minute
    @property
    def سیکنڈ(self):  return self._time.second
    @property
    def مائیکرو(self): return self._time.microsecond

    # ── Formatting ────────────────────────────────────────────────────────────
    def فارمیٹ(self, نمونہ: str = "%H:%M:%S") -> str:
        return _dt.datetime.combine(_dt.date.today(), self._time).strftime(نمونہ)

    def اردو_فارمیٹ(self) -> str:
        h = self._time.hour
        period = "صبح" if h < 12 else ("دوپہر" if h < 15 else ("شام" if h < 20 else "رات"))
        h12 = h % 12 or 12
        return f"{h12}:{self._time.minute:02d}:{self._time.second:02d} {period}"

    def __eq__(self, other):  return isinstance(other, وقت) and self._time == other._time
    def __lt__(self, other):  return self._time < other._time
    def __le__(self, other):  return self._time <= other._time
    def __gt__(self, other):  return self._time > other._time
    def __ge__(self, other):  return self._time >= other._time

    def __repr__(self):  return f"وقت({self._time.hour}, {self._time.minute}, {self._time.second})"
    def __str__(self):   return self._time.isoformat()


# ─── تاریخ_وقت (DateTime) ─────────────────────────────────────────────────────

class تاریخ_وقت:
    """Full timestamp — تاریخ + وقت."""

    def __init__(self, سال=None, مہینہ=None, دن=None, گھنٹہ=0, منٹ=0, سیکنڈ=0):
        if isinstance(سال, _dt.datetime):
            self._dt = سال
        elif سال is None:
            self._dt = _dt.datetime.now()
        else:
            self._dt = _dt.datetime(
                int(سال), int(مہینہ), int(دن),
                int(گھنٹہ), int(منٹ), int(سیکنڈ),
            )

    # ── Class methods ─────────────────────────────────────────────────────────
    @classmethod
    def ابھی(cls) -> "تاریخ_وقت":
        return cls(_dt.datetime.now())

    @classmethod
    def UTC(cls) -> "تاریخ_وقت":
        return cls(_dt.datetime.utcnow())

    @classmethod
    def پارس(cls, متن: str, نمونہ: str = "%Y-%m-%d %H:%M:%S") -> "تاریخ_وقت":
        return cls(_dt.datetime.strptime(متن, نمونہ))

    @classmethod
    def مہر_سے(cls, مہر) -> "تاریخ_وقت":
        return cls(_dt.datetime.fromtimestamp(float(مہر)))

    @classmethod
    def تاریخ_اور_وقت(cls, تاریخ_obj: تاریخ, وقت_obj: وقت) -> "تاریخ_وقت":
        return cls(_dt.datetime.combine(تاریخ_obj._date, وقت_obj._time))

    # ── Properties ────────────────────────────────────────────────────────────
    @property
    def سال(self):        return self._dt.year
    @property
    def مہینہ(self):      return self._dt.month
    @property
    def دن(self):         return self._dt.day
    @property
    def گھنٹہ(self):     return self._dt.hour
    @property
    def منٹ(self):       return self._dt.minute
    @property
    def سیکنڈ(self):     return self._dt.second
    @property
    def دن_نام(self):     return _DAYS[self._dt.weekday()]
    @property
    def مہینہ_نام(self):  return _GR_MONTHS[self._dt.month - 1]
    @property
    def تاریخ_حصہ(self): return تاریخ(self._dt.date())
    @property
    def وقت_حصہ(self):  return وقت(self._dt.time())

    # ── Formatting ────────────────────────────────────────────────────────────
    def فارمیٹ(self, نمونہ: str = "%Y-%m-%d %H:%M:%S") -> str:
        return self._dt.strftime(نمونہ)

    def اردو_فارمیٹ(self) -> str:
        d = self._dt
        period = "صبح" if d.hour < 12 else ("دوپہر" if d.hour < 15 else ("شام" if d.hour < 20 else "رات"))
        h12 = d.hour % 12 or 12
        return (f"{d.day} {_GR_MONTHS[d.month - 1]} {d.year}، "
                f"{h12}:{d.minute:02d} {period}")

    def مہر_وقت(self) -> int:
        return int(self._dt.timestamp())

    def ہجری_میں(self) -> "ہجری":
        y, m, d = _greg_to_hijri(self._dt.year, self._dt.month, self._dt.day)
        return ہجری(y, m, d)

    # ── Arithmetic ────────────────────────────────────────────────────────────
    def __add__(self, other):
        if isinstance(other, مدت):
            return تاریخ_وقت(self._dt + other._td)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, تاریخ_وقت):
            return مدت._from_td(self._dt - other._dt)
        if isinstance(other, مدت):
            return تاریخ_وقت(self._dt - other._td)
        return NotImplemented

    # ── Comparison ────────────────────────────────────────────────────────────
    def __eq__(self, other):  return isinstance(other, تاریخ_وقت) and self._dt == other._dt
    def __lt__(self, other):  return self._dt < other._dt
    def __le__(self, other):  return self._dt <= other._dt
    def __gt__(self, other):  return self._dt > other._dt
    def __ge__(self, other):  return self._dt >= other._dt

    def __repr__(self):
        d = self._dt
        return f"تاریخ_وقت({d.year}, {d.month}, {d.day}, {d.hour}, {d.minute}, {d.second})"

    def __str__(self):
        return self._dt.strftime("%Y-%m-%d %H:%M:%S")


# ─── ہجری (Hijri / Islamic Calendar Date) ────────────────────────────────────

class ہجری:
    """Hijri (Islamic) calendar date — سال ہجری, مہینہ, دن."""

    def __init__(self, سال=None, مہینہ=None, دن=None):
        if سال is None:
            today = _dt.date.today()
            self._year, self._month, self._day = _greg_to_hijri(
                today.year, today.month, today.day)
        else:
            self._year, self._month, self._day = int(سال), int(مہینہ), int(دن)

    # ── Class methods ─────────────────────────────────────────────────────────
    @classmethod
    def آج(cls) -> "ہجری":
        return cls()

    @classmethod
    def سے_تاریخ(cls, تاریخ_obj) -> "ہجری":
        if isinstance(تاریخ_obj, تاریخ):
            d = تاریخ_obj._date
        elif isinstance(تاریخ_obj, _dt.date):
            d = تاریخ_obj
        else:
            raise TypeError("تاریخ آبجیکٹ چاہیے")
        y, m, day = _greg_to_hijri(d.year, d.month, d.day)
        return cls(y, m, day)

    @classmethod
    def پارس(cls, متن: str) -> "ہجری":
        parts = متن.strip().split("-")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))

    # ── Properties ────────────────────────────────────────────────────────────
    @property
    def سال(self):        return self._year
    @property
    def مہینہ(self):      return self._month
    @property
    def دن(self):         return self._day
    @property
    def مہینہ_نام(self):  return _HIJRI_MONTHS[self._month - 1]

    def کیا_رمضان(self) -> bool:
        return self._month == 9

    def کیا_ذوالحجہ(self) -> bool:
        return self._month == 12

    # ── Calendar conversion ───────────────────────────────────────────────────
    def عیسوی_میں(self) -> تاریخ:
        y, m, d = _hijri_to_greg(self._year, self._month, self._day)
        return تاریخ(y, m, d)

    # ── Formatting ────────────────────────────────────────────────────────────
    def فارمیٹ(self, نمونہ: str = None) -> str:
        if نمونہ:
            result = نمونہ
            result = result.replace("%Y", str(self._year))
            result = result.replace("%m", f"{self._month:02d}")
            result = result.replace("%d", f"{self._day:02d}")
            result = result.replace("%B", self.مہینہ_نام)
            return result
        return f"{self._year}-{self._month:02d}-{self._day:02d}"

    def اردو_فارمیٹ(self) -> str:
        return f"{self._day} {_HIJRI_MONTHS[self._month - 1]} {self._year} ہجری"

    # ── Arithmetic ────────────────────────────────────────────────────────────
    def __add__(self, other):
        if isinstance(other, int):
            g = self.عیسوی_میں()
            g2 = g + other
            return ہجری.سے_تاریخ(g2)
        if isinstance(other, مدت):
            g = self.عیسوی_میں()
            g2 = g + other
            return ہجری.سے_تاریخ(g2)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, ہجری):
            g1 = self.عیسوی_میں()
            g2 = other.عیسوی_میں()
            return g1 - g2  # returns مدت
        if isinstance(other, int):
            g = self.عیسوی_میں()
            g2 = g - other
            return ہجری.سے_تاریخ(g2)
        return NotImplemented

    # ── Comparison ────────────────────────────────────────────────────────────
    def _tuple(self):
        return (self._year, self._month, self._day)

    def __eq__(self, other):  return isinstance(other, ہجری) and self._tuple() == other._tuple()
    def __lt__(self, other):  return self._tuple() < other._tuple()
    def __le__(self, other):  return self._tuple() <= other._tuple()
    def __gt__(self, other):  return self._tuple() > other._tuple()
    def __ge__(self, other):  return self._tuple() >= other._tuple()

    def __repr__(self):
        return f"ہجری({self._year}, {self._month}, {self._day})"

    def __str__(self):
        return self.اردو_فارمیٹ()


# ─── ٹائمر (Stopwatch) ───────────────────────────────────────────────────────

class ٹائمر:
    """Simple stopwatch — شروع / روکو / دوبارہ_شروع."""

    def __init__(self):
        self._start = None
        self._elapsed = 0.0
        self._running = False

    def شروع(self):
        self._start = _time.perf_counter()
        self._running = True
        return self

    def روکو(self):
        if self._running:
            self._elapsed += _time.perf_counter() - self._start
            self._running = False
        return self

    def دوبارہ_شروع(self):
        self._elapsed = 0.0
        self._start = _time.perf_counter()
        self._running = True
        return self

    @property
    def گزرا_وقت(self) -> float:
        if self._running:
            return self._elapsed + (_time.perf_counter() - self._start)
        return self._elapsed

    @property
    def ملی_سیکنڈ(self) -> float:
        return self.گزرا_وقت * 1000

    def __repr__(self):
        return f"ٹائمر({self.گزرا_وقت:.3f}s)"


# ─── Free utility functions ──────────────────────────────────────────────────

def آج() -> تاریخ:
    """Return today's Gregorian date."""
    return تاریخ.آج()


def ابھی() -> تاریخ_وقت:
    """Return current datetime."""
    return تاریخ_وقت.ابھی()


def مہر_وقت() -> int:
    """Return current Unix timestamp (seconds since epoch)."""
    return int(_time.time())


def مہر_سے_تاریخ(مہر) -> تاریخ_وقت:
    """Convert Unix timestamp to تاریخ_وقت."""
    return تاریخ_وقت.مہر_سے(مہر)


def نیند(سیکنڈ) -> None:
    """Sleep for the given number of seconds."""
    _time.sleep(float(سیکنڈ))


def کبیسہ_سال(سال: int) -> bool:
    """Return True if the given Gregorian year is a leap year."""
    return (سال % 4 == 0 and سال % 100 != 0) or (سال % 400 == 0)


def دنوں_کا_فرق(تاریخ1: تاریخ, تاریخ2: تاریخ) -> int:
    """Return absolute number of days between two dates."""
    return abs((تاریخ1._date - تاریخ2._date).days)


def عیسوی_سے_ہجری(سال: int, مہینہ: int, دن: int) -> ہجری:
    """Convert a Gregorian date to Hijri."""
    y, m, d = _greg_to_hijri(سال, مہینہ, دن)
    return ہجری(y, m, d)


def ہجری_سے_عیسوی(سال: int, مہینہ: int, دن: int) -> تاریخ:
    """Convert a Hijri date to Gregorian."""
    y, m, d = _hijri_to_greg(سال, مہینہ, دن)
    return تاریخ(y, m, d)


def وقت_پیمائش(فنکشن) -> float:
    """Measure execution time of a callable. Returns seconds elapsed."""
    t = ٹائمر().شروع()
    فنکشن()
    t.روکو()
    return t.گزرا_وقت


# ── Month / Day name helpers ───────────────────────────────────────────────────

def مہینہ_نام(مہینہ: int, ہجری_کیلنڈر: bool = False) -> str:
    """Return Urdu month name for given month number (1–12)."""
    if ہجری_کیلنڈر:
        return _HIJRI_MONTHS[مہینہ - 1]
    return _GR_MONTHS[مہینہ - 1]


def دن_نام(دن: int) -> str:
    """Return Urdu day name for weekday index (0=پیر … 6=اتوار)."""
    return _DAYS[دن % 7]


# ── All Hijri month names list ─────────────────────────────────────────────────
ہجری_مہینے = list(_HIJRI_MONTHS)
عیسوی_مہینے = list(_GR_MONTHS)
ہفتے_کے_دن = list(_DAYS)


__all__ = [
    # Classes
    "مدت", "تاریخ", "وقت", "تاریخ_وقت", "ہجری", "ٹائمر",
    # Free functions
    "آج", "ابھی", "مہر_وقت", "مہر_سے_تاریخ", "نیند",
    "کبیسہ_سال", "دنوں_کا_فرق",
    "عیسوی_سے_ہجری", "ہجری_سے_عیسوی",
    "وقت_پیمائش", "مہینہ_نام", "دن_نام",
    # Constants
    "ہجری_مہینے", "عیسوی_مہینے", "ہفتے_کے_دن",
]
