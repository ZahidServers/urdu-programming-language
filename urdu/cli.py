"""
Command-line interface for the Urdu Programming Language.

Usage:
    urdu run  hello_world.urdu
    urdu compile hello_world.urdu
    urdu repl
    urdu version
    urdu --help
"""

from __future__ import annotations
import sys
import os
import argparse
from pathlib import Path

from . import VERSION, DEVELOPER, version_info
from .compiler import UrduCompiler, UrduCompilerError


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="urdu",
        description="اردو پروگرامنگ لینگویج — Urdu Programming Language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
مثالیں / Examples:
  urdu run hello.urdu              -- فائل چلائیں
  urdu run hello.urdu -- arg1      -- دلائل کے ساتھ
  urdu compile hello.urdu          -- Python میں کمپائل کریں
  urdu repl                        -- انٹرایکٹو موڈ
  urdu version                     -- نسخہ دیکھیں
  urdu نصب flask                   -- پیکج نصب کریں
  urdu ہٹائیں flask                -- پیکج ہٹائیں
  urdu فہرست                       -- نصب شدہ پیکجز
  urdu فہرست django                -- نام سے تلاش
  urdu تازہ_کریں flask             -- پیکج اپ گریڈ
  urdu ماحول بنائیں myenv          -- ورچوئل ماحول بنائیں
  urdu ماحول چالو myenv            -- ماحول چالو کریں
  urdu بورڈ چلائیں                 -- TensorBoard چلائیں (logs/ فولڈر)
  urdu بورڈ چلائیں runs/ --پورٹ 8008 -- مخصوص فولڈر اور پورٹ

Developer: {DEVELOPER}
Version  : {VERSION}
"""
    )
    sub = p.add_subparsers(dest="command")

    # run
    run = sub.add_parser("run", help="اردو فائل چلائیں")
    run.add_argument("file", help=".urdu فائل کا راستہ، یا '-' stdin کے لیے")
    run.add_argument("args", nargs="*", help="پروگرام کو بھیجے جانے والے دلائل")
    run.add_argument("--debug", action="store_true", help="ٹوکن دکھائیں")
    run.add_argument("--show-python", action="store_true", help="Generated Python دکھائیں")

    # compile
    comp = sub.add_parser("compile", help="Python کوڈ میں تبدیل کریں")
    comp.add_argument("file", help=".urdu فائل")
    comp.add_argument("-o", "--output", help="آؤٹ پٹ فائل")
    comp.add_argument("--show-python", action="store_true")

    # repl
    sub.add_parser("repl", help="انٹرایکٹو REPL شروع کریں")

    # نصب (install)
    inst = sub.add_parser("نصب", help="پیکج نصب کریں | install packages")
    inst.add_argument("packages", nargs="+", metavar="پیکج", help="پیکج نام")

    # ہٹائیں (remove/uninstall)
    rem = sub.add_parser("ہٹائیں", help="پیکج ہٹائیں | uninstall packages")
    rem.add_argument("packages", nargs="+", metavar="پیکج", help="پیکج نام")

    # فہرست (list)
    lst = sub.add_parser("فہرست", help="نصب شدہ پیکجز دکھائیں | list packages")
    lst.add_argument("فلٹر", nargs="?", default="", help="نام میں تلاش")

    # تازہ_کریں (update)
    upd = sub.add_parser("تازہ_کریں", help="پیکج تازہ کریں | upgrade packages")
    upd.add_argument("packages", nargs="+", metavar="پیکج", help="پیکج نام")

    # ماحول (venv)
    env = sub.add_parser("ماحول", help="ورچوئل ماحول | virtual environment")
    env_sub = env.add_subparsers(dest="env_cmd")
    env_create = env_sub.add_parser("بنائیں", help="نیا ماحول بنائیں")
    env_create.add_argument("نام", nargs="?", default="ماحول", help="ماحول کا نام/راستہ")
    env_act = env_sub.add_parser("چالو", help="ماحول چالو کرنے کا طریقہ دکھائیں")
    env_act.add_argument("نام", nargs="?", default="ماحول", help="ماحول کا نام/راستہ")

    # version
    sub.add_parser("version", help="نسخہ اور ڈویلپر معلومات")

    # check
    chk = sub.add_parser("check", help="نحو جانچیں بغیر چلائے")
    chk.add_argument("file")

    # format (stub)
    fmt = sub.add_parser("format", help="کوڈ فارمیٹ کریں (جلد آ رہا ہے)")
    fmt.add_argument("file")

    # بورڈ (TensorBoard launcher)
    brd = sub.add_parser("بورڈ", help="TensorBoard ڈیش بورڈ | launch TensorBoard")
    brd_sub = brd.add_subparsers(dest="brd_cmd")
    brd_run = brd_sub.add_parser("چلائیں", help="TensorBoard چلائیں")
    brd_run.add_argument("فولڈر", nargs="?", default="logs", help="logs فولڈر (ڈیفالٹ: logs)")
    brd_run.add_argument("--پورٹ", type=int, default=6006, help="پورٹ نمبر (ڈیفالٹ: 6006)")
    brd_run.add_argument("--پس_منظر", action="store_true", help="پس منظر میں چلائیں")

    # مدد (help)
    mdad = sub.add_parser("مدد", help="مدد — زبان کے موضوعات، فنکشن، لائبریری")
    mdad.add_argument("موضوع", nargs="?", default=None,
                      help="موضوع یا زمرہ (مثلاً: زبان، متغیر، فلاسک، نمپائی)")

    return p


def main(argv: list[str] | None = None) -> int:
    # Ensure UTF-8 on both stdout and stderr (critical on Windows)
    import sys, io
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            try:
                _stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass

    # Reinstall Python's default SIGINT handler — Nuitka compiled binaries
    # can suppress it, causing Ctrl+C to be ignored for web servers.
    import signal
    try:
        signal.signal(signal.SIGINT, signal.default_int_handler)
    except (OSError, ValueError):
        pass

    parser = _build_parser()
    args = parser.parse_args(argv)

    if not args.command or args.command == "version":
        print(version_info())
        return 0

    compiler = UrduCompiler(
        debug=getattr(args, "debug", False),
        show_python=getattr(args, "show_python", False),
    )

    if args.command == "run":
        # stdin mode: urdu run - OR piped input
        if args.file == "-" or (args.file == "" and not sys.stdin.isatty()):
            try:
                source = sys.stdin.read()
                return compiler.run_source(source, "<stdin>", argv=args.args)
            except UrduCompilerError as e:
                print(f"\n{e}", file=sys.stderr)
                return 1
        path = Path(args.file)
        if not path.exists():
            print(f"خطا: فائل نہیں ملی '{args.file}'", file=sys.stderr)
            return 1
        if path.suffix not in (".urdu", ".urduc"):
            print(f"خطا: فائل کا لاحقہ '.urdu' ہونا چاہیے", file=sys.stderr)
            return 1
        try:
            return compiler.run_file(path, argv=args.args)
        except UrduCompilerError as e:
            print(f"\n{e}", file=sys.stderr)
            return 1

    if args.command == "compile":
        path = Path(args.file)
        if not path.exists():
            print(f"خطا: فائل نہیں ملی '{args.file}'", file=sys.stderr)
            return 1
        try:
            py_src = compiler.compile_file(path)
            out = args.output or str(path.with_suffix(".py"))
            Path(out).write_text(py_src, encoding="utf-8")
            print(f"✓ کمپائل مکمل: {out}")
            return 0
        except UrduCompilerError as e:
            print(f"\n{e}", file=sys.stderr)
            return 1

    if args.command == "repl":
        compiler.repl()
        return 0

    if args.command == "نصب":
        from .installer import install_packages
        return install_packages(args.packages)

    if args.command == "ہٹائیں":
        from .installer import remove_packages
        return remove_packages(args.packages)

    if args.command == "فہرست":
        from .installer import list_packages
        return list_packages(getattr(args, "فلٹر", ""))

    if args.command == "تازہ_کریں":
        from .installer import update_packages
        return update_packages(args.packages)

    if args.command == "ماحول":
        from .installer import create_venv, activate_venv_info
        env_cmd = getattr(args, "env_cmd", None)
        نام = getattr(args, "نام", "ماحول")
        if env_cmd == "بنائیں":
            return create_venv(نام)
        elif env_cmd == "چالو":
            return activate_venv_info(نام)
        else:
            print("استعمال: urdu ماحول بنائیں [نام]  یا  urdu ماحول چالو [نام]")
        return 0

    if args.command == "بورڈ":
        from .runtime.tensorboard_lib import بورڈ_چلائیں
        brd_cmd = getattr(args, "brd_cmd", None)
        if brd_cmd == "چلائیں":
            فولڈر = getattr(args, "فولڈر", "logs")
            پورٹ = getattr(args, "پورٹ", 6006)
            پس_منظر = getattr(args, "پس_منظر", False)
            return بورڈ_چلائیں(فولڈر, پورٹ=پورٹ, پس_منظر=پس_منظر)
        else:
            print("استعمال: urdu بورڈ چلائیں [فولڈر] [--پورٹ PORT]")
        return 0

    if args.command == "check":
        path = Path(args.file)
        try:
            source = path.read_text(encoding="utf-8")
            compiler.compile_source(source, str(path))
            print(f"✓ نحو درست ہے: {args.file}")
            return 0
        except UrduCompilerError as e:
            print(f"✗ نحو غلطی: {e}", file=sys.stderr)
            return 1

    if args.command == "format":
        print("کوڈ فارمیٹر جلد آ رہا ہے...")
        return 0

    if args.command == "مدد":
        from .runtime.help_lib import مدد
        مدد(getattr(args, "موضوع", None))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
