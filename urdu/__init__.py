"""
╔══════════════════════════════════════════════════════╗
║         اردو پروگرامنگ لینگویج                        ║
║         Urdu Programming Language                      ║
╠══════════════════════════════════════════════════════╣
║  Developer : Mohammed Zahid Wadiwale                   ║
║  Version   : 1.0.0                                     ║
║  Platform  : Windows | Linux | macOS                   ║
║  License   : MIT                                       ║
╚══════════════════════════════════════════════════════╝
"""

VERSION = "1.0.0"
VERSION_TUPLE = (1, 0, 0)
DEVELOPER = "Mohammed Zahid Wadiwale"
LANGUAGE_NAME = "اردو پروگرامنگ لینگویج"
LANGUAGE_NAME_EN = "Urdu Programming Language"
RELEASE_DATE = "2026-05-16"


def version_info() -> str:
    line = "=" * 56
    info = [
        line,
        "  Urdu Programming Language",
        f"  (Urdu: اردو پروگرامنگ لینگویج)",
        line,
        f"  Version   : {VERSION}",
        f"  Developer : {DEVELOPER}",
        f"  Released  : {RELEASE_DATE}",
        "  Platform  : Windows | Linux | macOS",
        "  Features  : OOP | Async | GUI | ML | DB | Web | Threads",
        "  License   : MIT",
        line,
    ]
    return "\n".join(info)


__version__ = VERSION
__author__ = DEVELOPER
__all__ = ["VERSION", "DEVELOPER", "LANGUAGE_NAME", "version_info"]
