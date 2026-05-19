"""
File utilities for the Urdu Programming Language.
Provides Urdu-named wrappers for zipfile (stdlib) and openpyxl (Excel).

Usage:
    درآمد { زپ_فائل, ایکسل_کتاب, زپ_بناؤ, ایکسل_پڑھو } سے "اردو/فائلیں";
"""

from __future__ import annotations
import os
import zipfile as _zf
from typing import Optional, List, Union
from .builtins import _UrduObj


# ══════════════════════════════════════════════════════════════════════════════
#  ZIP
# ══════════════════════════════════════════════════════════════════════════════

class زپ_فائل:
    """
    zipfile wrapper.

    طریقہ: "r" پڑھنا  |  "w" لکھنا  |  "a" شامل کرنا
    """

    def __init__(self, راستہ: str, طریقہ: str = "r"):
        self._path = راستہ
        self._mode = طریقہ
        self._zf   = _zf.ZipFile(راستہ, طریقہ)

    # ── Listing ───────────────────────────────────────────────────────────────

    def فہرست(self) -> List[str]:
        """List all file names inside the archive."""
        return self._zf.namelist()

    def معلومات(self, نام: str) -> _UrduObj:
        """Get metadata for one entry (size, compress_size, filename)."""
        info = self._zf.getinfo(نام)
        return _UrduObj({
            "نام":            info.filename,
            "اصل_سائز":       info.file_size,
            "سکڑا_سائز":      info.compress_size,
            "تاریخ":          str(info.date_time),
        })

    # ── Reading ───────────────────────────────────────────────────────────────

    def پڑھو(self, نام: str) -> bytes:
        """Read a file from the archive as bytes."""
        return self._zf.read(نام)

    def متن_پڑھو(self, نام: str, انکوڈنگ: str = "utf-8") -> str:
        """Read a file from the archive as text."""
        return self._zf.read(نام).decode(انکوڈنگ)

    # ── Extraction ────────────────────────────────────────────────────────────

    def نکالو(self, نام: str, منزل: str = ".") -> str:
        """Extract one file. Returns the extracted path."""
        return self._zf.extract(نام, منزل)

    def سب_نکالو(self, منزل: str = ".") -> List[str]:
        """Extract all files. Returns list of extracted paths."""
        self._zf.extractall(منزل)
        return [os.path.join(منزل, n) for n in self._zf.namelist()]

    # ── Writing ───────────────────────────────────────────────────────────────

    def شامل(self, فائل_راستہ: str, زپ_نام: str = None):
        """Add an existing file to the archive."""
        self._zf.write(فائل_راستہ, arcname=زپ_نام or os.path.basename(فائل_راستہ))

    def متن_شامل(self, زپ_نام: str, مواد: str, انکوڈنگ: str = "utf-8"):
        """Add a string as a file inside the archive."""
        self._zf.writestr(زپ_نام, مواد.encode(انکوڈنگ))

    def بائٹس_شامل(self, زپ_نام: str, مواد: bytes):
        """Add raw bytes as a file inside the archive."""
        self._zf.writestr(زپ_نام, مواد)

    # ── Close ─────────────────────────────────────────────────────────────────

    def بند(self):
        """Close the archive."""
        self._zf.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.بند()

    def __repr__(self):
        return f"<زپ_فائل '{self._path}' [{len(self.فہرست())} فائلیں]>"


# ── Standalone ZIP helpers ────────────────────────────────────────────────────

def زپ_بناؤ(زپ_راستہ: str, فائلیں: list) -> str:
    """
    Create a zip archive from a list of file paths (or (path, arcname) tuples).
    Returns the zip path.
    """
    with _zf.ZipFile(زپ_راستہ, "w", _zf.ZIP_DEFLATED) as zf:
        for item in فائلیں:
            if isinstance(item, (list, tuple)):
                src, arcname = item[0], item[1]
            else:
                src, arcname = item, os.path.basename(item)
            zf.write(src, arcname=arcname)
    return زپ_راستہ


def زپ_نکالو(زپ_راستہ: str, منزل: str = ".") -> List[str]:
    """Extract all files from a zip archive. Returns extracted paths."""
    with _zf.ZipFile(زپ_راستہ, "r") as zf:
        zf.extractall(منزل)
        return [os.path.join(منزل, n) for n in zf.namelist()]


def زپ_فہرست(زپ_راستہ: str) -> List[str]:
    """List file names inside a zip without extracting."""
    with _zf.ZipFile(زپ_راستہ, "r") as zf:
        return zf.namelist()


# ══════════════════════════════════════════════════════════════════════════════
#  Excel (openpyxl)
# ══════════════════════════════════════════════════════════════════════════════

def _openpyxl():
    try:
        import openpyxl
        return openpyxl
    except ImportError:
        raise ImportError("openpyxl نصب کریں:  urdu نصب اردو/فائلیں")


class ایکسل_ورق:
    """Wraps an openpyxl Worksheet with Urdu API."""

    def __init__(self, ws):
        self._ws = ws

    @property
    def نام(self) -> str:
        return self._ws.title

    @property
    def صف_تعداد(self) -> int:
        return self._ws.max_row

    @property
    def کالم_تعداد(self) -> int:
        return self._ws.max_column

    def خانہ(self, صف: int, کالم: int):
        """Get cell value at (row, col) — 1-indexed."""
        return self._ws.cell(row=صف, column=کالم).value

    def خانہ_مقرر(self, صف: int, کالم: int, قدر):
        """Set cell value at (row, col) — 1-indexed."""
        self._ws.cell(row=صف, column=کالم).value = قدر

    def قطار_پڑھو(self, صف: int) -> List:
        """Return all values in a row as a list."""
        return [self._ws.cell(row=صف, column=c).value
                for c in range(1, self._ws.max_column + 1)]

    def کالم_پڑھو(self, کالم: int) -> List:
        """Return all values in a column as a list."""
        return [self._ws.cell(row=r, column=کالم).value
                for r in range(1, self._ws.max_row + 1)]

    def سب_ڈیٹا(self) -> List[List]:
        """Return all rows as list of lists (includes header)."""
        return [[cell.value for cell in row] for row in self._ws.iter_rows()]

    def قطار_شامل(self, قدریں: list):
        """Append a row of values."""
        self._ws.append(قدریں)

    def __repr__(self):
        return f"<ایکسل_ورق '{self.نام}' {self.صف_تعداد}x{self.کالم_تعداد}>"


class ایکسل_کتاب:
    """
    openpyxl Workbook wrapper.

    ایکسل_کتاب()           — نئی کتاب
    ایکسل_کتاب("file.xlsx") — موجودہ فائل کھولو
    """

    def __init__(self, راستہ: str = None):
        ox = _openpyxl()
        if راستہ:
            self._wb   = ox.load_workbook(راستہ)
            self._path = راستہ
        else:
            self._wb   = ox.Workbook()
            self._path = None

    # ── Sheets ────────────────────────────────────────────────────────────────

    def ورق_فہرست(self) -> List[str]:
        """List all sheet names."""
        return self._wb.sheetnames

    def ورق(self, نام: str = None) -> ایکسل_ورق:
        """Get sheet by name. If None, returns the active sheet."""
        ws = self._wb[نام] if نام else self._wb.active
        return ایکسل_ورق(ws)

    def ورق_بنائیں(self, نام: str) -> ایکسل_ورق:
        """Create and return a new sheet."""
        ws = self._wb.create_sheet(نام)
        return ایکسل_ورق(ws)

    def ورق_حذف(self, نام: str):
        """Delete a sheet by name."""
        del self._wb[نام]

    # ── Save / Close ──────────────────────────────────────────────────────────

    def محفوظ(self, راستہ: str = None) -> str:
        """Save workbook. Uses original path if none given."""
        dest = راستہ or self._path
        if not dest:
            raise ValueError("محفوظ کرنے کے لیے راستہ دیں")
        self._wb.save(dest)
        self._path = dest
        return dest

    def بند(self):
        """Close the workbook."""
        self._wb.close()

    def __repr__(self):
        sheets = ", ".join(self.ورق_فہرست())
        return f"<ایکسل_کتاب ورق=[{sheets}]>"


# ── Standalone Excel helpers ──────────────────────────────────────────────────

def ایکسل_پڑھو(راستہ: str, ورق_نام: str = None) -> List[List]:
    """
    Read an Excel file and return all rows as a list of lists.
    ورق_نام=None uses the active sheet.
    """
    ox = _openpyxl()
    wb = ox.load_workbook(راستہ, read_only=True, data_only=True)
    ws = wb[ورق_نام] if ورق_نام else wb.active
    data = [[cell.value for cell in row] for row in ws.iter_rows()]
    wb.close()
    return data


def ایکسل_لکھو(ڈیٹا: list, راستہ: str, ورق_نام: str = "Sheet1") -> str:
    """
    Write a list-of-lists (or list-of-dicts) to an Excel file.
    Returns the saved path.
    """
    ox = _openpyxl()
    wb = ox.Workbook()
    ws = wb.active
    ws.title = ورق_نام
    for قطار in ڈیٹا:
        if isinstance(قطار, dict):
            ws.append(list(قطار.values()))
        else:
            ws.append(list(قطار))
    wb.save(راستہ)
    wb.close()
    return راستہ


# ── Exports ───────────────────────────────────────────────────────────────────

__all__ = [
    # ZIP
    "زپ_فائل", "زپ_بناؤ", "زپ_نکالو", "زپ_فہرست",
    # Excel
    "ایکسل_کتاب", "ایکسل_ورق", "ایکسل_پڑھو", "ایکسل_لکھو",
    # English aliases
    "ZipFile", "ExcelBook", "ExcelSheet",
    "zip_create", "zip_extract", "zip_list",
    "excel_read", "excel_write",
]

# English aliases
ZipFile    = زپ_فائل
ExcelBook  = ایکسل_کتاب
ExcelSheet = ایکسل_ورق
zip_create  = زپ_بناؤ
zip_extract = زپ_نکالو
zip_list    = زپ_فہرست
excel_read  = ایکسل_پڑھو
excel_write = ایکسل_لکھو
