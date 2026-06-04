# HikkiDub — платформа для просмотра аниме с русской озвучкой

<h1 align="center">
  <img src="https://img.shields.io/badge/Django-5.2-092E20?logo=django" alt="Django">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Status-Active-success" alt="Status">
</h1>

**HikkiDub** — веб-платформа для команды озвучки аниме. Позволяет загружать, организовывать и просматривать аниме-контент с субтитрами на русском и английском языках.

## 📸 Скриншоты

| Главная | Каталог | Плеер |
|---|---|---|

## 🚀 Возможности

### Для зрителей
- 🎬 Каталог аниме с фильтрацией по жанрам и статусу
- 🔍 Полнотекстовый поиск по названиям и описаниям
- 📺 Встроенный HTML5-плеер с переключением качества (480p–4K)
- 📝 Субтитры на русском и английском (WebVTT)
- 🌙 Тёмная / светлая тема
- 💾 Сохранение позиции просмотра
- 📱 Адаптивный дизайн (мобильные, планшеты, десктоп)

### Для модераторов
- ➕ Добавление и редактирование аниме (постер, описание, жанры, статус)
- 📤 Загрузка эпизодов с видеофайлами
- 🎭 Управление персонажами и актёрами озвучки
- 📊 Дашборд со статистикой

### Для переводчиков
- 🌐 Добавление субтитров (VTT) на русском и английском
- ✅ Таблица статуса перевода по всем эпизодам

### Для администраторов
- 🛡️ Полный доступ через Django Admin
- 💾 Резервное копирование и восстановление БД
- 🤖 AI-генерация постеров (AutoGLM API)

## 🏗️ Архитектура

```
Hikkidub/
├── hikkidub/                    # Django-проект
│   ├── hikkidub/                # Настройки проекта
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py / asgi.py
│   ├── hikkiinfo/               # Основное приложение
│   │   ├── models.py            # 8 моделей (Anime, Episode, Subtitle, ...)
│   │   ├── views.py             # Публичные представления
│   │   ├── views_panels.py      # Панели модератора и переводчика
│   │   ├── admin.py             # Кастомизированная админ-панель
│   │   ├── forms.py             # Формы (Anime, Episode, Subtitle, Register)
│   │   ├── signals.py           # Автоматические сигналы
│   │   ├── urls.py              # Маршруты (REST-like)
│   │   ├── management/commands/ # Кастомные команды
│   │   │   ├── setup_roles.py   # Создание ролей и групп
│   │   │   ├── seed_demo.py     # Наполнение демо-данными
│   │   │   └── generate_posters.py # AI-генерация постеров
│   │   └── templates/           # Шаблоны
│   ├── media/                   # Загружаемые файлы
│   └── manage.py
├── requirements.txt
├── env.example                  # Пример конфигурации
└── README.md
```

## 📊 Модели данных

| Модель | Описание | Ключевые поля |
|---|---|---|
| `Anime` | Аниме-тайтл | title, slug, poster, rating, status, genres |
| `Episode` | Эпизод | number, video_file, duration_seconds, views_count |
| `VideoQuality` | Качество видео | quality (480p–4K), video_url, is_active |
| `Subtitle` | Субтитры | language (ru/en), vtt_content |
| `Genre` | Жанр | name, slug, description |
| `Character` | Персонаж | name, anime FK, voice_actor FK |
| `VoiceActor` | Актёр озвучки | name, bio, photo |
| `DatabaseBackup` | Резервная копия | file_path, file_size, created_by |

## 🔐 Роли пользователей

| Роль | Группа | Права |
|---|---|---|
| **Администратор** | superuser | Полный доступ: админка, модерация, переводы |
| **Модератор** | Модераторы | Управление аниме, эпизодами, персонажами, жанрами |
| **Переводчик** | Переводчики | Добавление/редактирование субтитров |
| **Зритель** | — | Просмотр каталога и видео |

## ⚡ Быстрый старт

### Требования
- Python 3.11+
- SQLite (по умолчанию) или PostgreSQL

### Установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/ytkuramayt6-cloud/Hikkidub.git
cd Hikkidub/hikkidub

# 2. Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Применить миграции
python manage.py migrate

# 5. Создать роли и суперпользователя
python manage.py setup_roles --admin

# 6. Наполнить демо-данными (опционально)
python manage.py seed_demo

# 7. Запустить сервер
python manage.py runserver
```

Открыть в браузере: **http://127.0.0.1:8000/**

### Учётные записи (после seed_demo)

| Логин | Пароль | Роль |
|---|---|---|
| `admin` | `admin` | Администратор |
| `moderator` | `moderator123` | Модератор |
| `translator` | `translator123` | Переводчик |
| `viewer` | `viewer123` | Зритель |

### AI-генерация постеров

```bash
# Для всех аниме без постеров
python manage.py generate_posters

# Для конкретного аниме
python manage.py generate_posters --slug=tsvetok-sakury

# Перегенерировать все
python manage.py generate_posters --force
```

## 🌐 Маршруты

| URL | Страница | Доступ |
|---|---|---|
| `/` | Главная (хиро + рекомендуемое + новинки) | Все |
| `/catalog/` | Каталог с фильтрами и поиском | Все |
| `/anime/<slug>/` | Страница аниме | Все |
| `/anime/<slug>/episode/<n>/` | Плеер с субтитрами | Все |
| `/login/` / `/register/` | Аутентификация | Гости |
| `/moderate/` | Панель модератора | Модераторы |
| `/translate/` | Панель переводчика | Переводчики |
| `/admin/` | Django Admin | Админы |
| `/api/switch-quality/` | AJAX: смена качества | Все |
| `/api/subtitle/<id>/` | AJAX: получение VTT | Все |

## 🛠️ Технологический стек

| Категория | Технологии |
|---|---|
| **Backend** | Django 5.2, Python 3.11+ |
| **База данных** | SQLite (dev) / PostgreSQL (prod) |
| **Frontend** | HTML5, CSS3 (Custom Properties, Grid, Flexbox), Vanilla JS |
| **Плеер** | HTML5 `<video>` + WebVTT |
| **AI** | AutoGLM Image Generation API |
| **Дизайн** | Glassmorphism, тёмная/светлая тема, Manrope + Inter шрифты |

## 📝 Лицензия

Дипломный проект. Для ознакомительных целей.

---

*Разработано командой HikkiDub, 2025–2026*
