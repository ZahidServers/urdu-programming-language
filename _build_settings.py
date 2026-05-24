"""
Minimal Django settings used only during Nuitka compilation.
Not for production use — satisfies implicit-imports plugin evaluation.
"""
SECRET_KEY = "nuitka-build-only-not-for-production"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
]
DATABASES = {}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
