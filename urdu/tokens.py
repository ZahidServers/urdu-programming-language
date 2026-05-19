"""Token types and Urdu keyword mappings for the Urdu Programming Language."""

from enum import Enum, auto


class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    TEMPLATE_STRING = auto()
    IDENTIFIER = auto()
    REGEX = auto()

    # Variable declarations
    VAR = auto()           # متغیر
    CONST = auto()         # مستقل
    LET = auto()           # چھوٹا (alias)

    # Control flow
    IF = auto()            # اگر
    ELSE = auto()          # ورنہ
    ELIF = auto()          # ورنہ_اگر
    WHILE = auto()         # جبکہ
    FOR = auto()           # کے_لیے
    IN = auto()            # میں   (for...in / for...of)
    OF = auto()            # کا    (for...of)
    BREAK = auto()         # ٹوٹنا
    CONTINUE = auto()      # جاری
    RETURN = auto()        # واپس
    DO = auto()            # کرو

    # Switch
    SWITCH = auto()        # منتخب
    CASE = auto()          # صورت
    SWITCH_DEFAULT = auto()  # بصورت_دیگر

    # Functions
    FUNCTION = auto()      # فنکشن
    ASYNC = auto()         # غیر_متزامن
    AWAIT = auto()         # انتظار
    YIELD = auto()         # پیداوار

    # Classes / OOP
    CLASS = auto()         # کلاس
    EXTENDS = auto()       # توسیع
    CONSTRUCTOR = auto()   # تعمیر
    THIS = auto()          # یہ
    SUPER = auto()         # سپر
    NEW = auto()           # نیا
    PUBLIC = auto()        # عوامی
    PRIVATE = auto()       # نجی
    PROTECTED = auto()     # محفوظ
    STATIC = auto()        # جامد
    ABSTRACT = auto()      # خاکہ
    INTERFACE = auto()     # انٹرفیس
    IMPLEMENTS = auto()    # نافذ
    READONLY = auto()      # صرف_پڑھو
    OVERRIDE = auto()      # اوور_رائڈ
    GET = auto()           # حاصل_کرو
    SET = auto()           # مقرر_کرو

    # Exception handling
    TRY = auto()           # کوشش
    CATCH = auto()         # پکڑو
    FINALLY = auto()       # آخر
    THROW = auto()         # پھینکو

    # Import / Export
    IMPORT = auto()        # درآمد
    FROM = auto()          # سے
    EXPORT = auto()        # برآمد
    DEFAULT = auto()       # ڈیفالٹ
    AS = auto()            # بطور

    # Boolean / null
    TRUE = auto()          # سچ
    FALSE = auto()         # جھوٹ
    NULL = auto()          # خالی
    UNDEFINED = auto()     # غیر_معرف

    # Logical keyword operators
    AND = auto()           # اور
    OR = auto()            # یا
    NOT = auto()           # نہیں

    # Type operators
    TYPEOF = auto()        # قسم
    INSTANCEOF = auto()    # مثال
    DELETE = auto()        # حذف
    IN_OP = auto()         # میں_ہے
    VOID = auto()          # خلاء

    # Built-in functions
    PRINT = auto()         # لکھو
    INPUT_FN = auto()      # پڑھو

    # --- Operators ---
    PLUS = auto()                # +
    MINUS = auto()               # -
    MULTIPLY = auto()            # *
    DIVIDE = auto()              # /
    MODULO = auto()              # %
    POWER = auto()               # **
    FLOOR_DIVIDE = auto()        # //

    PLUS_ASSIGN = auto()         # +=
    MINUS_ASSIGN = auto()        # -=
    MULTIPLY_ASSIGN = auto()     # *=
    DIVIDE_ASSIGN = auto()       # /=
    MODULO_ASSIGN = auto()       # %=
    POWER_ASSIGN = auto()        # **=
    AND_ASSIGN = auto()          # &&=
    OR_ASSIGN = auto()           # ||=
    NULLISH_ASSIGN = auto()      # ??=
    BITAND_ASSIGN = auto()       # &=
    BITOR_ASSIGN = auto()        # |=

    EQUALS = auto()              # ==
    NOT_EQUALS = auto()          # !=
    STRICT_EQUALS = auto()       # ===
    STRICT_NOT_EQUALS = auto()   # !==
    LESS_THAN = auto()           # <
    GREATER_THAN = auto()        # >
    LESS_EQUAL = auto()          # <=
    GREATER_EQUAL = auto()       # >=

    ASSIGN = auto()              # =

    LOGICAL_AND = auto()         # &&
    LOGICAL_OR = auto()          # ||
    LOGICAL_NOT = auto()         # !

    BITWISE_AND = auto()         # &
    BITWISE_OR = auto()          # |
    BITWISE_XOR = auto()         # ^
    BITWISE_NOT = auto()         # ~
    LEFT_SHIFT = auto()          # <<
    RIGHT_SHIFT = auto()         # >>
    UNSIGNED_RIGHT_SHIFT = auto() # >>>

    ARROW = auto()               # => or ->
    OPTIONAL_CHAIN = auto()      # ?.
    NULLISH = auto()             # ??

    INCREMENT = auto()           # ++
    DECREMENT = auto()           # --
    SPREAD = auto()              # ...

    # Punctuation
    LEFT_BRACE = auto()     # {
    RIGHT_BRACE = auto()    # }
    LEFT_PAREN = auto()     # (
    RIGHT_PAREN = auto()    # )
    LEFT_BRACKET = auto()   # [
    RIGHT_BRACKET = auto()  # ]
    SEMICOLON = auto()      # ;
    COMMA = auto()          # ,
    DOT = auto()            # .
    COLON = auto()          # :
    QUESTION = auto()       # ?
    AT = auto()             # @ (decorators)
    HASH = auto()           # # (private fields)

    # Special
    EOF = auto()
    NEWLINE = auto()


# ─── Urdu Keyword → TokenType mapping ───────────────────────────────────────
URDU_KEYWORDS: dict[str, TokenType] = {
    # Variable declarations
    "متغیر":       TokenType.VAR,
    "مستقل":       TokenType.CONST,
    "چھوٹا":       TokenType.LET,

    # Control flow
    "اگر":         TokenType.IF,
    "ورنہ":        TokenType.ELSE,
    "ورنہ_اگر":    TokenType.ELIF,
    "جبکہ":        TokenType.WHILE,
    "کے_لیے":      TokenType.FOR,
    "میں":         TokenType.IN,
    "کا":          TokenType.OF,
    "ٹوٹنا":       TokenType.BREAK,
    "جاری":        TokenType.CONTINUE,
    "واپس":        TokenType.RETURN,
    "کرو":         TokenType.DO,

    # Switch
    "منتخب":       TokenType.SWITCH,
    "صورت":        TokenType.CASE,
    "بصورت_دیگر":  TokenType.SWITCH_DEFAULT,

    # Functions
    "فنکشن":       TokenType.FUNCTION,
    "غیر_متزامن":  TokenType.ASYNC,
    "انتظار":      TokenType.AWAIT,
    "پیداوار":     TokenType.YIELD,

    # Classes / OOP
    "کلاس":        TokenType.CLASS,
    "توسیع":       TokenType.EXTENDS,
    "تعمیر":       TokenType.CONSTRUCTOR,
    "یہ":          TokenType.THIS,
    "سپر":         TokenType.SUPER,
    "نیا":         TokenType.NEW,
    "عوامی":       TokenType.PUBLIC,
    "نجی":         TokenType.PRIVATE,
    "محفوظ":       TokenType.PROTECTED,
    "جامد":        TokenType.STATIC,
    "خاکہ":        TokenType.ABSTRACT,
    "انٹرفیس":     TokenType.INTERFACE,
    "نافذ":        TokenType.IMPLEMENTS,
    "صرف_پڑھو":    TokenType.READONLY,
    "اوور_رائڈ":   TokenType.OVERRIDE,
    "حاصل_کرو":    TokenType.GET,
    "مقرر_کرو":    TokenType.SET,

    # Exception handling
    "کوشش":        TokenType.TRY,
    "پکڑو":        TokenType.CATCH,
    "آخر":         TokenType.FINALLY,
    "پھینکو":      TokenType.THROW,

    # Import / Export
    "درآمد":       TokenType.IMPORT,
    "سے":          TokenType.FROM,
    "برآمد":       TokenType.EXPORT,
    "ڈیفالٹ":      TokenType.DEFAULT,
    "بطور":        TokenType.AS,

    # Boolean / null
    "سچ":          TokenType.TRUE,
    "جھوٹ":        TokenType.FALSE,
    "خالی":        TokenType.NULL,
    "غیر_معرف":    TokenType.UNDEFINED,

    # Logical
    "اور":         TokenType.AND,
    "یا":          TokenType.OR,
    "نہیں":        TokenType.NOT,

    # Type operators
    "قسم":         TokenType.TYPEOF,
    "مثال":        TokenType.INSTANCEOF,
    "حذف":         TokenType.DELETE,
    "میں_ہے":      TokenType.IN_OP,
    "خلاء":        TokenType.VOID,

    # Built-ins
    "لکھو":        TokenType.PRINT,
    "پڑھو":        TokenType.INPUT_FN,
}
