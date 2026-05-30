"""Main compiler/runner for the Urdu Programming Language.

Urdu source → Lex → Parse → Transpile → Python bytecode → Execute
"""

from __future__ import annotations
import os
import sys
import ast
import py_compile
import importlib.util
import tempfile
import textwrap
from pathlib import Path

from .lexer import Lexer, LexerError
from .parser import Parser, ParseError
from .transpiler import Transpiler, TranspilerError
from . import VERSION, DEVELOPER


class UrduCompilerError(Exception):
    pass


class UrduCompiler:
    """Compile and/or run Urdu source files."""

    EXTENSION = ".urdu"
    COMPILED_EXTENSION = ".urduc"   # compiled bytecode cache

    def __init__(self, *, debug: bool = False, show_python: bool = False):
        self.debug = debug
        self.show_python = show_python

    # ── public API ────────────────────────────────────────────────────────────

    def compile_source(self, source: str, filename: str = "<stdin>") -> str:
        """Urdu source → Python source string."""
        try:
            tokens = Lexer(source).tokenize()
            if self.debug:
                for tok in tokens:
                    print(f"  {tok}", file=sys.stderr)
        except LexerError as e:
            raise UrduCompilerError(str(e)) from e

        try:
            ast_tree = Parser(tokens).parse()
        except ParseError as e:
            raise UrduCompilerError(str(e)) from e

        try:
            py_src = Transpiler().transpile(ast_tree)
        except TranspilerError as e:
            raise UrduCompilerError(str(e)) from e

        if self.show_python:
            print("─" * 60, file=sys.stderr)
            print("Generated Python:", file=sys.stderr)
            print("─" * 60, file=sys.stderr)
            for i, line in enumerate(py_src.splitlines(), 1):
                print(f"{i:4}  {line}", file=sys.stderr)
            print("─" * 60, file=sys.stderr)

        return py_src

    def compile_file(self, path: str | Path) -> str:
        """Compile a .urdu file, return Python source. Cache .urduc alongside it."""
        path = Path(path)
        source = path.read_text(encoding="utf-8")
        py_src = self.compile_source(source, filename=str(path))

        # Write Python cache
        cache_path = path.with_suffix(self.COMPILED_EXTENSION)
        cache_path.write_text(py_src, encoding="utf-8")
        return py_src

    def run_source(self, source: str, filename: str = "<stdin>",
                   argv: list[str] | None = None) -> int:
        """Compile and execute Urdu source. Returns exit code."""
        py_src = self.compile_source(source, filename)
        return self._exec_python(py_src, filename, argv or [], urdu_src=source)

    def run_file(self, path: str | Path, argv: list[str] | None = None) -> int:
        """Compile and run a .urdu file. Returns exit code."""
        path = Path(path)
        if not path.exists():
            raise UrduCompilerError(f"فائل نہیں ملی (File not found): {path}")
        urdu_src = path.read_text(encoding="utf-8")
        py_src = self.compile_source(urdu_src, str(path))
        # Write Python cache alongside source
        path.with_suffix(self.COMPILED_EXTENSION).write_text(py_src, encoding="utf-8")
        return self._exec_python(py_src, str(path), argv or [], urdu_src=urdu_src)

    # ── internal execution ────────────────────────────────────────────────────

    def _exec_python(self, py_src: str, filename: str, argv: list[str],
                     urdu_src: str = "") -> int:
        # Validate Python syntax before exec
        try:
            code_obj = compile(py_src, filename, "exec")
        except SyntaxError as e:
            raise UrduCompilerError(
                f"Python syntax error in generated code: {e}\n"
                f"Line {e.lineno}: {e.text}"
            ) from e

        # Set up argv
        old_argv = sys.argv
        sys.argv = [filename] + argv

        # Add project dir to path
        project_dir = str(Path(filename).parent.resolve()) if filename != "<stdin>" else os.getcwd()
        if project_dir not in sys.path:
            sys.path.insert(0, project_dir)

        # Add package root to path (so 'urdu' package is importable)
        pkg_root = str(Path(__file__).parent.parent.resolve())
        if pkg_root not in sys.path:
            sys.path.insert(0, pkg_root)

        ns = {
            "__name__": "__main__",
            "__file__": filename,
        }

        exit_code = 0
        try:
            exec(code_obj, ns)
        except SystemExit as e:
            exit_code = e.code or 0
        except KeyboardInterrupt:
            print("\n^C — بند کیا گیا", file=sys.stderr)
            import os as _os; _os._exit(0)
        except Exception as e:
            import traceback, re as _re
            tb_str = traceback.format_exc()

            # Map Python line number back to Urdu source line via # urdu:N markers
            py_lines = py_src.splitlines()
            py_line = None
            for _m in _re.finditer(r", line (\d+)", tb_str):
                py_line = int(_m.group(1))   # keep last (deepest) frame

            urdu_line = None
            if py_line:
                for i in range(min(py_line - 1, len(py_lines) - 1), -1, -1):
                    _m = _re.match(r"\s*# urdu:(\d+)$", py_lines[i])
                    if _m:
                        urdu_line = int(_m.group(1))
                        break

            from .error_messages import translate_error, suggest_name, suggest_attr
            urdu_type, urdu_msg = translate_error(e)

            # Build did-you-mean hint for NameError / AttributeError
            hint = None
            if isinstance(e, NameError):
                bad = getattr(e, "name", None)
                if bad is None:
                    _nm = _re.search(r"name '([^']+)' is not defined", str(e))
                    bad = _nm.group(1) if _nm else None
                if bad:
                    hint = suggest_name(bad, ns, ns)
            elif isinstance(e, AttributeError):
                bad = getattr(e, "name", None)
                obj = getattr(e, "obj", None)
                if bad and obj is not None:
                    hint = suggest_attr(bad, obj)

            print(f"\nاردو غلطی (Runtime Error):", file=sys.stderr)
            if urdu_line and urdu_src:
                src_lines = urdu_src.splitlines()
                if 0 < urdu_line <= len(src_lines):
                    print(f"  ↳ سطر {urdu_line}: {src_lines[urdu_line - 1].strip()}",
                          file=sys.stderr)
            if urdu_type or urdu_msg:
                display_type = urdu_type or type(e).__name__
                display_msg  = urdu_msg  or str(e)
                print(f"  {display_type}: {display_msg}", file=sys.stderr)
            else:
                print(f"  {type(e).__name__}: {e}", file=sys.stderr)
            if hint:
                print(f"  💡 {hint}", file=sys.stderr)
            if self.debug:
                print("\n--- Python Traceback (--debug) ---", file=sys.stderr)
                traceback.print_exc()
            exit_code = 1
        finally:
            sys.argv = old_argv

        return exit_code

    # ── REPL ──────────────────────────────────────────────────────────────────

    def repl(self):
        """Start an interactive REPL for the Urdu language."""
        # Enable readline for arrow-key navigation and history (Urdu-safe)
        try:
            import readline as _rl
            _rl.parse_and_bind("tab: complete")
            _rl.set_completer_delims(" \t\n;")
        except ImportError:
            try:
                import pyreadline3 as _rl  # type: ignore
                _rl.parse_and_bind("tab: complete")
            except ImportError:
                pass  # gracefully continue without readline

        from . import version_info
        print(version_info())
        print("اردو REPL — Ctrl+C یا 'خروج()' سے باہر نکلیں\n")

        # Add pkg root
        pkg_root = str(Path(__file__).parent.parent.resolve())
        if pkg_root not in sys.path:
            sys.path.insert(0, pkg_root)

        ns = {"__name__": "__repl__"}
        # Import builtins into REPL namespace
        exec("from urdu.runtime.builtins import *", ns)

        def _incomplete(src: str) -> bool:
            """True when source is an open multi-line block (more { than })."""
            return src.count("{") > src.count("}")

        buf = []
        while True:
            try:
                prompt = ">>> " if not buf else "... "
                try:
                    line = input(prompt)
                except EOFError:
                    break

                if line.strip() in ("خروج()", "exit()", "quit()"):
                    break

                buf.append(line)
                src = "\n".join(buf)

                try:
                    py_src = self.compile_source(src, "<repl>")
                    try:
                        code_obj = compile(py_src, "<repl>", "exec")
                    except SyntaxError as e:
                        # Generated Python has a syntax error.  If the Urdu
                        # source still has unclosed braces, keep buffering.
                        # Otherwise it is a real error — show it and reset.
                        if _incomplete(src):
                            continue
                        print(f"نحوی غلطی: {e}", file=sys.stderr)
                        buf = []
                        continue

                    try:
                        exec(code_obj, ns)
                    except Exception as e:
                        import traceback
                        traceback.print_exc()

                    buf = []
                except UrduCompilerError as e:
                    # If source has unclosed braces the user is still typing a
                    # multi-line block — keep buffering and show the "..." prompt.
                    # Otherwise it is a genuine syntax error; show it and reset.
                    if _incomplete(src):
                        pass
                    else:
                        print(f"\n{e}", file=sys.stderr)
                        buf = []

            except KeyboardInterrupt:
                print("\nCtrl+C — خروج")
                buf = []
