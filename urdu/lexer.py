"""Lexer / Tokenizer for the Urdu Programming Language."""

from __future__ import annotations
from .tokens import TokenType, URDU_KEYWORDS


# ─── Token dataclass ─────────────────────────────────────────────────────────

class Token:
    __slots__ = ("type", "value", "line", "column")

    def __init__(self, type: TokenType, value, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


# ─── Helper predicates ───────────────────────────────────────────────────────

# Arabic punctuation to exclude from identifiers
_ARABIC_PUNCT = frozenset([
    0x060C,  # ،  Arabic comma   → maps to COMMA
    0x061B,  # ؛  Arabic semicolon → SEMICOLON
    0x061F,  # ؟  Arabic question mark → QUESTION
    0x060D,  # Arabic date separator
    0x060E, 0x060F,  # Signs
    0x0600, 0x0601, 0x0602, 0x0603, 0x0604, 0x0605,
    0x0609, 0x060A,  # Per mille, per ten thousand
    0x06D4,  # ۔  Urdu full stop (sentence end — not part of identifiers)
])


def _is_urdu_char(ch: str) -> bool:
    cp = ord(ch)
    if cp in _ARABIC_PUNCT:
        return False
    return (
        0x0610 <= cp <= 0x06FF or   # Arabic / Urdu (after punct range)
        0x0606 <= cp <= 0x0608 or   # Signs that are OK in identifiers
        0xFB50 <= cp <= 0xFDFF or   # Arabic Pres. Forms-A
        0xFE70 <= cp <= 0xFEFF or   # Arabic Pres. Forms-B
        0x200C <= cp <= 0x200F      # ZWNJ / ZWJ used in Urdu
    )


def _is_id_start(ch: str) -> bool:
    return ch == "_" or ch.isalpha() or _is_urdu_char(ch)


def _is_id_part(ch: str) -> bool:
    return ch == "_" or ch.isalnum() or _is_urdu_char(ch)


# ─── Lexer ───────────────────────────────────────────────────────────────────

class LexerError(Exception):
    def __init__(self, msg: str, line: int, col: int):
        super().__init__(f"لیکسر غلطی [{line}:{col}]: {msg}")
        self.line = line
        self.col = col


# Normalize Eastern Arabic (۰-۹) and Arabic-Indic (٠-٩) digits → ASCII 0-9
_URDU_DIGIT_TABLE = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹"   # U+06F0–06F9  Extended Arabic-Indic (Urdu/Farsi)
    "٠١٢٣٤٥٦٧٨٩",  # U+0660–0669  Arabic-Indic
    "01234567890123456789"
)


class Lexer:
    def __init__(self, source: str):
        self.source = source.translate(_URDU_DIGIT_TABLE)
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: list[Token] = []

    # ── low-level helpers ────────────────────────────────────────────────────

    def _peek(self, offset: int = 0) -> str | None:
        idx = self.pos + offset
        return self.source[idx] if idx < len(self.source) else None

    def _advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self.pos < len(self.source) and self.source[self.pos] == expected:
            self._advance()
            return True
        return False

    def _tok(self, type: TokenType, value, line: int, col: int) -> Token:
        t = Token(type, value, line, col)
        self.tokens.append(t)
        return t

    # ── skip whitespace / comments ───────────────────────────────────────────

    def _skip(self):
        while self.pos < len(self.source):
            ch = self._peek()
            if ch in " \t\r\n":
                self._advance()
            elif ch == "/" and self._peek(1) == "/":
                while self.pos < len(self.source) and self._peek() != "\n":
                    self._advance()
            elif ch == "/" and self._peek(1) == "*":
                self._advance(); self._advance()
                while self.pos < len(self.source):
                    if self._peek() == "*" and self._peek(1) == "/":
                        self._advance(); self._advance()
                        break
                    self._advance()
            else:
                break

    # ── string literals ──────────────────────────────────────────────────────

    _ESCAPES = {
        "n": "\n", "t": "\t", "r": "\r", "\\": "\\",
        '"': '"', "'": "'", "0": "\0", "b": "\b",
        "f": "\f", "v": "\v", "`": "`",
    }

    def _read_string(self, quote: str) -> Token:
        sl, sc = self.line, self.col
        self._advance()          # opening quote
        buf: list[str] = []
        while self.pos < len(self.source):
            ch = self._peek()
            if ch == quote:
                self._advance()
                break
            if ch == "\n":
                raise LexerError("Unterminated string literal", sl, sc)
            if ch == "\\":
                self._advance()
                esc = self._advance()
                buf.append(self._ESCAPES.get(esc, esc))
            else:
                buf.append(self._advance())
        return Token(TokenType.STRING, "".join(buf), sl, sc)

    def _read_template(self) -> Token:
        sl, sc = self.line, self.col
        self._advance()          # opening backtick
        parts: list[tuple[str, str]] = []
        cur: list[str] = []
        while self.pos < len(self.source):
            ch = self._peek()
            if ch == "`":
                self._advance()
                break
            if ch == "$" and self._peek(1) == "{":
                parts.append(("text", "".join(cur)))
                cur = []
                self._advance(); self._advance()  # $, {
                depth = 1
                expr: list[str] = []
                while self.pos < len(self.source) and depth > 0:
                    c = self._peek()
                    if c == "{":
                        depth += 1
                    elif c == "}":
                        depth -= 1
                        if depth == 0:
                            self._advance()
                            break
                    expr.append(self._advance())
                parts.append(("expr", "".join(expr)))
            elif ch == "\\":
                self._advance()
                esc = self._advance()
                cur.append(self._ESCAPES.get(esc, esc))
            else:
                cur.append(self._advance())
        parts.append(("text", "".join(cur)))
        return Token(TokenType.TEMPLATE_STRING, parts, sl, sc)

    # ── number literals ──────────────────────────────────────────────────────

    def _read_number(self) -> Token:
        sl, sc = self.line, self.col
        buf: list[str] = []
        is_float = False

        # hex
        if self._peek() == "0" and self._peek(1) in ("x", "X"):
            buf += [self._advance(), self._advance()]
            while self.pos < len(self.source) and self._peek() in "0123456789abcdefABCDEF_":
                ch = self._advance()
                if ch != "_": buf.append(ch)
            return Token(TokenType.NUMBER, int("".join(buf), 16), sl, sc)

        # binary
        if self._peek() == "0" and self._peek(1) in ("b", "B"):
            buf += [self._advance(), self._advance()]
            while self.pos < len(self.source) and self._peek() in "01_":
                ch = self._advance()
                if ch != "_": buf.append(ch)
            return Token(TokenType.NUMBER, int("".join(buf), 2), sl, sc)

        while self.pos < len(self.source) and (self._peek().isdigit() or self._peek() == "_"):
            ch = self._advance()
            if ch != "_": buf.append(ch)

        if (self.pos < len(self.source) and self._peek() == "." and
                self._peek(1) and self._peek(1).isdigit()):
            is_float = True
            buf.append(self._advance())
            while self.pos < len(self.source) and (self._peek().isdigit() or self._peek() == "_"):
                ch = self._advance()
                if ch != "_": buf.append(ch)

        if self.pos < len(self.source) and self._peek() in ("e", "E"):
            is_float = True
            buf.append(self._advance())
            if self.pos < len(self.source) and self._peek() in ("+", "-"):
                buf.append(self._advance())
            while self.pos < len(self.source) and self._peek().isdigit():
                buf.append(self._advance())

        s = "".join(buf)
        return Token(TokenType.NUMBER, float(s) if is_float else int(s), sl, sc)

    # ── identifiers / keywords ───────────────────────────────────────────────

    def _read_identifier(self) -> Token:
        sl, sc = self.line, self.col
        buf: list[str] = []
        while self.pos < len(self.source) and _is_id_part(self._peek()):
            buf.append(self._advance())
        word = "".join(buf)
        tok_type = URDU_KEYWORDS.get(word, TokenType.IDENTIFIER)
        return Token(tok_type, word, sl, sc)

    # ── main tokenize ────────────────────────────────────────────────────────

    def tokenize(self) -> list[Token]:
        while True:
            self._skip()
            if self.pos >= len(self.source):
                self._tok(TokenType.EOF, None, self.line, self.col)
                break

            sl, sc = self.line, self.col
            ch = self._peek()

            # --- string / template ---
            if ch in ('"', "'"):
                self.tokens.append(self._read_string(ch)); continue
            if ch == "`":
                self.tokens.append(self._read_template()); continue

            # --- number ---
            if ch.isdigit() or (ch == "." and self._peek(1) and self._peek(1).isdigit()):
                self.tokens.append(self._read_number()); continue

            # --- identifier / keyword ---
            if _is_id_start(ch):
                self.tokens.append(self._read_identifier()); continue

            # --- decorator ---
            if ch == "@":
                self._advance()
                self._tok(TokenType.AT, "@", sl, sc); continue

            self._advance()  # consume operator char

            # ── two/three-char operators ────────────────────────────────────
            if ch == "+":
                if self._match("+"):  self._tok(TokenType.INCREMENT, "++", sl, sc)
                elif self._match("="): self._tok(TokenType.PLUS_ASSIGN, "+=", sl, sc)
                else:                  self._tok(TokenType.PLUS, "+", sl, sc)

            elif ch == "-":
                if self._match("-"):   self._tok(TokenType.DECREMENT, "--", sl, sc)
                elif self._match("="): self._tok(TokenType.MINUS_ASSIGN, "-=", sl, sc)
                elif self._match(">"): self._tok(TokenType.ARROW, "->", sl, sc)
                else:                  self._tok(TokenType.MINUS, "-", sl, sc)

            elif ch == "*":
                if self._peek() == "*":
                    self._advance()
                    if self._match("="): self._tok(TokenType.POWER_ASSIGN, "**=", sl, sc)
                    else:                self._tok(TokenType.POWER, "**", sl, sc)
                elif self._match("="): self._tok(TokenType.MULTIPLY_ASSIGN, "*=", sl, sc)
                else:                  self._tok(TokenType.MULTIPLY, "*", sl, sc)

            elif ch == "/":
                if self._match("="): self._tok(TokenType.DIVIDE_ASSIGN, "/=", sl, sc)
                elif self._match("/"): self._tok(TokenType.FLOOR_DIVIDE, "//", sl, sc)
                else:                 self._tok(TokenType.DIVIDE, "/", sl, sc)

            elif ch == "%":
                if self._match("="): self._tok(TokenType.MODULO_ASSIGN, "%=", sl, sc)
                else:                self._tok(TokenType.MODULO, "%", sl, sc)

            elif ch == "=":
                if self._peek() == "=":
                    self._advance()
                    if self._match("="): self._tok(TokenType.STRICT_EQUALS, "===", sl, sc)
                    else:                self._tok(TokenType.EQUALS, "==", sl, sc)
                elif self._match(">"): self._tok(TokenType.ARROW, "=>", sl, sc)
                else:                  self._tok(TokenType.ASSIGN, "=", sl, sc)

            elif ch == "!":
                if self._peek() == "=":
                    self._advance()
                    if self._match("="): self._tok(TokenType.STRICT_NOT_EQUALS, "!==", sl, sc)
                    else:                self._tok(TokenType.NOT_EQUALS, "!=", sl, sc)
                else:                   self._tok(TokenType.LOGICAL_NOT, "!", sl, sc)

            elif ch == "<":
                if self._match("<"):   self._tok(TokenType.LEFT_SHIFT, "<<", sl, sc)
                elif self._match("="): self._tok(TokenType.LESS_EQUAL, "<=", sl, sc)
                else:                  self._tok(TokenType.LESS_THAN, "<", sl, sc)

            elif ch == ">":
                if self._peek() == ">":
                    self._advance()
                    if self._match(">"): self._tok(TokenType.UNSIGNED_RIGHT_SHIFT, ">>>", sl, sc)
                    else:                self._tok(TokenType.RIGHT_SHIFT, ">>", sl, sc)
                elif self._match("="): self._tok(TokenType.GREATER_EQUAL, ">=", sl, sc)
                else:                  self._tok(TokenType.GREATER_THAN, ">", sl, sc)

            elif ch == "&":
                if self._peek() == "&":
                    self._advance()
                    if self._match("="): self._tok(TokenType.AND_ASSIGN, "&&=", sl, sc)
                    else:                self._tok(TokenType.LOGICAL_AND, "&&", sl, sc)
                elif self._match("="): self._tok(TokenType.BITAND_ASSIGN, "&=", sl, sc)
                else:                  self._tok(TokenType.BITWISE_AND, "&", sl, sc)

            elif ch == "|":
                if self._peek() == "|":
                    self._advance()
                    if self._match("="): self._tok(TokenType.OR_ASSIGN, "||=", sl, sc)
                    else:                self._tok(TokenType.LOGICAL_OR, "||", sl, sc)
                elif self._match("="): self._tok(TokenType.BITOR_ASSIGN, "|=", sl, sc)
                else:                  self._tok(TokenType.BITWISE_OR, "|", sl, sc)

            elif ch == "^":  self._tok(TokenType.BITWISE_XOR, "^", sl, sc)
            elif ch == "~":  self._tok(TokenType.BITWISE_NOT, "~", sl, sc)

            elif ch == "?":
                if self._peek() == "?":
                    self._advance()
                    if self._match("="): self._tok(TokenType.NULLISH_ASSIGN, "??=", sl, sc)
                    else:                self._tok(TokenType.NULLISH, "??", sl, sc)
                elif self._peek() == ".":
                    self._advance()
                    self._tok(TokenType.OPTIONAL_CHAIN, "?.", sl, sc)
                else:
                    self._tok(TokenType.QUESTION, "?", sl, sc)

            elif ch == ".":
                if self._peek() == "." and self._peek(1) == ".":
                    self._advance(); self._advance()
                    self._tok(TokenType.SPREAD, "...", sl, sc)
                else:
                    self._tok(TokenType.DOT, ".", sl, sc)

            elif ch == "{":  self._tok(TokenType.LEFT_BRACE, "{", sl, sc)
            elif ch == "}":  self._tok(TokenType.RIGHT_BRACE, "}", sl, sc)
            elif ch == "(":  self._tok(TokenType.LEFT_PAREN, "(", sl, sc)
            elif ch == ")":  self._tok(TokenType.RIGHT_PAREN, ")", sl, sc)
            elif ch == "[":  self._tok(TokenType.LEFT_BRACKET, "[", sl, sc)
            elif ch == "]":  self._tok(TokenType.RIGHT_BRACKET, "]", sl, sc)
            elif ch == ";":  self._tok(TokenType.SEMICOLON, ";", sl, sc)
            elif ch == ",":  self._tok(TokenType.COMMA, ",", sl, sc)
            elif ch == ":":  self._tok(TokenType.COLON, ":", sl, sc)
            elif ch == "#":  self._tok(TokenType.HASH, "#", sl, sc)
            # Arabic punctuation
            elif ch == "،":  self._tok(TokenType.COMMA, ",", sl, sc)       # ،
            elif ch == "؛":  self._tok(TokenType.SEMICOLON, ";", sl, sc)   # ؛
            elif ch == "؟":  self._tok(TokenType.QUESTION, "?", sl, sc)    # ؟
            elif ch == "۔":  self._tok(TokenType.SEMICOLON, ";", sl, sc)   # ۔ full stop
            else:
                raise LexerError(f"Unexpected character: {ch!r}", sl, sc)

        return self.tokens
