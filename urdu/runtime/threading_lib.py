"""
Multithreading and async utilities for the Urdu Programming Language.

Usage from Urdu:
    درآمد { دھاگہ, قطار, تالہ, ٹائمر } سے "اردو/دھاگہ";
"""

from __future__ import annotations
import threading
import asyncio
import time
import queue
import concurrent.futures
from typing import Any, Callable, Optional


# ─── Thread ───────────────────────────────────────────────────────────────────

class دھاگہ:
    """Thread wrapper."""

    def __init__(self, کام: Callable, *دلائل, نام: str = None, جمعہ: bool = False, **kwargs):
        self._thread = threading.Thread(
            target=کام,
            args=دلائل,
            kwargs=kwargs,
            name=نام,
            daemon=جمعہ,
        )
        self._result = None
        self._error = None

    def شروع(self):
        self._thread.start()
        return self

    def انتظار(self, وقفہ: float = None):
        self._thread.join(timeout=وقفہ)
        return self

    def چل_رہا(self) -> bool:
        return self._thread.is_alive()

    def شناخت(self) -> int:
        return self._thread.ident

    @staticmethod
    def موجودہ() -> threading.Thread:
        return threading.current_thread()

    @staticmethod
    def گنتی() -> int:
        return threading.active_count()

    @staticmethod
    def سبھی() -> list:
        return threading.enumerate()


# ─── Thread pool ─────────────────────────────────────────────────────────────

class دھاگہ_تالاب:
    """Thread pool executor."""

    def __init__(self, کارکن: int = 4):
        self._pool = concurrent.futures.ThreadPoolExecutor(max_workers=کارکن)

    def جمع_کرو(self, کام: Callable, *دلائل, **kwargs):
        return self._pool.submit(کام, *دلائل, **kwargs)

    def جمع_کرو_مستقبل(self, کام: Callable, *دلائل, **kwargs) -> "مستقبل":
        """Submit work and return a مستقبل (Future) wrapper."""
        return مستقبل(self._pool.submit(کام, *دلائل, **kwargs))

    async def غیر_متزامن_جمع(self, کام: Callable, *دلائل):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._pool, کام, *دلائل)

    def نقشہ(self, کام: Callable, اشیاء: list) -> list:
        return list(self._pool.map(کام, اشیاء))

    def بند(self, انتظار: bool = True):
        self._pool.shutdown(wait=انتظار)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.بند()


# ─── Process pool ────────────────────────────────────────────────────────────

class عمل_تالاب:
    """Process pool executor for CPU-bound work."""

    def __init__(self, کارکن: int = None):
        self._pool = concurrent.futures.ProcessPoolExecutor(max_workers=کارکن)

    def جمع_کرو(self, کام: Callable, *دلائل):
        return self._pool.submit(کام, *دلائل)

    def نقشہ(self, کام: Callable, اشیاء: list) -> list:
        return list(self._pool.map(کام, اشیاء))

    def بند(self):
        self._pool.shutdown()


# ─── Lock ─────────────────────────────────────────────────────────────────────

class تالہ:
    """Thread lock."""

    def __init__(self, دوبارہ: bool = False):
        self._lock = threading.RLock() if دوبارہ else threading.Lock()

    def قبضہ(self, وقفہ: float = -1) -> bool:
        return self._lock.acquire(timeout=وقفہ)

    def چھوڑو(self):
        self._lock.release()

    def __enter__(self):
        self._lock.acquire()
        return self

    def __exit__(self, *_):
        self._lock.release()


# ─── Event ───────────────────────────────────────────────────────────────────

class واقعہ:
    """Thread event."""

    def __init__(self):
        self._event = threading.Event()

    def مقرر(self):
        self._event.set()
        return self

    def صاف(self):
        self._event.clear()
        return self

    def انتظار(self, وقفہ: float = None) -> bool:
        return self._event.wait(timeout=وقفہ)

    def لگا_ہوا(self) -> bool:
        return self._event.is_set()


# ─── Semaphore ───────────────────────────────────────────────────────────────

class سیمافور:
    """Thread semaphore."""

    def __init__(self, قدر: int = 1):
        self._sem = threading.Semaphore(قدر)

    def __enter__(self):
        self._sem.acquire()
        return self

    def __exit__(self, *_):
        self._sem.release()

    def حاصل(self, وقفہ: float = -1) -> bool:
        return self._sem.acquire(timeout=وقفہ)

    def چھوڑو(self):
        self._sem.release()


# ─── Queue ───────────────────────────────────────────────────────────────────

class قطار:
    """Thread-safe queue."""

    def __init__(self, زیادہ: int = 0):
        self._q = queue.Queue(maxsize=زیادہ)

    def ڈالو(self, آئٹم: Any, وقفہ: float = None):
        self._q.put(آئٹم, timeout=وقفہ)
        return self

    append = ڈالو   # English alias (transpiler: .شامل → .append)

    def نکالو(self, وقفہ: float = None) -> Any:
        """Blocking dequeue. وقفہ: timeout in seconds (None = block forever)."""
        return self._q.get(timeout=وقفہ)

    pop = نکالو   # English alias (transpiler maps .نکالو → .pop)

    def نکالو_نہ_رکو(self) -> Any:
        try:
            return self._q.get_nowait()
        except queue.Empty:
            return None

    def خالی(self) -> bool:
        return self._q.empty()

    def لمبائی(self) -> int:
        return self._q.qsize()

    def __len__(self) -> int:
        return self._q.qsize()

    def مکمل(self):
        self._q.task_done()

    def انتظار(self):
        self._q.join()


class ترجیحی_قطار:
    """Priority queue."""

    def __init__(self):
        self._q = queue.PriorityQueue()

    def ڈالو(self, ترجیح: int, آئٹم: Any):
        self._q.put((ترجیح, آئٹم))

    def نکالو(self) -> tuple:
        """Dequeue the (priority, item) pair with the lowest priority number."""
        return self._q.get()

    pop = نکالو   # English alias (transpiler maps .نکالو → .pop)


# ─── Timer ───────────────────────────────────────────────────────────────────

class ٹائمر:
    """One-shot timer."""

    def __init__(self, وقفہ: float, کام: Callable, *دلائل):
        self._timer = threading.Timer(وقفہ, کام, args=دلائل)

    def شروع(self):
        self._timer.start()
        return self

    def منسوخ(self):
        self._timer.cancel()


class وقفہ_ٹائمر:
    """Repeating interval timer."""

    def __init__(self, وقفہ: float, کام: Callable, *دلائل):
        self._interval = وقفہ
        self._fn = کام
        self._args = دلائل
        self._running = False
        self._timer = None

    def شروع(self):
        self._running = True
        self._tick()
        return self

    def _tick(self):
        if self._running:
            self._fn(*self._args)
            self._timer = threading.Timer(self._interval, self._tick)
            self._timer.daemon = True
            self._timer.start()

    def روکو(self):
        self._running = False
        if self._timer:
            self._timer.cancel()


# ─── Async helpers ────────────────────────────────────────────────────────────

def غیر_متزامن_چلائیں(coroutine):
    """Run a coroutine from sync context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            fut = concurrent.futures.Future()

            async def _wrap():
                try:
                    result = await coroutine
                    fut.set_result(result)
                except Exception as e:
                    fut.set_exception(e)

            asyncio.ensure_future(_wrap())
            return fut
        else:
            return loop.run_until_complete(coroutine)
    except RuntimeError:
        return asyncio.run(coroutine)


def نئی_قطار_async(زیادہ: int = 0) -> asyncio.Queue:
    return asyncio.Queue(maxsize=زیادہ)


class AsyncLock:
    """Asyncio lock."""

    def __init__(self):
        self._lock = asyncio.Lock()

    async def __aenter__(self):
        await self._lock.acquire()
        return self

    async def __aexit__(self, *_):
        self._lock.release()


# ─── Future ──────────────────────────────────────────────────────────────────

class مستقبل:
    """
    Wraps concurrent.futures.Future with an Urdu-named API.

    Usage:
        تالاب = دھاگہ_تالاب(4)
        م = تالاب.جمع_کرو_مستقبل(کام, دلیل1)
        نتیجہ = م.نتیجہ(وقفہ=5)
    """

    def __init__(self, fut: concurrent.futures.Future):
        self._fut = fut

    def نتیجہ(self, وقفہ: float = None) -> Any:
        """Block until result is ready, then return it."""
        return self._fut.result(timeout=وقفہ)

    def منسوخ(self) -> bool:
        """Cancel the task if it hasn't started yet. Returns True on success."""
        return self._fut.cancel()

    def منسوخ_ہوا(self) -> bool:
        """Return True if the task was cancelled."""
        return self._fut.cancelled()

    def مکمل(self) -> bool:
        """Return True if done (finished or cancelled)."""
        return self._fut.done()

    def چل_رہا(self) -> bool:
        """Return True if currently executing."""
        return self._fut.running()

    def غلطی(self) -> Optional[BaseException]:
        """Return the exception raised, or None if succeeded."""
        try:
            return self._fut.exception()
        except concurrent.futures.CancelledError:
            return None

    def مکمل_ہونے_پر(self, کال_بیک: Callable) -> "مستقبل":
        """Register a callback fired when this future completes."""
        self._fut.add_done_callback(lambda f: کال_بیک(مستقبل(f)))
        return self

    def __repr__(self) -> str:
        state = "منسوخ" if self.منسوخ_ہوا() else ("مکمل" if self.مکمل() else "چل رہا")
        return f"<مستقبل [{state}]>"


# ─── Cancellable task ─────────────────────────────────────────────────────────

class منسوخ_ہونے_والا:
    """
    Wraps a callable so it can be cooperatively cancelled via an event.

    Usage:
        def کام(رکو):
            جبکہ نہ رکو.ہوا():
                ...

        م = منسوخ_ہونے_والا(کام)
        م.شروع()
        وقت.سو(2)
        م.منسوخ()
        م.انتظار()
    """

    def __init__(self, کام: Callable, *دلائل, نام: str = None):
        self._stop_event = threading.Event()
        self._fn = کام
        self._args = دلائل
        self._thread = threading.Thread(
            target=self._run,
            name=نام,
            daemon=True,
        )

    def _run(self):
        self._fn(self._stop_event, *self._args)

    def شروع(self) -> "منسوخ_ہونے_والا":
        self._thread.start()
        return self

    def منسوخ(self):
        """Signal the task to stop."""
        self._stop_event.set()

    def انتظار(self, وقفہ: float = None):
        self._thread.join(timeout=وقفہ)

    def چل_رہا(self) -> bool:
        return self._thread.is_alive()

    def __repr__(self) -> str:
        state = "چل رہا" if self.چل_رہا() else "بند"
        return f"<منسوخ_ہونے_والا [{state}]>"


# ─── Async future helper ──────────────────────────────────────────────────────

async def غیر_متزامن_مستقبل(تالاب: دھاگہ_تالاب, کام: Callable, *دلائل) -> Any:
    """Run a sync callable in a thread pool and await its result."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(تالاب._pool, کام, *دلائل)


# ─── Thread-local storage ────────────────────────────────────────────────────

class مقامی_ذخیرہ:
    """Thread-local storage."""

    def __init__(self):
        self._local = threading.local()

    def مقرر(self, نام: str, قدر: Any):
        setattr(self._local, نام, قدر)

    def حاصل(self, نام: str, ڈیفالٹ: Any = None) -> Any:
        return getattr(self._local, نام, ڈیفالٹ)


__all__ = [
    "دھاگہ", "دھاگہ_تالاب", "عمل_تالاب",
    "تالہ", "واقعہ", "سیمافور",
    "قطار", "ترجیحی_قطار",
    "ٹائمر", "وقفہ_ٹائمر",
    "مستقبل", "منسوخ_ہونے_والا",
    "غیر_متزامن_چلائیں", "غیر_متزامن_مستقبل", "نئی_قطار_async", "AsyncLock",
    "مقامی_ذخیرہ",
]
