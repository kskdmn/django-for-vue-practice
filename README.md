# Note

# venv

```bash
python -m venv .venv
source .venv/bin/activate
```


# django

## Fist project

```bash
# Check if Django is installed
python -m django --version

# Create a new Django project
django-admin startproject config

# Start the Django development server
python manage.py runserver
```

## First app

```bash
# Create a new Django app
python manage.py startapp myapp
# It's possible to specify a directory.
# Just use this after creating `apps/myapp` directory.
python manage.py startapp myapp apps/myapp
```

## Migrations

```bash
# Create a migration file
python manage.py makemigrations myapp

# Check the SQL (NOT running the SQL)
python manage.py sqlmigrate myapp 0001

# Run the SQL
python manage.py migrate myapp
```

## Shell 

```bash
# Start a shell with Django settings.
# The settings can be specified with `--settings` option.
python manage.py shell
```

## Admin

```bash
# Create a superuser
# This requires tables to be created.
python manage.py createsuperuser
```

## Unit tests

```bash
# Run all tests
python manage.py test {{path.to.test_case}}
```

## Recommended directory structure

- [【Python】Django おすすめのディレクトリ構成【django 3.2対応】(Best practice for Django project directory structure)](https://plus-info-tech.com/django-pj-directory-structure)   
- [【Django】個人的に好きなディレクトリ構成と設定方法](https://qiita.com/tsk1000/items/01ee3e800c57a2f008bc)  
- [【Django】ディレクトリ構成のプラクティス + 注意点](https://qiita.com/nilwurtz/items/defab259cde73669cc6d)  
- [3.Djangoのアーキテクチャとディレクトリ構成](https://denno-sekai.com/django-directory-structure/)  

Steps (mostly based on the first link):
1. Rename `myproject` to `config` and move `settings.py` to `config/settings` directory and rename it to `base.py`.
2. In `config/settings`, create `dev.py` and `prd.py` files.
3. Update paths.
   - `base.py`: `BASE_DIR` to `Path(__file__).resolve().parent.parent.parent`, `ROOT_URLCONF` and `WSGI_APPLICATION`.
   - `manage.py`: `DJANGO_SETTINGS_MODULE` to `config.settings.dev`.
   - `wsgi.py`: `DJANGO_SETTINGS_MODULE` to `config.settings.dev`.
   - `asgi.py`: `DJANGO_SETTINGS_MODULE` to `config.settings.dev`.
4. Move `static` and `templates` to the project level.
    - Add `STATICFILES_DIRS = [BASE_DIR / 'static']` to `base.py`.
5. Create apps in `apps` directory. (The name can be anything.)
    - If moving existing apps to `apps`, update `urls.py`, the `name` in `apps.py`, and `INSTALLED_APPS` in `base.py`.

### dev.py sample

```Python
from .base import *
DEBUG = True
ALLOWED_HOSTS = ['*']
```

### Running the server with different settings

```bash
python manage.py runserver --settings=config.settings.dev
python manage.py runserver --settings=config.settings.prd
```


# Swagger

- [Creating Interactive API Documentation with Swagger UI in Django](https://medium.com/@chodvadiyasaurabh/creating-interactive-api-documentation-with-swagger-ui-in-django-53fa9e9898dc)

1. Add `drf-yasg` to `INSTALLED_APPS` in `base.py`.
2. Add `schema_view`, `path('/swagger')`, and `path('/redoc')` to `urls.py`.
3. Access http://localhost:8000/swagger/ for Swagger UI and http://localhost:8000/redoc/ for ReDoc.


# Uvicorn 

```bash
export DJANGO_SETTINGS_MODULE=config.settings.dev
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload
```