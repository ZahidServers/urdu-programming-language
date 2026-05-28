"""اردو/ڈھانچے — Data Structures Library for Urdu Programming Language."""

from __future__ import annotations
from collections import deque as _deque
from collections import defaultdict as _defaultdict
import heapq as _heapq
import itertools as _itertools


# ─── Linked List ─────────────────────────────────────────────────────────────

class _گرہ:
    __slots__ = ("قدر", "اگلا")
    def __init__(self, قدر, اگلا=None):
        self.قدر = قدر
        self.اگلا = اگلا


class مربوط_فہرست:
    """یک طرفہ مربوط فہرست / Singly Linked List"""

    def __init__(self):
        self._سر = None
        self._تعداد = 0

    def شامل_کریں(self, قدر):
        """آخر میں شامل کریں (append)"""
        نئی = _گرہ(قدر)
        if self._سر is None:
            self._سر = نئی
        else:
            موجودہ = self._سر
            while موجودہ.اگلا:
                موجودہ = موجودہ.اگلا
            موجودہ.اگلا = نئی
        self._تعداد += 1

    def شروع_میں_شامل(self, قدر):
        """شروع میں شامل کریں (prepend)"""
        self._سر = _گرہ(قدر, self._سر)
        self._تعداد += 1

    def نکالیں(self, قدر):
        """قدر نکالیں — True اگر ملی"""
        پچھلا, موجودہ = None, self._سر
        while موجودہ:
            if موجودہ.قدر == قدر:
                if پچھلا:
                    پچھلا.اگلا = موجودہ.اگلا
                else:
                    self._سر = موجودہ.اگلا
                self._تعداد -= 1
                return True
            پچھلا, موجودہ = موجودہ, موجودہ.اگلا
        return False

    def موجود_ہے(self, قدر):
        موجودہ = self._سر
        while موجودہ:
            if موجودہ.قدر == قدر:
                return True
            موجودہ = موجودہ.اگلا
        return False

    def فہرست(self):
        نتیجہ = []
        موجودہ = self._سر
        while موجودہ:
            نتیجہ.append(موجودہ.قدر)
            موجودہ = موجودہ.اگلا
        return نتیجہ

    def الٹا_کریں(self):
        """فہرست پلٹ دیں (in-place)"""
        پچھلا, موجودہ = None, self._سر
        while موجودہ:
            اگلا = موجودہ.اگلا
            موجودہ.اگلا = پچھلا
            پچھلا, موجودہ = موجودہ, اگلا
        self._سر = پچھلا

    def __len__(self):
        return self._تعداد

    def __iter__(self):
        موجودہ = self._سر
        while موجودہ:
            yield موجودہ.قدر
            موجودہ = موجودہ.اگلا

    def __repr__(self):
        return "مربوط_فہرست(" + " → ".join(repr(v) for v in self) + ")"


# ─── Stack ────────────────────────────────────────────────────────────────────

class ڈھیر:
    """Stack — آخری داخل، پہلے خارج (LIFO)"""

    def __init__(self):
        self._ڈھیر = []

    def دھکیلیں(self, قدر):
        self._ڈھیر.append(قدر)

    def نکالیں(self):
        if not self._ڈھیر:
            raise IndexError("ڈھیر خالی ہے")
        return self._ڈھیر.pop()

    def جھانکیں(self):
        if not self._ڈھیر:
            raise IndexError("ڈھیر خالی ہے")
        return self._ڈھیر[-1]

    def خالی_ہے(self):
        return len(self._ڈھیر) == 0

    def __len__(self):
        return len(self._ڈھیر)

    def __repr__(self):
        return f"ڈھیر({self._ڈھیر!r})"


# ─── Queue ───────────────────────────────────────────────────────────────────

class قطار:
    """Queue — پہلے داخل، پہلے خارج (FIFO)"""

    def __init__(self):
        self._q = _deque()

    def شامل_کریں(self, قدر):
        self._q.append(قدر)

    def نکالیں(self):
        if not self._q:
            raise IndexError("قطار خالی ہے")
        return self._q.popleft()

    def اگلا(self):
        if not self._q:
            raise IndexError("قطار خالی ہے")
        return self._q[0]

    def خالی_ہے(self):
        return len(self._q) == 0

    def __len__(self):
        return len(self._q)

    def __repr__(self):
        return f"قطار({list(self._q)!r})"


# ─── Deque ───────────────────────────────────────────────────────────────────

class دوطرفہ_قطار:
    """Double-Ended Queue — دونوں طرف سے شامل/نکال"""

    def __init__(self):
        self._dq = _deque()

    def بائیں_شامل(self, قدر):
        self._dq.appendleft(قدر)

    def دائیں_شامل(self, قدر):
        self._dq.append(قدر)

    def بائیں_نکالیں(self):
        if not self._dq:
            raise IndexError("دوطرفہ قطار خالی ہے")
        return self._dq.popleft()

    def دائیں_نکالیں(self):
        if not self._dq:
            raise IndexError("دوطرفہ قطار خالی ہے")
        return self._dq.pop()

    def بائیں_جھانکیں(self):
        if not self._dq:
            raise IndexError("دوطرفہ قطار خالی ہے")
        return self._dq[0]

    def دائیں_جھانکیں(self):
        if not self._dq:
            raise IndexError("دوطرفہ قطار خالی ہے")
        return self._dq[-1]

    def خالی_ہے(self):
        return len(self._dq) == 0

    def __len__(self):
        return len(self._dq)

    def __repr__(self):
        return f"دوطرفہ_قطار({list(self._dq)!r})"


# ─── Priority Queue / Heap ────────────────────────────────────────────────────

class ترجیحی_قطار:
    """Min-Heap priority queue (زیادہ_سے_زیادہ=True → Max-Heap)"""

    def __init__(self, زیادہ_سے_زیادہ: bool = False):
        self._h = []
        self._زیادہ = زیادہ_سے_زیادہ
        self._seq = _itertools.count()

    def شامل_کریں(self, قدر, ترجیح: float = 0):
        علامت = -1 if self._زیادہ else 1
        _heapq.heappush(self._h, (علامت * ترجیح, next(self._seq), قدر))

    def نکالیں(self):
        if not self._h:
            raise IndexError("ترجیحی قطار خالی ہے")
        return _heapq.heappop(self._h)[2]

    def جھانکیں(self):
        if not self._h:
            raise IndexError("ترجیحی قطار خالی ہے")
        return self._h[0][2]

    def خالی_ہے(self):
        return len(self._h) == 0

    def __len__(self):
        return len(self._h)

    def __repr__(self):
        return f"ترجیحی_قطار(تعداد={len(self._h)})"


# ─── Binary Search Tree ───────────────────────────────────────────────────────

class _بی_ایس_ٹی_گرہ:
    __slots__ = ("قدر", "بایاں", "دایاں")
    def __init__(self, قدر):
        self.قدر = قدر
        self.بایاں = None
        self.دایاں = None


class بائنری_تلاش_درخت:
    """Binary Search Tree — ترتیب شدہ بائنری درخت"""

    def __init__(self):
        self._جڑ = None

    def داخل_کریں(self, قدر):
        self._جڑ = self._داخل(self._جڑ, قدر)

    def _داخل(self, گ, قدر):
        if گ is None:
            return _بی_ایس_ٹی_گرہ(قدر)
        if قدر < گ.قدر:
            گ.بایاں = self._داخل(گ.بایاں, قدر)
        elif قدر > گ.قدر:
            گ.دایاں = self._داخل(گ.دایاں, قدر)
        return گ

    def موجود_ہے(self, قدر):
        گ = self._جڑ
        while گ:
            if قدر == گ.قدر:
                return True
            گ = گ.بایاں if قدر < گ.قدر else گ.دایاں
        return False

    def نکالیں(self, قدر):
        self._جڑ = self._نکالیں(self._جڑ, قدر)

    def _نکالیں(self, گ, قدر):
        if گ is None:
            return None
        if قدر < گ.قدر:
            گ.بایاں = self._نکالیں(گ.بایاں, قدر)
        elif قدر > گ.قدر:
            گ.دایاں = self._نکالیں(گ.دایاں, قدر)
        else:
            if گ.بایاں is None:
                return گ.دایاں
            if گ.دایاں is None:
                return گ.بایاں
            جانشین = گ.دایاں
            while جانشین.بایاں:
                جانشین = جانشین.بایاں
            گ.قدر = جانشین.قدر
            گ.دایاں = self._نکالیں(گ.دایاں, جانشین.قدر)
        return گ

    def ترتیب_سے(self):
        """Inorder traversal — ترتیب شدہ فہرست"""
        نتیجہ = []
        def _io(گ):
            if گ:
                _io(گ.بایاں)
                نتیجہ.append(گ.قدر)
                _io(گ.دایاں)
        _io(self._جڑ)
        return نتیجہ

    def سب_سے_چھوٹا(self):
        if self._جڑ is None:
            raise ValueError("درخت خالی ہے")
        گ = self._جڑ
        while گ.بایاں:
            گ = گ.بایاں
        return گ.قدر

    def سب_سے_بڑا(self):
        if self._جڑ is None:
            raise ValueError("درخت خالی ہے")
        گ = self._جڑ
        while گ.دایاں:
            گ = گ.دایاں
        return گ.قدر

    def اونچائی(self):
        def _h(گ):
            return 0 if گ is None else 1 + max(_h(گ.بایاں), _h(گ.دایاں))
        return _h(self._جڑ)

    def __len__(self):
        def _n(گ):
            return 0 if گ is None else 1 + _n(گ.بایاں) + _n(گ.دایاں)
        return _n(self._جڑ)

    def __repr__(self):
        return f"بائنری_تلاش_درخت(اونچائی={self.اونچائی()}, تعداد={len(self)})"


# ─── Graph ────────────────────────────────────────────────────────────────────

class گراف:
    """گراف — ملحقہ فہرست (adjacency list)
    ہدایت_یافتہ=True → directed, False → undirected"""

    def __init__(self, ہدایت_یافتہ: bool = False):
        self._adj: dict = _defaultdict(dict)
        self._ہدایت = ہدایت_یافتہ

    def کونا_شامل_کریں(self, v):
        if v not in self._adj:
            self._adj[v] = {}

    def کنارہ_شامل_کریں(self, u, v, وزن: float = 1):
        self.کونا_شامل_کریں(u)
        self.کونا_شامل_کریں(v)
        self._adj[u][v] = وزن
        if not self._ہدایت:
            self._adj[v][u] = وزن

    def ہم_سایہ(self, v):
        return list(self._adj.get(v, {}).keys())

    def کونے(self):
        return list(self._adj.keys())

    def کنارے(self):
        نتیجہ = []
        ملے = set()
        for u, پڑوسی in self._adj.items():
            for v, w in پڑوسی.items():
                جوڑا = (min(u, v, key=str), max(u, v, key=str)) if not self._ہدایت else (u, v)
                if جوڑا not in ملے:
                    ملے.add(جوڑا)
                    نتیجہ.append((u, v, w))
        return نتیجہ

    def چوڑائی_تلاش(self, آغاز):
        """BFS — چوڑائی پہلے تلاش"""
        ملے = {آغاز}
        ترتیب = []
        صف = _deque([آغاز])
        while صف:
            v = صف.popleft()
            ترتیب.append(v)
            for u in self._adj.get(v, {}):
                if u not in ملے:
                    ملے.add(u)
                    صف.append(u)
        return ترتیب

    def گہرائی_تلاش(self, آغاز):
        """DFS — گہرائی پہلے تلاش"""
        ملے = set()
        ترتیب = []
        def _dfs(v):
            ملے.add(v)
            ترتیب.append(v)
            for u in self._adj.get(v, {}):
                if u not in ملے:
                    _dfs(u)
        _dfs(آغاز)
        return ترتیب

    def راستہ_ہے(self, آغاز, منزل):
        return منزل in set(self.چوڑائی_تلاش(آغاز))

    def مختصر_راستہ(self, آغاز, منزل):
        """Dijkstra shortest path — مختصر راستہ"""
        if آغاز not in self._adj:
            return None
        seq = _itertools.count()
        فاصلہ = {آغاز: 0}
        والد = {آغاز: None}
        ملے = set()
        heap = [(0, next(seq), آغاز)]
        while heap:
            د, _, v = _heapq.heappop(heap)
            if v in ملے:
                continue
            ملے.add(v)
            if v == منزل:
                break
            for u, w in self._adj.get(v, {}).items():
                نیا = د + w
                if u not in ملے and نیا < فاصلہ.get(u, float('inf')):
                    فاصلہ[u] = نیا
                    والد[u] = v
                    _heapq.heappush(heap, (نیا, next(seq), u))
        if منزل not in والد:
            return None
        راستہ, curr = [], منزل
        while curr is not None:
            راستہ.append(curr)
            curr = والد[curr]
        return راستہ[::-1]

    def طوپو_ترتیب(self):
        """Topological sort (DAG only) — کاہن الگورتھم; None اگر چکر ہو"""
        اندر = {v: 0 for v in self._adj}
        for v in self._adj:
            for u in self._adj[v]:
                اندر[u] = اندر.get(u, 0) + 1
        صف = _deque(v for v, d in اندر.items() if d == 0)
        نتیجہ = []
        while صف:
            v = صف.popleft()
            نتیجہ.append(v)
            for u in self._adj.get(v, {}):
                اندر[u] -= 1
                if اندر[u] == 0:
                    صف.append(u)
        return نتیجہ if len(نتیجہ) == len(self._adj) else None

    def __repr__(self):
        نوع = "ہدایت_یافتہ" if self._ہدایت else "غیر_ہدایت_یافتہ"
        return f"گراف({نوع}, کونے={len(self._adj)})"


# ─── English aliases ──────────────────────────────────────────────────────────

LinkedList       = مربوط_فہرست
Stack            = ڈھیر
Queue            = قطار
Deque            = دوطرفہ_قطار
PriorityQueue    = ترجیحی_قطار
BST              = بائنری_تلاش_درخت
BinarySearchTree = بائنری_تلاش_درخت
Graph            = گراف

__all__ = [
    "مربوط_فہرست", "ڈھیر", "قطار", "دوطرفہ_قطار",
    "ترجیحی_قطار", "بائنری_تلاش_درخت", "گراف",
    "LinkedList", "Stack", "Queue", "Deque",
    "PriorityQueue", "BST", "BinarySearchTree", "Graph",
]
