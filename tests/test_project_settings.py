import os
from importlib import reload
from pathlib import Path

from django.conf import settings

import cargotracker.settings as project_settings


def test_database_defaults_to_postgresql():
    configured_database = {
        key: settings.DATABASES['default'][key]
        for key in ('ENGINE', 'NAME', 'USER', 'PASSWORD', 'HOST', 'PORT')
    }
    configured_database['NAME'] = configured_database['NAME'].removeprefix('test_')
    assert configured_database == {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'cargotracker'),
        'USER': os.environ.get('POSTGRES_USER', 'cargotracker'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }


def test_project_uses_utc_for_dates():
    assert settings.TIME_ZONE == 'UTC'
    assert settings.USE_TZ


def test_project_installs_django_htmx_middleware():
    assert 'django_htmx.middleware.HtmxMiddleware' in settings.MIDDLEWARE


def test_django_application_settings():
    assert settings.BASE_DIR == Path(__file__).resolve().parents[1]
    assert settings.SECRET_KEY == os.environ.get(
        'DJANGO_SECRET_KEY', 'development-only-not-for-production'
    )
    assert settings.DEBUG is (os.environ.get('DJANGO_DEBUG', '').lower() == 'true')
    expected_hosts = [
        host.strip()
        for host in os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
        if host.strip()
    ]
    assert settings.ALLOWED_HOSTS == expected_hosts + ['testserver']
    assert settings.INSTALLED_APPS == [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_htmx',
        'cargotracker.location.apps.LocationConfig',
        'cargotracker.voyage.apps.VoyageConfig',
        'cargotracker.cargo.apps.CargoConfig',
    ]
    assert settings.MIDDLEWARE == [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django_htmx.middleware.HtmxMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    assert settings.ROOT_URLCONF == 'cargotracker.urls'
    assert settings.WSGI_APPLICATION == 'cargotracker.wsgi.application'
    assert settings.AUTH_PASSWORD_VALIDATORS == [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ]
    assert settings.LANGUAGE_CODE == 'en-us'
    assert settings.USE_I18N
    assert settings.STATIC_URL == '/static/'
    assert settings.STATICFILES_DIRS == [settings.BASE_DIR / 'assets']
    assert settings.STATIC_ROOT == settings.BASE_DIR / 'staticfiles'
    assert settings.DEFAULT_AUTO_FIELD == 'django.db.models.BigAutoField'


def test_django_template_configuration():
    assert settings.TEMPLATES == [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [settings.BASE_DIR / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ]
            },
        }
    ]


def test_settings_read_environment_overrides(monkeypatch):
    try:
        with monkeypatch.context() as environment:
            environment.setenv('DJANGO_SECRET_KEY', 'test-secret')
            environment.setenv('DJANGO_DEBUG', 'TRUE')
            environment.setenv('DJANGO_ALLOWED_HOSTS', 'cargo.example, tracker.example,, ')
            environment.setenv('POSTGRES_DB', 'cargo_test')
            environment.setenv('POSTGRES_USER', 'cargo_user')
            environment.setenv('POSTGRES_PASSWORD', 'test-password')
            environment.setenv('POSTGRES_HOST', 'postgres.example')
            environment.setenv('POSTGRES_PORT', '5544')
            reload(project_settings)

            assert project_settings.SECRET_KEY == 'test-secret'
            assert project_settings.DEBUG
            assert project_settings.ALLOWED_HOSTS == ['cargo.example', 'tracker.example']
            assert project_settings.DATABASES == {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'cargo_test',
                    'USER': 'cargo_user',
                    'PASSWORD': 'test-password',
                    'HOST': 'postgres.example',
                    'PORT': '5544',
                }
            }
    finally:
        reload(project_settings)
