"""Генерация постеров для аниме через AutoGLM Image API.

Использование:
    python manage.py generate_posters                    # все аниме без постеров
    python manage.py generate_posters --slug=anime-slug  # конкретное аниме
    python manage.py generate_posters --force            # перегенерировать все (даже с постерами)
"""
import hashlib
import json
import os
import sys
import time
import tempfile
import urllib.request
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from hikkiinfo.models import Anime


APP_ID = "100003"
APP_KEY = "38d2391985e2369a5fb8227d8e6cd5e5"
API_URL = "https://autoglm-api.autoglm.ai/agentdr/v1/assistant/skills/generate-image"
TOKEN_URL = "http://127.0.0.1:18432/get_token"


def get_token():
    """Получает токен авторизации от локального сервиса."""
    try:
        with urllib.request.urlopen(TOKEN_URL) as resp:
            token = resp.read().decode("utf-8").strip()
    except Exception as e:
        raise RuntimeError(f"Не удалось получить токен: {e}")
    if not token:
        raise RuntimeError("Токен пуст.")
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    return token


def generate_poster_image(prompt):
    """Генерирует изображение через AutoGLM API, возвращает bytes."""
    token = get_token()
    timestamp = str(int(time.time()))
    sign_data = f"{APP_ID}&{timestamp}&{APP_KEY}"
    sign = hashlib.md5(sign_data.encode("utf-8")).hexdigest()

    payload = json.dumps({"text": prompt}).encode("utf-8")
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "X-Auth-Appid": APP_ID,
        "X-Auth-TimeStamp": timestamp,
        "X-Auth-Sign": sign,
    }

    req = urllib.request.Request(API_URL, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    if result.get("code") != 0:
        raise RuntimeError(f"API ошибка: {result.get('msg', 'неизвестная ошибка')}")

    image_url = result.get("data", {}).get("image_url")
    if not image_url:
        raise RuntimeError("API не вернул image_url")

    # Скачиваем изображение
    with urllib.request.urlopen(image_url) as resp:
        return resp.read()


class Command(BaseCommand):
    help = 'Генерирует AI-постеры для аниме через AutoGLM Image API'

    def add_arguments(self, parser):
        parser.add_argument('--slug', help='Slug конкретного аниме')
        parser.add_argument('--force', action='store_true', help='Перегенерировать все, включая с постерами')

    def handle(self, *args, **options):
        slug = options.get('slug')
        force = options.get('force')

        if slug:
            queryset = Anime.objects.filter(slug=slug)
            if not queryset.exists():
                self.stdout.write(self.style.ERROR(f'Аниме со slug "{slug}" не найдено.'))
                return
        elif force:
            queryset = Anime.objects.all()
        else:
            queryset = Anime.objects.filter(poster='')

        if not queryset.exists():
            self.stdout.write('Нет аниме для генерации постеров.')
            return

        self.stdout.write(f'Найдено аниме для генерации: {queryset.count()}')

        for anime in queryset:
            self.stdout.write(f'\nГенерация постера для: {anime.title}')
            prompt = self._build_prompt(anime)

            try:
                image_bytes = generate_poster_image(prompt)
                filename = f"{anime.slug or anime.pk}_ai_poster.png"
                anime.poster.save(filename, ContentFile(image_bytes), save=True)
                self.stdout.write(self.style.SUCCESS(f'  OK! Постер сохранён.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  Ошибка: {e}'))

        self.stdout.write(self.style.SUCCESS('\nГотово!'))

    def _build_prompt(self, anime):
        """Строит промпт для генерации на основе данных аниме."""
        parts = [
            "Anime-style poster illustration",
            f"for anime titled '{anime.title}'",
        ]
        if anime.title_original:
            parts.append(f"(original: {anime.title_original})")
        if anime.description:
            # Берём первые 200 символов описания
            desc = anime.description[:200]
            parts.append(f"depicting: {desc}")
        parts.extend([
            "Vertical poster format, 2:3 aspect ratio",
            "High quality digital art, vibrant colors, cinematic lighting",
            "Professional anime key visual style, clean composition",
        ])
        return ", ".join(parts)
