"""
Cryptography library for the Urdu Programming Language.
Wraps: hashlib, hmac, secrets, cryptography (Fernet, RSA, AES-GCM), bcrypt, base64.

Usage from Urdu:
    درآمد { ہیش, متناسق, غیر_متناسق, پاس_ورڈ, محفوظ, بنیاد64, AES } سے "اردو/رمز";
"""

from __future__ import annotations
import hashlib
import hmac as _hmac
import secrets
import base64


# ─── Hash ─────────────────────────────────────────────────────────────────────

class ہیش:
    """Cryptographic hashing utilities (hashlib + hmac)."""

    @staticmethod
    def sha256(data: str | bytes) -> str:
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def sha512(data: str | bytes) -> str:
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha512(data).hexdigest()

    @staticmethod
    def md5(data: str | bytes) -> str:
        if isinstance(data, str):
            data = data.encode()
        return hashlib.md5(data).hexdigest()

    @staticmethod
    def blake2b(data: str | bytes, *, digest_size: int = 32) -> str:
        if isinstance(data, str):
            data = data.encode()
        return hashlib.blake2b(data, digest_size=digest_size).hexdigest()

    @staticmethod
    def hmac(data: str | bytes, key: str | bytes, *, الگورتھم: str = "sha256") -> str:
        if isinstance(data, str):
            data = data.encode()
        if isinstance(key, str):
            key = key.encode()
        algo = getattr(hashlib, الگورتھم, None)
        if algo is None:
            raise ValueError(f"نامعلوم الگورتھم: {الگورتھم}")
        return _hmac.new(key, data, algo).hexdigest()

    @staticmethod
    def pbkdf2(پاس_ورڈ: str, نمک: str | bytes, *, دور: int = 100_000, طول: int = 32) -> str:
        if isinstance(نمک, str):
            نمک = نمک.encode()
        dk = hashlib.pbkdf2_hmac("sha256", پاس_ورڈ.encode(), نمک, دور, طول)
        return dk.hex()

    # اردو عرفیات
    ہیش_256     = sha256
    ہیش_512     = sha512
    ایم_ڈی_5    = md5
    بلیک_2بی    = blake2b
    ہمیک        = hmac
    کلید_استخراج = pbkdf2


# ─── Symmetric Encryption (Fernet / AES-128-CBC + HMAC-SHA256) ───────────────

class متناسق:
    """Symmetric encryption using Fernet (AES-128-CBC + HMAC-SHA256)."""

    def __init__(self, کلید: str | bytes = None):
        try:
            from cryptography.fernet import Fernet
        except ImportError:
            raise ImportError("pip install cryptography")
        if کلید is None:
            self._key = Fernet.generate_key()
        elif isinstance(کلید, str):
            self._key = کلید.encode()
        else:
            self._key = کلید
        from cryptography.fernet import Fernet as _F
        self._fernet = _F(self._key)

    def خفیہ_کریں(self, پیغام: str | bytes) -> str:
        if isinstance(پیغام, str):
            پیغام = پیغام.encode()
        return self._fernet.encrypt(پیغام).decode()

    def ظاہر_کریں(self, خفیہ_متن: str | bytes) -> str:
        if isinstance(خفیہ_متن, str):
            خفیہ_متن = خفیہ_متن.encode()
        return self._fernet.decrypt(خفیہ_متن).decode()

    @property
    def کلید(self) -> str:
        return self._key.decode() if isinstance(self._key, bytes) else self._key

    @staticmethod
    def نئی_کلید() -> str:
        from cryptography.fernet import Fernet
        return Fernet.generate_key().decode()


# ─── AES-256-GCM ─────────────────────────────────────────────────────────────

class AES:
    """AES-256-GCM authenticated encryption (nonce prepended to ciphertext)."""

    def __init__(self, کلید: str | bytes = None):
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        except ImportError:
            raise ImportError("pip install cryptography")
        if کلید is None:
            self._key = secrets.token_bytes(32)
        elif isinstance(کلید, str):
            raw = کلید.encode()
            self._key = raw[:32].ljust(32, b'\0')
        else:
            self._key = کلید

    def خفیہ_کریں(self, پیغام: str, *, اضافی: bytes = None) -> str:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        nonce = secrets.token_bytes(12)
        ct = AESGCM(self._key).encrypt(nonce, پیغام.encode(), اضافی)
        return base64.b64encode(nonce + ct).decode()

    def ظاہر_کریں(self, خفیہ_متن: str, *, اضافی: bytes = None) -> str:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        raw = base64.b64decode(خفیہ_متن)
        nonce, ct = raw[:12], raw[12:]
        return AESGCM(self._key).decrypt(nonce, ct, اضافی).decode()

    @property
    def کلید(self) -> str:
        return base64.b64encode(self._key).decode()


# ─── Asymmetric Encryption (RSA) ─────────────────────────────────────────────

class غیر_متناسق:
    """RSA asymmetric encryption and digital signing."""

    def __init__(self, بٹس: int = 2048):
        try:
            from cryptography.hazmat.primitives.asymmetric import rsa as _rsa
            from cryptography.hazmat.backends import default_backend
        except ImportError:
            raise ImportError("pip install cryptography")
        from cryptography.hazmat.primitives.asymmetric import rsa as _rsa
        from cryptography.hazmat.backends import default_backend
        self._private = _rsa.generate_private_key(
            public_exponent=65537,
            key_size=بٹس,
            backend=default_backend(),
        )
        self._public = self._private.public_key()

    def عوامی_کلید(self) -> str:
        from cryptography.hazmat.primitives import serialization
        return self._public.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

    def نجی_کلید(self) -> str:
        from cryptography.hazmat.primitives import serialization
        return self._private.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ).decode()

    def خفیہ_کریں(self, پیغام: str) -> str:
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives import hashes
        ct = self._public.encrypt(
            پیغام.encode(),
            padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
        )
        return base64.b64encode(ct).decode()

    def ظاہر_کریں(self, خفیہ_متن: str) -> str:
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives import hashes
        ct = base64.b64decode(خفیہ_متن)
        return self._private.decrypt(
            ct,
            padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
        ).decode()

    def دستخط(self, پیغام: str) -> str:
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives import hashes
        sig = self._private.sign(
            پیغام.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return base64.b64encode(sig).decode()

    def تصدیق(self, پیغام: str, دستخط: str) -> bool:
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives import hashes
        from cryptography.exceptions import InvalidSignature
        try:
            self._public.verify(
                base64.b64decode(دستخط),
                پیغام.encode(),
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256(),
            )
            return True
        except InvalidSignature:
            return False


# ─── Password Hashing (bcrypt) ───────────────────────────────────────────────

class پاس_ورڈ:
    """Secure password hashing using bcrypt."""

    @staticmethod
    def ہیش(پاس_ورڈ_متن: str, *, چکر: int = 12) -> str:
        try:
            import bcrypt
        except ImportError:
            raise ImportError("pip install bcrypt")
        salt = bcrypt.gensalt(rounds=چکر)
        return bcrypt.hashpw(پاس_ورڈ_متن.encode(), salt).decode()

    @staticmethod
    def جانچیں(پاس_ورڈ_متن: str, ہیش_شدہ: str) -> bool:
        try:
            import bcrypt
        except ImportError:
            raise ImportError("pip install bcrypt")
        return bcrypt.checkpw(پاس_ورڈ_متن.encode(), ہیش_شدہ.encode())


# ─── Secure Random (secrets) ─────────────────────────────────────────────────

class تصادفی:
    """Cryptographically secure random generation (secrets module)."""

    @staticmethod
    def ٹوکن(لمبائی: int = 32) -> str:
        return secrets.token_hex(لمبائی)

    @staticmethod
    def ٹوکن_url(لمبائی: int = 32) -> str:
        return secrets.token_urlsafe(لمبائی)

    @staticmethod
    def بائٹ(تعداد: int = 32) -> bytes:
        return secrets.token_bytes(تعداد)

    @staticmethod
    def عدد(کم: int, زیادہ: int) -> int:
        return secrets.randbelow(زیادہ - کم) + کم

    @staticmethod
    def انتخاب(فہرست: list):
        return secrets.choice(فہرست)

    @staticmethod
    def OTP(ہندسے: int = 6) -> str:
        return str(secrets.randbelow(10 ** ہندسے)).zfill(ہندسے)

    یک_وقتی_پاس_ورڈ = OTP

# backward-compat alias (avoid using keyword محفوظ in Urdu code)
محفوظ_اعداد = تصادفی


# ─── Base64 ──────────────────────────────────────────────────────────────────

class بنیاد64:
    """Base64 encoding and decoding (standard and URL-safe)."""

    @staticmethod
    def کوڈ(data: str | bytes) -> str:
        if isinstance(data, str):
            data = data.encode()
        return base64.b64encode(data).decode()

    @staticmethod
    def ڈی_کوڈ(data: str | bytes) -> str:
        if isinstance(data, bytes):
            data = data.decode()
        return base64.b64decode(data).decode()

    @staticmethod
    def url_کوڈ(data: str | bytes) -> str:
        if isinstance(data, str):
            data = data.encode()
        return base64.urlsafe_b64encode(data).decode()

    @staticmethod
    def url_ڈی_کوڈ(data: str | bytes) -> str:
        if isinstance(data, bytes):
            data = data.decode()
        return base64.urlsafe_b64decode(data).decode()

    # اردو عرفیات
    ربط_کوڈ   = url_کوڈ
    ربط_ڈی_کوڈ = url_ڈی_کوڈ


# ─── اردو عرفیات ─────────────────────────────────────────────────────────────

اے_ای_ایس = AES


# ─── Exports ─────────────────────────────────────────────────────────────────

__all__ = [
    "ہیش", "متناسق",
    "AES", "اے_ای_ایس",
    "غیر_متناسق",
    "پاس_ورڈ", "تصادفی", "محفوظ_اعداد", "بنیاد64",
]
