"""
urdu_templates.py — Urdu template keyword support for Jinja2 (Flask) and Django.

Allows writing .html templates with Urdu tag keywords, operators, and filter
names. All Urdu syntax is preprocessed into standard Jinja2/Django syntax
transparently before rendering — no changes to the underlying engines.

Supported syntax:
  {% اگر x %}          →  {% if x %}
  {% کے_لیے i کا list %} →  {% for i in list %}
  {{ نام|بڑا }}         →  {{ نام|upper }}
  {{ سچ }}              →  {{ true }}
"""

from __future__ import annotations
import re

# ── Tag keyword map  ({% first_word ... %}) ───────────────────────────────────

TAG_MAP: dict[str, str] = {
    "اگر":               "if",
    "ورنہ":              "else",
    "وگرنہ":             "elif",
    "اگر_ختم":           "endif",
    "کے_لیے":            "for",
    "کے_لیے_ختم":        "endfor",
    "بلاک":              "block",
    "بلاک_ختم":          "endblock",
    "توسیع":             "extends",
    "شامل":              "include",
    "متغیر":             "set",
    "ساتھ":              "with",
    "ساتھ_ختم":          "endwith",
    "میکرو":             "macro",
    "میکرو_ختم":         "endmacro",
    "کال":               "call",
    "کال_ختم":           "endcall",
    "فلٹر_لگائیں":        "filter",
    "فلٹر_لگائیں_ختم":    "endfilter",
    "خام":               "raw",
    "خام_ختم":           "endraw",
    "درآمد_سانچہ":        "import",
    "سے_سانچہ":           "from",
    "بطور":              "as",
}

# ── Expression keyword map  (operators, literals, special vars) ───────────────

EXPR_MAP: dict[str, str] = {
    # operators
    "اور":        "and",
    "یا":         "or",
    "نہیں":       "not",
    "کا":         "in",           # for x کا items  /  if x کا items
    "ہے":         "is",
    # literals
    "سچ":         "true",
    "جھوٹ":       "false",
    "خالی":       "none",
    # special Jinja2 vars
    "لوپ":        "loop",
    "سپر":        "super",
    "خود":        "self",
}

# ── Attribute map  (.اردو → .english, for loop.*, request.*, etc.) ────────────

ATTR_MAP: dict[str, str] = {
    # loop variable attributes
    "اشاریہ":         "index",
    "اشاریہ0":        "index0",
    "الٹا_اشاریہ":    "revindex",
    "الٹا_اشاریہ0":   "revindex0",
    "پہلا":           "first",
    "آخری":           "last",
    "طول":            "length",
    "گہرائی":         "depth",
    "گہرائی0":        "depth0",
    "بدلا":           "changed",
    "گنا":            "count",
    # common request/object attributes (passthrough if not matched)
    "طریقہ":          "method",
    "راستہ":          "path",
    "نام":            "name",
    "قدر":            "value",
    "اقدار":          "values",
    "کلیدیں":         "keys",
    "اشیاء":          "items",
}

# ── Filter map  (|اردو → |english) ───────────────────────────────────────────

FILTER_MAP: dict[str, str] = {
    "بڑا":            "upper",
    "چھوٹا":           "lower",
    "طول":            "length",
    "ملائیں":          "join",
    "پہلے_سے":         "default",
    "محفوظ":           "safe",
    "فرار":            "escape",
    "تراشیں":          "trim",
    "بدلیں":           "replace",
    "پہلا":            "first",
    "آخری":            "last",
    "الٹا":            "reverse",
    "ترتیب":           "sort",
    "منفرد":           "unique",
    "فہرست_بنائیں":    "list",
    "سلسلہ":           "string",
    "عدد":             "int",
    "اعشاری":          "float",
    "گول":             "round",
    "مطلق":            "abs",
    "جمع":             "sum",
    "شمار":            "count",
    "عنوانی":          "title",
    "بڑا_حرف":         "capitalize",
    "صاف":             "strip",
    "کاٹیں":           "truncate",
    "الفاظ":           "wordcount",
    "ٹیگ_ہٹائیں":      "striptags",
    "فائل_حجم":        "filesizeformat",
    "نقشہ":            "map",
    "چنیں":            "select",
    "رد":              "reject",
    "خاصیت_چنیں":     "selectattr",
    "گروہ":            "batch",
    "گروہ_بندی":       "groupby",
    "ترتیب_لغت":       "dictsort",
    "دانت":            "indent",
    "ربط":             "urlize",
    "فارمیٹ":          "format",
    "مواد":            "items",
    "اشیاء":           "items",
    "قدریں":           "values",
    "کلیدیں":          "keys",
}

# ── Regex patterns ────────────────────────────────────────────────────────────

# Matches any Urdu/Arabic word (starts with Arabic-script char)
_U = r"[؀-ۿݐ-ݿ]"
_UWORD = _U + r"[؀-ۿݐ-ݿ\w_]*"


# ── Expression translator ─────────────────────────────────────────────────────

def _translate_expr(expr: str) -> str:
    """Translate Urdu filters, operators and special vars inside an expression."""

    # 1. Filter names after |
    def _filt(m: re.Match) -> str:
        name = m.group(1)
        return "|" + FILTER_MAP.get(name, name)

    expr = re.sub(r"\|(" + _UWORD + r")", _filt, expr)

    # 2. Attribute access  .اردو → .english
    def _attr(m: re.Match) -> str:
        name = m.group(1)
        return "." + ATTR_MAP.get(name, name)

    expr = re.sub(r"\.(" + _UWORD + r")", _attr, expr)

    # 3. Standalone Urdu words (operators, literals, special vars)
    def _word(m: re.Match) -> str:
        word = m.group(0)
        return EXPR_MAP.get(word, word)

    expr = re.sub(_UWORD, _word, expr)

    return expr


# ── Tag translator ────────────────────────────────────────────────────────────

def _translate_tag(inner: str) -> str:
    """Translate the body of a {% ... %} tag."""
    inner = inner.strip()
    if not inner:
        return inner
    m = re.match(r"^(\S+)(.*)", inner, re.DOTALL)
    if not m:
        return inner
    keyword, rest = m.group(1), m.group(2)
    keyword = TAG_MAP.get(keyword, keyword)
    if rest:
        rest = _translate_expr(rest)
    return keyword + rest


# ── Main preprocessor ─────────────────────────────────────────────────────────

def preprocess(source: str) -> str:
    """
    Preprocess a Jinja2/Django template, translating Urdu keywords.

    Handles {% %}, {{ }}, {# #} tokens; plain HTML/text is untouched.
    Urdu and standard Jinja2 keywords can be freely mixed in the same file.
    """
    parts: list[str] = []
    i = 0
    n = len(source)

    while i < n:
        c2 = source[i:i + 2]

        if c2 == "{#":                          # comment — pass through unchanged
            end = source.find("#}", i + 2)
            if end == -1:
                parts.append(source[i:])
                break
            parts.append(source[i:end + 2])
            i = end + 2

        elif c2 == "{{":                        # variable expression
            end = source.find("}}", i + 2)
            if end == -1:
                parts.append(source[i:])
                break
            inner = source[i + 2:end]
            parts.append("{{" + _translate_expr(inner) + "}}")
            i = end + 2

        elif c2 == "{%":                        # tag
            end = source.find("%}", i + 2)
            if end == -1:
                parts.append(source[i:])
                break
            inner = source[i + 2:end]
            # Preserve Jinja2 whitespace-control dashes
            ls = "-" if inner.startswith("-") else ""
            rs = "-" if inner.endswith("-") else ""
            body = inner.lstrip("-").rstrip("-")
            translated = _translate_tag(body)
            parts.append("{%" + ls + " " + translated + " " + rs + "%}")
            i = end + 2

        else:                                   # plain text
            j = source.find("{", i + 1)
            if j == -1:
                parts.append(source[i:])
                break
            parts.append(source[i:j])
            i = j

    return "".join(parts)


# ── Jinja2 / Flask loader ─────────────────────────────────────────────────────

class UrduJinja2Loader:
    """
    Wraps any Jinja2 loader and preprocesses Urdu keywords transparently.
    Assign to flask_app.jinja_loader after creating the Flask instance.
    """

    def __init__(self, inner):
        self._inner = inner

    def get_source(self, environment, template):
        source, filename, uptodate = self._inner.get_source(environment, template)
        return preprocess(source), filename, uptodate

    def list_templates(self):
        return self._inner.list_templates()


# ── Django loader ─────────────────────────────────────────────────────────────

def make_django_loader_class():
    """
    Lazily build UrduFilesystemLoader so Django is not imported at module load.
    Returns a Django template loader class that preprocesses Urdu keywords.
    """
    from django.template.loaders.filesystem import Loader as _FSLoader

    class UrduFilesystemLoader(_FSLoader):
        def get_contents(self, origin):
            return preprocess(super().get_contents(origin))

    return UrduFilesystemLoader


try:
    from django.template.loaders.filesystem import Loader as _DjangoFSLoader

    class UrduFilesystemLoader(_DjangoFSLoader):
        """
        Django template loader that preprocesses Urdu keywords.
        Use dotted path ``urdu.runtime.urdu_templates.UrduFilesystemLoader``
        in Django's TEMPLATES OPTIONS loaders list.
        """
        def get_contents(self, origin):
            return preprocess(super().get_contents(origin))

except ImportError:
    class UrduFilesystemLoader:  # type: ignore[no-redef]
        """Placeholder when Django is not installed."""


# ── Public API ────────────────────────────────────────────────────────────────

__all__ = [
    "preprocess",
    "UrduJinja2Loader",
    "UrduFilesystemLoader",
    "make_django_loader_class",
    "TAG_MAP",
    "EXPR_MAP",
    "ATTR_MAP",
    "FILTER_MAP",
]
