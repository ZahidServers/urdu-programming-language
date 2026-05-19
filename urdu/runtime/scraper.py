"""
HTML/XML parser and web scraper for the Urdu Programming Language.
Wraps BeautifulSoup4 with Urdu-named methods and properties.

Usage:
    درآمد { صفحہ_بناؤ, کھرچو } سے "اردو/کھرچنی";
"""

from __future__ import annotations
import asyncio
from typing import Optional, List
from .builtins import _UrduObj


# ─── helpers ─────────────────────────────────────────────────────────────────

def _wrap(tag):
    if tag is None or not hasattr(tag, "name") or tag.name is None:
        return None
    return _عنصر(tag)

def _wrap_list(tags):
    return [_عنصر(t) for t in tags]

def _attr_val(val):
    """BS4 returns list for multi-value attrs like class; join them."""
    return " ".join(val) if isinstance(val, list) else val


# ─── Element wrapper ──────────────────────────────────────────────────────────

class _عنصر:
    """Wraps a BeautifulSoup Tag with Urdu-named interface."""

    def __init__(self, tag):
        self._tag = tag

    # ── Identity ──────────────────────────────────────────────────────────────

    @property
    def ٹیگ(self) -> str:
        """Tag name — e.g. 'div', 'a', 'p'."""
        return self._tag.name or ""

    @property
    def شناخت(self) -> str:
        """Value of the id attribute."""
        return self._tag.get("id", "") or ""

    # ── Content ───────────────────────────────────────────────────────────────

    @property
    def متن(self) -> str:
        """All text content (get_text())."""
        return self._tag.get_text()

    @property
    def صاف_متن(self) -> str:
        """Text with leading/trailing whitespace stripped."""
        return self._tag.get_text(strip=True)

    @property
    def اندرونی_html(self) -> str:
        """Inner HTML (children serialised, no outer tag)."""
        return self._tag.decode_contents()

    @property
    def بیرونی_html(self) -> str:
        """Outer HTML including this tag."""
        return str(self._tag)

    @property
    def خوبصورت(self) -> str:
        """Prettified / indented outer HTML."""
        return self._tag.prettify()

    # ── Attributes ────────────────────────────────────────────────────────────

    @property
    def خصوصیات(self) -> _UrduObj:
        """All attributes as an _UrduObj dict."""
        return _UrduObj({k: _attr_val(v) for k, v in self._tag.attrs.items()})

    def __getitem__(self, key: str):
        """Access an attribute by name: عنصر["href"]."""
        return _attr_val(self._tag.get(key))

    # ── Navigation ────────────────────────────────────────────────────────────

    @property
    def والد(self) -> Optional["_عنصر"]:
        """Parent element."""
        p = self._tag.parent
        return _wrap(p)

    @property
    def بچے(self) -> List["_عنصر"]:
        """Direct child elements (tags only, no text nodes)."""
        return [_عنصر(c) for c in self._tag.children
                if hasattr(c, "name") and c.name]

    @property
    def اگلا(self) -> Optional["_عنصر"]:
        """Next sibling element."""
        s = self._tag.next_sibling
        while s and not (hasattr(s, "name") and s.name):
            s = s.next_sibling
        return _wrap(s)

    @property
    def پچھلا(self) -> Optional["_عنصر"]:
        """Previous sibling element."""
        s = self._tag.previous_sibling
        while s and not (hasattr(s, "name") and s.name):
            s = s.previous_sibling
        return _wrap(s)

    # ── Search ────────────────────────────────────────────────────────────────

    def تلاش(self, ٹیگ_نام: str = None,
              خصوصیات: dict = None) -> Optional["_عنصر"]:
        """Find first matching descendant (find())."""
        result = self._tag.find(ٹیگ_نام, attrs=خصوصیات or {})
        return _wrap(result)

    def سب_تلاش(self, ٹیگ_نام: str = None,
                 خصوصیات: dict = None,
                 حد: int = 0) -> List["_عنصر"]:
        """Find all matching descendants (find_all()). حد limits results."""
        kwargs: dict = {"attrs": خصوصیات or {}}
        if حد:
            kwargs["limit"] = حد
        return _wrap_list(self._tag.find_all(ٹیگ_نام, **kwargs))

    def چنو(self, انتخاب: str) -> List["_عنصر"]:
        """CSS selector — returns list of matches (select())."""
        return _wrap_list(self._tag.select(انتخاب))

    def ایک_چنو(self, انتخاب: str) -> Optional["_عنصر"]:
        """CSS selector — first match only (select_one())."""
        return _wrap(self._tag.select_one(انتخاب))

    # ── Misc ──────────────────────────────────────────────────────────────────

    def __str__(self):
        return str(self._tag)

    def __repr__(self):
        return f"<عنصر <{self.ٹیگ}>>"

    def __bool__(self):
        return self._tag is not None

    def __len__(self):
        return len(self.بچے)


# ─── Document (صفحہ) ──────────────────────────────────────────────────────────

class صفحہ(_عنصر):
    """
    HTML/XML document parser — BeautifulSoup4 wrapper.

    تجزیہ_کار options:
      "html.parser"  — Python stdlib (no extra install)
      "lxml"         — faster, requires lxml
      "html5lib"     — most lenient, requires html5lib
    """

    def __init__(self, html: str, تجزیہ_کار: str = "html.parser"):
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            raise ImportError(
                "beautifulsoup4 نصب کریں:  urdu نصب اردو/کھرچنی"
            )
        super().__init__(BeautifulSoup(html, تجزیہ_کار))

    @property
    def عنوان(self) -> str:
        """Page <title> text."""
        t = self._tag.find("title")
        return t.get_text(strip=True) if t else ""

    def __repr__(self):
        return f"<صفحہ عنوان='{self.عنوان}'>"


# ─── Standalone functions ─────────────────────────────────────────────────────

def صفحہ_بناؤ(html: str, تجزیہ_کار: str = "html.parser") -> صفحہ:
    """Parse an HTML/XML string. Returns صفحہ."""
    return صفحہ(html, تجزیہ_کار)


async def کھرچو(url: str,
                 سرخط: dict = None,
                 تجزیہ_کار: str = "html.parser") -> صفحہ:
    """Fetch a URL and parse its HTML. Returns صفحہ."""
    def _fetch():
        import requests as _req
        r = _req.get(url, headers=سرخط or {}, timeout=30)
        r.raise_for_status()
        return r.text

    html = await asyncio.to_thread(_fetch)
    return صفحہ(html, تجزیہ_کار)


# ─── Exports ──────────────────────────────────────────────────────────────────

__all__ = [
    "صفحہ", "_عنصر",
    "صفحہ_بناؤ", "کھرچو",
    # English aliases
    "Page", "Element",
    "parse_html", "scrape",
]

# English aliases
Page       = صفحہ
Element    = _عنصر
parse_html = صفحہ_بناؤ
scrape     = کھرچو
