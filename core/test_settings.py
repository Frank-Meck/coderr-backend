"""
Django settings for running automated tests.

This configuration overrides the default settings with:
- an in-memory SQLite database for faster test execution
- a faster password hasher to reduce test runtime

Run tests with:

    python manage.py test --settings=core.test_settings
"""

from .settings import *  # noqa: F401, F403


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
