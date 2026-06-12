# 🔧 Настройка Django проекта LearnHub

## Структура проекта (финальная)

```
learnhub/
├── .venv/                      # Виртуальное окружение (uv)
├── backend/
│   ├── apps/
│   │   ├── __init__.py
│   │   ├── courses/            # Приложение курсов
│   │   │   ├── migrations/
│   │   │   ├── tests/
│   │   │   │   └── __init__.py
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── permissions.py
│   │   │   └── urls.py
│   │   └── users/              # Приложение пользователей
│   │       ├── migrations/
│   │       ├── __init__.py
│   │       ├── admin.py
│   │       ├── apps.py
│   │       └── models.py
│   ├── conf/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   └── celery.py
│   ├── pytest.ini
│   ├── conftest.py
│   └── manage.py
├── .env                        # Ваши переменные (НЕ коммитить!)
├── .env.example                # Шаблон переменных
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml              # Конфигурация проекта (uv)
└── requirements.txt            # Зависимости (для совместимости)
```

---

## Шаг 1: Создание базовой структуры

```bash
# Убедитесь, что вы в корне проекта learnhub/
# и виртуальное окружение активировано

# Создайте папку backend
mkdir backend
cd backend

# Создайте Django проект conf
django-admin startproject conf .

# Создайте папку для приложений
mkdir apps
touch apps/__init__.py
```

---

## Шаг 2: Создание приложения users

```bash
# Находясь в backend/
python manage.py startapp users
mv users apps/

# Создайте файл models.py с кастомной моделью User
```

**Создайте `backend/apps/users/models.py`:**

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    telegram_id = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name='Telegram ID'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
```

**Обновите `backend/apps/users/apps.py`:**

```python
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
```

**Создайте `backend/apps/users/admin.py`:**

```python
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'telegram_id', 'is_staff']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
```

---

## Шаг 3: Обновление settings.py

**Откройте `backend/conf/settings.py` и внесите изменения:**

### 1. Импорты в начале файла:

```python
from pathlib import Path
from decouple import config
```

### 2. Измените SECRET_KEY и DEBUG:

```python
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

### 3. Добавьте приложения в INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps
    'apps.users',
    'apps.courses',  # добавим на следующем шаге
    
    # Third-party
    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_spectacular',
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
]
```

### 4. Укажите кастомную модель User:

```python
AUTH_USER_MODEL = 'users.User'
```

### 5. Настройте базу данных:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

### 6. Настройте DRF:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

### 7. Настройте drf-spectacular:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'LearnHub API',
    'DESCRIPTION': '''
    Система управления онлайн-обучением с ролями участников:

    - **INSTRUCTOR**: преподаватель курса, полный доступ
    - **TEACHING_ASSISTANT**: ассистент преподавателя
    - **STUDENT**: студент курса
    - **OBSERVER**: наблюдатель, только чтение
    ''',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
}
```

### 8. Настройте CORS (если нужно для фронтенда):

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]
```

### 9. Добавьте MIDDLEWARE для CORS:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Добавить
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

## Шаг 4: Создание .env файла

```bash
# Скопируйте шаблон
cp ../.env.example ../.env

# Отредактируйте .env с вашими настройками
```

**Пример `.env`:**

```env
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True

DB_NAME=learnhub_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Шаг 5: Создание базы данных PostgreSQL

```bash
# Подключитесь к PostgreSQL
psql -U postgres

# Создайте базу данных
CREATE DATABASE learnhub_db;

# Выйдите
\q
```

---

## Шаг 6: Применение миграций

```bash
# Находясь в backend/
python manage.py makemigrations
python manage.py migrate
```

---

## Шаг 7: Создание суперпользователя

```bash
python manage.py createsuperuser
```

---

## Шаг 8: Тестовый запуск

```bash
python manage.py runserver
```

Откройте в браузере:
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/

---

## Шаг 9: Настройка conftest.py для pytest

**Создайте `backend/conftest.py`:**

```python
import pytest
from apps.users.models import User
from rest_framework.test import APIClient


@pytest.fixture
def user(db):
    """Базовый пользователь для тестов"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def auth_client(user):
    """Авторизованный API клиент"""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def create_user(db):
    """Фабрика для создания пользователей"""
    def _create_user(username, **kwargs):
        defaults = {
            'email': f'{username}@example.com',
            'password': 'testpass123',
        }
        defaults.update(kwargs)
        return User.objects.create_user(username=username, **defaults)
    return _create_user
```

---

## ✅ Проверка установки

```bash
# Запустите тесты (должно быть 0 тестов, это нормально)
pytest

# Проверьте что Django запускается
python manage.py check

# Проверьте миграции
python manage.py showmigrations
```

---

## 🎯 Готово! Базовый проект настроен

Теперь можно переходить к **Шагу 1: Создание приложения courses**!
