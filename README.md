# Note

- Create an app (login, current user info)
- Set up Swagger-UI.

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
django-admin startproject myproject

# Start the Django development server
python manage.py runserver
```

## First app

```bash
# Create a new Django app
python manage.py startapp myapp
# It's possible to specify a directory.
# Just use this after creating `apps` directory.
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
# Start a shell with Django settings (`settings.py`).
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

1. Create `config/settings` directory.
2. Move `static` and `templates` to the project level.
3. Create apps in `apps` directory (or another directory).

### Running the server with different settings

```bash
python manage.py runserver --settings=config.settings.dev
python manage.py runserver --settings=config.settings.prd
```

### Additional information

1. We should change the default settings in manage.py.

```Python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
⬇️
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
```

2. We should update `apps/myapp/apps.py`.

```Python
name = 'myapp'
⬇️
name = 'apps.myapp'
```

# Swagger

- [Creating Interactive API Documentation with Swagger UI in Django](https://medium.com/@chodvadiyasaurabh/creating-interactive-api-documentation-with-swagger-ui-in-django-53fa9e9898dc)

# Uvicorn 

```bash
export DJANGO_SETTINGS_MODULE=config.settings.dev
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload
```