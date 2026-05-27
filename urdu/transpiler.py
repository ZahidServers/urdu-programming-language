"""AST → Python source transpiler for the Urdu Programming Language."""

from __future__ import annotations
import re
from .ast_nodes import *
from . import VERSION, DEVELOPER

# Urdu module path → Python runtime path
_MODULE_MAP = {
    "اردو/گوئی":        "urdu.runtime.gui",
    "اردو/ڈیٹا_بیس":    "urdu.runtime.database",
    "اردو/ذہین":         "urdu.runtime.ml",
    "اردو/ویب":          "urdu.runtime.web",
    "اردو/لاگ":          "urdu.runtime.logging_lib",
    "اردو/دھاگہ":        "urdu.runtime.threading_lib",
    "اردو/رمز":          "urdu.runtime.crypto",
    "اردو/تاریخ":        "urdu.runtime.datetime_lib",
    "اردو/کرل":          "urdu.runtime.curl",
    "اردو/کھرچنی":       "urdu.runtime.scraper",
    "اردو/فائلیں":       "urdu.runtime.files",
    "اردو/پایتھن":       None,   # passthrough to Python stdlib
}

_ASSIGN_OP_MAP = {
    "+=": "+=", "-=": "-=", "*=": "*=", "/=": "/=",
    "%=": "%=", "**=": "**=",
    "&&=": " = _ and ", "||=": " = _ or ",
    "??=": None,   # handled specially
    "&=": "&=", "|=": "|=",
}


class TranspilerError(Exception):
    def __init__(self, msg: str, line: int = 0):
        super().__init__(f"ٹرانسپائلر غلطی [{line}]: {msg}")
        self.line = line


class Transpiler:
    def __init__(self):
        self._lines: list[str] = []
        self._indent = 0
        self._in_class: list[str] = []   # stack of class names
        self._in_async = False
        self._lambda_counter = 0
        self._deferred: list[str] = []   # module-level deferred (imports, etc.)
        self._pending_defs: list[str] = []  # inline closures to flush before next statement
        self._has_async = False
        self._exports: list[str] = []
        # Stack tracking whether each nested function scope is async (True) or sync (False).
        # Empty means module-level (will be wrapped in async _اردو_main if _has_async is set).
        self._async_scope: list[bool] = []

    # ── output helpers ────────────────────────────────────────────────────────

    def _w(self, line: str = ""):
        # flush any inline closure defs accumulated during expression evaluation
        if self._pending_defs:
            for pd in self._pending_defs:
                self._lines.append(pd)
            self._pending_defs.clear()
        self._lines.append("    " * self._indent + line)

    def _blank(self):
        if self._lines and self._lines[-1].strip():
            self._lines.append("")

    def _ind(self): self._indent += 1
    def _ded(self): self._indent -= 1

    # ── entry ─────────────────────────────────────────────────────────────────

    def transpile(self, node: Program) -> str:
        header = [
            f"# ═══════════════════════════════════════",
            f"# اردو پروگرامنگ لینگویج — Generated Code",
            f"# Developer: {DEVELOPER}",
            f"# Version  : {VERSION}",
            f"# ═══════════════════════════════════════",
            "from __future__ import annotations",
            "import asyncio, sys, os",
            "from urdu.runtime.builtins import *",
            "",
        ]
        for stmt in node.body:
            self._stmt(stmt)

        if self._has_async:
            main_lines = list(self._lines)
            self._lines = header + self._deferred + ["", "async def _اردو_main():"] + \
                          ["    " + l for l in main_lines] + \
                          ["", "asyncio.run(_اردو_main())"]
        else:
            self._lines = header + self._deferred + self._lines

        if self._exports:
            self._lines += ["", f"__all__ = {self._exports!r}"]

        return "\n".join(self._lines)

    # ── statements ────────────────────────────────────────────────────────────

    def _stmt(self, node: ASTNode):
        line = getattr(node, "line", 0)
        if line:
            self._w(f"# urdu:{line}")
        method = getattr(self, f"_s_{type(node).__name__}", None)
        if method:
            method(node)
        else:
            self._w(self._expr(node))

    def _s_EmptyStatement(self, _): pass

    def _s_ExpressionStatement(self, node: ExpressionStatement):
        expr = node.expression
        # i++ / i-- as a statement → i += 1 / i -= 1
        if isinstance(expr, UpdateExpr):
            tgt = self._expr(expr.operand)
            op = "+= 1" if expr.op == "++" else "-= 1"
            self._w(f"{tgt} {op}")
            return
        # assignment as statement
        if isinstance(expr, AssignExpr):
            self._w(self._expr(expr))
            return
        # Auto-await coroutines only when inside an async scope.
        # _async_scope is empty at module level (which becomes _اردو_main, itself async).
        _in_async_ctx = self._has_async and (
            not self._async_scope or self._async_scope[-1]
        )
        if isinstance(expr, CallExpr) and _in_async_ctx:
            py = self._expr(expr)
            self._w(f"_r = {py}")
            self._w("if asyncio.iscoroutine(_r): await _r")
            return
        self._w(self._expr(expr))

    def _s_VarDeclaration(self, node: VarDeclaration):
        for decl in node.declarations:
            lhs = self._pattern(decl.id)
            if decl.init is None:
                self._w(f"{lhs} = None")
            else:
                self._w(f"{lhs} = {self._expr(decl.init)}")

    def _s_FunctionDecl(self, node: FunctionDecl):
        self._blank()
        for dec in getattr(node, "decorators", []):
            self._w(f"@{self._expr(dec.expression)}")
        prefix = "async " if node.is_async else ""
        if node.is_async:
            self._has_async = True
        params = self._params(node.params, in_class=bool(self._in_class))
        # Python generators use yield internally; no * in function name
        self._w(f"{prefix}def {node.name}({params}):")
        self._ind()
        self._async_scope.append(node.is_async)
        if not node.body.body:
            self._w("pass")
        else:
            for s in node.body.body:
                self._stmt(s)
        self._async_scope.pop()
        self._ded()
        self._blank()

    def _s_ClassDecl(self, node: ClassDecl):
        self._blank()
        base = f"({self._expr(node.superclass)})" if node.superclass else ""
        self._w(f"class {node.name}{base}:")
        self._ind()
        self._in_class.append(node.name)

        # Collect instance fields for injection into __init__
        instance_fields = [(m.key, m.value) for m in node.body
                           if m.kind == "field" and not m.is_static]

        has_constructor = any(m.kind == "constructor" for m in node.body)

        # If no constructor but we have instance fields, emit a default __init__
        if not has_constructor and instance_fields:
            self._blank()
            self._w("def __init__(self):")
            self._ind()
            for key, val in instance_fields:
                v = self._expr(val) if val is not None else "None"
                self._w(f"self.{key} = {v}")
            self._ded()

        for member in node.body:
            # Always inject instance_fields into the constructor
            if member.kind == "constructor":
                self._class_member(member, instance_fields)
            else:
                self._class_member(member, [])

        if not node.body:
            self._w("pass")

        self._in_class.pop()
        self._ded()
        self._blank()

    def _class_member(self, m: ClassMember, auto_fields: list):
        if m.kind == "constructor":
            fn: FunctionDecl = m.value
            self._blank()
            # _params with in_class=True already prepends 'self'
            params = self._params(fn.params, in_class=True)
            self._w(f"def __init__({params}):")
            self._ind()
            self._async_scope.append(False)
            for key, val in auto_fields:
                v = self._expr(val) if val is not None else "None"
                self._w(f"self.{key} = {v}")
            if not fn.body.body and not auto_fields:
                self._w("pass")
            for s in fn.body.body:
                self._stmt(s)
            self._async_scope.pop()
            self._ded()
            return

        if m.kind == "field":
            if m.is_static:
                v = self._expr(m.value) if m.value is not None else "None"
                self._w(f"{m.key} = {v}")
            return

        if m.kind in ("method", "get", "set"):
            fn: FunctionDecl = m.value
            self._blank()
            if m.kind == "get":
                self._w("@property")
            elif m.kind == "set":
                self._w(f"@{m.key}.setter")
            if m.is_static:
                self._w("@staticmethod")
            prefix = "async " if m.is_async else ""
            if m.is_async:
                self._has_async = True
            # static methods don't have self; instance methods do
            params = self._params(fn.params, in_class=not m.is_static)
            self._w(f"{prefix}def {m.key}({params}):")
            self._ind()
            self._async_scope.append(m.is_async)
            if not fn.body.body:
                self._w("pass")
            else:
                for s in fn.body.body:
                    self._stmt(s)
            self._async_scope.pop()
            self._ded()

    def _s_IfStatement(self, node: IfStatement):
        self._w(f"if {self._expr(node.condition)}:")
        self._ind()
        self._block_body(node.consequent)
        self._ded()
        if node.alternate:
            if isinstance(node.alternate, IfStatement):
                # Write elif chain
                self._lines.append("    " * self._indent + "elif " + self._expr(node.alternate.condition) + ":")
                self._ind()
                self._block_body(node.alternate.consequent)
                self._ded()
                if node.alternate.alternate:
                    self._emit_elif_chain(node.alternate.alternate)
            elif isinstance(node.alternate, Block):
                self._w("else:")
                self._ind()
                self._block_body(node.alternate)
                self._ded()

    def _emit_elif_chain(self, node):
        if isinstance(node, IfStatement):
            self._w(f"elif {self._expr(node.condition)}:")
            self._ind()
            self._block_body(node.consequent)
            self._ded()
            if node.alternate:
                self._emit_elif_chain(node.alternate)
        elif isinstance(node, Block):
            self._w("else:")
            self._ind()
            self._block_body(node)
            self._ded()

    def _s_WhileStatement(self, node: WhileStatement):
        self._w(f"while {self._expr(node.condition)}:")
        self._ind()
        self._block_body(node.body)
        self._ded()

    def _s_DoWhileStatement(self, node: DoWhileStatement):
        self._w("while True:")
        self._ind()
        self._block_body(node.body)
        self._w(f"if not ({self._expr(node.condition)}): break")
        self._ded()

    def _s_ForStatement(self, node: ForStatement):
        if node.init:
            if isinstance(node.init, VarDeclaration):
                for d in node.init.declarations:
                    v = self._expr(d.init) if d.init else "None"
                    self._w(f"{self._pattern(d.id)} = {v}")
            else:
                self._w(self._expr(node.init.expression))

        cond = self._expr(node.condition) if node.condition else "True"

        self._w(f"while {cond}:")
        self._ind()
        self._block_body(node.body)
        # update expression as a statement
        if node.update:
            self._stmt(ExpressionStatement(expression=node.update, line=node.line))
        self._ded()

    def _s_ForInStatement(self, node: ForInStatement):
        if isinstance(node.left, VarDeclaration):
            lhs = self._pattern(node.left.declarations[0].id)
        else:
            lhs = self._expr(node.left)
        rhs = self._expr(node.right)
        # Both for...in and for...of map to Python's for...in
        # (Python iterates values for lists/tuples, keys for dicts)
        self._w(f"for {lhs} in {rhs}:")
        self._ind()
        self._block_body(node.body)
        self._ded()

    def _s_SwitchStatement(self, node: SwitchStatement):
        disc = self._expr(node.discriminant)
        tmp = f"_sw_{id(node) & 0xFFFF}"
        self._w(f"{tmp} = {disc}")
        first = True
        has_break_equivalent = False
        for case in node.cases:
            kw = "if" if first else "elif"
            first = False
            if case.test is None:
                self._w("else:")
            else:
                self._w(f"{kw} {tmp} == {self._expr(case.test)}:")
            self._ind()
            if not case.consequent:
                self._w("pass")
            for s in case.consequent:
                if isinstance(s, BreakStatement):
                    pass  # break in switch → nothing (we use if/elif)
                else:
                    self._stmt(s)
            self._ded()

    def _s_ReturnStatement(self, node: ReturnStatement):
        if node.argument is None:
            self._w("return")
        else:
            self._w(f"return {self._expr(node.argument)}")

    def _s_BreakStatement(self, _): self._w("break")
    def _s_ContinueStatement(self, _): self._w("continue")

    def _s_ThrowStatement(self, node: ThrowStatement):
        self._w(f"raise {self._expr(node.argument)}")

    def _s_TryStatement(self, node: TryStatement):
        self._w("try:")
        self._ind()
        self._block_body(node.block)
        self._ded()
        if node.handler:
            h = node.handler
            if h.param:
                _eparam = self._expr(h.param)
                self._w(f"except Exception as {_eparam}:")
                self._ind()
                # Ensure .پیغام always works on any caught Python exception
                self._w(f"if not hasattr({_eparam}, 'پیغام'): {_eparam}.پیغام = str({_eparam})")
            else:
                self._w("except Exception:")
                self._ind()
            self._block_body(h.body)
            self._ded()
        if node.finalizer:
            self._w("finally:")
            self._ind()
            self._block_body(node.finalizer)
            self._ded()

    def _s_ImportDeclaration(self, node: ImportDeclaration):
        src = node.source
        # Strip file-relative prefix (./ or .\) — the project directory is
        # already on sys.path, so the bare module name resolves correctly.
        # Leaving the leading dot produces a relative Python import which
        # fails because user scripts run as __main__ (not a package).
        _src_clean = src
        if _src_clean.startswith(("./", ".\\")):
            _src_clean = _src_clean[2:]
        elif _src_clean.startswith(("../", "..\\")):
            _src_clean = _src_clean[3:]
        py_mod = _MODULE_MAP.get(src, _src_clean.replace("/", ".").replace("\\", ".").replace("-", "_"))

        if not node.specifiers:
            self._w(f"import {py_mod}")
            return

        for spec in node.specifiers:
            if spec.kind == "namespace":
                self._w(f"import {py_mod} as {spec.local}")
            elif spec.kind == "default":
                if py_mod is None:
                    self._w(f"import {src} as {spec.local}")
                else:
                    self._w(f"from {py_mod} import *")
                    self._w(f"import {py_mod} as {spec.local}")
            else:
                if py_mod is None:
                    self._w(f"from {src} import {spec.imported} as {spec.local}")
                else:
                    alias = f" as {spec.local}" if spec.local != spec.imported else ""
                    self._w(f"from {py_mod} import {spec.imported}{alias}")

    def _s_ExportDeclaration(self, node: ExportDeclaration):
        if node.declaration:
            self._stmt(node.declaration)
            if isinstance(node.declaration, (FunctionDecl, ClassDecl)):
                self._exports.append(node.declaration.name)
            elif isinstance(node.declaration, VarDeclaration):
                for d in node.declaration.declarations:
                    self._exports.append(self._pattern(d.id))
        for spec in node.specifiers:
            self._exports.append(spec.local)

    def _s_Block(self, node: Block):
        self._block_body(node)

    def _block_body(self, node: Block):
        if not node.body:
            self._w("pass")
        else:
            for s in node.body:
                self._stmt(s)

    # ── expressions ───────────────────────────────────────────────────────────

    def _expr(self, node: ASTNode) -> str:
        method = getattr(self, f"_e_{type(node).__name__}", None)
        if method:
            return method(node)
        raise TranspilerError(f"Unknown expression node: {type(node).__name__}", getattr(node, "line", 0))

    def _e_NumberLiteral(self, n): return repr(n.value)
    def _e_StringLiteral(self, n): return repr(n.value)
    def _e_BooleanLiteral(self, n): return "True" if n.value else "False"
    def _e_NullLiteral(self, _): return "None"
    def _e_UndefinedLiteral(self, _): return "None"
    def _e_ThisExpression(self, _): return "self"
    def _e_SuperExpression(self, _): return "super()"
    def _e_Identifier(self, n): return n.name

    def _e_TemplateLiteral(self, n: TemplateLiteral) -> str:
        parts = []
        for kind, content in n.parts:
            if kind == "text":
                escaped = (content
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                    .replace("\r", "\\r")
                    .replace("\t", "\\t")
                    .replace("{", "{{")
                    .replace("}", "}}"))
                parts.append(escaped)
            else:
                parts.append("{" + self._expr(content) + "}")
        return 'f"' + "".join(parts) + '"'

    def _e_ArrayLiteral(self, n: ArrayLiteral) -> str:
        elems = []
        for e in n.elements:
            if e is None:
                elems.append("None")
            elif isinstance(e, SpreadElement):
                elems.append(f"*{self._expr(e.argument)}")
            else:
                elems.append(self._expr(e))
        return f"[{', '.join(elems)}]"

    def _e_ObjectLiteral(self, n: ObjectLiteral) -> str:
        parts = []
        for prop in n.properties:
            if isinstance(prop.value, SpreadElement):
                parts.append(f"**{self._expr(prop.value.argument)}")
            elif prop.computed:
                parts.append(f"{self._expr(prop.key)}: {self._expr(prop.value)}")
            elif prop.shorthand:
                parts.append(f'"{prop.key}": {prop.key}')
            elif prop.method:
                parts.append(f'"{prop.key}": {self._expr(prop.value)}')
            else:
                key_s = repr(prop.key) if isinstance(prop.key, str) else self._expr(prop.key)
                parts.append(f"{key_s}: {self._expr(prop.value)}")
        return "_UrduObj({" + ", ".join(parts) + "})"

    def _e_BinaryExpr(self, n: BinaryExpr) -> str:
        op = n.op
        return f"({self._expr(n.left)} {op} {self._expr(n.right)})"

    def _e_LogicalExpr(self, n: LogicalExpr) -> str:
        py_op = "and" if n.op in ("&&", "اور") else "or"
        return f"({self._expr(n.left)} {py_op} {self._expr(n.right)})"

    def _e_UnaryExpr(self, n: UnaryExpr) -> str:
        op = n.op
        if op == "not":
            return f"(not {self._expr(n.operand)})"
        return f"({op}{self._expr(n.operand)})"

    def _e_UpdateExpr(self, n: UpdateExpr) -> str:
        tgt = self._expr(n.operand)
        if n.op == "++":
            return f"({tgt} + 1)"   # used as expression; side-effect emitted by _s_ExpressionStatement
        else:
            return f"({tgt} - 1)"

    def _e_AssignExpr(self, n: AssignExpr) -> str:
        lhs = self._expr(n.left)
        rhs = self._expr(n.right)
        op = n.op
        if op == "=":
            return f"{lhs} = {rhs}"
        elif op == "??=":
            return f"{lhs} = {lhs} if {lhs} is not None else {rhs}"
        else:
            return f"{lhs} {op} {rhs}"

    def _e_TernaryExpr(self, n: TernaryExpr) -> str:
        cond = self._expr(n.condition)
        cons = self._expr(n.consequent)
        alt  = self._expr(n.alternate)
        # Wrap condition in parens: prevents Python precedence issues when the
        # condition contains logical operators (and/or) or when ternaries are
        # deeply nested — Python's if/else has lower precedence than and/or.
        return f"({cons} if ({cond}) else {alt})"

    def _e_NullishExpr(self, n: NullishExpr) -> str:
        lhs = self._expr(n.left)
        rhs = self._expr(n.right)
        return f"({lhs} if {lhs} is not None else {rhs})"

    # JS properties that map to Python expressions
    _JS_PROP_MAP: dict[str, str] = {
        "length":    "len({obj})",
        "size":      "len({obj})",
    }

    def _e_MemberExpr(self, n: MemberExpr) -> str:
        obj = self._expr(n.obj)
        if n.computed:
            idx = self._expr(n.prop)
            if n.optional:
                return f"(_urdu_opt({obj}, {idx}))"
            return f"{obj}[{idx}]"
        prop = self._expr(n.prop)
        # Urdu + JS property → Python expression mapping
        if not n.optional:
            if prop in self._URDU_PROP_MAP:
                return self._URDU_PROP_MAP[prop].format(obj=obj)
            if prop in self._JS_PROP_MAP:
                return self._JS_PROP_MAP[prop].format(obj=obj)
        if n.optional:
            return f"(getattr({obj}, {prop!r}, None) if {obj} is not None else None)"
        return f"{obj}.{prop}"

    # Urdu method names → JS method names (normalised before JS→Python mapping)
    _URDU_TO_JS_METHOD: dict[str, str] = {
        # ── String ──────────────────────────────────────────────────────────
        "چھاٹو":          "trim",           # trim whitespace
        "شروع_چھاٹو":     "trimStart",      # ltrim
        "آخر_چھاٹو":      "trimEnd",        # rtrim
        "بڑے_حروف":       "toUpperCase",    # uppercase
        "چھوٹے_حروف":     "toLowerCase",    # lowercase
        "شروع_ہے":        "startsWith",     # startsWith
        "ختم_ہے":         "endsWith",       # endsWith
        "مقام":           "indexOf",        # indexOf
        "آخری_مقام":      "lastIndexOf",    # lastIndexOf
        "بدلو":           "replaceAll",     # replace / replaceAll
        "دہراؤ":          "repeat",         # repeat
        "شامل_ہے":        "includes",       # includes (str & arr)
        "جوڑو":           "join",           # arr.join(sep)
        "حصہ":            "slice",          # slice(start, end)
        # ── Array ───────────────────────────────────────────────────────────
        "شامل":           "push",           # push / append
        "نکالو":          "pop",            # pop
        "پہلا_نکالو":     "shift",          # shift / pop(0)
        "پہلے_شامل":      "unshift",        # unshift / insert(0,x)
        "چھانو":          "filter",         # filter
        "تبدیل":          "map",            # map
        "اکٹھا":          "reduce",         # reduce
        "ہر_ایک":         "forEach",        # forEach
        "تلاش":           "find",           # find
        "تلاش_مقام":      "findIndex",      # findIndex
        "کوئی":           "some",           # some
        "سب":             "every",          # every
        "پھیلاؤ":         "flat",           # flat
        "پھیلا_تبدیل":    "flatMap",        # flatMap
        "ملاؤ":           "concat",         # concat
        "بھرو":           "fill",           # fill
        "کاٹو":           "splice",         # splice
        "ترتیب_دو":       "sort",           # sort (ترتیب is already a builtin)
        "پلٹاؤ":          "reverse",        # reverse
    }

    # JS properties that also have Urdu aliases
    _URDU_PROP_MAP: dict[str, str] = {
        "لمبائی":    "len({obj})",   # .length / .لمبائی
    }

    # JS method names that map directly to Python equivalents
    _JS_TO_PY_METHOD: dict[str, str] = {
        # String
        "trim":         "strip",
        "trimStart":    "lstrip",
        "trimEnd":      "rstrip",
        "toUpperCase":  "upper",
        "toLowerCase":  "lower",
        "startsWith":   "startswith",
        "endsWith":     "endswith",
        "indexOf":      "find",
        "lastIndexOf":  "rfind",
        "replaceAll":   "replace",
        "padStart":     "rjust",
        "padEnd":       "ljust",
        "repeat":       "__mul__",   # handled specially below
        "charAt":       "__getitem__",
        # Array
        "push":         "append",
        "pop":          "pop",
        "shift":        "pop",       # pop(0) — handled below
        "unshift":      "insert",    # insert(0, x) — handled below
        "indexOf":      "index",
        "splice":       "_urdu_splice",
        "flat":         "_urdu_flat",
    }

    def _e_CallExpr(self, n: CallExpr) -> str:
        # ── JS method-name aliasing ─────────────────��────────────────────────
        if isinstance(n.callee, MemberExpr) and not n.callee.computed:
            obj  = self._expr(n.callee.obj)
            meth = n.callee.prop.name if isinstance(n.callee.prop, Identifier) else ""
            _orig_meth = meth  # save before Urdu normalisation
            # Normalise Urdu method name → JS name before further processing
            meth = self._URDU_TO_JS_METHOD.get(meth, meth)
            args_list = n.args

            # includes(x)  →  (x in obj)
            if meth == "includes" and len(args_list) == 1:
                return f"({self._expr(args_list[0])} in {obj})"

            # جوڑو(sep)  →  sep.join(obj)   (JS: arr.join(sep) = Python: sep.join(arr))
            # Only invert when the Urdu keyword جوڑو was used.  Raw .join() calls
            # (e.g. os.path.join, str.join) must pass through unchanged.
            if meth == "join" and _orig_meth == "جوڑو":
                sep = self._expr(args_list[0]) if args_list else '""'
                return f"{sep}.join({obj})"

            # ── Array functional methods ─────────────────────────────────────
            # Only apply when argument is a function (arrow/expr/identifier).
            # If the argument is a dict, list, or literal, fall through so the
            # object's own Python method is called (e.g. MongoDB col.find({})).
            def _is_fn(node) -> bool:
                return isinstance(node, (ArrowFunction, FunctionExpr, Identifier))

            # filter(fn)  →  list(filter(fn, obj))
            if meth == "filter" and len(args_list) == 1 and _is_fn(args_list[0]):
                fn = self._expr(args_list[0])
                return f"list(filter({fn}, {obj}))"

            # map(fn)  →  list(map(fn, obj))
            if meth == "map" and len(args_list) == 1 and _is_fn(args_list[0]):
                fn = self._expr(args_list[0])
                return f"list(map({fn}, {obj}))"

            # reduce(fn) / reduce(fn, init)
            if meth == "reduce" and args_list and _is_fn(args_list[0]):
                fn = self._expr(args_list[0])
                if len(args_list) == 2:
                    init = self._expr(args_list[1])
                    return f"__import__('functools').reduce({fn}, {obj}, {init})"
                return f"__import__('functools').reduce({fn}, {obj})"

            # forEach(fn)  →  side-effect loop
            if meth == "forEach" and len(args_list) == 1 and _is_fn(args_list[0]):
                fn = self._expr(args_list[0])
                return f"[{fn}(_x) for _x in {obj}] and None"

            # every(fn)  →  all(fn(x) for x in obj)
            if meth == "every" and len(args_list) == 1 and _is_fn(args_list[0]):
                fn = self._expr(args_list[0])
                return f"all({fn}(_x) for _x in {obj})"

            # some(fn)  →  any(fn(x) for x in obj)
            if meth == "some" and len(args_list) == 1 and _is_fn(args_list[0]):
                fn = self._expr(args_list[0])
                return f"any({fn}(_x) for _x in {obj})"

            # find(fn)  →  next((x for x in obj if fn(x)), None)
            if meth == "find" and len(args_list) == 1 and _is_fn(args_list[0]):
                fn = self._expr(args_list[0])
                return f"next((_x for _x in {obj} if {fn}(_x)), None)"

            # findIndex(fn)  →  next((i for i,x in enumerate(obj) if fn(x)), -1)
            if meth == "findIndex" and len(args_list) == 1 and _is_fn(args_list[0]):
                fn = self._expr(args_list[0])
                return f"next((_i for _i, _x in enumerate({obj}) if {fn}(_x)), -1)"

            # flatMap(fn)  →  [y for x in obj for y in fn(x)]
            if meth == "flatMap" and len(args_list) == 1 and _is_fn(args_list[0]):
                fn = self._expr(args_list[0])
                return f"[_y for _x in {obj} for _y in {fn}(_x)]"

            # slice(start) / slice(start, end)  →  obj[start:end]
            if meth == "slice":
                start = self._expr(args_list[0]) if len(args_list) > 0 else ""
                end   = self._expr(args_list[1]) if len(args_list) > 1 else ""
                return f"{obj}[{start}:{end}]"

            # reverse()  →  obj[::-1]  (copy, chainable; Python's list.reverse() returns None)
            if meth == "reverse" and len(args_list) == 0:
                return f"{obj}[::-1]"

            # sort() / sort(fn)  →  sorted(obj) / sorted(obj, key=fn)
            if meth == "sort":
                if args_list:
                    fn = self._expr(args_list[0])
                    return f"sorted({obj}, key={fn})"
                return f"sorted({obj})"

            # concat(...arrays)  →  obj + arr1 + arr2 ...
            if meth == "concat":
                parts = " + ".join(self._expr(a) for a in args_list)
                return f"({obj} + {parts})" if parts else f"list({obj})"

            # fill(val, start, end) — mutates; returns obj
            if meth == "fill":
                val   = self._expr(args_list[0]) if args_list else "None"
                start = self._expr(args_list[1]) if len(args_list) > 1 else "0"
                end   = self._expr(args_list[2]) if len(args_list) > 2 else f"len({obj})"
                return f"_urdu_fill({obj}, {val}, {start}, {end})"

            # shift()  →  obj.pop(0)
            if meth == "shift" and len(args_list) == 0:
                return f"{obj}.pop(0)"

            # unshift(x)  →  obj.insert(0, x)
            if meth == "unshift" and len(args_list) == 1:
                return f"{obj}.insert(0, {self._expr(args_list[0])})"

            # repeat(n)  →  obj * n
            if meth == "repeat" and len(args_list) == 1:
                return f"({obj} * {self._expr(args_list[0])})"

            # splice(start, count)  →  del obj[start:start+count]  (as expr: _urdu_splice)
            if meth == "splice":
                args = self._args(args_list)
                return f"_urdu_splice({obj}, {args})"

            # flat() / flat(depth)  →  _urdu_flat(obj, depth)
            if meth == "flat":
                depth = self._expr(args_list[0]) if args_list else "1"
                return f"_urdu_flat({obj}, {depth})"

            # direct rename
            py_meth = self._JS_TO_PY_METHOD.get(meth)
            if py_meth:
                args = self._args(args_list)
                if n.callee.optional:
                    return f"(getattr({obj}, {py_meth!r}, lambda *a: None)({args}) if {obj} is not None else None)"
                return f"{obj}.{py_meth}({args})"

        callee = self._expr(n.callee)
        # map built-ins
        callee = {"لکھو": "print", "پڑھو": "input"}.get(callee, callee)
        args = self._args(n.args)
        # super(...) in constructor context → super().__init__(...)
        if callee == "super()":
            return f"super().__init__({args})"
        if n.optional:
            return f"({callee}({args}) if {callee} is not None else None)"
        return f"{callee}({args})"

    def _e_NewExpr(self, n: NewExpr) -> str:
        callee = self._expr(n.callee)
        args = self._args(n.args)
        return f"{callee}({args})"

    def _e_SpreadElement(self, n: SpreadElement) -> str:
        return f"*{self._expr(n.argument)}"

    def _e_SequenceExpr(self, n: SequenceExpr) -> str:
        return ", ".join(self._expr(e) for e in n.expressions)

    def _e_AwaitExpr(self, n: AwaitExpr) -> str:
        self._has_async = True
        return f"(await {self._expr(n.argument)})"

    def _e_YieldExpr(self, n: YieldExpr) -> str:
        if n.delegate:
            return f"(yield from {self._expr(n.argument)})"
        if n.argument:
            return f"(yield {self._expr(n.argument)})"
        return "(yield)"

    def _e_TypeofExpr(self, n: TypeofExpr) -> str:
        return f"_urdu_typeof({self._expr(n.argument)})"

    def _e_DeleteExpr(self, n: DeleteExpr) -> str:
        return f"_urdu_delete(lambda: {self._expr(n.argument)})"

    def _e_VoidExpr(self, n: VoidExpr) -> str:
        return f"(({self._expr(n.argument)}) and None)"

    def _e_InstanceofExpr(self, n: InstanceofExpr) -> str:
        return f"isinstance({self._expr(n.left)}, {self._expr(n.right)})"

    def _e_InExpr(self, n: InExpr) -> str:
        return f"({self._expr(n.key)} in {self._expr(n.obj)})"

    def _e_TaggedTemplateExpr(self, n: TaggedTemplateExpr) -> str:
        tag = self._expr(n.tag)
        tmpl = self._e_TemplateLiteral(n.template)
        return f"{tag}({tmpl})"

    def _e_FunctionExpr(self, n: FunctionExpr) -> str:
        name = n.name or f"_fn_{self._lambda_counter}"
        self._lambda_counter += 1
        params = self._params(n.params, in_class=False)
        prefix = "async " if n.is_async else ""
        cur_ind = "    " * self._indent
        # capture body at indent=0 base, then re-indent to current scope
        old_indent = self._indent
        old_lines = self._lines
        self._indent = 0
        self._lines = []
        if n.body.body:
            for s in n.body.body:
                self._stmt(s)
        else:
            self._w("pass")
        body_lines = self._lines
        self._lines = old_lines
        self._indent = old_indent
        # emit inline so the closure captures the enclosing scope
        self._pending_defs.append(f"{cur_ind}{prefix}def {name}({params}):")
        for bl in body_lines:
            self._pending_defs.append(f"{cur_ind}    {bl}")
        self._pending_defs.append("")
        return name

    def _e_ArrowFunction(self, n: ArrowFunction) -> str:
        if n.is_expression and not n.is_async:
            params = self._params(n.params, in_class=False)
            body = self._expr(n.body)
            return f"(lambda {params}: {body})" if params else f"(lambda: {body})"
        # block-body or async arrow → emit inline as closure
        name = f"_arrow_{self._lambda_counter}"
        self._lambda_counter += 1
        params = self._params(n.params, in_class=False)
        prefix = "async " if n.is_async else ""
        if n.is_async:
            self._has_async = True
        cur_ind = "    " * self._indent
        old_indent = self._indent
        old_lines = self._lines
        self._indent = 0
        self._lines = []
        if n.is_expression:
            self._w(f"return {self._expr(n.body)}")
        else:
            for s in n.body.body:
                self._stmt(s)
            if not n.body.body:
                self._w("pass")
        body_lines = self._lines
        self._lines = old_lines
        self._indent = old_indent
        self._pending_defs.append(f"{cur_ind}{prefix}def {name}({params}):")
        for bl in body_lines:
            self._pending_defs.append(f"{cur_ind}    {bl}")
        self._pending_defs.append("")
        return name

    # ── helpers ───────────────────────────────────────────────────────────────

    def _params(self, params: list[Param], in_class: bool = False) -> str:
        parts = []
        if in_class:
            parts.append("self")
        for p in params:
            name = self._pattern(p.name)
            if p.rest:
                s = f"*{name}"
            elif p.default is not None:
                s = f"{name}={self._expr(p.default)}"
            else:
                s = name
            parts.append(s)
        return ", ".join(parts)

    def _args(self, args: list[ASTNode]) -> str:
        parts = []
        for a in args:
            if isinstance(a, SpreadElement):
                parts.append(f"*{self._expr(a.argument)}")
            else:
                parts.append(self._expr(a))
        return ", ".join(parts)

    def _pattern(self, node: ASTNode) -> str:
        if isinstance(node, Identifier):
            return node.name
        if isinstance(node, ArrayPattern):
            elems = [self._pattern(e) if e else "_" for e in node.elements]
            return f"[{', '.join(elems)}]"
        if isinstance(node, ObjectPattern):
            # Python doesn't support object destructuring natively in assignment
            # Generate tuple of values
            keys = [p.key for p in node.properties if isinstance(p, ObjectPatternProp)]
            return ", ".join(keys)
        if isinstance(node, RestElement):
            return f"*{self._pattern(node.argument)}"
        if isinstance(node, AssignPattern):
            return f"{self._pattern(node.left)}={self._expr(node.right)}"
        return self._expr(node)
