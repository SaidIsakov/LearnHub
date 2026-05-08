# 🎓 LearnHub

> Современная платформа для онлайн-обучения с гибкой системой ролей

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-5.0+-green.svg)](https://www.djangoproject.com/)
[![DRF Version](https://img.shields.io/badge/DRF-3.14+-orange.svg)](https://www.django-rest-framework.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 О проекте

**LearnHub** — это RESTful API для управления онлайн-курсами, построенное на Django REST Framework. Система предоставляет гибкую ролевую модель доступа, позволяющую эффективно организовать процесс обучения для преподавателей, ассистентов и студентов.

### Основные возможности

- ✅ **Управление курсами** - создание, редактирование, публикация курсов
- ✅ **Ролевая система** - INSTRUCTOR, TEACHING_ASSISTANT, STUDENT, OBSERVER
- ✅ **Управление уроками** - структурированные материалы курса
- 🚧 **Домашние задания** - создание, сдача и проверка работ *(в разработке)*
- 🚧 **Тесты и квизы** - автоматизированная проверка знаний *(в разработке)*
- 🚧 **Уведомления** - интеграция с Telegram для напоминаний *(в разработке)*
- 🚧 **Аналитика** - статистика прогресса студентов *(в разработке)*

---

## 🏗️ Технологический стек

### Backend
- **Python 3.11+**
- **Django 5.0+** - веб-фреймворк
- **Django REST Framework** - API
- **PostgreSQL** - основная база данных
- **Redis** - кэширование и брокер сообщений
- **Celery** - асинхронные задачи
- **pytest** - тестирование

### Интеграции
- **Telegram Bot API** - уведомления пользователям
- **drf-spectacular** - автоматическая документация API (OpenAPI/Swagger)

---

## 📋 Требования

- Python 3.11 или выше
- PostgreSQL 14+
- Redis 6+
- pip или uv и virtualenv

---

## ⚙️ Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/YOUR_USERNAME/learnhub.git
cd learnhub
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
# или
venv\Scripts\activate  # для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DB_NAME=learnhub_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Telegram (опционально)
SOCIAL_AUTH_TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 5. Применение миграций

```bash
cd backend
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

API будет доступно по адресу: `http://localhost:8000/api/`

### 8. Запуск Celery (опционально)

```bash
# В отдельном терминале
celery -A conf worker -l info

# Для периодических задач
celery -A conf beat -l info
```

---

## 📚 API Документация

После запуска сервера документация доступна по адресам:

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

---

## 🧪 Тестирование

Запуск всех тестов:

```bash
pytest
```

Запуск с покрытием кода:

```bash
pytest --cov=apps --cov-report=html
```

Запуск конкретного модуля:

```bash
pytest apps/courses/tests/
```

---

## 📁 Структура проекта

```
learnhub/
├── backend/
│   ├── apps/
│   │   ├── courses/          # Управление курсами
│   │   │   ├── models.py     # Course, CourseMember, Lesson
│   │   │   ├── views.py      # ViewSets для API
│   │   │   ├── serializers.py
│   │   │   ├── permissions.py # Права доступа
│   │   │   └── tests/
│   │   ├── assignments/      # Домашние задания (в разработке)
│   │   ├── quizzes/          # Тесты и квизы (в разработке)
│   │   └── users/            # Пользователи
│   ├── conf/                 # Настройки проекта
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── celery.py
│   ├── manage.py
│   └── conftest.py           # Фикстуры для pytest
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔐 Роли и права доступа

| Действие | INSTRUCTOR | TEACHING_ASSISTANT | STUDENT | OBSERVER |
|----------|------------|-------------------|---------|----------|
| Создать курс | ✅ | ❌ | ❌ | ❌ |
| Редактировать курс | ✅ | ❌ | ❌ | ❌ |
| Удалить курс | ✅ | ❌ | ❌ | ❌ |
| Создать урок | ✅ | ✅ | ❌ | ❌ |
| Редактировать урок | ✅ | ✅ | ❌ | ❌ |
| Просмотр материалов | ✅ | ✅ | ✅ | ✅ |
| Создать задание | ✅ | ✅ | ❌ | ❌ |
| Сдать задание | ❌ | ❌ | ✅ | ❌ |
| Проверить задание | ✅ | ✅ | ❌ | ❌ |
| Просмотр оценок (своих) | ✅ | ✅ | ✅ | ❌ |
| Просмотр оценок (всех) | ✅ | ✅ | ❌ | ❌ |

---

## 🛣️ Roadmap

### ✅ Реализовано (v0.1)
- [x] Базовая структура проекта
- [x] Модели Course, CourseMember, Lesson
- [x] CRUD API для курсов
- [x] Ролевая система доступа
- [x] Базовые тесты

### 🚧 В разработке (v0.2)
- [ ] Модуль домашних заданий (Assignment, Submission)
- [ ] Система оценивания
- [ ] Дедлайны и напоминания
- [ ] Telegram-уведомления

### 📅 Планируется (v0.3+)
- [ ] Тесты и квизы с автопроверкой
- [ ] Прогресс студента по курсу
- [ ] Сертификаты о прохождении
- [ ] Комментарии к урокам
- [ ] Загрузка файлов (презентации, видео)
- [ ] Аналитика и отчёты
- [ ] GraphQL API (опционально)

---

## 🤝 Вклад в проект

Проект создан в образовательных целях. Если вы хотите предложить улучшения:

1. Форкните репозиторий
2. Создайте ветку для вашей фичи (`git checkout -b feature/AmazingFeature`)
3. Закоммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

---

## 👤 Автор

**[Ваше имя]**

- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your Profile](https://linkedin.com/in/your-profile)
- Email: your.email@example.com

---

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

---

## 🙏 Благодарности

- Вдохновлён реальными LMS-платформами (Moodle, Canvas)
- Основан на best practices Django REST Framework
- Использует паттерны из Django Task Manager

---

**⭐ Если проект был полезен, поставьте звёздочку!**
