"""Urdu translations for common Python runtime errors."""

from __future__ import annotations
import re

# ── Exception type names ──────────────────────────────────────────────────────

TYPE_MAP: dict[str, str] = {
    # ── Built-in exceptions ───────────────────────────────────────────────────
    "Exception":              "غلطی",
    "BaseException":          "بنیادی غلطی",
    "TypeError":              "قسم کی غلطی",
    "ValueError":             "قدر کی غلطی",
    "NameError":              "نام کی غلطی",
    "UnboundLocalError":      "غیر متعین متغیر",
    "AttributeError":         "خصوصیت کی غلطی",
    "IndexError":             "اشاریہ کی غلطی",
    "KeyError":               "کلید کی غلطی",
    "ZeroDivisionError":      "صفر سے تقسیم",
    "OverflowError":          "عدد حد سے باہر",
    "ArithmeticError":        "حسابی غلطی",
    "FloatingPointError":     "اعشاریہ حساب غلطی",
    "RecursionError":         "تکرار کی حد ختم",
    "MemoryError":            "یادداشت ختم",
    "RuntimeError":           "چلتے وقت غلطی",
    "NotImplementedError":    "نافذ نہیں",
    "AssertionError":         "دعویٰ ناکام",
    "StopIteration":          "تکرار ختم",
    "StopAsyncIteration":     "غیر متزامن تکرار ختم",
    "GeneratorExit":          "جنریٹر بند",
    "SystemExit":             "نظام بند",
    "KeyboardInterrupt":      "کی بورڈ سے روکا",
    "SyntaxError":            "نحوی غلطی",
    "IndentationError":       "خلا کی غلطی",
    "TabError":               "ٹیب کی غلطی",
    "SystemError":            "نظامی غلطی",
    "LookupError":            "تلاش کی غلطی",
    "EOFError":               "فائل کا آخر",
    "BufferError":            "بفر غلطی",
    "ReferenceError":         "حوالہ کی غلطی",
    "UnicodeError":           "یونیکوڈ غلطی",
    "UnicodeDecodeError":     "یونیکوڈ ڈی کوڈ غلطی",
    "UnicodeEncodeError":     "یونیکوڈ انکوڈ غلطی",
    "UnicodeTranslateError":  "یونیکوڈ ترجمہ غلطی",

    # ── OS / File ─────────────────────────────────────────────────────────────
    "OSError":                "نظام کی غلطی",
    "IOError":                "ان پٹ/آؤٹ پٹ غلطی",
    "EnvironmentError":       "ماحول کی غلطی",
    "FileNotFoundError":      "فائل نہیں ملی",
    "FileExistsError":        "فائل پہلے سے موجود",
    "PermissionError":        "اجازت نہیں",
    "IsADirectoryError":      "یہ فولڈر ہے",
    "NotADirectoryError":     "یہ فولڈر نہیں",
    "InterruptedError":       "عمل روکا گیا",
    "BlockingIOError":        "بلاکنگ IO غلطی",
    "ChildProcessError":      "ذیلی عمل غلطی",
    "ProcessLookupError":     "عمل نہیں ملا",

    # ── Network ───────────────────────────────────────────────────────────────
    "TimeoutError":           "وقت ختم",
    "ConnectionError":        "رابطہ کی غلطی",
    "ConnectionRefusedError": "رابطہ مسترد",
    "ConnectionResetError":   "رابطہ منقطع",
    "ConnectionAbortedError": "رابطہ منسوخ",
    "BrokenPipeError":        "پائپ ٹوٹ گئی",
    "socket.gaierror":        "DNS تلاش ناکام",
    "socket.timeout":         "سوکٹ وقت ختم",

    # ── Import ────────────────────────────────────────────────────────────────
    "ImportError":            "درآمد کی غلطی",
    "ModuleNotFoundError":    "ماڈول نہیں ملا",

    # ── Async / Coroutine ─────────────────────────────────────────────────────
    "asyncio.InvalidStateError":   "غیر درست حالت",
    "asyncio.CancelledError":      "کام منسوخ",
    "asyncio.TimeoutError":        "غیر متزامن وقت ختم",
    "asyncio.IncompleteReadError": "نامکمل ریڈ",
    "CancelledError":              "کام منسوخ",

    # ── Database — SQLite ─────────────────────────────────────────────────────
    "sqlite3.OperationalError":    "SQLite آپریشنل غلطی",
    "sqlite3.IntegrityError":      "SQLite سالمیت غلطی",
    "sqlite3.ProgrammingError":    "SQLite پروگرامنگ غلطی",
    "sqlite3.DataError":           "SQLite ڈیٹا غلطی",
    "sqlite3.InterfaceError":      "SQLite انٹرفیس غلطی",
    "sqlite3.DatabaseError":       "SQLite ڈیٹا بیس غلطی",

    # ── Database — MySQL ──────────────────────────────────────────────────────
    "mysql.connector.Error":          "MySQL غلطی",
    "mysql.connector.IntegrityError": "MySQL سالمیت غلطی",
    "mysql.connector.OperationalError": "MySQL آپریشنل غلطی",
    "mysql.connector.ProgrammingError": "MySQL پروگرامنگ غلطی",
    "mysql.connector.DataError":      "MySQL ڈیٹا غلطی",

    # ── Database — PostgreSQL (psycopg2) ──────────────────────────────────────
    "psycopg2.OperationalError":   "PostgreSQL آپریشنل غلطی",
    "psycopg2.IntegrityError":     "PostgreSQL سالمیت غلطی",
    "psycopg2.ProgrammingError":   "PostgreSQL پروگرامنگ غلطی",
    "psycopg2.DataError":          "PostgreSQL ڈیٹا غلطی",
    "psycopg2.InterfaceError":     "PostgreSQL انٹرفیس غلطی",
    "psycopg2.DatabaseError":      "PostgreSQL ڈیٹا بیس غلطی",
    "psycopg2.InternalError":      "PostgreSQL داخلی غلطی",
    "psycopg2.NotSupportedError":  "PostgreSQL غیر حمایت یافتہ",
    "UniqueViolation":             "منفرد قید کی خلاف ورزی",
    "ForeignKeyViolation":         "غیر ملکی کلید کی خلاف ورزی",
    "NotNullViolation":            "خالی قدر ممنوع",
    "CheckViolation":              "شرط کی خلاف ورزی",
    "ExclusionViolation":          "اخراج قید کی خلاف ورزی",

    # ── Database — Generic ────────────────────────────────────────────────────
    "OperationalError":  "ڈیٹا بیس آپریشنل غلطی",
    "IntegrityError":    "ڈیٹا بیس سالمیت غلطی",
    "ProgrammingError":  "ڈیٹا بیس پروگرامنگ غلطی",
    "DataError":         "ڈیٹا غلطی",
    "DatabaseError":     "ڈیٹا بیس غلطی",
    "InterfaceError":    "انٹرفیس غلطی",
    "InternalError":     "داخلی غلطی",

    # ── MongoDB ───────────────────────────────────────────────────────────────
    "pymongo.errors.ConnectionFailure":    "MongoDB رابطہ ناکام",
    "pymongo.errors.ServerSelectionTimeoutError": "MongoDB سرور نہیں ملا",
    "pymongo.errors.DuplicateKeyError":    "MongoDB دوہری کلید",
    "pymongo.errors.OperationFailure":     "MongoDB آپریشن ناکام",
    "pymongo.errors.WriteError":           "MongoDB لکھنے کی غلطی",

    # ── ML / TensorFlow / Keras ───────────────────────────────────────────────
    "tensorflow.python.framework.errors_impl.InvalidArgumentError": "TF غلط دلیل",
    "tensorflow.python.framework.errors_impl.ResourceExhaustedError": "TF وسائل ختم",
    "tensorflow.python.framework.errors_impl.NotFoundError": "TF چیز نہیں ملی",
    "keras.src.errors.ValidationError":    "Keras تصدیق غلطی",

    # ── HTTP / Web ────────────────────────────────────────────────────────────
    "fastapi.HTTPException":    "HTTP غلطی",
    "starlette.exceptions.HTTPException": "HTTP غلطی",
    "requests.ConnectionError": "HTTP رابطہ غلطی",
    "requests.Timeout":         "HTTP وقت ختم",
    "requests.HTTPError":       "HTTP جواب غلطی",

    # ── DateTime ─────────────────────────────────────────────────────────────
    "datetime.ValueError":      "تاریخ/وقت قدر غلط",
}

# ── Message patterns (regex → Urdu template) ─────────────────────────────────
# Use named groups in the regex; reference them in the template as {name}.

_MSG_PATTERNS: list[tuple[str, str]] = [

    # ══ TypeError ═══════════════════════════════════════════════════════════════
    (r"unsupported operand type\(s\) for (?P<op>[^:]+): '(?P<t1>[^']+)' and '(?P<t2>[^']+)'",
     "آپریشن '{op}' قسم '{t1}' اور '{t2}' پر نہیں چل سکتا"),

    (r"'(?P<t>[^']+)' object is not callable",
     "قسم '{t}' کو فنکشن کی طرح نہیں بلایا جا سکتا"),

    (r"'(?P<t>[^']+)' object is not iterable",
     "قسم '{t}' قابل تکرار نہیں"),

    (r"'(?P<t>[^']+)' object is not subscriptable",
     "قسم '{t}' پر [] نہیں چل سکتا"),

    (r"'(?P<t>[^']+)' object has no attribute '(?P<a>[^']+)'",
     "قسم '{t}' میں خصوصیت '{a}' موجود نہیں"),

    (r"(?P<fn>\w+)\(\) takes (?P<exp>.+?) argument",
     "فنکشن '{fn}' کو مختلف تعداد میں دلائل چاہئیں"),

    (r"(?P<fn>\w+)\(\) missing (?P<n>\d+) required positional argument",
     "فنکشن '{fn}' کے لیے {n} لازمی دلیل غائب"),

    (r"(?P<fn>\w+)\(\) got an unexpected keyword argument '(?P<k>[^']+)'",
     "فنکشن '{fn}' کو نامعلوم کلیدی دلیل '{k}' ملی"),

    (r"(?P<fn>\w+)\(\) got multiple values for argument '(?P<k>[^']+)'",
     "فنکشن '{fn}' کو دلیل '{k}' ایک سے زیادہ بار ملی"),

    (r"can only concatenate (?P<t1>[^(]+) \(not \"(?P<t2>[^\"]+)\"\) to",
     "صرف '{t1}' کو '{t1}' سے جوڑا جا سکتا ہے، '{t2}' سے نہیں"),

    (r"'(?P<t>[^']+)' object cannot be interpreted as an integer",
     "قسم '{t}' کو عدد صحیح نہیں سمجھا جا سکتا"),

    (r"argument of type '(?P<t>[^']+)' is not iterable",
     "قسم '{t}' قابل تکرار نہیں"),

    (r"(?P<t>[^']+) indices must be integers or slices, not (?P<g>[^']+)",
     "'{t}' کا اشاریہ عدد صحیح یا سلائس ہونا چاہیے، '{g}' نہیں"),

    (r"string indices must be integers",
     "متن کا اشاریہ عدد صحیح ہونا چاہیے"),

    (r"a bytes-like object is required, not '(?P<t>[^']+)'",
     "بائٹس درکار ہیں، '{t}' نہیں"),

    (r"expected str, bytes or os.PathLike object, not (?P<t>\w+)",
     "متن یا راستہ درکار ہے، '{t}' نہیں"),

    # ══ ValueError ══════════════════════════════════════════════════════════════
    (r"invalid literal for int\(\) with base \d+: '(?P<v>[^']+)'",
     "'{v}' کو عدد صحیح میں تبدیل نہیں کیا جا سکتا"),

    (r"could not convert string to float: '(?P<v>[^']+)'",
     "'{v}' کو اعشاریہ عدد میں تبدیل نہیں کیا جا سکتا"),

    (r"too many values to unpack",
     "قدریں ضرورت سے زیادہ ہیں"),

    (r"not enough values to unpack",
     "قدریں ضرورت سے کم ہیں"),

    (r"math domain error",
     "ریاضیاتی قدر درست نہیں"),

    (r"math range error",
     "ریاضیاتی حد سے باہر"),

    (r"list\.remove\(x\): x not in list",
     "فہرست میں قدر موجود نہیں"),

    (r"(?P<t>day|month|year|hour|minute|second) is out of range",
     "'{t}' کی قدر حد سے باہر"),

    (r"day is out of range for month",
     "اس مہینے میں اتنے دن نہیں"),

    (r"month must be in 1\.\.12",
     "مہینہ 1 سے 12 کے درمیان ہونا چاہیے"),

    (r"time data '(?P<v>[^']+)' does not match format '(?P<f>[^']+)'",
     "تاریخ '{v}' نمونے '{f}' سے مطابقت نہیں"),

    (r"unconverted data remains: (?P<r>.+)",
     "تاریخ پارس کے بعد باقی ڈیٹا: {r}"),

    # ══ NameError ═══════════════════════════════════════════════════════════════
    (r"name '(?P<n>[^']+)' is not defined",
     "'{n}' متعین نہیں"),

    (r"free variable '(?P<n>[^']+)' referenced before assignment",
     "متغیر '{n}' تفویض سے پہلے استعمال ہوا"),

    (r"cannot access local variable '(?P<n>[^']+)' where it is not associated with a value",
     "متغیر '{n}' کو قدر ملنے سے پہلے استعمال نہیں کیا جا سکتا"),

    # ══ IndexError ══════════════════════════════════════════════════════════════
    (r"list index out of range",
     "فہرست کا اشاریہ حد سے باہر"),

    (r"string index out of range",
     "متن کا اشاریہ حد سے باہر"),

    (r"tuple index out of range",
     "ٹیپل کا اشاریہ حد سے باہر"),

    (r"bytearray index out of range",
     "بائٹ فہرست کا اشاریہ حد سے باہر"),

    # ══ KeyError ════════════════════════════════════════════════════════════════
    (r"^'(?P<k>[^']+)'$",
     "کلید '{k}' موجود نہیں"),

    # ══ ZeroDivisionError ═══════════════════════════════════════════════════════
    (r"division by zero",
     "صفر سے تقسیم ممنوع"),

    (r"modulo by zero",
     "صفر سے باقی ممنوع"),

    (r"float division by zero",
     "اعشاریہ صفر سے تقسیم ممنوع"),

    # ══ AttributeError ══════════════════════════════════════════════════════════
    (r"'(?P<t>[^']+)' object has no attribute '(?P<a>[^']+)'",
     "'{t}' میں '{a}' خصوصیت نہیں"),

    (r"module '(?P<m>[^']+)' has no attribute '(?P<a>[^']+)'",
     "ماڈول '{m}' میں '{a}' نہیں"),

    (r"type object '(?P<t>[^']+)' has no attribute '(?P<a>[^']+)'",
     "کلاس '{t}' میں '{a}' نہیں"),

    # ══ RecursionError ══════════════════════════════════════════════════════════
    (r"maximum recursion depth exceeded",
     "تکرار کی زیادہ سے زیادہ حد پار ہو گئی"),

    # ══ FileNotFoundError ═══════════════════════════════════════════════════════
    (r"\[Errno 2\] No such file or directory: '(?P<p>[^']+)'",
     "فائل یا فولڈر نہیں ملا: '{p}'"),

    (r"No such file or directory: '(?P<p>[^']+)'",
     "فائل یا فولڈر نہیں ملا: '{p}'"),

    # ══ PermissionError ═════════════════════════════════════════════════════════
    (r"\[Errno 13\] Permission denied: '(?P<p>[^']+)'",
     "اجازت نہیں: '{p}'"),

    # ══ ModuleNotFoundError ═════════════════════════════════════════════════════
    (r"No module named '(?P<m>[^']+)'",
     "ماڈول '{m}' نہیں ملا — pip install {m} چلائیں"),

    # ══ ImportError ═════════════════════════════════════════════════════════════
    (r"cannot import name '(?P<n>[^']+)' from '(?P<m>[^']+)'",
     "'{m}' سے '{n}' درآمد نہیں ہو سکتا"),

    # ══ OverflowError ═══════════════════════════════════════════════════════════
    (r"int too large to convert to float",
     "عدد بہت بڑا ہے"),

    (r"Result too large",
     "نتیجہ بہت بڑا ہے"),

    # ══ MemoryError ═════════════════════════════════════════════════════════════
    (r"^$",
     "یادداشت ناکافی"),

    # ══ TimeoutError / asyncio ══════════════════════════════════════════════════
    (r"timed? ?out",
     "وقت ختم ہو گیا"),

    # ══ Network ═════════════════════════════════════════════════════════════════
    (r"Connection refused",
     "رابطہ مسترد ہو گیا"),

    (r"\[Errno 111\] Connection refused",
     "رابطہ مسترد — سرور چل رہا ہے؟"),

    (r"\[Errno 61\] Connection refused",
     "رابطہ مسترد — سرور چل رہا ہے؟"),

    (r"Connection reset by peer",
     "دوسرے سرے نے رابطہ توڑ دیا"),

    (r"Network is unreachable",
     "نیٹ ورک دستیاب نہیں"),

    (r"Name or service not known",
     "ڈومین نام حل نہیں ہوا"),

    # ══ AsyncIO / Coroutine ══════════════════════════════════════════════════════
    (r"no running event loop",
     "کوئی ایونٹ لوپ نہیں چل رہا"),

    (r"coroutine '(?P<n>[^']+)' was never awaited",
     "کورٹین '{n}' کا انتظار نہیں کیا گیا"),

    (r"Task was destroyed but it is pending",
     "کام نامکمل ختم ہو گیا"),

    (r"Future is not done yet",
     "کام ابھی مکمل نہیں"),

    (r"Event loop is closed",
     "ایونٹ لوپ بند ہو گیا"),

    # ══ Database — Generic ══════════════════════════════════════════════════════
    (r"table \"?(?P<t>\w+)\"? (already exists|does not exist)",
     "جدول '{t}' پہلے سے موجود ہے / نہیں ملا"),

    (r"column \"?(?P<c>[^\"]+)\"? of relation \"?(?P<t>[^\"]+)\"? does not exist",
     "جدول '{t}' میں کالم '{c}' نہیں"),

    (r"relation \"?(?P<t>[^\"]+)\"? does not exist",
     "جدول/ویو '{t}' موجود نہیں"),

    (r"duplicate key value violates unique constraint \"?(?P<c>[^\"]+)\"?",
     "منفرد قید '{c}' کی خلاف ورزی — قدر پہلے سے موجود ہے"),

    (r"null value in column \"?(?P<c>[^\"]+)\"? of relation",
     "کالم '{c}' میں خالی قدر ممنوع"),

    (r"insert or update on table \"?(?P<t>[^\"]+)\"? violates foreign key constraint",
     "جدول '{t}' میں غیر ملکی کلید کی خلاف ورزی"),

    (r"value too long for type (?P<tp>.+)",
     "قدر قسم {tp} کے لیے بہت لمبی ہے"),

    (r"syntax error at or near \"(?P<t>[^\"]+)\"",
     "SQL نحوی غلطی: '{t}' کے قریب"),

    (r"column \"(?P<c>[^\"]+)\" does not exist",
     "کالم '{c}' موجود نہیں"),

    (r"permission denied for (table|relation) (?P<t>\w+)",
     "جدول '{t}' تک رسائی کی اجازت نہیں"),

    (r"password authentication failed for user \"(?P<u>[^\"]+)\"",
     "صارف '{u}' کے لیے پاس ورڈ غلط"),

    (r"database \"(?P<d>[^\"]+)\" does not exist",
     "ڈیٹا بیس '{d}' موجود نہیں"),

    (r"could not connect to server",
     "ڈیٹا بیس سرور سے رابطہ ناکام"),

    (r"SSL connection has been closed unexpectedly",
     "SSL رابطہ اچانک بند ہو گیا"),

    (r"Table '(?P<t>[^']+)' doesn't exist",
     "جدول '{t}' موجود نہیں"),

    (r"Unknown column '(?P<c>[^']+)' in '(?P<ctx>[^']+)'",
     "'{ctx}' میں کالم '{c}' نامعلوم"),

    (r"Duplicate entry '(?P<v>[^']+)' for key '(?P<k>[^']+)'",
     "کلید '{k}' کے لیے قدر '{v}' پہلے سے موجود"),

    (r"Data too long for column '(?P<c>[^']+)'",
     "کالم '{c}' کے لیے ڈیٹا بہت لمبا"),

    (r"Cannot add or update a child row: a foreign key constraint fails",
     "غیر ملکی کلید کی شرط پوری نہیں — والدین ریکارڈ نہیں ملا"),

    (r"UNIQUE constraint failed: (?P<t>.+)",
     "منفرد قید ناکام: {t}"),

    (r"NOT NULL constraint failed: (?P<c>.+)",
     "خالی قدر ممنوع: {c}"),

    (r"FOREIGN KEY constraint failed",
     "غیر ملکی کلید کی شرط ناکام"),

    # ══ MongoDB ══════════════════════════════════════════════════════════════════
    (r"E11000 duplicate key error collection: (?P<c>[^ ]+)",
     "MongoDB دوہری کلید: مجموعہ '{c}'"),

    (r"ServerSelectionTimeoutError",
     "MongoDB سرور نہیں ملا — کیا mongod چل رہا ہے؟"),

    # ══ DateTime ════════════════════════════════════════════════════════════════
    (r"year (?P<y>\d+) is out of range",
     "سال {y} درست نہیں"),

    (r"date value out of range",
     "تاریخ کی قدر حد سے باہر"),

    (r"strptime\(\) time data '(?P<v>[^']+)' does not match format '(?P<f>[^']+)'",
     "تاریخ '{v}' نمونے '{f}' سے مطابقت نہیں"),

    # ══ ML / Tensor ════════════════════════════════════════════════════════════
    (r"This model has not yet been built",
     "ماڈل ابھی بنا نہیں — پہلے build() کریں"),

    (r"Input (?P<n>\d+) of layer .+ is incompatible with the layer",
     "ماڈل کی ان پٹ {n} غیر موافق"),

    (r"Invalid input shape",
     "ان پٹ کی شکل غلط"),

    (r"Failed to convert a NumPy array to a Tensor",
     "NumPy سرنی کو Tensor میں تبدیل نہیں کیا جا سکا"),

    (r"CUDA out of memory",
     "GPU میموری ختم"),

    (r"No GPU\/CUDA found",
     "GPU نہیں ملا"),

    # ══ Web / HTTP ═══════════════════════════════════════════════════════════════
    (r"(?P<code>4\d{2}) (?P<msg>.+)",
     "HTTP {code}: {msg}"),

    (r"(?P<code>5\d{2}) (?P<msg>.+)",
     "سرور غلطی {code}: {msg}"),

    # ══ JSON ════════════════════════════════════════════════════════════════════
    (r"Expecting value: line (?P<l>\d+) column (?P<c>\d+)",
     "JSON میں قدر غائب: سطر {l}، خانہ {c}"),

    (r"Expecting property name enclosed in double quotes",
     "JSON خصوصیت کا نام ڈبل اقتباس میں ہونا چاہیے"),

    (r"Object of type (?P<t>\w+) is not JSON serializable",
     "قسم '{t}' کو JSON میں تبدیل نہیں کیا جا سکتا"),

    # ══ Crypto ══════════════════════════════════════════════════════════════════
    (r"Invalid key size",
     "کلید کا حجم غلط"),

    (r"Invalid token",
     "ٹوکن غلط یا میعاد ختم"),

    (r"Fernet key must be 32 url-safe base64-encoded bytes",
     "خفیہ کاری کلید 32 بائٹ ہونی چاہیے"),

    # ══ General ════════════════════════════════════════════════════════════════
    (r"maximum recursion depth exceeded in comparison",
     "موازنہ میں تکرار کی حد پار"),

    (r"unhashable type: '(?P<t>[^']+)'",
     "قسم '{t}' ہیش نہیں ہو سکتی"),

    (r"object of type '(?P<t>[^']+)' has no len\(\)",
     "قسم '{t}' کی لمبائی نہیں"),

    (r"pop from empty (?P<t>list|set|dict)",
     "خالی {t} سے نہیں نکال سکتے"),

    (r"(?P<fn>min|max)\(\) arg is an empty sequence",
     "{fn}() کے لیے فہرست خالی ہے"),

    (r"division by zero",
     "صفر سے تقسیم ممنوع"),
]

# Pre-compile patterns for speed
_COMPILED: list[tuple[re.Pattern, str]] = [
    (re.compile(pat, re.IGNORECASE), tmpl)
    for pat, tmpl in _MSG_PATTERNS
]


def _translate_message(msg: str) -> str | None:
    for pattern, template in _COMPILED:
        m = pattern.search(msg)
        if m:
            try:
                return template.format(**m.groupdict())
            except KeyError:
                return template
    return None


def translate_error(e: Exception) -> tuple[str | None, str | None]:
    """Return (urdu_type, urdu_message).  Either may be None if untranslatable."""
    # Try fully-qualified name first (e.g. psycopg2.OperationalError)
    cls = type(e)
    fqn = f"{cls.__module__}.{cls.__name__}" if cls.__module__ not in ("builtins", "__main__") else cls.__name__
    urdu_type = TYPE_MAP.get(fqn) or TYPE_MAP.get(cls.__name__)
    urdu_msg  = _translate_message(str(e))
    return urdu_type, urdu_msg
