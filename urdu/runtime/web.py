"""
Web framework library for the Urdu Programming Language.
Wraps: FastAPI, Flask, Django, Socket.IO, WebRTC signalling.
"""

from __future__ import annotations
from typing import Any, Callable, Optional
import json
import inspect


def _urduobj_to_plain(obj):
    """Recursively convert _UrduObj / nested dicts/lists to plain Python types.

    FastAPI's jsonable_encoder enters infinite recursion on dict subclasses
    that don't register a custom encoder.  Converting to plain dict/list first
    avoids this.
    """
    if type(obj).__name__ == "_UrduObj" or (isinstance(obj, dict) and type(obj) is not dict):
        return {k: _urduobj_to_plain(v) for k, v in obj.items()}
    if isinstance(obj, dict):
        return {k: _urduobj_to_plain(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_urduobj_to_plain(i) for i in obj]
    return obj


def _inject_request_type(fn: Callable, route_path: str = "") -> Callable:
    """Wrap a route handler to:
    1. Auto-annotate unannotated non-path params as FastAPI Request.
    2. Convert _UrduObj responses to plain dicts (avoids jsonable_encoder recursion).

    Path parameters (e.g. {id} in /items/{id}) keep their default str type so
    FastAPI extracts them from the URL correctly.  Any other unannotated,
    no-default parameter is treated as the HTTP request body accessor.
    """
    import asyncio as _asyncio
    import functools
    import re

    try:
        from fastapi import Request
    except ImportError:
        return fn

    # Extract path param names from template like /items/{id}/{name}
    path_params = set(re.findall(r"\{(\w+)\}", route_path))

    sig = inspect.signature(fn)
    new_params = []
    changed = False
    for p in sig.parameters.values():
        if (p.annotation is inspect.Parameter.empty
                and p.default is inspect.Parameter.empty
                and p.name not in path_params):
            new_params.append(p.replace(annotation=Request))
            changed = True
        else:
            new_params.append(p)

    if _asyncio.iscoroutinefunction(fn):
        @functools.wraps(fn)
        async def _async_wrapper(*args, **kwargs):
            result = await fn(*args, **kwargs)
            return _urduobj_to_plain(result)
        wrapper = _async_wrapper
    else:
        @functools.wraps(fn)
        def _sync_wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            return _urduobj_to_plain(result)
        wrapper = _sync_wrapper

    if changed:
        wrapper.__signature__ = sig.replace(parameters=new_params)
    return wrapper


# ─── FastAPI adapter ──────────────────────────────────────────────────────────

class فاسٹ_اے_پی_آئی:
    """Urdu-friendly FastAPI wrapper with full feature support."""

    def __init__(self, ترتیب=None, *, عنوان: str = "اردو API", نسخہ: str = "1.0.0",
                 تفصیل: str = ""):
        try:
            from fastapi import FastAPI
        except ImportError:
            raise ImportError("FastAPI کے لیے چلائیں: pip install fastapi uvicorn")
        if isinstance(ترتیب, dict):
            عنوان = ترتیب.get("عنوان", عنوان)
            نسخہ = ترتیب.get("نسخہ", نسخہ)
            تفصیل = ترتیب.get("تفصیل", تفصیل)
        self._app = FastAPI(title=عنوان, version=نسخہ, description=تفصیل)

    # ── HTTP method decorators ────────────────────────────────────────────────

    def حاصل(self, راستہ: str, **kwargs):
        """GET route decorator."""
        def decorator(fn):
            self._app.get(راستہ, **kwargs)(_inject_request_type(fn, راستہ))
            return fn
        return decorator

    def بھیجیں(self, راستہ: str, **kwargs):
        """POST route decorator."""
        def decorator(fn):
            self._app.post(راستہ, **kwargs)(_inject_request_type(fn, راستہ))
            return fn
        return decorator

    def تازہ_کریں(self, راستہ: str, **kwargs):
        """PUT route decorator."""
        def decorator(fn):
            self._app.put(راستہ, **kwargs)(_inject_request_type(fn, راستہ))
            return fn
        return decorator

    def حذف(self, راستہ: str, **kwargs):
        """DELETE route decorator."""
        def decorator(fn):
            self._app.delete(راستہ, **kwargs)(_inject_request_type(fn, راستہ))
            return fn
        return decorator

    def پیچ(self, راستہ: str, **kwargs):
        """PATCH route decorator."""
        def decorator(fn):
            self._app.patch(راستہ, **kwargs)(_inject_request_type(fn, راستہ))
            return fn
        return decorator

    # ── Middleware ────────────────────────────────────────────────────────────

    def درمیانی(self, fn: Callable):
        """HTTP middleware decorator."""
        self._app.middleware("http")(fn)
        return fn

    def کورس(self, *, اصل: list = None, اسناد: bool = True,
              طریقے: list = None, سرخیاں: list = None):
        """Add CORS middleware."""
        try:
            from fastapi.middleware.cors import CORSMiddleware
        except ImportError:
            raise ImportError("pip install fastapi")
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=اصل or ["*"],
            allow_credentials=اسناد,
            allow_methods=طریقے or ["*"],
            allow_headers=سرخیاں or ["*"],
        )
        return self

    # ── Router ────────────────────────────────────────────────────────────────

    def شامل_کریں(self, راؤٹر, *, سابقہ: str = ""):
        """Include a router with optional prefix override."""
        if سابقہ:
            self._app.include_router(راؤٹر._router, prefix=سابقہ)
        else:
            self._app.include_router(راؤٹر._router)
        return self

    # ── Exception handlers ────────────────────────────────────────────────────

    def غلطی_ہینڈلر(self, exception_class):
        """Exception handler decorator."""
        def decorator(fn):
            self._app.exception_handler(exception_class)(fn)
            return fn
        return decorator

    # ── Background tasks helper ───────────────────────────────────────────────

    @staticmethod
    def پس_منظر_کام():
        """Return a BackgroundTasks instance."""
        from fastapi import BackgroundTasks
        return BackgroundTasks()

    # ── Dependency helpers ────────────────────────────────────────────────────

    @staticmethod
    def انحصار(fn: Callable):
        """Wrap a function as a FastAPI Depends dependency."""
        from fastapi import Depends
        return Depends(fn)

    @staticmethod
    def حامل_ٹوکن():
        """OAuth2 Bearer token dependency."""
        from fastapi.security import OAuth2PasswordBearer
        return OAuth2PasswordBearer(tokenUrl="ٹوکن")

    # ── WebSocket endpoint ────────────────────────────────────────────────────

    def ویب_ساکٹ(self, راستہ: str):
        """WebSocket endpoint decorator for FastAPI."""
        def decorator(fn):
            self._app.websocket(راستہ)(fn)
            return fn
        return decorator

    # ── Startup / shutdown events ─────────────────────────────────────────────

    def آغاز(self, fn: Callable):
        """Startup event."""
        self._app.on_event("startup")(fn)
        return fn

    def اختتام(self, fn: Callable):
        """Shutdown event."""
        self._app.on_event("shutdown")(fn)
        return fn

    # ── Run ───────────────────────────────────────────────────────────────────

    def چلائیں(self, *, میزبان: str = "0.0.0.0", پورٹ: int = 8000,
               دوبارہ_لوڈ: bool = False):
        """Run the FastAPI server with uvicorn."""
        try:
            import uvicorn
        except ImportError:
            raise ImportError("pip install uvicorn")
        uvicorn.run(self._app, host=میزبان, port=پورٹ, reload=دوبارہ_لوڈ)

    @property
    def ایپ(self):
        return self._app


# ─── FastAPI Router ───────────────────────────────────────────────────────────

class راؤٹر:
    """FastAPI APIRouter wrapper."""

    def __init__(self, ترتیب=None, *, سابقہ: str = "", ٹیگ: list = None):
        try:
            from fastapi import APIRouter
        except ImportError:
            raise ImportError("pip install fastapi")
        if isinstance(ترتیب, dict):
            سابقہ = ترتیب.get("سابقہ", سابقہ)
            ٹیگ = ترتیب.get("ٹیگ", ٹیگ)
        self._router = APIRouter(prefix=سابقہ, tags=ٹیگ or [])

    def حاصل(self, راستہ: str, **kwargs):
        def decorator(fn):
            self._router.get(راستہ, **kwargs)(_inject_request_type(fn, راستہ))
            return fn
        return decorator

    def بھیجیں(self, راستہ: str, **kwargs):
        def decorator(fn):
            self._router.post(راستہ, **kwargs)(_inject_request_type(fn, راستہ))
            return fn
        return decorator

    def تازہ_کریں(self, راستہ: str, **kwargs):
        def decorator(fn):
            self._router.put(راستہ, **kwargs)(_inject_request_type(fn, راستہ))
            return fn
        return decorator

    def حذف(self, راستہ: str, **kwargs):
        def decorator(fn):
            self._router.delete(راستہ, **kwargs)(_inject_request_type(fn, راستہ))
            return fn
        return decorator


# ─── FastAPI request helpers (importable from Urdu) ──────────────────────────

class جیسن_جواب:
    """Return JSON response from a FastAPI/Starlette route."""
    def __new__(cls, data, رمز: int = 200, سرخیاں: dict = None):
        try:
            from fastapi.responses import JSONResponse as _JR
        except ImportError:
            raise ImportError("pip install fastapi")
        return _JR(content=data, status_code=رمز, headers=سرخیاں)


class ایچ_ٹی_ایم_ایل_جواب:
    """Return HTML response."""
    def __new__(cls, مواد: str, رمز: int = 200):
        from fastapi.responses import HTMLResponse as _HR
        return _HR(content=مواد, status_code=رمز)


class سادہ_جواب:
    """Return plain-text response."""
    def __new__(cls, مواد: str, رمز: int = 200):
        from fastapi.responses import PlainTextResponse as _PR
        return _PR(content=مواد, status_code=رمز)


class رجوع_جواب:
    """HTTP redirect response."""
    def __new__(cls, url: str, رمز: int = 307):
        from fastapi.responses import RedirectResponse as _RR
        return _RR(url=url, status_code=رمز)


class جالی_خطا:
    def __new__(cls, رمز: int, تفصیل: str = ""):
        try:
            from fastapi import HTTPException as _HE
        except ImportError:
            raise ImportError("pip install fastapi")
        raise _HE(status_code=رمز, detail=تفصیل)


def سوال_پیرامیٹر(پہلے_سے=..., *, تفصیل: str = ""):
    """FastAPI Query parameter with optional default."""
    from fastapi import Query
    return Query(پہلے_سے, description=تفصیل)


def راستہ_پیرامیٹر(*, تفصیل: str = ""):
    """FastAPI Path parameter."""
    from fastapi import Path
    return Path(..., description=تفصیل)


async def درخواست_باڈی(درخواست):
    """Parse JSON body from a FastAPI Request object."""
    try:
        return await درخواست.json()
    except Exception:
        return {}


def درخواست_سوال(درخواست, کلید: str, پہلے_سے=None):
    """Get query param from FastAPI request."""
    return درخواست.query_params.get(کلید, پہلے_سے)


def درخواست_سرخی(درخواست, کلید: str, پہلے_سے=None):
    """Get header from FastAPI request."""
    return درخواست.headers.get(کلید, پہلے_سے)


# ─── JWT helpers ─────────────────────────────────────────────────────────────

class جے_ڈبلیو_ٹی:
    """Simple JWT encode/decode helpers (requires python-jose)."""

    @staticmethod
    def بنائیں(ڈیٹا: dict, خفیہ: str, اختیارات=None, *, میعاد_منٹ: int = 30,
               طریقہ: str = "HS256") -> str:
        try:
            from jose import jwt as _jwt
        except ImportError:
            raise ImportError("pip install python-jose[cryptography]")
        import datetime
        if isinstance(اختیارات, dict):
            میعاد_منٹ = اختیارات.get("میعاد_منٹ", میعاد_منٹ)
            طریقہ = اختیارات.get("طریقہ", طریقہ)
        payload = dict(ڈیٹا)
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=میعاد_منٹ)
        return _jwt.encode(payload, خفیہ, algorithm=طریقہ)

    @staticmethod
    def جانچیں(ٹوکن: str, خفیہ: str, *, طریقہ: str = "HS256") -> dict:
        try:
            from jose import jwt as _jwt, JWTError
        except ImportError:
            raise ImportError("pip install python-jose[cryptography]")
        try:
            return _jwt.decode(ٹوکن, خفیہ, algorithms=[طریقہ])
        except JWTError as e:
            raise ValueError(f"ٹوکن غلط: {e}")


# ─── Flask adapter ────────────────────────────────────────────────────────────

class فلاسک:
    """Urdu-friendly Flask wrapper with full feature support."""

    def __init__(self, ترتیب=None, *, نام: str = "__main__",
                 سانچہ_فولڈر: str = "templates", جامد_فولڈر: str = "static"):
        try:
            from flask import Flask
        except ImportError:
            raise ImportError("Flask کے لیے چلائیں: pip install flask")
        if isinstance(ترتیب, dict):
            نام = ترتیب.get("نام", نام)
            سانچہ_فولڈر = ترتیب.get("سانچہ_فولڈر", سانچہ_فولڈر)
            جامد_فولڈر = ترتیب.get("جامد_فولڈر", جامد_فولڈر)
        elif isinstance(ترتیب, str):
            نام = ترتیب
        # Resolve root_path from the .urdu script's directory so that
        # Flask finds templates/ and static/ next to the script, not next
        # to the urdu package itself.
        import os, sys as _sys
        root_path = None
        frame = _sys._getframe(1)
        while frame is not None:
            f = frame.f_globals.get("__file__", "")
            if f and f.endswith((".urdu", ".urduc")):
                root_path = os.path.dirname(os.path.abspath(f))
                break
            frame = frame.f_back
        if root_path is None:
            root_path = os.getcwd()
        self._app = Flask(نام,
                          template_folder=سانچہ_فولڈر,
                          static_folder=جامد_فولڈر,
                          root_path=root_path)
        try:
            from urdu.runtime.urdu_templates import UrduJinja2Loader
            if self._app.jinja_loader is not None:
                self._app.jinja_loader = UrduJinja2Loader(self._app.jinja_loader)
        except ImportError:
            pass

    # ── Routes ────────────────────────────────────────────────────────────────

    def راستہ(self, url: str, طریقے: list = None):
        def decorator(fn):
            import asyncio, functools, contextvars
            if asyncio.iscoroutinefunction(fn):
                import concurrent.futures
                @functools.wraps(fn)
                def _sync(*args, **kw):
                    ctx = contextvars.copy_context()
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
                        return ex.submit(ctx.run, asyncio.run, fn(*args, **kw)).result()
                self._app.route(url, methods=طریقے or ["GET"])(_sync)
            else:
                self._app.route(url, methods=طریقے or ["GET"])(fn)
            return fn
        return decorator

    def حاصل(self, url: str):
        return self.راستہ(url, ["GET"])

    def بھیجیں(self, url: str):
        return self.راستہ(url, ["POST"])

    def تازہ_کریں(self, url: str):
        return self.راستہ(url, ["PUT"])

    def حذف(self, url: str):
        return self.راستہ(url, ["DELETE"])

    def پیچ(self, url: str):
        return self.راستہ(url, ["PATCH"])

    # ── Blueprints ────────────────────────────────────────────────────────────

    def بلیو_پرنٹ_شامل(self, بلیو_پرنٹ, *, سابقہ: str = ""):
        """Register a blueprint."""
        url_prefix = سابقہ or بلیو_پرنٹ._prefix
        self._app.register_blueprint(بلیو_پرنٹ._bp, url_prefix=url_prefix)
        return self

    # ── Error handlers ────────────────────────────────────────────────────────

    def غلطی(self, رمز: int):
        """Error handler decorator: @app.غلطی(404)"""
        def decorator(fn):
            self._app.errorhandler(رمز)(fn)
            return fn
        return decorator

    # ── Before/after request hooks ────────────────────────────────────────────

    def قبل_درخواست(self, fn: Callable):
        self._app.before_request(fn)
        return fn

    def بعد_درخواست(self, fn: Callable):
        self._app.after_request(fn)
        return fn

    # ── Context processor ─────────────────────────────────────────────────────

    def سیاق(self, fn: Callable):
        self._app.context_processor(fn)
        return fn

    # ── Config ────────────────────────────────────────────────────────────────

    def ترتیب_دیں(self, کلید: str, قدر):
        self._app.config[کلید] = قدر
        return self

    # ── Run ───────────────────────────────────────────────────────────────────

    def چلائیں(self, *, میزبان: str = "0.0.0.0", پورٹ: int = 5000,
               ڈیبگ: bool = True, تھریڈ: bool = False, **kwargs):
        self._app.run(host=میزبان, port=پورٹ, debug=ڈیبگ, threaded=تھریڈ, **kwargs)

    @property
    def ایپ(self):
        return self._app


class بلیو_پرنٹ:
    """Flask Blueprint wrapper."""

    def __init__(self, نام: str, ترتیب=None, *, سابقہ: str = ""):
        try:
            from flask import Blueprint
        except ImportError:
            raise ImportError("pip install flask")
        if isinstance(ترتیب, dict):
            سابقہ = ترتیب.get("سابقہ", سابقہ)
        self._prefix = سابقہ
        self._bp = Blueprint(نام, __name__)

    def راستہ(self, url: str, طریقے: list = None):
        def decorator(fn):
            self._bp.route(url, methods=طریقے or ["GET"])(fn)
            return fn
        return decorator

    def حاصل(self, url: str):
        return self.راستہ(url, ["GET"])

    def بھیجیں(self, url: str):
        return self.راستہ(url, ["POST"])

    def غلطی(self, رمز: int):
        def decorator(fn):
            self._bp.errorhandler(رمز)(fn)
            return fn
        return decorator

    def قبل_درخواست(self, fn: Callable):
        self._bp.before_request(fn)
        return fn


# ─── Flask helpers ────────────────────────────────────────────────────────────

def flask_json(data, status: int = 200):
    """Return a Flask JSON response."""
    try:
        from flask import jsonify
        response = jsonify(data)
        response.status_code = status
        return response
    except ImportError:
        raise ImportError("pip install flask")


def flask_request():
    """Get the current Flask request object."""
    try:
        from flask import request
        return request
    except ImportError:
        raise ImportError("pip install flask")


def flask_redirect(مقام: str, رمز: int = 302):
    """Flask redirect."""
    from flask import redirect
    return redirect(مقام, code=رمز)


def flask_url(اختتام_نقطہ: str, **قدریں):
    """Flask url_for."""
    from flask import url_for
    return url_for(اختتام_نقطہ, **قدریں)


def flask_render(سانچہ: str, **سیاق):
    """Render a Jinja2 template."""
    from flask import render_template
    return render_template(سانچہ, **سیاق)


def flask_response(مواد: str = "", رمز: int = 200, مائم: str = "text/plain"):
    """Build a custom Flask response."""
    from flask import make_response
    resp = make_response(مواد, رمز)
    resp.content_type = مائم
    return resp


def flask_abort(رمز: int):
    """Abort with HTTP status code."""
    from flask import abort
    abort(رمز)


def flask_session():
    """Return Flask session proxy."""
    from flask import session
    return session


def flask_g():
    """Return Flask g proxy."""
    from flask import g
    return g


# ─── Django adapter ───────────────────────────────────────────────────────────

class ڈجانگو:
    """Urdu-friendly Django project builder and launcher."""

    _url_patterns: list = []

    def __init__(self, ترتیب: dict = None):
        try:
            import django
        except ImportError:
            raise ImportError("Django کے لیے چلائیں: pip install django")
        self._config = ترتیب or {}
        ڈجانگو._url_patterns = []

    def ترتیب_دیں(self):
        """Configure Django settings programmatically."""
        import django
        from django.conf import settings

        # django.contrib.auth and contenttypes are NOT included by default
        # because their AppConfig.ready() transitively imports
        # django.core.management, which is excluded from the compiled exe.
        # Add them explicitly via the "ایپس" config key if your project needs them.
        installed = self._config.get("ایپس", [])

        db_cfg = self._config.get("ڈیٹا_بیس", {})
        if isinstance(db_cfg, str):
            db_cfg = {"ENGINE": "django.db.backends.sqlite3", "NAME": db_cfg}
        elif not db_cfg:
            db_cfg = {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}

        cfg = {
            "DEBUG": self._config.get("ڈیبگ", True),
            "SECRET_KEY": self._config.get("خفیہ_کلید", "urdu-lang-dev-secret-key-32"),
            "ALLOWED_HOSTS": self._config.get("اجازت_یافتہ", ["*"]),
            "INSTALLED_APPS": installed,
            "DATABASES": {"default": db_cfg},
            "ROOT_URLCONF": "__urdu_urls__",
            "USE_TZ": False,
            "DEFAULT_AUTO_FIELD": "django.db.models.BigAutoField",
            "MIDDLEWARE": [
                "django.middleware.common.CommonMiddleware",
            ] + self._config.get("درمیانی", []),
            "TEMPLATES": [{
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": self._config.get("سانچہ_فولڈر", []),
                "APP_DIRS": False,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.request",
                    ],
                    "loaders": [
                        "urdu.runtime.urdu_templates.UrduFilesystemLoader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                },
            }],
        }
        if not settings.configured:
            settings.configure(**cfg)
        django.setup()

        # Install dynamic URL module
        import sys, types
        mod = types.ModuleType("__urdu_urls__")
        mod.urlpatterns = ڈجانگو._url_patterns
        sys.modules["__urdu_urls__"] = mod

        return self

    # ── URL registration ──────────────────────────────────────────────────────

    def راستہ(self, url: str, نظارہ_fn: Callable, اختیارات=None, *, نام: str = ""):
        """Register a URL pattern."""
        from django.urls import path
        if isinstance(اختیارات, dict):
            نام = اختیارات.get("نام", نام)
        ڈجانگو._url_patterns.append(path(url, نظارہ_fn, name=نام))
        # refresh the module
        import sys
        if "__urdu_urls__" in sys.modules:
            sys.modules["__urdu_urls__"].urlpatterns = ڈجانگو._url_patterns
        return self

    def شامل_راستے(self, سابقہ: str, راؤٹر):
        """include() another set of URL patterns."""
        from django.urls import path, include
        ڈجانگو._url_patterns.append(path(سابقہ, include(راؤٹر._patterns)))
        return self

    # ── Database migrations ───────────────────────────────────────────────────

    def میزیں_بنائیں(self):
        """Run migrate (create tables)."""
        from django.core.management import call_command
        call_command("migrate", "--run-syncdb", verbosity=0)
        return self

    # ── Run development server ────────────────────────────────────────────────

    def چلائیں(self, *, پورٹ: int = 8000):
        from django.core.management import execute_from_command_line
        execute_from_command_line(["manage.py", "runserver", f"0.0.0.0:{پورٹ}"])


# ─── Django view helpers ──────────────────────────────────────────────────────

def django_response(مواد: str = "", رمز: int = 200, مائم: str = "text/plain"):
    """Django HttpResponse."""
    from django.http import HttpResponse
    return HttpResponse(مواد, status=رمز, content_type=مائم)


def django_json(data, رمز: int = 200):
    """Django JsonResponse (auto-serializes dict/list)."""
    from django.http import JsonResponse
    if isinstance(data, list):
        return JsonResponse(data, safe=False, status=رمز)
    return JsonResponse(data, status=رمز)


def django_redirect(مقام: str, *, مستقل: bool = False):
    """Django redirect."""
    from django.shortcuts import redirect
    return redirect(مقام, permanent=مستقل)


def django_render(درخواست, سانچہ: str, سیاق: dict = None):
    """Django render template."""
    from django.shortcuts import render
    return render(درخواست, سانچہ, سیاق or {})


def django_404(پیغام: str = "نہیں ملا"):
    """Raise Django Http404."""
    from django.http import Http404
    raise Http404(پیغام)


def django_get_or_404(ماڈل, **کوارگز):
    """get_object_or_404."""
    from django.shortcuts import get_object_or_404
    return get_object_or_404(ماڈل, **کوارگز)


class ڈجانگو_درمیانی:
    """Base class for Urdu Django middleware."""

    def __init__(self, اگلا_جواب):
        self.اگلا_جواب = اگلا_جواب

    def __call__(self, درخواست):
        self.قبل(درخواست)
        جواب = self.اگلا_جواب(درخواست)
        return self.بعد(درخواست, جواب)

    def قبل(self, درخواست):
        """Override: runs before view."""

    def بعد(self, درخواست, جواب):
        """Override: runs after view."""
        return جواب


class ڈجانگو_آزمائش:
    """Thin wrapper around Django's test client for in-process testing."""

    def __init__(self):
        from django.test import Client
        self._c = Client()

    def حاصل(self, url: str, **kwargs):
        r = self._c.get(url, **kwargs)
        return {"رمز": r.status_code, "مواد": r.content.decode(), "json": self._try_json(r)}

    def بھیجیں(self, url: str, data=None, *, json=None, **kwargs):
        import json as _json
        # Allow {"json": {...}} pattern as second positional arg
        if isinstance(data, dict) and "json" in data and json is None:
            json = data["json"]
            data = None
        if json is not None:
            body = _json.dumps(_urduobj_to_plain(json) if hasattr(json, "items") else json)
            r = self._c.post(url, data=body, content_type="application/json")
        else:
            r = self._c.post(url, data=data or {}, **kwargs)
        return {"رمز": r.status_code, "مواد": r.content.decode(), "json": self._try_json(r)}

    @staticmethod
    def _try_json(r):
        try:
            import json as _json
            return _json.loads(r.content)
        except Exception:
            return None


# ─── Socket.IO adapter ────────────────────────────────────────────────────────

class ساکٹ_آئی_او:
    """
    Socket.IO server — auto-adapts to Flask/Django (WSGI) and FastAPI (ASGI).

    پر()       → event handler decorator
    بھیجو()    → emit to a client or room
    نشر()      → broadcast to all
    wsgi_ایپ() → WSGI wrapper for Flask / Django
    asgi_ایپ() → ASGI wrapper for FastAPI
    چلائیں()   → run (picks werkzeug or uvicorn automatically)
    """

    def __init__(self, ترتیب=None, *, ایپ=None, کورس: list = None, غیر_متزامن: bool = True):
        try:
            import socketio
        except ImportError:
            raise ImportError("Socket.IO کے لیے چلائیں: pip install python-socketio")
        if isinstance(ترتیب, dict):
            ایپ = ترتیب.get("ایپ", ایپ)
            کورس = ترتیب.get("کورس", کورس)
            غیر_متزامن = ترتیب.get("غیر_متزامن", غیر_متزامن)
        # WSGI frameworks → sync threading server; ASGI → async server
        if isinstance(ایپ, (فلاسک, ڈجانگو)):
            غیر_متزامن = False
        elif isinstance(ایپ, فاسٹ_اے_پی_آئی):
            غیر_متزامن = True
        self._is_async = غیر_متزامن
        if غیر_متزامن:
            self._sio = socketio.AsyncServer(
                async_mode="asgi",
                cors_allowed_origins=کورس or "*",
            )
        else:
            # threading mode: safe with Flask/Django, no eventlet/gevent needed
            self._sio = socketio.Server(
                async_mode="threading",
                cors_allowed_origins=کورس or "*",
            )
        self._ایپ = ایپ

    # ── Event decorators ──────────────────────────────────────────────────────

    def پر(self, واقعہ: str, *, نام_فضا: str = "/"):
        """Register an event handler: @sio.پر('message')"""
        def decorator(fn):
            self._sio.on(واقعہ, fn, namespace=نام_فضا)
            return fn
        return decorator

    def پر_جڑنا(self, *, نام_فضا: str = "/"):
        return self.پر("connect", نام_فضا=نام_فضا)

    def پر_منقطع(self, *, نام_فضا: str = "/"):
        return self.پر("disconnect", نام_فضا=نام_فضا)

    # ── Emit ──────────────────────────────────────────────────────────────────

    async def بھیجو(self, واقعہ: str, ڈیٹا, *, کمرہ: str = None, نام_فضا: str = "/", مستثنی: str = None):
        """Emit to a specific sid/room (or broadcast if کمرہ=None)."""
        if self._is_async:
            await self._sio.emit(واقعہ, ڈیٹا, room=کمرہ, namespace=نام_فضا, skip_sid=مستثنی)
        else:
            self._sio.emit(واقعہ, ڈیٹا, room=کمرہ, namespace=نام_فضا, skip_sid=مستثنی)

    async def نشر(self, واقعہ: str, ڈیٹا, *, نام_فضا: str = "/"):
        """Broadcast to all connected clients."""
        if self._is_async:
            await self._sio.emit(واقعہ, ڈیٹا, namespace=نام_فضا)
        else:
            self._sio.emit(واقعہ, ڈیٹا, namespace=نام_فضا)

    # ── Room management ───────────────────────────────────────────────────────

    async def کمرہ_میں_شامل(self, sid: str, کمرہ: str, *, نام_فضا: str = "/"):
        if self._is_async:
            await self._sio.enter_room(sid, کمرہ, namespace=نام_فضا)
        else:
            self._sio.enter_room(sid, کمرہ, namespace=نام_فضا)

    async def کمرہ_چھوڑیں(self, sid: str, کمرہ: str, *, نام_فضا: str = "/"):
        if self._is_async:
            await self._sio.leave_room(sid, کمرہ, namespace=نام_فضا)
        else:
            self._sio.leave_room(sid, کمرہ, namespace=نام_فضا)

    def کمرے(self, sid: str, *, نام_فضا: str = "/") -> list:
        return list(self._sio.rooms(sid, namespace=نام_فضا))

    # ── WSGI app (Flask + Django) ─────────────────────────────────────────────

    def wsgi_ایپ(self, src=None):
        """Wrap Flask or Django app + SocketIO into a single WSGI app."""
        import socketio
        src = src or self._ایپ
        if isinstance(src, فلاسک):
            raw = src.ایپ
        elif isinstance(src, ڈجانگو):
            from django.core.wsgi import get_wsgi_application
            raw = get_wsgi_application()
        else:
            raw = src  # already a raw WSGI callable
        if raw is None:
            raise ValueError("Flask، Django، یا WSGI callable پاس کریں")
        return socketio.WSGIApp(self._sio, raw)

    # ── ASGI app (FastAPI) ────────────────────────────────────────────────────

    def asgi_ایپ(self, src=None):
        """Wrap FastAPI app + SocketIO into a single ASGI app."""
        import socketio
        src = src or self._ایپ
        if isinstance(src, فاسٹ_اے_پی_آئی):
            raw = src.ایپ
        else:
            raw = src  # already a raw ASGI callable
        if raw is None:
            raise ValueError("FastAPI یا ASGI callable پاس کریں")
        return socketio.ASGIApp(self._sio, raw)

    # ── Run ───────────────────────────────────────────────────────────────────

    def چلائیں(self, ایپ=None, *, میزبان: str = "0.0.0.0", پورٹ: int = 8000):
        """Start the server — werkzeug for Flask/Django, uvicorn for FastAPI."""
        src = ایپ or self._ایپ
        if isinstance(src, (فلاسک, ڈجانگو)) or not self._is_async:
            from werkzeug.serving import run_simple
            run_simple(میزبان, پورٹ, self.wsgi_ایپ(src))
        else:
            import uvicorn
            uvicorn.run(self.asgi_ایپ(src), host=میزبان, port=پورٹ)

    @property
    def سرور(self):
        return self._sio


# ─── WebRTC signalling server ─────────────────────────────────────────────────

class ویب_آر_ٹی_سی:
    """
    WebRTC signalling server built on top of WebSockets (websockets library).

    Handles:
      offer      → forward SDP offer to peer
      answer     → forward SDP answer
      ice        → forward ICE candidate
      join       → join a room (peer pairing)
    """

    def __init__(self, ترتیب=None, *, میزبان: str = "0.0.0.0", پورٹ: int = 9000):
        if isinstance(ترتیب, dict):
            میزبان = ترتیب.get("میزبان", میزبان)
            پورٹ = ترتیب.get("پورٹ", پورٹ)
        self.میزبان = میزبان
        self.پورٹ = پورٹ
        self._کمرے: dict = {}    # room_id → [ws, ws]
        self._sid_to_room: dict = {}

    async def _ہینڈل(self, ws):
        try:
            async for raw in ws:
                try:
                    msg = json.loads(raw)
                except Exception:
                    continue
                قسم = msg.get("type", "")
                await self._راؤٹ(ws, قسم, msg)
        finally:
            await self._صاف_کریں(ws)

    async def _راؤٹ(self, ws, قسم: str, msg: dict):
        if قسم == "join":
            await self._جوائن(ws, msg.get("room", "default"))
        elif قسم in ("offer", "answer", "ice"):
            await self._فارورڈ(ws, msg)
        else:
            await ws.send(json.dumps({"type": "error", "detail": f"نامعلوم پیغام: {قسم}"}))

    async def _جوائن(self, ws, کمرہ: str):
        کمرہ_فہرست = self._کمرے.setdefault(کمرہ, [])
        if ws in کمرہ_فہرست:
            return
        کمرہ_فہرست.append(ws)
        self._sid_to_room[id(ws)] = کمرہ
        نمبر = len(کمرہ_فہرست)
        await ws.send(json.dumps({"type": "joined", "room": کمرہ, "peers": نمبر - 1}))
        if نمبر == 2:
            # Notify first peer a second peer arrived
            await کمرہ_فہرست[0].send(json.dumps({"type": "peer_joined", "room": کمرہ}))

    async def _فارورڈ(self, ws, msg: dict):
        کمرہ = self._sid_to_room.get(id(ws))
        if not کمرہ:
            await ws.send(json.dumps({"type": "error", "detail": "پہلے کمرے میں شامل ہوں"}))
            return
        for peer in self._کمرے.get(کمرہ, []):
            if peer is not ws:
                await peer.send(json.dumps(msg))

    async def _صاف_کریں(self, ws):
        کمرہ = self._sid_to_room.pop(id(ws), None)
        if کمرہ and کمرہ in self._کمرے:
            try:
                self._کمرے[کمرہ].remove(ws)
            except ValueError:
                pass
            if not self._کمرے[کمرہ]:
                del self._کمرے[کمرہ]

    def چلائیں(self):
        """Start the WebRTC signalling WebSocket server."""
        try:
            import websockets
            import asyncio
        except ImportError:
            raise ImportError("pip install websockets")
        import asyncio, websockets

        async def _main():
            async with websockets.serve(self._ہینڈل, self.میزبان, self.پورٹ):
                print(f"✓ WebRTC سگنلنگ: ws://{self.میزبان}:{self.پورٹ}")
                await asyncio.Future()

        asyncio.run(_main())


# ─── Basic WebSocket server ───────────────────────────────────────────────────

class ویب_ساکٹ:
    """Simple WebSocket server using websockets library."""

    def __init__(self, ترتیب=None, *, میزبان: str = "localhost", پورٹ: int = 8765):
        if isinstance(ترتیب, dict):
            میزبان = ترتیب.get("میزبان", میزبان)
            پورٹ = ترتیب.get("پورٹ", پورٹ)
        self.میزبان = میزبان
        self.پورٹ = پورٹ
        self._ہینڈلر = None
        self._جڑنا_ہینڈلر = None
        self._منقطع_ہینڈلر = None
        self._clients: set = set()

    def پر_پیغام(self, fn):
        self._ہینڈلر = fn
        return fn

    def پر_جڑنا(self, fn):
        self._جڑنا_ہینڈلر = fn
        return fn

    def پر_منقطع(self, fn):
        self._منقطع_ہینڈلر = fn
        return fn

    async def نشر(self, پیغام: str, *, مستثنی=None):
        """Broadcast to all connected clients."""
        import asyncio
        targets = [c for c in self._clients if c is not مستثنی]
        if targets:
            await asyncio.gather(*[c.send(پیغام) for c in targets])

    def چلائیں(self):
        try:
            import websockets
            import asyncio
        except ImportError:
            raise ImportError("pip install websockets")

        async def _serve(ws, path=""):
            self._clients.add(ws)
            if self._جڑنا_ہینڈلر:
                r = self._جڑنا_ہینڈلر(ws)
                if asyncio.iscoroutine(r):
                    await r
            try:
                async for msg in ws:
                    if self._ہینڈلر:
                        result = self._ہینڈلر(ws, msg)
                        if asyncio.iscoroutine(result):
                            result = await result
                        if result is not None:
                            await ws.send(str(result))
            finally:
                self._clients.discard(ws)
                if self._منقطع_ہینڈلر:
                    r2 = self._منقطع_ہینڈلر(ws)
                    if asyncio.iscoroutine(r2):
                        await r2

        import asyncio, websockets

        async def _main():
            async with websockets.serve(_serve, self.میزبان, self.پورٹ):
                print(f"✓ WebSocket: ws://{self.میزبان}:{self.پورٹ}")
                await asyncio.Future()

        asyncio.run(_main())


# ─── HTTP client ─────────────────────────────────────────────────────────────

class جالی_کلائنٹ:
    """Async HTTP client wrapper (aiohttp)."""

    @staticmethod
    async def حاصل(url: str, **kwargs) -> dict:
        try:
            import aiohttp
        except ImportError:
            raise ImportError("pip install aiohttp")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, **kwargs) as resp:
                ct = resp.content_type or ""
                return {
                    "رمز": resp.status,
                    "status": resp.status,
                    "data": await resp.json() if "json" in ct else await resp.text(),
                    "headers": dict(resp.headers),
                }

    @staticmethod
    async def بھیجیں(url: str, json=None, data=None, **kwargs) -> dict:
        try:
            import aiohttp
        except ImportError:
            raise ImportError("pip install aiohttp")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json, data=data, **kwargs) as resp:
                ct = resp.content_type or ""
                return {
                    "رمز": resp.status,
                    "status": resp.status,
                    "data": await resp.json() if "json" in ct else await resp.text(),
                }

    @staticmethod
    async def تازہ_کریں(url: str, json=None, **kwargs) -> dict:
        try:
            import aiohttp
        except ImportError:
            raise ImportError("pip install aiohttp")
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=json, **kwargs) as resp:
                ct = resp.content_type or ""
                return {"رمز": resp.status, "status": resp.status,
                        "data": await resp.json() if "json" in ct else await resp.text()}

    @staticmethod
    async def حذف(url: str, **kwargs) -> dict:
        try:
            import aiohttp
        except ImportError:
            raise ImportError("pip install aiohttp")
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, **kwargs) as resp:
                return {"رمز": resp.status, "status": resp.status}


نیٹ = جالی_کلائنٹ()
fetch = جالی_کلائنٹ.حاصل


# ─── پسماندہ مطابقت — انگریزی نام بطور عرفیات ──────────────────────────────────

UrduFastAPI       = فاسٹ_اے_پی_آئی
UrduRouter        = راؤٹر
JSONResponse      = جیسن_جواب
HTMLResponse      = ایچ_ٹی_ایم_ایل_جواب
PlainTextResponse = سادہ_جواب
RedirectResponse  = رجوع_جواب
HTTPException     = جالی_خطا
JWT               = جے_ڈبلیو_ٹی
UrduFlask         = فلاسک
UrduBlueprint     = بلیو_پرنٹ
UrduDjango        = ڈجانگو
DjangoMiddleware  = ڈجانگو_درمیانی
DjangoTestClient  = ڈجانگو_آزمائش
UrduSocketIO      = ساکٹ_آئی_او
WebRTCSignalling  = ویب_آر_ٹی_سی
WebSocket         = ویب_ساکٹ
HTTPClient        = جالی_کلائنٹ

# Flask مددگار اردو عرفیات
فلاسک_جیسن    = flask_json
فلاسک_درخواست = flask_request
فلاسک_رجوع   = flask_redirect
فلاسک_ربط    = flask_url
فلاسک_سانچہ  = flask_render
فلاسک_جواب   = flask_response
فلاسک_منسوخ  = flask_abort
فلاسک_نشست   = flask_session
فلاسک_عالمی  = flask_g

# Django مددگار اردو عرفیات
ڈجانگو_جواب        = django_response
ڈجانگو_جیسن        = django_json
ڈجانگو_رجوع        = django_redirect
ڈجانگو_سانچہ       = django_render
ڈجانگو_۴۰۴         = django_404
ڈجانگو_حاصل_یا_۴۰۴ = django_get_or_404


# ─── Exports ──────────────────────────────────────────────────────────────────

__all__ = [
    # FastAPI — اردو نام
    "فاسٹ_اے_پی_آئی", "راؤٹر",
    "جیسن_جواب", "ایچ_ٹی_ایم_ایل_جواب", "سادہ_جواب", "رجوع_جواب",
    "جالی_خطا", "جے_ڈبلیو_ٹی",
    "سوال_پیرامیٹر", "راستہ_پیرامیٹر",
    "درخواست_باڈی", "درخواست_سوال", "درخواست_سرخی",
    # FastAPI — English aliases
    "UrduFastAPI", "UrduRouter",
    "JSONResponse", "HTMLResponse", "PlainTextResponse", "RedirectResponse",
    "HTTPException", "JWT",
    # Flask — اردو نام
    "فلاسک", "بلیو_پرنٹ",
    "فلاسک_جیسن", "فلاسک_درخواست", "فلاسک_رجوع", "فلاسک_ربط",
    "فلاسک_سانچہ", "فلاسک_جواب", "فلاسک_منسوخ", "فلاسک_نشست", "فلاسک_عالمی",
    # Flask — English aliases
    "UrduFlask", "UrduBlueprint",
    "flask_json", "flask_request", "flask_redirect", "flask_url",
    "flask_render", "flask_response", "flask_abort", "flask_session", "flask_g",
    # Django — اردو نام
    "ڈجانگو", "ڈجانگو_درمیانی", "ڈجانگو_آزمائش",
    "ڈجانگو_جواب", "ڈجانگو_جیسن", "ڈجانگو_رجوع",
    "ڈجانگو_سانچہ", "ڈجانگو_۴۰۴", "ڈجانگو_حاصل_یا_۴۰۴",
    # Django — English aliases
    "UrduDjango", "DjangoMiddleware", "DjangoTestClient",
    "django_response", "django_json", "django_redirect",
    "django_render", "django_404", "django_get_or_404",
    # Socket.IO
    "ساکٹ_آئی_او", "UrduSocketIO",
    # WebRTC
    "ویب_آر_ٹی_سی", "WebRTCSignalling",
    # WebSocket
    "ویب_ساکٹ", "WebSocket",
    # HTTP client
    "جالی_کلائنٹ", "HTTPClient", "نیٹ", "fetch",
]
