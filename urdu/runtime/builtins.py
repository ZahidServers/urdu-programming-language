"""
Built-in functions and objects for the Urdu Programming Language runtime.
All names here are injected into every Urdu program's global namespace.
"""

from __future__ import annotations
import math
import time
import json
import os
import sys
import re
import hashlib
import datetime
import random
import asyncio
from typing import Any


# ─── Core object wrapper ─────────────────────────────────────────────────────

class _UrduObj(dict):
    """JavaScript-style object: supports both obj.key and obj['key'] access."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    def __repr__(self):
        return "{" + ", ".join(f"{k!r}: {v!r}" for k, v in self.items()) + "}"

    # Array-like helpers
    def push(self, *items):
        if isinstance(self, list): self.extend(items)

    def keys(self): return list(super().keys())
    def values(self): return list(super().values())
    def entries(self): return list(self.items())

    @staticmethod
    def فریز(obj):
        return obj

    @staticmethod
    def مفاتیح(obj):
        if isinstance(obj, dict): return list(obj.keys())
        return [k for k in dir(obj) if not k.startswith("_")]

    @staticmethod
    def اقدار(obj):
        if isinstance(obj, dict): return list(obj.values())
        return []

    @staticmethod
    def ضم(**kwargs):
        result = _UrduObj()
        for d in kwargs.values():
            if isinstance(d, dict): result.update(d)
        return result


# ─── BiDi helpers ────────────────────────────────────────────────────────────

# Unicode directional isolate markers
_RLI = "⁧"   # Right-to-Left Isolate  — starts RTL context
_PDI = "⁩"   # Pop Directional Isolate — ends RLI/LRI/FSI
_RLM = "‏"   # Right-to-Left Mark      — lightweight nudge (fallback)

# Arabic/Urdu Unicode ranges (any char in these blocks = RTL content present)
def _has_urdu(text: str) -> bool:
    return any(
        "؀" <= ch <= "ۿ"   # Arabic + Urdu letters/digits
        or "ݐ" <= ch <= "ݿ"  # Arabic Supplement
        or "ﭐ" <= ch <= "﷿"  # Arabic Presentation Forms-A
        or "ﹰ" <= ch <= "﻿"  # Arabic Presentation Forms-B
        for ch in text
    )

def _bidi_safe(text: str) -> str:
    """Wrap mixed-direction text so terminals that honour Unicode BiDi
    markers (Windows Terminal, VS Code, modern xterm) render it correctly.
    Terminals that ignore invisible Unicode chars are unaffected."""
    s = str(text)
    if _has_urdu(s):
        return f"{_RLI}{s}{_PDI}"
    return s


# ─── Built-in functions ───────────────────────────────────────────────────────

def لکھو(*args, **kwargs):
    """print — اردو میں لکھو"""
    sep  = kwargs.get("sep",  " ")
    end  = kwargs.get("end",  "\n")
    file = kwargs.get("file", sys.stdout)
    safe_args = [_bidi_safe(a) for a in args]
    print(*safe_args, sep=sep, end=end, file=file)


def پڑھو(prompt=""):
    """input — اردو میں پڑھو"""
    return input(_bidi_safe(prompt))


def عدد(x):
    """int(x)"""
    try:
        return int(x)
    except (ValueError, TypeError):
        return float("nan")


def اعشاریہ(x):
    """float(x)"""
    try:
        return float(x)
    except (ValueError, TypeError):
        return float("nan")


def متن(x):
    """str(x)"""
    return str(x)


def بولین(x):
    """bool(x)"""
    return bool(x)


def فہرست(*args):
    """list(*args)"""
    if not args: return []
    if len(args) == 1: return list(args[0])
    return list(args)


def ٹپل(*args):
    """tuple(*args)"""
    if not args: return ()
    if len(args) == 1: return tuple(args[0])
    return tuple(args)


def لغت(*args, **kwargs):
    """dict(*args, **kwargs)"""
    return _UrduObj(*args, **kwargs)


def مجموعہ(*args):
    """set(*args)"""
    if not args: return set()
    if len(args) == 1: return set(args[0])
    return set(args)


def لمبائی(x):
    """len(x)"""
    return len(x)


def قسم(x):
    """type name of x"""
    return type(x).__name__


def نمونہ(cls, obj):
    """isinstance(obj, cls)"""
    return isinstance(obj, cls)


def حد(start, stop=None, step=None):
    """range()"""
    if stop is None: return range(start)
    if step is None: return range(start, stop)
    return range(start, stop, step)


def گنو(iterable, start=0):
    """enumerate()"""
    return enumerate(iterable, start)


def زپ(*iterables):
    """zip()"""
    return zip(*iterables)


def نقشہ(func, *iterables):
    """map()"""
    return list(map(func, *iterables))


def فلٹر(func, iterable):
    """filter()"""
    return list(filter(func, iterable))


def ترتیب(iterable, *, کلید=None, الٹا=False):
    """sorted()"""
    return sorted(iterable, key=کلید, reverse=الٹا)


def ریورس(iterable):
    """reversed()"""
    return list(reversed(iterable))


def مجموع(iterable, start=0):
    """sum()"""
    return sum(iterable, start)


def کم(iterable, *args, **kwargs):
    """min()"""
    return min(iterable, *args, **kwargs)


def زیادہ(iterable, *args, **kwargs):
    """max()"""
    return max(iterable, *args, **kwargs)


def مطلق(x):
    """abs(x)"""
    return abs(x)


def گول(x, n=0):
    """round(x, n)"""
    return round(x, n)


def طاقت(x, y):
    """pow(x, y)"""
    return pow(x, y)


def ربط(separator, iterable):
    """str.join()"""
    return separator.join(str(x) for x in iterable)


def تقسیم(string, sep=None):
    """str.split()"""
    return string.split(sep)


def شامل(string, sub):
    """in operator"""
    return sub in string


def JSON_پڑھو(s):
    """JSON.parse"""
    return json.loads(s)


def JSON_لکھو(obj, indent=None):
    """JSON.stringify"""
    return json.dumps(obj, ensure_ascii=False, indent=indent)


def وقت():
    """Date.now() / time.time()"""
    return time.time() * 1000


def تاریخ():
    """new Date()"""
    return datetime.datetime.now()


def اتفاقی(a=0, b=1):
    """Math.random()"""
    return random.uniform(a, b)


def اتفاقی_عدد(a, b):
    """random integer in [a, b]"""
    return random.randint(a, b)


# ─── Promise / async helpers ─────────────────────────────────────────────────

class وعدہ:
    """JavaScript-like Promise wrapper around asyncio."""

    def __init__(self, executor=None):
        self._loop = asyncio.get_event_loop() if asyncio._get_running_loop() else None
        self._future = None
        if executor:
            async def _run():
                resolve_called = asyncio.get_event_loop().create_future()
                reject_called = asyncio.get_event_loop().create_future()

                def resolve(val):
                    if not resolve_called.done():
                        resolve_called.set_result(val)

                def reject(err):
                    if not reject_called.done():
                        reject_called.set_result(err)

                executor(resolve, reject)
                done, _ = await asyncio.wait(
                    [asyncio.ensure_future(resolve_called), asyncio.ensure_future(reject_called)],
                    return_when=asyncio.FIRST_COMPLETED
                )
                for t in done:
                    return t.result()

    @staticmethod
    async def سبھی(promises):
        """Promise.all"""
        return await asyncio.gather(*promises)

    @staticmethod
    async def کوئی(promises):
        """Promise.race"""
        done, pending = await asyncio.wait(promises, return_when=asyncio.FIRST_COMPLETED)
        for t in pending: t.cancel()
        return next(iter(done)).result()

    @staticmethod
    def حل(value):
        async def _resolved():
            return value
        return _resolved()

    @staticmethod
    def رد(reason):
        async def _rejected():
            raise Exception(reason)
        return _rejected()


async def انتظار_سبھی(*args):
    """await Promise.all"""
    return await asyncio.gather(*args)


def تاخیر(ms: float):
    """setTimeout equivalent — returns awaitable"""
    return asyncio.sleep(ms / 1000)


# ─── Console object ───────────────────────────────────────────────────────────

class _Console:
    def log(self, *args):          print(*[_bidi_safe(a) for a in args])
    def لکھو(self, *args):          self.log(*args)
    def error(self, *args):        print("✗", *[_bidi_safe(a) for a in args], file=sys.stderr)
    def غلطی(self, *args):          self.error(*args)
    def warn(self, *args):         print("⚠", *[_bidi_safe(a) for a in args], file=sys.stderr)
    def انتباہ(self, *args):         self.warn(*args)
    def info(self, *args):         print("ℹ", *[_bidi_safe(a) for a in args])
    def معلومات(self, *args):        self.info(*args)
    def debug(self, *args):        print("🔍", *[_bidi_safe(a) for a in args])
    def ڈیبگ(self, *args):          self.debug(*args)
    def table(self, data):
        if isinstance(data, (list, tuple)):
            for i, row in enumerate(data):
                print(f"[{i}]", row)
        else:
            for k, v in (data.items() if isinstance(data, dict) else vars(data).items()):
                print(f"  {k}: {v}")
    def جدول(self, data):          self.table(data)
    def clear(self):               print("\033[2J\033[H", end="")
    def صاف(self):                  self.clear()
    def group(self, label=""):     print(f"▼ {label}")
    def گروپ(self, label=""):      self.group(label)
    def groupEnd(self):            pass
    def گروپ_ختم(self):            pass
    def time(self, label=""):
        import time as _t
        self._timers = getattr(self, "_timers", {})
        self._timers[label] = _t.perf_counter()
    def وقت_شروع(self, label=""):  self.time(label)
    def timeEnd(self, label=""):
        import time as _t
        self._timers = getattr(self, "_timers", {})
        elapsed = (_t.perf_counter() - self._timers.get(label, _t.perf_counter())) * 1000
        print(f"{label}: {elapsed:.2f}ms")
    def وقت_ختم(self, label=""):   self.timeEnd(label)

console = _Console()


# ─── Math object ─────────────────────────────────────────────────────────────

class _Math:
    # Constants — English + Urdu
    PI    = math.pi;      پائی   = math.pi
    E     = math.e;       قدرتی  = math.e
    SQRT2 = math.sqrt(2); جذر_دو = math.sqrt(2)
    LN2   = math.log(2);  لن_دو  = math.log(2)
    LN10  = math.log(10); لن_دس  = math.log(10)
    TAU   = math.tau;     دائرہ  = math.tau

    # Roots / powers
    def sqrt(self, x):          return math.sqrt(x)
    def جذر(self, x):           return math.sqrt(x)
    def جذر_مربع(self, x):      return math.sqrt(x)
    def cbrt(self, x):          return x ** (1/3)
    def جذر_مکعب(self, x):      return x ** (1/3)
    def pow(self, x, y):        return x ** y
    def طاقت(self, x, y):       return x ** y
    def exp(self, x):           return math.exp(x)
    def مرتفع(self, x):         return math.exp(x)

    # Rounding
    def abs(self, x):           return abs(x)
    def مطلق(self, x):          return abs(x)
    def ceil(self, x):          return math.ceil(x)
    def چھت(self, x):           return math.ceil(x)
    def floor(self, x):         return math.floor(x)
    def فرش(self, x):           return math.floor(x)
    def round(self, x):         return round(x)
    def گول(self, x):           return round(x)
    def trunc(self, x):         return int(x)
    def تراش(self, x):          return int(x)
    def sign(self, x):          return (1 if x > 0 else -1 if x < 0 else 0)
    def علامت(self, x):         return (1 if x > 0 else -1 if x < 0 else 0)

    # Min / Max
    def max(self, *args):       return max(*args)
    def زیادہ(self, *args):     return max(*args)
    def min(self, *args):       return min(*args)
    def کم(self, *args):        return min(*args)

    # Logarithms
    def log(self, x):           return math.log(x)
    def لاگ(self, x):           return math.log(x)
    def log2(self, x):          return math.log2(x)
    def لاگ2(self, x):          return math.log2(x)
    def log10(self, x):         return math.log10(x)
    def لاگ10(self, x):         return math.log10(x)

    # Trigonometry
    def sin(self, x):           return math.sin(x)
    def سائن(self, x):          return math.sin(x)
    def cos(self, x):           return math.cos(x)
    def کوسائن(self, x):        return math.cos(x)
    def tan(self, x):           return math.tan(x)
    def ٹینجنٹ(self, x):        return math.tan(x)
    def asin(self, x):          return math.asin(x)
    def معکوس_سائن(self, x):   return math.asin(x)
    def acos(self, x):          return math.acos(x)
    def معکوس_کوسائن(self, x): return math.acos(x)
    def atan(self, x):          return math.atan(x)
    def معکوس_ٹینجنٹ(self, x): return math.atan(x)
    def atan2(self, y, x):      return math.atan2(y, x)
    def ٹینجنٹ2(self, y, x):   return math.atan2(y, x)

    # Geometry
    def hypot(self, *args):     return math.hypot(*args)
    def وتر(self, *args):       return math.hypot(*args)

    # Random
    def random(self):           return random.random()
    def اتفاقی(self):           return random.random()

    # Degrees ↔ Radians
    def degrees(self, x):       return math.degrees(x)
    def درجے(self, x):          return math.degrees(x)
    def radians(self, x):       return math.radians(x)
    def ریڈین(self, x):         return math.radians(x)

    # Combinatorics
    def factorial(self, n):     return math.factorial(int(n))
    def ضربی(self, n):          return math.factorial(int(n))
    def gcd(self, a, b):        return math.gcd(int(a), int(b))
    def مشترک_قسم(self, a, b): return math.gcd(int(a), int(b))

ریاضی = _Math()
Math = ریاضی


# ─── String helpers ───────────────────────────────────────────────────────────

class _StringHelper:
    @staticmethod
    def سے(x): return str(x)
    @staticmethod
    def کوڈ(s, i=0): return ord(s[i])
    @staticmethod
    def حرف(code): return chr(code)

String = _StringHelper()


# ─── Array helpers ────────────────────────────────────────────────────────────

class _ArrayHelper:
    @staticmethod
    def سے(iterable): return list(iterable)
    @staticmethod
    def ہے(x): return isinstance(x, (list, tuple))

Array = _ArrayHelper()


# ─── Object helpers ───────────────────────────────────────────────────────────

class _ObjectHelper:
    @staticmethod
    def مفاتیح(obj):
        if isinstance(obj, dict): return list(obj.keys())
        return [k for k in dir(obj) if not k.startswith("_")]

    @staticmethod
    def اقدار(obj):
        if isinstance(obj, dict): return list(obj.values())
        return []

    @staticmethod
    def اندراج(obj):
        if isinstance(obj, dict): return list(obj.items())
        return []

    @staticmethod
    def تفویض(target, *sources):
        if isinstance(target, dict):
            for src in sources:
                if isinstance(src, dict): target.update(src)
        return target

    @staticmethod
    def منجمد(obj): return obj

    @staticmethod
    def بنا(**kwargs): return _UrduObj(kwargs)

Object = _ObjectHelper()


# ─── Error types ─────────────────────────────────────────────────────────────

class غلطی(Exception):
    """Base Urdu error type"""
    def __init__(self, message="", *args):
        super().__init__(message, *args)
        self.پیغام = message
        self.message = message

    def __str__(self): return self.پیغام

class قسم_غلطی(غلطی, TypeError): pass
class حد_غلطی(غلطی, IndexError): pass
class حوالہ_غلطی(غلطی, NameError): pass
class نحو_غلطی(غلطی, SyntaxError): pass
class رینج_غلطی(غلطی, ValueError): pass
class نیٹ_غلطی(غلطی, ConnectionError): pass
class فائل_غلطی(غلطی, FileNotFoundError): pass

Error = غلطی
TypeError_ = قسم_غلطی
RangeError = رینج_غلطی


# ─── Global utility helpers ──────────────────────────────────────────────────

def _urdu_typeof(x):
    if x is None: return "خالی"
    if isinstance(x, bool): return "بولین"
    if isinstance(x, (int, float)): return "عدد"
    if isinstance(x, str): return "متن"
    if callable(x): return "فنکشن"
    if isinstance(x, (list, tuple)): return "فہرست"
    if isinstance(x, dict): return "شے"
    return "شے"


def _urdu_opt(obj, key):
    if obj is None: return None
    if isinstance(obj, dict): return obj.get(key)
    return getattr(obj, str(key), None)


def _urdu_delete(fn):
    try:
        fn()
        return True
    except Exception:
        return False


# ─── NaN / Infinity ──────────────────────────────────────────────────────────

NaN       = float("nan")
نان       = float("nan")       # Urdu alias
Infinity  = float("inf")
لامحدود  = float("inf")        # Urdu alias
undefined = None
غیر_متعین = None               # Urdu alias


def isNaN(x):
    try: return math.isnan(float(x))
    except Exception: return True

def نان_ہے(x):                  # Urdu alias
    return isNaN(x)


def isFinite(x):
    try: return math.isfinite(float(x))
    except Exception: return False

def محدود_ہے(x):                # Urdu alias
    return isFinite(x)


def parseInt(s, base=10):
    try: return int(str(s).strip(), base)
    except Exception: return NaN

def صحیح_پارس(s, base=10):     # Urdu alias
    return parseInt(s, base)


def parseFloat(s):
    try: return float(str(s).strip())
    except Exception: return NaN

def اعشاریہ_پارس(s):            # Urdu alias
    return parseFloat(s)


# ─── JS array helpers ────────────────────────────────────────────────────────

# ─── Promise (JS-compatible) ───────────────────────────────────────────────��─

class _PromiseObj:
    """Awaitable Promise-like wrapper for synchronous and async values."""
    __slots__ = ("_val", "_is_coro")

    def __init__(self, val):
        import asyncio as _aio
        self._is_coro = _aio.iscoroutine(val) or _aio.isfuture(val)
        self._val = val

    def then(self, on_fulfilled=None, on_rejected=None):
        import asyncio as _aio
        if self._is_coro:
            async def _chain():
                val = await self._val
                return on_fulfilled(val) if on_fulfilled else val
            return _PromiseObj(_chain())
        try:
            result = on_fulfilled(self._val) if on_fulfilled else self._val
            if _aio.iscoroutine(result):
                return _PromiseObj(result)
            return _PromiseObj(result)
        except Exception as e:
            return _RejectedPromiseObj(e)

    def catch(self, fn):
        return self

    def finally_(self, fn):
        fn(); return self

    def __await__(self):
        if self._is_coro:
            # yield from properly delegates to the coroutine and returns its result
            return (yield from self._val.__await__())
        # synchronous value — no suspension needed
        if False: yield
        return self._val


class _RejectedPromiseObj(_PromiseObj):
    def __init__(self, err):
        self._val = err
        self._is_coro = False

    def then(self, on_fulfilled=None, on_rejected=None):
        if on_rejected:
            return _PromiseObj(on_rejected(self._val))
        return self

    def catch(self, fn):
        return _PromiseObj(fn(self._val))

    def __await__(self):
        raise self._val
        if False: yield  # noqa: unreachable — needed for generator protocol


class _Promise:
    @staticmethod
    def resolve(val):
        return _PromiseObj(val)

    @staticmethod
    def reject(err):
        if isinstance(err, Exception):
            return _RejectedPromiseObj(err)
        return _RejectedPromiseObj(Exception(str(err)))

    @staticmethod
    def all(promises):
        import asyncio as _aio
        async def _all():
            results = []
            for p in promises:
                if isinstance(p, _PromiseObj):
                    results.append(await p)
                else:
                    results.append(p)
            return results
        return _PromiseObj(_all())

    @staticmethod
    def race(promises):
        return promises[0] if promises else _PromiseObj(None)

Promise = _Promise


def مدد(موضوع=None):
    """مدد گار — مدد("زمرہ") یا مدد("موضوع")"""
    from .help_lib import مدد as _مدد
    _مدد(موضوع)


def متحرک_چلاؤ(کوڈ: str, ماحول: dict = None):
    """
    Execute a code string dynamically.
    - Urdu code (contains Urdu chars) → transpiled to Python then exec'd
    - Pure Python code → exec'd directly
    ماحول: optional dict used as the execution scope (globals + locals).
    Returns the scope dict after execution.
    """
    scope = ماحول if ماحول is not None else {}

    # Always inject Urdu builtins so exec'd code can call لکھو, لمبائی etc.
    if "__builtins__" not in scope:
        import builtins as _py_builtins
        scope["__builtins__"] = _py_builtins

    if _has_urdu(کوڈ):
        from urdu.lexer      import Lexer
        from urdu.parser     import Parser
        from urdu.transpiler import Transpiler

        py_src = Transpiler().transpile(
            Parser(Lexer(کوڈ).tokenize()).parse()
        )

        # Header prefixes produced by the transpiler — skip these
        _SKIP = (
            "# ═", "# اردو", "# Developer", "# Version",
            "from __future__", "import asyncio", "from urdu.runtime.builtins",
        )

        lines   = py_src.splitlines()
        body    = []
        in_main = False

        for line in lines:
            if line.startswith("async def _اردو_main():"):
                in_main = True
                continue
            if in_main:
                if line.startswith("asyncio.run("):
                    break
                # de-indent one level (4 spaces added by transpiler)
                body.append(line[4:] if line.startswith("    ") else line)
            else:
                # No async wrapper — skip header lines, keep the rest
                stripped = line.strip()
                if not stripped:
                    continue
                if any(stripped.startswith(p) for p in _SKIP):
                    continue
                body.append(line)

        exec("\n".join(body), scope, scope)
    else:
        exec(کوڈ, scope, scope)

    return scope


def _urdu_fill(lst: list, val, start: int = 0, end: int = None) -> list:
    """arr.fill(val, start, end) — mutates list, returns it."""
    if end is None:
        end = len(lst)
    for i in range(start, end):
        lst[i] = val
    return lst

def _urdu_splice(lst: list, start: int, delete_count: int = None, *items):
    """arr.splice(start, deleteCount, ...items) — mutates list, returns removed."""
    if delete_count is None:
        delete_count = len(lst) - start
    removed = lst[start: start + delete_count]
    lst[start: start + delete_count] = list(items)
    return removed

def _urdu_flat(lst: list, depth: int = 1) -> list:
    """arr.flat(depth) — flatten nested arrays up to depth."""
    if depth == 0:
        return list(lst)
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(_urdu_flat(item, depth - 1))
        else:
            result.append(item)
    return result


# ─── Export all built-ins ─────────────────────────────────────────────────────

__all__ = [
    # core
    "_UrduObj", "لکھو", "پڑھو",
    "_urdu_splice", "_urdu_flat", "_urdu_fill",
    "Promise",
    # type conversion
    "عدد", "اعشاریہ", "متن", "بولین",
    # collections
    "فہرست", "ٹپل", "لغت", "مجموعہ",
    # iteration
    "لمبائی", "حد", "گنو", "زپ", "نقشہ", "فلٹر",
    "ترتیب", "ریورس", "مجموع", "کم", "زیادہ",
    # math
    "مطلق", "گول", "طاقت",
    # string
    "ربط", "تقسیم", "شامل",
    # json
    "JSON_پڑھو", "JSON_لکھو",
    # time
    "وقت", "تاریخ", "تاخیر",
    # random
    "اتفاقی", "اتفاقی_عدد",
    # async
    "وعدہ", "انتظار_سبھی",
    # objects
    "console", "ریاضی", "Math", "String", "Array", "Object",
    # type helpers
    "قسم", "نمونہ",
    # errors
    "غلطی", "قسم_غلطی", "حد_غلطی", "حوالہ_غلطی", "نحو_غلطی",
    "رینج_غلطی", "نیٹ_غلطی", "فائل_غلطی", "Error", "RangeError",
    # globals — English
    "NaN", "Infinity", "undefined", "isNaN", "isFinite", "parseInt", "parseFloat",
    # globals — Urdu aliases
    "نان", "لامحدود", "غیر_متعین",
    "نان_ہے", "محدود_ہے", "صحیح_پارس", "اعشاریہ_پارس",
    # help
    "مدد",
    # dynamic execution
    "متحرک_چلاؤ",
    # internals
    "_urdu_typeof", "_urdu_opt", "_urdu_delete",
]
