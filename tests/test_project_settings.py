from django.conf import settings


def test_database_defaults_to_postgresql():
    assert settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql'


def test_project_uses_utc_for_dates():
    assert settings.TIME_ZONE == 'UTC'
    assert settings.USE_TZ


def test_project_installs_django_htmx_middleware():
    assert 'django_htmx.middleware.HtmxMiddleware' in settings.MIDDLEWARE
