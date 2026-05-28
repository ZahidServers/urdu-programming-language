"""اردو/متن — Text & String Library for Urdu Programming Language."""

from __future__ import annotations
import re as _re
import unicodedata as _ud

# ─── Urdu/Arabic Unicode constants ───────────────────────────────────────────

# Diacritical marks (اعراب): fathatan → wavy hamza + superscript alef
_DIACRITICS = _re.compile(r'[ً-ٰٟ]')

# Eastern Arabic ↔ Western numeral tables
_EAST_TO_WEST = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
_WEST_TO_EAST = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')

# Nastaliq normalisation map
_NASTALIQ = str.maketrans({
    'أ': 'ا',   # أ  → ا
    'إ': 'ا',   # إ  → ا
    'ؤ': 'و',   # ؤ  → و
    'ئ': 'ی',   # ئ  → ی
    'ك': 'ک',   # ك  → ک  (Arabic kaf → Urdu kaf)
    'ي': 'ی',   # ي  → ی  (Arabic ya → Urdu ya)
    'ة': 'ہ',   # ة  → ہ  (teh marbuta → he)
    'ه': 'ہ',   # ه  → ہ  (Arabic he → Urdu he)
})

# ─── Urdu number words ────────────────────────────────────────────────────────

_اعداد_0_99 = [
    "صفر",    "ایک",     "دو",      "تین",     "چار",     "پانچ",    "چھ",      "سات",     "آٹھ",     "نو",
    "دس",     "گیارہ",   "بارہ",    "تیرہ",    "چودہ",    "پندرہ",   "سولہ",    "سترہ",    "اٹھارہ",  "انیس",
    "بیس",    "اکیس",    "بائیس",   "تئیس",    "چوبیس",   "پچیس",    "چھبیس",   "ستائیس",  "اٹھائیس", "انتیس",
    "تیس",    "اکتیس",   "بتیس",    "تینتیس",  "چونتیس",  "پینتیس",  "چھتیس",   "سینتیس",  "اڑتیس",   "انتالیس",
    "چالیس",  "اکتالیس", "بیالیس",  "تینتالیس","چوالیس",  "پینتالیس","چھیالیس", "سینتالیس","اڑتالیس", "انچاس",
    "پچاس",   "اکاون",   "باون",    "ترپن",    "چوون",    "پچپن",    "چھپن",    "ستاون",   "اٹھاون",  "انسٹھ",
    "ساٹھ",   "اکسٹھ",   "باسٹھ",   "ترسٹھ",   "چوسٹھ",   "پینسٹھ",  "چھیاسٹھ", "سڑسٹھ",   "اڑسٹھ",   "انہتر",
    "ستر",    "اکہتر",   "بہتر",    "تہتر",    "چوہتر",   "پچہتر",   "چھہتر",   "ستہتر",   "اٹھہتر",  "نوہتر",
    "اسی",    "اکیاسی",  "بیاسی",   "تراسی",   "چوراسی",  "پچاسی",   "چھیاسی",  "ستاسی",   "اٹھاسی",  "نواسی",
    "نوے",    "اکانوے",  "بانوے",   "ترانوے",  "چورانوے", "پچانوے",  "چھیانوے", "ستانوے",  "اٹھانوے", "نناوے",
]


def _عدد_لفظ(ن: int) -> str:
    if ن < 100:
        return _اعداد_0_99[ن]
    if ن < 1_000:
        سو, باقی = divmod(ن, 100)
        return _اعداد_0_99[سو] + " سو" + (" " + _اعداد_0_99[باقی] if باقی else "")
    if ن < 100_000:
        ہزار, باقی = divmod(ن, 1_000)
        return _عدد_لفظ(ہزار) + " ہزار" + (" " + _عدد_لفظ(باقی) if باقی else "")
    if ن < 10_000_000:
        لاکھ, باقی = divmod(ن, 100_000)
        return _عدد_لفظ(لاکھ) + " لاکھ" + (" " + _عدد_لفظ(باقی) if باقی else "")
    کروڑ, باقی = divmod(ن, 10_000_000)
    return _عدد_لفظ(کروڑ) + " کروڑ" + (" " + _عدد_لفظ(باقی) if باقی else "")


# ─── Basic string operations ─────────────────────────────────────────────────

def بڑے_حروف(متن: str) -> str:     return متن.upper()
def چھوٹے_حروف(متن: str) -> str:   return متن.lower()
def عنوانی(متن: str) -> str:        return متن.title()
def الٹا_کریں(متن: str) -> str:    return متن[::-1]
def تراشو(متن: str, حروف=None) -> str:       return متن.strip(حروف)
def بائیں_تراشو(متن: str, حروف=None) -> str: return متن.lstrip(حروف)
def دائیں_تراشو(متن: str, حروف=None) -> str: return متن.rstrip(حروف)

def تقسیم(متن: str, جدا=None, زیادہ: int = -1) -> list:
    return متن.split(جدا) if زیادہ < 0 else متن.split(جدا, زیادہ)

def سطر_تقسیم(متن: str) -> list:
    return متن.splitlines()

def ملائیں(جوڑ: str, فہرست) -> str:
    return جوڑ.join(str(x) for x in فہرست)

def بدلیں(متن: str, پرانا: str, نیا: str, گنتی: int = -1) -> str:
    return متن.replace(پرانا, نیا) if گنتی < 0 else متن.replace(پرانا, نیا, گنتی)

def گنو(متن: str, ذیل: str) -> int:           return متن.count(ذیل)
def موجود_ہے(متن: str, ذیل: str) -> bool:      return ذیل in متن
def شروع_سے(متن: str, پیشوند: str) -> bool:   return متن.startswith(پیشوند)
def آخر_سے(متن: str, لاحقہ: str) -> bool:      return متن.endswith(لاحقہ)
def خالی_ہے(متن: str) -> bool:                 return not متن.strip()
def صرف_اعداد(متن: str) -> bool:               return متن.isdigit()
def صرف_حروف(متن: str) -> bool:                return متن.isalpha()
def لمبائی(متن: str) -> int:                   return len(متن)

def پیڈ_بائیں(متن: str, چوڑائی: int, حرف: str = " ") -> str:  return متن.ljust(چوڑائی, حرف)
def پیڈ_دائیں(متن: str, چوڑائی: int, حرف: str = " ") -> str:  return متن.rjust(چوڑائی, حرف)
def پیڈ_وسط(متن: str, چوڑائی: int, حرف: str = " ") -> str:    return متن.center(چوڑائی, حرف)
def صفر_بھریں(متن: str, چوڑائی: int) -> str:                   return متن.zfill(چوڑائی)

def ذیل_متن(متن: str, آغاز: int, آخر: int = None) -> str:
    return متن[آغاز:آخر]

def تلاش_کریں(متن: str, ذیل: str, آغاز: int = 0) -> int:
    """اشاریہ یا -1"""
    return متن.find(ذیل, آغاز)

def فارمیٹ(سانچہ: str, *دلائل, **نامی) -> str:
    return سانچہ.format(*دلائل, **نامی)

def ریجیکس_تلاش(نمونہ: str, متن: str):
    return _re.search(نمونہ, متن)

def ریجیکس_بدلیں(نمونہ: str, نیا: str, متن: str) -> str:
    return _re.sub(نمونہ, نیا, متن)

def ریجیکس_تمام(نمونہ: str, متن: str) -> list:
    return _re.findall(نمونہ, متن)

def دہرائیں(متن: str, تعداد: int) -> str:
    return متن * تعداد

def ترتیب_دیں(فہرست, *, الٹا: bool = False) -> list:
    """فہرست کو حروف تہجی کے مطابق ترتیب دیں"""
    return sorted(فہرست, reverse=الٹا)


# ─── Urdu-specific ────────────────────────────────────────────────────────────

def اعراب_ہٹائیں(متن: str) -> str:
    """اعراب / diacritical marks ہٹائیں"""
    return _DIACRITICS.sub("", متن)


def نستعلیق_معیاری(متن: str) -> str:
    """Normalise Urdu text: Arabic → Urdu equivalents, remove diacritics"""
    return _ud.normalize("NFC", اعراب_ہٹائیں(متن).translate(_NASTALIQ))


def الفاظ(متن: str) -> list:
    """Urdu word tokenisation — اردو الفاظ میں تقسیم
    Arabic/Urdu Unicode blocks only; ignores punctuation and Latin."""
    return _re.findall(
        r'[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]+',
        متن
    )


def اردو_حروف_ہیں(متن: str) -> bool:
    """کیا متن میں اردو/عربی حروف ہیں؟"""
    return bool(_re.search(r'[؀-ۿ]', متن))


def ہندی_اعداد(متن: str) -> str:
    """Eastern Arabic ۰–۹ → Western 0–9"""
    return متن.translate(_EAST_TO_WEST)


def ہندی_اعداد_میں(متن: str) -> str:
    """Western 0–9 → Eastern Arabic ۰–۹"""
    return متن.translate(_WEST_TO_EAST)


def اردو_میں_گنتی(ن: int) -> str:
    """Integer → Urdu words (منفی supported; up to کروڑs)"""
    if ن < 0:
        return "منفی " + اردو_میں_گنتی(-ن)
    return _عدد_لفظ(ن)


def _ترمیم_فاصلہ(الف: str, ب: str) -> int:
    m, n = len(الف), len(ب)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        پچھلا = dp[:]
        dp[0] = i
        for j in range(1, n + 1):
            dp[j] = پچھلا[j-1] if الف[i-1] == ب[j-1] else 1 + min(پچھلا[j], dp[j-1], پچھلا[j-1])
    return dp[n]


def مماثلت(الف: str, ب: str) -> float:
    """String similarity 0.0–1.0 (Levenshtein-based)"""
    بڑا = max(len(الف), len(ب))
    return 1.0 if بڑا == 0 else 1.0 - _ترمیم_فاصلہ(الف, ب) / بڑا


def ایک_جیسا_ہے(الف: str, ب: str, حساسیت: bool = True) -> bool:
    """دو متن برابر ہیں؟ حساسیت=False → case-insensitive"""
    return (الف == ب) if حساسیت else (الف.lower() == ب.lower())


def حروف_گنو(متن: str) -> dict:
    """ہر حرف کی تعداد — character frequency"""
    from collections import Counter
    return dict(Counter(متن))


def انکوڈ(متن: str, کوڈنگ: str = "utf-8") -> bytes:
    return متن.encode(کوڈنگ)


def ڈیکوڈ(بائٹس: bytes, کوڈنگ: str = "utf-8") -> str:
    return بائٹس.decode(کوڈنگ)


# ─── English aliases ──────────────────────────────────────────────────────────

upper            = بڑے_حروف
lower            = چھوٹے_حروف
title            = عنوانی
reverse          = الٹا_کریں
strip            = تراشو
lstrip           = بائیں_تراشو
rstrip           = دائیں_تراشو
split            = تقسیم
splitlines       = سطر_تقسیم
join             = ملائیں
replace          = بدلیں
count            = گنو
contains         = موجود_ہے
starts_with      = شروع_سے
ends_with        = آخر_سے
is_empty         = خالی_ہے
is_digits        = صرف_اعداد
is_alpha         = صرف_حروف
length           = لمبائی
pad_left         = پیڈ_بائیں
pad_right        = پیڈ_دائیں
pad_center       = پیڈ_وسط
zero_fill        = صفر_بھریں
substring        = ذیل_متن
find             = تلاش_کریں
format_str       = فارمیٹ
regex_search     = ریجیکس_تلاش
regex_sub        = ریجیکس_بدلیں
regex_all        = ریجیکس_تمام
repeat           = دہرائیں
sort_strings     = ترتیب_دیں
remove_diacritics = اعراب_ہٹائیں
normalize        = نستعلیق_معیاری
tokenize         = الفاظ
is_urdu          = اردو_حروف_ہیں
to_western       = ہندی_اعداد
to_eastern       = ہندی_اعداد_میں
number_words     = اردو_میں_گنتی
similarity       = مماثلت
equals           = ایک_جیسا_ہے
char_freq        = حروف_گنو
encode           = انکوڈ
decode           = ڈیکوڈ

__all__ = [
    # Urdu names
    "بڑے_حروف", "چھوٹے_حروف", "عنوانی", "الٹا_کریں",
    "تراشو", "بائیں_تراشو", "دائیں_تراشو",
    "تقسیم", "سطر_تقسیم", "ملائیں", "بدلیں",
    "گنو", "موجود_ہے", "شروع_سے", "آخر_سے",
    "خالی_ہے", "صرف_اعداد", "صرف_حروف", "لمبائی",
    "پیڈ_بائیں", "پیڈ_دائیں", "پیڈ_وسط", "صفر_بھریں",
    "ذیل_متن", "تلاش_کریں", "فارمیٹ",
    "ریجیکس_تلاش", "ریجیکس_بدلیں", "ریجیکس_تمام",
    "دہرائیں", "ترتیب_دیں",
    "اعراب_ہٹائیں", "نستعلیق_معیاری", "الفاظ",
    "اردو_حروف_ہیں", "ہندی_اعداد", "ہندی_اعداد_میں",
    "اردو_میں_گنتی", "مماثلت", "ایک_جیسا_ہے",
    "حروف_گنو", "انکوڈ", "ڈیکوڈ",
    # English aliases
    "upper", "lower", "title", "reverse",
    "strip", "lstrip", "rstrip", "split", "splitlines",
    "join", "replace", "count", "contains",
    "starts_with", "ends_with", "is_empty",
    "is_digits", "is_alpha", "length",
    "pad_left", "pad_right", "pad_center", "zero_fill",
    "substring", "find", "format_str",
    "regex_search", "regex_sub", "regex_all",
    "repeat", "sort_strings",
    "remove_diacritics", "normalize", "tokenize",
    "is_urdu", "to_western", "to_eastern",
    "number_words", "similarity", "equals",
    "char_freq", "encode", "decode",
]
