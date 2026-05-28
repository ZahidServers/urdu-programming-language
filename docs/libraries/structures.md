# Data Structures — اردو/ڈھانچے

The `اردو/ڈھانچے` library provides classic data structures with Urdu-named classes and methods. No pip install needed — it uses only Python's standard library.

> **اردو:** `اردو/ڈھانچے` لائبریری مشہور ڈیٹا ڈھانچوں کو اردو ناموں کے ساتھ فراہم کرتی ہے۔ کوئی اضافی نصب کاری ضروری نہیں۔

**Import:**

```urdu
درآمد {
    مربوط_فہرست, ڈھیر, قطار, دوطرفہ_قطار,
    ترجیحی_قطار, بائنری_تلاش_درخت, گراف
} سے "اردو/ڈھانچے"
```

---

## مربوط_فہرست — Singly Linked List

یک طرفہ مربوط فہرست — each node holds a value and a pointer to the next node.

```urdu
متغیر فہ = نیا مربوط_فہرست()
فہ.شامل_کریں(10)
فہ.شامل_کریں(20)
فہ.شامل_کریں(30)
فہ.شروع_میں_شامل(5)
لکھو(فہ.فہرست())    // [5, 10, 20, 30]
فہ.الٹا_کریں()
لکھو(فہ.فہرست())    // [30, 20, 10, 5]
```

| Method | Description |
|--------|-------------|
| `.شامل_کریں(قدر)` | Append to end — O(n) |
| `.شروع_میں_شامل(قدر)` | Prepend to front — O(1) |
| `.نکالیں(قدر)` | Remove first occurrence — returns `True`/`False` |
| `.موجود_ہے(قدر)` | Membership test — O(n) |
| `.فہرست()` | Return all values as a Python list |
| `.الٹا_کریں()` | Reverse in-place — O(n) |
| `len(فہ)` | Number of nodes |

---

## ڈھیر — Stack (LIFO)

آخری داخل، پہلے خارج — Last-In First-Out.

```urdu
متغیر ڈ = نیا ڈھیر()
ڈ.دھکیلیں(1)
ڈ.دھکیلیں(2)
ڈ.دھکیلیں(3)
لکھو(ڈ.جھانکیں())   // 3  (بغیر نکالے)
لکھو(ڈ.نکالیں())    // 3
لکھو(ڈ.نکالیں())    // 2
لکھو(ڈ.خالی_ہے())   // False
```

| Method | Description |
|--------|-------------|
| `.دھکیلیں(قدر)` | Push onto top — O(1) |
| `.نکالیں()` | Pop from top — raises `IndexError` if empty |
| `.جھانکیں()` | Peek at top without removing |
| `.خالی_ہے()` | `True` if empty |
| `len(ڈ)` | Current depth |

---

## قطار — Queue (FIFO)

پہلے داخل، پہلے خارج — First-In First-Out. Backed by `collections.deque` for O(1) operations.

```urdu
متغیر ق = نیا قطار()
ق.شامل_کریں("الف")
ق.شامل_کریں("ب")
ق.شامل_کریں("ج")
لکھو(ق.اگلا())       // "الف"  (بغیر نکالے)
لکھو(ق.نکالیں())     // "الف"
لکھو(ق.نکالیں())     // "ب"
```

| Method | Description |
|--------|-------------|
| `.شامل_کریں(قدر)` | Enqueue at back — O(1) |
| `.نکالیں()` | Dequeue from front — O(1); raises `IndexError` if empty |
| `.اگلا()` | Peek at front without removing |
| `.خالی_ہے()` | `True` if empty |
| `len(ق)` | Current length |

---

## دوطرفہ_قطار — Deque

دونوں طرف سے شامل اور نکال — insert/remove from either end in O(1).

```urdu
متغیر دق = نیا دوطرفہ_قطار()
دق.دائیں_شامل(10)
دق.دائیں_شامل(20)
دق.بائیں_شامل(5)
لکھو(دق.بائیں_نکالیں())    // 5
لکھو(دق.دائیں_نکالیں())    // 20
لکھو(دق.بائیں_جھانکیں())   // 10
```

| Method | Description |
|--------|-------------|
| `.دائیں_شامل(قدر)` | Append to right — O(1) |
| `.بائیں_شامل(قدر)` | Prepend to left — O(1) |
| `.دائیں_نکالیں()` | Pop from right — O(1) |
| `.بائیں_نکالیں()` | Pop from left — O(1) |
| `.دائیں_جھانکیں()` | Peek right without removing |
| `.بائیں_جھانکیں()` | Peek left without removing |
| `.خالی_ہے()` | `True` if empty |
| `len(دق)` | Current length |

---

## ترجیحی_قطار — Priority Queue / Heap

Min-Heap by default. Pass `زیادہ_سے_زیادہ=سچ` for Max-Heap.

```urdu
متغیر پق = نیا ترجیحی_قطار()          // Min-Heap
پق.شامل_کریں("کم", ترجیح=1)
پق.شامل_کریں("درمیانی", ترجیح=5)
پق.شامل_کریں("زیادہ", ترجیح=10)
لکھو(پق.نکالیں())    // "کم"  (lowest priority number = highest priority)
لکھو(پق.نکالیں())    // "درمیانی"

متغیر زق = نیا ترجیحی_قطار(زیادہ_سے_زیادہ=سچ)  // Max-Heap
زق.شامل_کریں("الف", ترجیح=3)
زق.شامل_کریں("ب", ترجیح=7)
لکھو(زق.نکالیں())    // "ب"  (highest priority number first)
```

| Method | Description |
|--------|-------------|
| `.شامل_کریں(قدر, ترجیح=0)` | Push with numeric priority — O(log n) |
| `.نکالیں()` | Pop highest-priority item — O(log n) |
| `.جھانکیں()` | Peek without removing |
| `.خالی_ہے()` | `True` if empty |
| `len(پق)` | Number of items |

---

## بائنری_تلاش_درخت — Binary Search Tree

ترتیب شدہ بائنری درخت — sorted insert, in-order traversal, min/max, height.

```urdu
متغیر درخت = نیا بائنری_تلاش_درخت()
کے_لیے (متغیر ق کا [5, 3, 7, 1, 4, 6, 8]) {
    درخت.داخل_کریں(ق)
}
لکھو(درخت.ترتیب_سے())       // [1, 3, 4, 5, 6, 7, 8]
لکھو(درخت.سب_سے_چھوٹا())   // 1
لکھو(درخت.سب_سے_بڑا())     // 8
لکھو(درخت.اونچائی())        // 3
درخت.نکالیں(3)
لکھو(درخت.ترتیب_سے())       // [1, 4, 5, 6, 7, 8]
```

| Method | Description |
|--------|-------------|
| `.داخل_کریں(قدر)` | Insert value — O(log n) average |
| `.نکالیں(قدر)` | Remove value — O(log n) average |
| `.ترتیب_سے()` | In-order traversal — returns sorted list |
| `.سب_سے_چھوٹا()` | Minimum value |
| `.سب_سے_بڑا()` | Maximum value |
| `.اونچائی()` | Tree height |
| `len(درخت)` | Number of nodes |

---

## گراف — Graph

ملحقہ فہرست (adjacency-list) graph. Supports directed and undirected, weighted edges, BFS, DFS, Dijkstra shortest path, and topological sort.

```urdu
متغیر گ = نیا گراف()                     // undirected
گ.کنارہ_شامل_کریں("الف", "ب", وزن=4)
گ.کنارہ_شامل_کریں("الف", "ج", وزن=2)
گ.کنارہ_شامل_کریں("ب", "د", وزن=1)
گ.کنارہ_شامل_کریں("ج", "د", وزن=5)

لکھو(گ.چوڑائی_تلاش("الف"))     // BFS order
لکھو(گ.گہرائی_تلاش("الف"))     // DFS order
لکھو(گ.مختصر_راستہ("الف", "د")) // Dijkstra — {'الف': 0, 'ب': 4, 'ج': 2, 'د': 5}

// Directed graph + topological sort
متغیر ہ = نیا گراف(ہدایت_یافتہ=سچ)
ہ.کنارہ_شامل_کریں("A", "B")
ہ.کنارہ_شامل_کریں("A", "C")
ہ.کنارہ_شامل_کریں("B", "D")
لکھو(ہ.طوپو_ترتیب())           // ['A', 'C', 'B', 'D'] (one valid order)
```

| Method | Description |
|--------|-------------|
| `.کونا_شامل_کریں(v)` | Add a vertex |
| `.کنارہ_شامل_کریں(u, v, وزن=1)` | Add an edge (both directions if undirected) |
| `.ہم_سایہ(v)` | Neighbours of vertex v |
| `.کونے()` | All vertices |
| `.کنارے()` | All edges as `(u, v, weight)` tuples |
| `.چوڑائی_تلاش(آغاز)` | BFS — returns visit order |
| `.گہرائی_تلاش(آغاز)` | DFS — returns visit order |
| `.مختصر_راستہ(آغاز, ہدف=None)` | Dijkstra — returns `{vertex: distance}` dict |
| `.طوپو_ترتیب()` | Topological sort (directed graphs only) |

---

## All Classes — Quick Reference

| Class | Type | Key operations |
|-------|------|---------------|
| `مربوط_فہرست` | Singly linked list | `شامل_کریں`, `نکالیں`, `الٹا_کریں` |
| `ڈھیر` | Stack (LIFO) | `دھکیلیں`, `نکالیں`, `جھانکیں` |
| `قطار` | Queue (FIFO) | `شامل_کریں`, `نکالیں`, `اگلا` |
| `دوطرفہ_قطار` | Deque | `بائیں/دائیں_شامل`, `بائیں/دائیں_نکالیں` |
| `ترجیحی_قطار` | Min/Max heap | `شامل_کریں(قدر, ترجیح)`, `نکالیں` |
| `بائنری_تلاش_درخت` | BST | `داخل_کریں`, `نکالیں`, `ترتیب_سے` |
| `گراف` | Adjacency-list graph | `کنارہ_شامل_کریں`, `BFS`, `Dijkstra` |
