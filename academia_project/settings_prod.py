import copy

import environ

from . import settings as base

env = environ.Env()

# Heredar estructuras claves del base:
MIDDLEWARE = list(getattr(base, "MIDDLEWARE", []))
INSTALLED_APPS = list(getattr(base, "INSTALLED_APPS", []))
TEMPLATES = copy.deepcopy(getattr(base, "TEMPLATES", []))
DATABASES = copy.deepcopy(getattr(base, "DATABASES", {}))

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["example.com"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["https://example.com"])

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"

# LOGGING (como te dejé antes)
if hasattr(base, "LOGGING") and base.LOGGING:
    LOGGING = copy.deepcopy(base.LOGGING)
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {"console": {"class": "logging.StreamHandler"}},
        "loggers": {},
    }
LOGGING.setdefault("loggers", {})
LOGGING["loggers"]["django"] = {**LOGGING["loggers"].get("django", {}), "level": "INFO"}
