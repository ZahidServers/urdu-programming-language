"""
Database library for the Urdu Programming Language.
Supports: MySQL, PostgreSQL, MongoDB, Firebase/Firestore, Cassandra, SQLite.

Usage from Urdu:
    درآمد { MySQL, PostgreSQL, MongoDB } سے "اردو/ڈیٹا_بیس";
"""

from __future__ import annotations
import asyncio
from typing import Any, Optional
from .builtins import _UrduObj


def _wrap_row(row: dict) -> _UrduObj:
    """Wrap a database result row in _UrduObj for dot-access."""
    return _UrduObj(row)


# ─── Base connection ─────────────────────────────────────────────────────────

class _UrduDB:
    """Base class for all database connections."""

    def __init__(self, config: dict):
        self._config = config
        self._conn = None
        self._connected = False
        self._in_transaction = False

    async def جوڑیں(self):
        raise NotImplementedError

    async def منقطع(self):
        raise NotImplementedError

    async def سوال(self, query: str, params=None) -> list[dict]:
        raise NotImplementedError

    async def چلائیں(self, query: str, params=None) -> int:
        raise NotImplementedError

    # ── Transaction API (shared stubs; overridden per class) ──────────────────

    async def لین_دین_شروع(self):
        """BEGIN a transaction."""
        raise NotImplementedError

    async def کمٹ(self):
        """COMMIT the current transaction."""
        raise NotImplementedError

    async def واپسی(self):
        """ROLLBACK the current transaction."""
        raise NotImplementedError

    async def نقطہ_محفوظ(self, نام: str):
        """SAVEPOINT name"""
        raise NotImplementedError

    async def نقطہ_واپسی(self, نام: str):
        """ROLLBACK TO SAVEPOINT name"""
        raise NotImplementedError

    async def نقطہ_چھوڑیں(self, نام: str):
        """RELEASE SAVEPOINT name"""
        raise NotImplementedError

    async def لین_دین(self, callback):
        """Run callback inside a transaction; auto-commit or rollback."""
        await self.لین_دین_شروع()
        try:
            await callback()
            await self.کمٹ()
        except Exception:
            await self.واپسی()
            raise

    def __repr__(self):
        return f"{type(self).__name__}(host={self._config.get('میزبان', '?')})"


# ─── MySQL ────────────────────────────────────────────────────────────────────

class مائی_ایس_کیو_ایل(_UrduDB):
    """MySQL connection using mysql-connector-python."""

    def __init__(self, config: dict):
        super().__init__(config)

    async def جوڑیں(self):
        try:
            import mysql.connector
        except ImportError:
            raise ImportError("MySQL کے لیے چلائیں: pip install mysql-connector-python")

        kwargs = dict(
            host=self._config.get("میزبان", "localhost"),
            user=self._config.get("صارف", "root"),
            password=self._config.get("پاس_ورڈ", ""),
            port=self._config.get("پورٹ", 3306),
            use_pure=True,      # avoids C-extension crash on some platforms
            charset="utf8mb4",  # required for Urdu/Arabic column names
            autocommit=True,    # each statement auto-commits; explicit BEGIN for transactions
        )
        db_name = self._config.get("ڈیٹا_بیس", "")
        if db_name:
            kwargs["database"] = db_name
        self._conn = mysql.connector.connect(**kwargs)
        self._conn.set_charset_collation("utf8mb4", "utf8mb4_unicode_ci")
        # Default to InnoDB for transaction support; allow override via config
        engine = self._config.get("انجن", self._config.get("engine", "InnoDB"))
        self._conn.cursor().execute(f"SET default_storage_engine = {engine}")
        self._connected = True
        return self

    @staticmethod
    def _q(query: str) -> str:
        """Convert SQLite-style ? placeholders to MySQL %s."""
        return query.replace("?", "%s")

    async def سوال(self, query: str, params=None) -> list[dict]:
        if not self._connected:
            await self.جوڑیں()
        cursor = self._conn.cursor(dictionary=True)
        cursor.execute(self._q(query), params or ())
        return [_wrap_row(row) for row in cursor.fetchall()]

    async def چلائیں(self, query: str, params=None) -> int:
        if not self._connected:
            await self.جوڑیں()
        cursor = self._conn.cursor()
        cursor.execute(self._q(query), params or ())
        # autocommit=True handles commit automatically outside transactions
        return cursor.rowcount

    async def داخل(self, جدول: str, ڈیٹا: dict) -> int:
        cols = ", ".join(ڈیٹا.keys())
        vals = ", ".join(["%s"] * len(ڈیٹا))
        q = f"INSERT INTO {جدول} ({cols}) VALUES ({vals})"
        return await self.چلائیں(q, list(ڈیٹا.values()))

    # ── Transactions ──────────────────────────────────────────────────────────

    async def لین_دین_شروع(self):
        if not self._connected:
            await self.جوڑیں()
        # Explicit BEGIN disables autocommit for this transaction block
        self._conn.cursor().execute("BEGIN")
        self._in_transaction = True

    async def کمٹ(self):
        self._conn.cursor().execute("COMMIT")
        self._in_transaction = False

    async def واپسی(self):
        self._conn.cursor().execute("ROLLBACK")
        self._in_transaction = False

    async def نقطہ_محفوظ(self, نام: str):
        self._conn.cursor().execute(f"SAVEPOINT {نام}")

    async def نقطہ_واپسی(self, نام: str):
        self._conn.cursor().execute(f"ROLLBACK TO SAVEPOINT {نام}")

    async def نقطہ_چھوڑیں(self, نام: str):
        self._conn.cursor().execute(f"RELEASE SAVEPOINT {نام}")

    async def منقطع(self):
        if self._conn:
            if self._in_transaction:
                self._conn.rollback()
            self._conn.close()
            self._connected = False


# ─── PostgreSQL ───────────────────────────────────────────────────────────────

class پوسٹ_گریس(_UrduDB):
    """PostgreSQL connection using psycopg2."""

    def __init__(self, config: dict):
        super().__init__(config)

    async def جوڑیں(self):
        try:
            import psycopg2
            import psycopg2.extras
        except ImportError:
            raise ImportError("PostgreSQL کے لیے چلائیں: pip install psycopg2-binary")

        kwargs = dict(
            host=self._config.get("میزبان", "localhost"),
            user=self._config.get("صارف", "postgres"),
            password=self._config.get("پاس_ورڈ", ""),
            port=self._config.get("پورٹ", 5432),
            dbname=self._config.get("ڈیٹا_بیس", "postgres"),
        )
        self._conn = psycopg2.connect(**kwargs)
        self._conn.autocommit = False
        # Ensure UTF-8 encoding for Urdu text
        self._conn.cursor().execute("SET client_encoding TO 'UTF8'")
        self._conn.commit()
        self._connected = True
        return self

    @staticmethod
    def _q(query: str) -> str:
        """Convert ? placeholders to psycopg2-style %s."""
        return query.replace("?", "%s")

    async def سوال(self, query: str, params=None) -> list[dict]:
        if not self._connected:
            await self.جوڑیں()
        import psycopg2.extras
        cursor = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(self._q(query), params or ())
        rows = [_wrap_row(dict(row)) for row in cursor.fetchall()]
        if not self._in_transaction:
            self._conn.commit()
        return rows

    async def چلائیں(self, query: str, params=None) -> int:
        if not self._connected:
            await self.جوڑیں()
        cursor = self._conn.cursor()
        cursor.execute(self._q(query), params or ())
        rowcount = cursor.rowcount
        if not self._in_transaction:
            self._conn.commit()
        return rowcount

    async def داخل(self, جدول: str, ڈیٹا: dict) -> int:
        cols = ", ".join(ڈیٹا.keys())
        vals = ", ".join(["%s"] * len(ڈیٹا))
        q = f"INSERT INTO {جدول} ({cols}) VALUES ({vals})"
        return await self.چلائیں(q, list(ڈیٹا.values()))

    async def آخری_شناخت(self, جدول: str, کالم: str = "شناخت") -> int:
        rows = await self.سوال(f"SELECT currval(pg_get_serial_sequence('{جدول}', '{کالم}'))")
        return rows[0]["currval"] if rows else None

    # ── Transactions ──────────────────────────────────────────────────────────

    async def لین_دین_شروع(self):
        if not self._connected:
            await self.جوڑیں()
        self._conn.cursor().execute("BEGIN")
        self._in_transaction = True

    async def کمٹ(self):
        self._conn.commit()
        self._in_transaction = False

    async def واپسی(self):
        self._conn.rollback()
        self._in_transaction = False

    async def نقطہ_محفوظ(self, نام: str):
        self._conn.cursor().execute(f"SAVEPOINT {نام}")

    async def نقطہ_واپسی(self, نام: str):
        self._conn.cursor().execute(f"ROLLBACK TO SAVEPOINT {نام}")

    async def نقطہ_چھوڑیں(self, نام: str):
        self._conn.cursor().execute(f"RELEASE SAVEPOINT {نام}")

    async def منقطع(self):
        if self._conn:
            if self._in_transaction:
                self._conn.rollback()
            self._conn.close()
            self._connected = False


# ─── SQLite (built-in) ───────────────────────────────────────────────────────

class ایس_کیو_لائٹ(_UrduDB):
    """SQLite connection (no extra install needed)."""

    def __init__(self, config: dict | str):
        if isinstance(config, str):
            config = {"فائل": config}
        super().__init__(config)

    async def جوڑیں(self):
        import sqlite3
        path = self._config.get("فائل", ":memory:")
        self._conn = sqlite3.connect(path, isolation_level=None)  # manual transaction mode
        self._conn.row_factory = sqlite3.Row
        self._connected = True
        return self

    async def سوال(self, query: str, params=None) -> list[dict]:
        if not self._connected:
            await self.جوڑیں()
        cursor = self._conn.cursor()
        cursor.execute(query, params or ())
        return [_wrap_row(dict(row)) for row in cursor.fetchall()]

    async def چلائیں(self, query: str, params=None) -> int:
        if not self._connected:
            await self.جوڑیں()
        cursor = self._conn.cursor()
        if not self._in_transaction:
            # auto-wrap in a transaction so changes are durable
            cursor.execute("BEGIN")
        cursor.execute(query, params or ())
        if not self._in_transaction:
            self._conn.commit()
        return cursor.rowcount

    async def لین_دین_شروع(self):
        if not self._connected:
            await self.جوڑیں()
        self._conn.execute("BEGIN")
        self._in_transaction = True

    async def کمٹ(self):
        self._conn.commit()
        self._in_transaction = False

    async def واپسی(self):
        self._conn.rollback()
        self._in_transaction = False

    async def نقطہ_محفوظ(self, نام: str):
        self._conn.execute(f"SAVEPOINT {نام}")

    async def نقطہ_واپسی(self, نام: str):
        self._conn.execute(f"ROLLBACK TO SAVEPOINT {نام}")

    async def نقطہ_چھوڑیں(self, نام: str):
        self._conn.execute(f"RELEASE SAVEPOINT {نام}")

    async def منقطع(self):
        if self._conn:
            if self._in_transaction:
                self._conn.rollback()
            self._conn.close()
            self._connected = False

    async def جدول_بنائیں(self, نام: str, کالمیں: dict) -> bool:
        cols_def = ", ".join(f"{k} {v}" for k, v in کالمیں.items())
        await self.چلائیں(f"CREATE TABLE IF NOT EXISTS {نام} ({cols_def})")
        return True


# ─── MongoDB ─────────────────────────────────────────────────────────────────

class مونگو_ڈی_بی(_UrduDB):
    """MongoDB connection using pymongo."""

    def __init__(self, config: dict):
        super().__init__(config)
        self._db = None
        self._session = None

    async def جوڑیں(self):
        try:
            from pymongo import MongoClient
        except ImportError:
            raise ImportError("MongoDB کے لیے چلائیں: pip install pymongo")

        uri = self._config.get("uri") or (
            f"mongodb://{self._config.get('میزبان', 'localhost')}:"
            f"{self._config.get('پورٹ', 27017)}"
        )
        self._client = MongoClient(uri)
        self._db = self._client[self._config.get("ڈیٹا_بیس", "test")]
        self._connected = True
        return self

    def مجموعہ(self, نام: str) -> "_MongoCollection":
        if not self._connected:
            raise RuntimeError("پہلے جوڑیں() کریں")
        return _MongoCollection(self._db[نام], self)

    # ── Transactions (requires MongoDB replica set) ───────────────────────────

    async def لین_دین_شروع(self):
        self._session = self._client.start_session()
        self._session.start_transaction()
        self._in_transaction = True

    async def کمٹ(self):
        if self._session:
            self._session.commit_transaction()
            self._session.end_session()
            self._session = None
        self._in_transaction = False

    async def واپسی(self):
        if self._session:
            self._session.abort_transaction()
            self._session.end_session()
            self._session = None
        self._in_transaction = False

    async def لین_دین(self, callback):
        """Run callback inside a MongoDB transaction (requires replica set)."""
        await self.لین_دین_شروع()
        try:
            await callback()
            await self.کمٹ()
        except Exception:
            await self.واپسی()
            raise

    async def منقطع(self):
        if self._in_transaction and self._session:
            self._session.abort_transaction()
            self._session.end_session()
        if hasattr(self, "_client"):
            self._client.close()
            self._connected = False


class _MongoCollection:
    def __init__(self, col, db: مونگو_ڈی_بی = None):
        self._col = col
        self._db = db  # reference to parent MongoDB for session access

    def _sess(self):
        return self._db._session if self._db and self._db._in_transaction else None

    async def تلاش(self, فلٹر: dict = None, اختیارات: dict = None, *, حد: int = 0) -> list[dict]:
        if اختیارات:
            حد = اختیارات.get("حد", حد)
        kw = {}
        if self._sess():
            kw["session"] = self._sess()
        cursor = self._col.find(فلٹر or {}, **kw)
        if حد:
            cursor = cursor.limit(حد)
        return [_wrap_row(dict(row)) for row in cursor]

    async def ایک_تلاش(self, فلٹر: dict) -> Optional[dict]:
        kw = {}
        if self._sess():
            kw["session"] = self._sess()
        row = self._col.find_one(فلٹر, **kw)
        return _wrap_row(dict(row)) if row else None

    async def داخل(self, دستاویز: dict) -> str:
        kw = {}
        if self._sess():
            kw["session"] = self._sess()
        result = self._col.insert_one(دستاویز, **kw)
        return str(result.inserted_id)

    async def بہت_داخل(self, دستاویزات: list) -> list:
        kw = {}
        if self._sess():
            kw["session"] = self._sess()
        result = self._col.insert_many(دستاویزات, **kw)
        return [str(i) for i in result.inserted_ids]

    async def تازہ_کاری(self, فلٹر: dict, تازہ_قدر: dict) -> int:
        kw = {}
        if self._sess():
            kw["session"] = self._sess()
        result = self._col.update_many(فلٹر, {"$set": تازہ_قدر}, **kw)
        return result.modified_count

    async def حذف(self, فلٹر: dict) -> int:
        kw = {}
        if self._sess():
            kw["session"] = self._sess()
        result = self._col.delete_many(فلٹر, **kw)
        return result.deleted_count

    async def گنتی(self, فلٹر: dict = None) -> int:
        kw = {}
        if self._sess():
            kw["session"] = self._sess()
        return self._col.count_documents(فلٹر or {}, **kw)


# ─── Firebase / Firestore ────────────────────────────────────────────────────

class فائر_بیس(_UrduDB):
    """Firebase/Firestore — admin SDK mode (اسناد key) or web/REST mode (apiKey)."""

    _AUTH = "https://identitytoolkit.googleapis.com/v1/accounts"

    def __init__(self, config: dict):
        super().__init__(config)
        self._mode = "web" if ("apiKey" in config or "apiکلید" in config) else "admin"
        if self._mode == "web":
            self._api_key     = config.get("apiKey") or config.get("apiکلید", "")
            self._project_id  = config.get("projectId") or config.get("منصوبہ", "")
            self._rtdb_url    = (config.get("databaseURL") or config.get("ڈیٹا_بیس_url", "")).rstrip("/")
            self._id_token    = None
            self._refresh_token = None
            self._local_id    = None

    # ── Connection ────────────────────────────────────────────────────────────

    async def جوڑیں(self):
        if self._mode == "web":
            self._connected = True
            return self
        # admin mode
        try:
            import firebase_admin
        except ImportError:
            raise ImportError("Firebase کے لیے چلائیں: pip install firebase-admin")

        cred_path = self._config.get("اسناد", "serviceAccountKey.json")
        options: dict = {}
        db_url = self._config.get("databaseURL") or self._config.get("ڈیٹا_بیس_url", "")
        if db_url:
            options["databaseURL"] = db_url
        proj = self._config.get("منصوبہ") or self._config.get("projectId", "")
        if proj:
            options["projectId"] = proj

        if not firebase_admin._apps:
            cred = firebase_admin.credentials.Certificate(cred_path)
            self._app = firebase_admin.initialize_app(cred, options)
        else:
            self._app = firebase_admin.get_app()

        from firebase_admin import firestore as fs
        self._db = fs.client(app=self._app)
        self._connected = True
        return self

    async def منقطع(self):
        self._connected = False

    # ── Admin Auth management ─────────────────────────────────────────────────

    async def ایڈمن_صارف_بنائیں(self, ای_میل: str, پاس_ورڈ: str,
                                  نام: str = None, فون: str = None) -> dict:
        from firebase_admin import auth
        kwargs = {"email": ای_میل, "password": پاس_ورڈ}
        if نام:
            kwargs["display_name"] = نام
        if فون:
            kwargs["phone_number"] = فون
        user = auth.create_user(**kwargs)
        return _wrap_row({
            "uid": user.uid, "email": user.email,
            "displayName": user.display_name, "phoneNumber": user.phone_number,
        })

    async def ایڈمن_صارف_حاصل(self, uid: str) -> dict:
        from firebase_admin import auth
        user = auth.get_user(uid)
        return _wrap_row({
            "uid": user.uid, "email": user.email,
            "displayName": user.display_name, "emailVerified": user.email_verified,
            "disabled": user.disabled,
        })

    async def ایڈمن_صارف_ای_میل(self, ای_میل: str) -> dict:
        from firebase_admin import auth
        user = auth.get_user_by_email(ای_میل)
        return _wrap_row({
            "uid": user.uid, "email": user.email,
            "displayName": user.display_name, "emailVerified": user.email_verified,
        })

    async def ایڈمن_صارف_تازہ(self, uid: str, **kwargs) -> dict:
        from firebase_admin import auth
        user = auth.update_user(uid, **kwargs)
        return _wrap_row({"uid": user.uid, "displayName": user.display_name})

    async def ایڈمن_ٹوکن_تصدیق(self, id_token: str) -> dict:
        from firebase_admin import auth
        decoded = auth.verify_id_token(id_token)
        return _wrap_row(decoded)

    async def ایڈمن_کسٹم_ٹوکن(self, uid: str, claims: dict = None) -> str:
        from firebase_admin import auth
        token = auth.create_custom_token(uid, claims or {})
        return token.decode("utf-8") if isinstance(token, bytes) else token

    async def ایڈمن_دعوے_مقرر(self, uid: str, دعوے: dict) -> None:
        from firebase_admin import auth
        auth.set_custom_user_claims(uid, دعوے)

    async def ایڈمن_صارف_حذف(self, uid: str) -> None:
        from firebase_admin import auth
        auth.delete_user(uid)

    async def ایڈمن_صارفین_فہرست(self, حد: int = 10) -> list:
        from firebase_admin import auth
        page = auth.list_users()
        users = []
        for user in page.users[:حد]:
            users.append(_wrap_row({
                "uid": user.uid, "email": user.email,
                "displayName": user.display_name,
            }))
        return users

    # ── Admin Realtime Database ───────────────────────────────────────────────

    def _admin_rtdb_ref(self, path: str):
        from firebase_admin import db as rtdb
        return rtdb.reference(path.lstrip("/"), app=self._app)

    async def ریئل_لکھو(self, راستہ: str, ڈیٹا):
        if self._mode == "admin":
            self._admin_rtdb_ref(راستہ).set(ڈیٹا)
            return ڈیٹا
        return self._rtdb("put", راستہ, ڈیٹا)

    async def ریئل_شامل(self, راستہ: str, ڈیٹا) -> str:
        if self._mode == "admin":
            ref = self._admin_rtdb_ref(راستہ).push(ڈیٹا)
            return ref.key
        result = self._rtdb("post", راستہ, ڈیٹا)
        return result.get("name", "") if isinstance(result, dict) else str(result)

    async def ریئل_پڑھو(self, راستہ: str):
        if self._mode == "admin":
            return self._admin_rtdb_ref(راستہ).get()
        return self._rtdb("get", راستہ)

    async def ریئل_تازہ(self, راستہ: str, ڈیٹا: dict):
        if self._mode == "admin":
            self._admin_rtdb_ref(راستہ).update(ڈیٹا)
            return ڈیٹا
        return self._rtdb("patch", راستہ, ڈیٹا)

    async def ریئل_حذف(self, راستہ: str) -> None:
        if self._mode == "admin":
            self._admin_rtdb_ref(راستہ).delete()
            return
        self._rtdb("delete", راستہ)

    # ── Email Auth (web mode) ─────────────────────────────────────────────────

    async def ای_میل_رجسٹر(self, ای_میل: str, پاس_ورڈ: str) -> dict:
        import requests as _req
        r = _req.post(f"{self._AUTH}:signUp?key={self._api_key}",
                      json={"email": ای_میل, "password": پاس_ورڈ, "returnSecureToken": True},
                      timeout=10)
        data = r.json()
        if "error" in data:
            raise Exception(data["error"]["message"])
        self._id_token = data["idToken"]
        self._refresh_token = data.get("refreshToken")
        self._local_id = data.get("localId")
        self._connected = True
        return _wrap_row(data)

    async def ای_میل_داخل(self, ای_میل: str, پاس_ورڈ: str) -> dict:
        import requests as _req
        r = _req.post(f"{self._AUTH}:signInWithPassword?key={self._api_key}",
                      json={"email": ای_میل, "password": پاس_ورڈ, "returnSecureToken": True},
                      timeout=10)
        data = r.json()
        if "error" in data:
            raise Exception(data["error"]["message"])
        self._id_token = data["idToken"]
        self._refresh_token = data.get("refreshToken")
        self._local_id = data.get("localId")
        self._connected = True
        return _wrap_row(data)

    async def صارف_معلومات(self) -> dict:
        import requests as _req
        r = _req.post(f"{self._AUTH}:lookup?key={self._api_key}",
                      json={"idToken": self._id_token}, timeout=10)
        data = r.json()
        if "error" in data:
            raise Exception(data["error"]["message"])
        users = data.get("users", [])
        return _wrap_row(users[0]) if users else _wrap_row({})

    async def صارف_حذف(self) -> None:
        import requests as _req
        r = _req.post(f"{self._AUTH}:delete?key={self._api_key}",
                      json={"idToken": self._id_token}, timeout=10)
        data = r.json()
        if "error" in data:
            raise Exception(data["error"]["message"])
        self._id_token = None
        self._local_id = None

    # ── Phone Auth (web mode) ─────────────────────────────────────────────────

    async def فون_کوڈ_بھیجو(self, فون: str) -> str:
        """Send phone OTP. Returns sessionInfo. Works with Firebase Console test numbers."""
        import requests as _req
        r = _req.post(f"{self._AUTH}:sendVerificationCode?key={self._api_key}",
                      json={"phoneNumber": فون, "recaptchaToken": "test"},
                      timeout=10)
        data = r.json()
        if "error" in data:
            raise Exception(data["error"]["message"])
        return data.get("sessionInfo", "")

    async def فون_تصدیق(self, session_info: str, کوڈ: str) -> dict:
        import requests as _req
        r = _req.post(f"{self._AUTH}:signInWithPhoneNumber?key={self._api_key}",
                      json={"sessionInfo": session_info, "code": کوڈ},
                      timeout=10)
        data = r.json()
        if "error" in data:
            raise Exception(data["error"]["message"])
        self._id_token = data["idToken"]
        self._refresh_token = data.get("refreshToken")
        self._local_id = data.get("localId")
        self._connected = True
        return _wrap_row(data)

    # ── Firestore ─────────────────────────────────────────────────────────────

    def مجموعہ(self, نام: str):
        if self._mode == "web":
            return _FirestoreWebCollection(self._project_id, نام,
                                           self._api_key, lambda: self._id_token)
        return _FirestoreCollection(self._db.collection(نام))

    async def لین_دین(self, callback):
        if self._mode == "web":
            await callback()
            return
        batch = self._db.batch()
        self._batch = batch
        self._in_transaction = True
        try:
            await callback()
            batch.commit()
        except Exception:
            raise
        finally:
            self._in_transaction = False
            self._batch = None


Firestore = فائر_بیس


# ─── Firestore Admin Collection ───────────────────────────────────────────────

class _FirestoreCollection:
    def __init__(self, ref):
        self._ref = ref

    async def اضافہ(self, ڈیٹا: dict) -> str:
        _, doc = self._ref.add(ڈیٹا)
        return doc.id

    async def مقرر(self, id: str, ڈیٹا: dict):
        self._ref.document(id).set(ڈیٹا)

    async def حاصل(self, id: str) -> Optional[dict]:
        doc = self._ref.document(id).get()
        return _wrap_row(doc.to_dict()) if doc.exists else None

    async def سبھی(self) -> list[dict]:
        return [_wrap_row({"id": d.id, **d.to_dict()}) for d in self._ref.stream()]

    async def حذف(self, id: str):
        self._ref.document(id).delete()


# ─── Firestore Web/REST Collection ───────────────────────────────────────────

class _FirestoreWebCollection:
    """Firestore CRUD via REST API — no service account needed."""

    _FS = "https://firestore.googleapis.com/v1"

    def __init__(self, project_id: str, name: str, api_key: str, token_fn):
        self._project  = project_id
        self._col      = name
        self._key      = api_key
        self._token_fn = token_fn  # callable → current idToken or None

    def _base(self):
        return f"{self._FS}/projects/{self._project}/databases/(default)/documents/{self._col}"

    def _headers(self):
        token = self._token_fn()
        return {"Authorization": f"Bearer {token}"} if token else {}

    @staticmethod
    def _py_to_fs(val) -> dict:
        if val is None:             return {"nullValue": None}
        if isinstance(val, bool):  return {"booleanValue": val}
        if isinstance(val, int):   return {"integerValue": str(val)}
        if isinstance(val, float): return {"doubleValue": val}
        if isinstance(val, str):   return {"stringValue": val}
        if isinstance(val, dict):
            return {"mapValue": {"fields": {k: _FirestoreWebCollection._py_to_fs(v)
                                            for k, v in val.items()}}}
        if isinstance(val, (list, tuple)):
            return {"arrayValue": {"values": [_FirestoreWebCollection._py_to_fs(v)
                                              for v in val]}}
        return {"stringValue": str(val)}

    @staticmethod
    def _fs_to_py(val: dict):
        if "nullValue"    in val: return None
        if "booleanValue" in val: return val["booleanValue"]
        if "integerValue" in val: return int(val["integerValue"])
        if "doubleValue"  in val: return val["doubleValue"]
        if "stringValue"  in val: return val["stringValue"]
        if "mapValue"     in val:
            return {k: _FirestoreWebCollection._fs_to_py(v)
                    for k, v in val["mapValue"].get("fields", {}).items()}
        if "arrayValue"   in val:
            return [_FirestoreWebCollection._fs_to_py(v)
                    for v in val["arrayValue"].get("values", [])]
        return None

    def _doc_to_py(self, doc: dict) -> dict:
        fields = doc.get("fields", {})
        result = {k: self._fs_to_py(v) for k, v in fields.items()}
        name = doc.get("name", "")
        doc_id = name.split("/")[-1] if name else ""
        if doc_id:
            result["id"] = doc_id
        return _wrap_row(result)

    def _py_to_doc(self, data: dict) -> dict:
        return {"fields": {k: self._py_to_fs(v)
                           for k, v in data.items() if k != "id"}}

    async def اضافہ(self, ڈیٹا: dict) -> str:
        import requests as _req
        r = _req.post(f"{self._base()}?key={self._key}",
                      json=self._py_to_doc(ڈیٹا), headers=self._headers(), timeout=10)
        data = r.json()
        if "error" in data:
            raise Exception(data["error"]["message"])
        return data.get("name", "").split("/")[-1]

    async def مقرر(self, doc_id: str, ڈیٹا: dict):
        import requests as _req
        r = _req.patch(f"{self._base()}/{doc_id}?key={self._key}",
                       json=self._py_to_doc(ڈیٹا), headers=self._headers(), timeout=10)
        data = r.json()
        if "error" in data:
            raise Exception(data["error"]["message"])

    async def حاصل(self, doc_id: str) -> Optional[dict]:
        import requests as _req
        r = _req.get(f"{self._base()}/{doc_id}?key={self._key}",
                     headers=self._headers(), timeout=10)
        data = r.json()
        if "error" in data:
            return None
        return self._doc_to_py(data)

    async def سبھی(self) -> list:
        import requests as _req
        r = _req.get(f"{self._base()}?key={self._key}",
                     headers=self._headers(), timeout=10)
        data = r.json()
        if "error" in data:
            raise Exception(data["error"]["message"])
        return [self._doc_to_py(d) for d in data.get("documents", [])]

    async def حذف(self, doc_id: str):
        import requests as _req
        _req.delete(f"{self._base()}/{doc_id}?key={self._key}",
                    headers=self._headers(), timeout=10)


# ─── Cassandra ───────────────────────────────────────────────────────────────

class کسینڈرا(_UrduDB):
    """Cassandra connection using cassandra-driver."""

    def __init__(self, config: dict):
        super().__init__(config)

    async def جوڑیں(self):
        try:
            from cassandra.cluster import Cluster
            from cassandra.auth import PlainTextAuthProvider
        except ImportError:
            raise ImportError("Cassandra کے لیے چلائیں: pip install cassandra-driver")

        hosts = self._config.get("میزبان", ["localhost"])
        if isinstance(hosts, str):
            hosts = [hosts]

        auth = None
        if "صارف" in self._config:
            from cassandra.auth import PlainTextAuthProvider
            auth = PlainTextAuthProvider(
                username=self._config["صارف"],
                password=self._config.get("پاس_ورڈ", "")
            )

        from cassandra.cluster import Cluster
        self._cluster = Cluster(hosts, auth_provider=auth)
        self._session = self._cluster.connect(self._config.get("کی_اسپیس", ""))
        self._connected = True
        return self

    # ── Query helpers ─────────────────────────────────────────────────────────

    async def سوال(self, query: str, params=None) -> list[dict]:
        """Execute a SELECT and return list of _UrduObj rows."""
        rows = self._session.execute(query, params or [])
        return [_wrap_row(dict(row._asdict())) for row in rows]

    async def چلائیں(self, query: str, params=None) -> int:
        """Execute a non-SELECT CQL statement."""
        self._session.execute(query, params or [])
        return 0

    async def داخل(self, جدول: str, ڈیٹا: dict) -> int:
        """INSERT a row. Returns 0 (Cassandra has no row-count)."""
        cols = ", ".join(ڈیٹا.keys())
        placeholders = ", ".join(["%s"] * len(ڈیٹا))
        vals = list(ڈیٹا.values())
        self._session.execute(
            f"INSERT INTO {جدول} ({cols}) VALUES ({placeholders})", vals)
        return 0

    # ── DDL ───────────────────────────────────────────────────────────────────

    async def کی_اسپیس_بنائیں(self, نام: str,
                                حکمت: str = "SimpleStrategy",
                                نقلیں: int = 1) -> bool:
        """Create a keyspace if it does not exist."""
        self._session.execute(
            f"CREATE KEYSPACE IF NOT EXISTS {نام} "
            f"WITH replication = {{'class': '{حکمت}', "
            f"'replication_factor': {نقلیں}}}"
        )
        return True

    async def کی_اسپیس_چنو(self, نام: str):
        """USE / switch to a keyspace."""
        self._session.set_keyspace(نام)

    async def جدول_بنائیں(self, نام: str, کالمیں: dict) -> bool:
        """CREATE TABLE IF NOT EXISTS from a {col: type} dict.
        Mark primary key with 'PRIMARY KEY' in the type string."""
        cols_def = ", ".join(f"{k} {v}" for k, v in کالمیں.items())
        self._session.execute(
            f"CREATE TABLE IF NOT EXISTS {نام} ({cols_def})")
        return True

    async def جدول_مٹائیں(self, نام: str) -> bool:
        """DROP TABLE IF EXISTS."""
        self._session.execute(f"DROP TABLE IF EXISTS {نام}")
        return True

    async def کی_اسپیس_مٹائیں(self, نام: str) -> bool:
        """DROP KEYSPACE IF EXISTS."""
        self._session.execute(f"DROP KEYSPACE IF EXISTS {نام}")
        return True

    # ── Prepared statements ───────────────────────────────────────────────────

    def تیار(self, query: str):
        """Prepare a CQL statement. Returns a PreparedStatement."""
        return self._session.prepare(query)

    async def تیار_چلائیں(self, تیار_سوال, params=None) -> int:
        """Execute a prepared statement."""
        self._session.execute(تیار_سوال, params or [])
        return 0

    async def تیار_سوال(self, تیار_stmt, params=None) -> list[dict]:
        """Execute a prepared SELECT statement, return rows."""
        rows = self._session.execute(تیار_stmt, params or [])
        return [_wrap_row(dict(row._asdict())) for row in rows]

    # ── Batch ─────────────────────────────────────────────────────────────────

    async def بیچ(self, بیانات: list) -> int:
        """Execute a list of (query, params) pairs as a LOGGED BATCH."""
        from cassandra.query import BatchStatement, BatchType
        batch = BatchStatement(batch_type=BatchType.LOGGED)
        for item in بیانات:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                q, p = item
                batch.add(q, p)
            else:
                batch.add(item, [])
        self._session.execute(batch)
        return len(بیانات)

    # ── Disconnect ────────────────────────────────────────────────────────────

    async def منقطع(self):
        if hasattr(self, "_cluster"):
            self._cluster.shutdown()
            self._connected = False


# ─── Connection factory ───────────────────────────────────────────────────────

def ڈیٹا_بیس_جوڑو(قسم: str, config: dict) -> _UrduDB:
    """Factory function to create DB connection by type name."""
    qsm = قسم.lower()
    if qsm == "mysql":     return مائی_ایس_کیو_ایل(config)
    if qsm in ("pg", "postgresql", "postgres"): return پوسٹ_گریس(config)
    if qsm == "sqlite":    return ایس_کیو_لائٹ(config)
    if qsm == "mongodb":   return مونگو_ڈی_بی(config)
    if qsm in ("firebase", "firestore"): return فائر_بیس(config)
    if qsm == "cassandra": return کسینڈرا(config)
    raise ValueError(f"نامعلوم ڈیٹا بیس قسم: {قسم}")


# ─── پسماندہ مطابقت — انگریزی نام بطور عرفیات ──────────────────────────────────

MySQL      = مائی_ایس_کیو_ایل
PostgreSQL = پوسٹ_گریس
SQLite     = ایس_کیو_لائٹ
MongoDB    = مونگو_ڈی_بی
Firebase   = فائر_بیس
Cassandra  = کسینڈرا


__all__ = [
    # اردو نام (بنیادی)
    "مائی_ایس_کیو_ایل", "پوسٹ_گریس", "ایس_کیو_لائٹ",
    "مونگو_ڈی_بی", "فائر_بیس", "کسینڈرا",
    # انگریزی عرفیات
    "MySQL", "PostgreSQL", "SQLite", "MongoDB",
    "Firebase", "Firestore", "Cassandra",
    "ڈیٹا_بیس_جوڑو",
]
