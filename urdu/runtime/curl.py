"""
HTTP client (cURL-style) for the Urdu Programming Language.
Supports GET, POST, PUT, PATCH, DELETE, file upload, file download,
Bearer/Basic auth, cookies, query params, custom headers, proxy, SSL toggle.

Usage:
    درآمد { کرل, حاصل_کرو, بھیجو } سے "اردو/کرل";
"""

from __future__ import annotations
import asyncio
import base64
import os
from typing import Optional
from .builtins import _UrduObj


# ─── Response wrapper ────────────────────────────────────────────────────────

class _کرل_جواب:
    """Wraps an HTTP response with Urdu-named properties."""

    def __init__(self, resp):
        self._resp = resp

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def حالت(self) -> int:
        """HTTP status code (e.g. 200, 404)."""
        return self._resp.status_code

    @property
    def متن(self) -> str:
        """Response body as text."""
        return self._resp.text

    @property
    def مواد(self) -> bytes:
        """Response body as raw bytes."""
        return self._resp.content

    @property
    def سرخط(self) -> dict:
        """Response headers dict."""
        return dict(self._resp.headers)

    @property
    def ٹھیک(self) -> bool:
        """True if status code is 2xx."""
        return self._resp.status_code < 400

    @property
    def ربط(self) -> str:
        """Response URL."""
        return str(self._resp.url)

    def جے_سون(self):
        """Parse response body as JSON. Returns _UrduObj for dicts."""
        data = self._resp.json()
        if isinstance(data, dict):
            return _UrduObj(data)
        if isinstance(data, list):
            return [_UrduObj(d) if isinstance(d, dict) else d for d in data]
        return data

    # English aliases for Python interop
    @property
    def url(self): return self.ربط
    def json(self): return self.جے_سون()

    def __bool__(self):
        return self._resp.status_code < 400

    def __str__(self):
        return f"<جواب [{self._resp.status_code}] {self._resp.url}>"

    def __repr__(self):
        return self.__str__()


# ─── Main cURL class ──────────────────────────────────────────────────────────

class کرل:
    """
    HTTP client with a cURL-like interface.

    config keys:
      سرخط          — default headers dict
      ختمی           — timeout in seconds (default 30)
      تصدیق_نہ_کرو  — disable SSL verification (default False)
      بنیادی_url     — base URL prefix
      پراکسی         — {"http": "...", "https": "..."}
      ری_ڈائریکٹ    — follow redirects (default True)
    """

    def __init__(self, config: dict = None):
        cfg = config or {}
        self._headers:  dict = dict(cfg.get("سرخط", {}))
        self._timeout:  int  = cfg.get("ختمی", 30)
        self._verify:   bool = not cfg.get("تصدیق_نہ_کرو", False)
        self._base_url: str  = cfg.get("بنیادی_url", "").rstrip("/")
        self._proxies        = cfg.get("پراکسی", None)
        self._redirects:bool = cfg.get("ری_ڈائریکٹ", True)
        self._cookies:  dict = {}
        self._session        = None   # lazy requests.Session

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _session_(self):
        if self._session is None:
            import requests as _req
            self._session = _req.Session()
        return self._session

    def _full_url(self, url: str) -> str:
        if self._base_url and not url.startswith("http"):
            return f"{self._base_url}/{url.lstrip('/')}"
        return url

    def _hdrs(self, extra: dict = None) -> dict:
        h = dict(self._headers)
        if extra:
            h.update(extra)
        return h

    def _req(self, method: str, url: str, **kwargs) -> _کرل_جواب:
        """Synchronous request — called via asyncio.to_thread."""
        import requests as _req
        kwargs.setdefault("timeout", self._timeout)
        kwargs.setdefault("verify",  self._verify)
        kwargs.setdefault("allow_redirects", self._redirects)
        if self._proxies:
            kwargs.setdefault("proxies", self._proxies)
        if self._cookies:
            kwargs.setdefault("cookies", self._cookies)
        r = self._session_().request(method, self._full_url(url), **kwargs)
        return _کرل_جواب(r)

    async def _areq(self, method: str, url: str, **kwargs) -> _کرل_جواب:
        return await asyncio.to_thread(self._req, method, url, **kwargs)

    # ── HTTP verbs ────────────────────────────────────────────────────────────

    async def حاصل(self, url: str, پیرامیٹر: dict = None,
                    سرخط: dict = None) -> _کرل_جواب:
        """GET request."""
        return await self._areq("GET", url,
                                params=پیرامیٹر, headers=self._hdrs(سرخط))

    async def بھیجو(self, url: str, ڈیٹا=None,
                     سرخط: dict = None) -> _کرل_جواب:
        """POST request. Sends dict as JSON, string/bytes as body."""
        h = self._hdrs(سرخط)
        if isinstance(ڈیٹا, dict):
            return await self._areq("POST", url, json=ڈیٹا, headers=h)
        return await self._areq("POST", url, data=ڈیٹا, headers=h)

    async def فارم_بھیجو(self, url: str, ڈیٹا: dict,
                           سرخط: dict = None) -> _کرل_جواب:
        """POST with application/x-www-form-urlencoded."""
        return await self._areq("POST", url,
                                data=ڈیٹا, headers=self._hdrs(سرخط))

    async def تازہ(self, url: str, ڈیٹا=None,
                    سرخط: dict = None) -> _کرل_جواب:
        """PUT request."""
        h = self._hdrs(سرخط)
        if isinstance(ڈیٹا, dict):
            return await self._areq("PUT", url, json=ڈیٹا, headers=h)
        return await self._areq("PUT", url, data=ڈیٹا, headers=h)

    async def جزوی_تازہ(self, url: str, ڈیٹا: dict = None,
                          سرخط: dict = None) -> _کرل_جواب:
        """PATCH request."""
        return await self._areq("PATCH", url,
                                json=ڈیٹا, headers=self._hdrs(سرخط))

    async def مٹاؤ(self, url: str, سرخط: dict = None) -> _کرل_جواب:
        """DELETE request."""
        return await self._areq("DELETE", url, headers=self._hdrs(سرخط))

    async def سر(self, url: str, سرخط: dict = None) -> _کرل_جواب:
        """HEAD request."""
        return await self._areq("HEAD", url, headers=self._hdrs(سرخط))

    async def اختیارات(self, url: str, سرخط: dict = None) -> _کرل_جواب:
        """OPTIONS request."""
        return await self._areq("OPTIONS", url, headers=self._hdrs(سرخط))

    # ── File operations ───────────────────────────────────────────────────────

    async def فائل_بھیجو(self, url: str, فائل_راستہ: str,
                           خانہ: str = "file",
                           اضافی_ڈیٹا: dict = None,
                           سرخط: dict = None) -> _کرل_جواب:
        """Upload a file via multipart/form-data."""
        def _upload():
            import requests as _req
            fname = os.path.basename(فائل_راستہ)
            with open(فائل_راستہ, "rb") as f:
                files = {خانہ: (fname, f)}
                data  = اضافی_ڈیٹا or {}
                r = _req.post(self._full_url(url), files=files, data=data,
                              headers=self._hdrs(سرخط),
                              timeout=self._timeout, verify=self._verify)
                return _کرل_جواب(r)
        return await asyncio.to_thread(_upload)

    async def فائل_حاصل(self, url: str, محفوظ_راستہ: str,
                          سرخط: dict = None) -> _کرل_جواب:
        """Download a file and save to disk. Returns response."""
        def _download():
            import requests as _req
            with _req.get(self._full_url(url), headers=self._hdrs(سرخط),
                          stream=True, timeout=self._timeout,
                          verify=self._verify) as r:
                with open(محفوظ_راستہ, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                return _کرل_جواب(r)
        return await asyncio.to_thread(_download)

    # ── Auth shortcuts ────────────────────────────────────────────────────────

    def ٹوکن_مقرر(self, token: str) -> "کرل":
        """Set Authorization: Bearer <token>."""
        self._headers["Authorization"] = f"Bearer {token}"
        return self

    def بنیادی_توثیق(self, صارف: str, پاس_ورڈ: str) -> "کرل":
        """Set Authorization: Basic <base64(user:pass)>."""
        cred = base64.b64encode(f"{صارف}:{پاس_ورڈ}".encode()).decode()
        self._headers["Authorization"] = f"Basic {cred}"
        return self

    def کلید_توثیق(self, کلید: str, قدر: str,
                    جگہ: str = "header") -> "کرل":
        """Set API key — جگہ='header' or 'query' (not implemented for query)."""
        if جگہ == "header":
            self._headers[کلید] = قدر
        return self

    def سرخط_مقرر(self, کلید: str, قدر: str) -> "کرل":
        """Set a single request header."""
        self._headers[کلید] = قدر
        return self

    def کوکی_مقرر(self, کلید: str, قدر: str) -> "کرل":
        """Set a cookie."""
        self._cookies[کلید] = قدر
        return self

    def سیشن_بند(self):
        """Close the underlying requests.Session."""
        if self._session:
            self._session.close()
            self._session = None


# ─── pycurl helper ───────────────────────────────────────────────────────────

class پائی_کرل:
    """
    Low-level pycurl wrapper for advanced use cases
    (custom SSL ciphers, SFTP, FTP, DNS override, etc.).
    """

    @staticmethod
    def دستیاب() -> bool:
        try:
            import pycurl
            return True
        except ImportError:
            return False

    @staticmethod
    async def حاصل(url: str, سرخط: list = None) -> bytes:
        """GET via pycurl, returns raw bytes."""
        def _go():
            import pycurl, io
            buf = io.BytesIO()
            c = pycurl.Curl()
            c.setopt(pycurl.URL, url.encode())
            c.setopt(pycurl.WRITEDATA, buf)
            if سرخط:
                c.setopt(pycurl.HTTPHEADER, [h.encode() for h in سرخط])
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.TIMEOUT, 30)
            c.perform()
            c.close()
            return buf.getvalue()
        return await asyncio.to_thread(_go)

    @staticmethod
    async def بھیجو(url: str, ڈیٹا: str, سرخط: list = None) -> bytes:
        """POST via pycurl, returns raw bytes."""
        def _go():
            import pycurl, io
            buf = io.BytesIO()
            c = pycurl.Curl()
            c.setopt(pycurl.URL, url.encode())
            c.setopt(pycurl.WRITEDATA, buf)
            post_bytes = ڈیٹا.encode('utf-8') if isinstance(ڈیٹا, str) else ڈیٹا
            c.setopt(pycurl.POSTFIELDSIZE, len(post_bytes))
            c.setopt(pycurl.COPYPOSTFIELDS, post_bytes)
            hdrs = سرخط or []
            if isinstance(ڈیٹا, (dict, list)):
                import json as _json
                c.setopt(pycurl.POSTFIELDS, _json.dumps(ڈیٹا))
                hdrs = list(hdrs) + ["Content-Type: application/json"]
            if hdrs:
                c.setopt(pycurl.HTTPHEADER, [h.encode() for h in hdrs])
            c.setopt(pycurl.TIMEOUT, 30)
            c.perform()
            c.close()
            return buf.getvalue()
        return await asyncio.to_thread(_go)


# ─── Standalone quick functions ───────────────────────────────────────────────

_default = کرل()


async def کرل_حاصل(url: str, پیرامیٹر: dict = None,
                    سرخط: dict = None) -> _کرل_جواب:
    """Quick GET request."""
    return await _default.حاصل(url, پیرامیٹر=پیرامیٹر, سرخط=سرخط)


async def بھیجو_کرو(url: str, ڈیٹا=None,
                     سرخط: dict = None) -> _کرل_جواب:
    """Quick POST request."""
    return await _default.بھیجو(url, ڈیٹا, سرخط=سرخط)


async def تازہ_کرو(url: str, ڈیٹا=None,
                    سرخط: dict = None) -> _کرل_جواب:
    """Quick PUT request."""
    return await _default.تازہ(url, ڈیٹا, سرخط=سرخط)


async def جزوی_تازہ_کرو(url: str, ڈیٹا: dict = None,
                           سرخط: dict = None) -> _کرل_جواب:
    """Quick PATCH request."""
    return await _default.جزوی_تازہ(url, ڈیٹا, سرخط=سرخط)


async def مٹاؤ_کرو(url: str, سرخط: dict = None) -> _کرل_جواب:
    """Quick DELETE request."""
    return await _default.مٹاؤ(url, سرخط=سرخط)


# ─── Exports ──────────────────────────────────────────────────────────────────

__all__ = [
    # classes
    "کرل", "پائی_کرل", "_کرل_جواب",
    # standalone functions
    "کرل_حاصل", "بھیجو_کرو", "تازہ_کرو", "جزوی_تازہ_کرو", "مٹاؤ_کرو",
    # English aliases
    "Curl", "PyCurl", "CurlResponse",
    "curl_get", "curl_post", "curl_put", "curl_patch", "curl_delete",
]

# English aliases
Curl        = کرل
PyCurl      = پائی_کرل
CurlResponse = _کرل_جواب
curl_get    = کرل_حاصل
curl_post   = بھیجو_کرو
curl_put    = تازہ_کرو
curl_patch  = جزوی_تازہ_کرو
curl_delete = مٹاؤ_کرو
