"""Команда для создания ролей и групп пользователей HikkiDub.

Использование:
    python manage.py setup_roles          # Создать группы и разрешения
    python manage.py setup_roles --admin  # + создать суперпользователя
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from hikkiinfo.models import Anime, Episode, VideoQuality, Genre, Character, VoiceActor, Subtitle


ROLES = {
    'Модераторы': {
        'models': [Anime, Episode, VideoQuality, Genre, Character, VoiceActor],
        'permissions': ['view', 'add', 'change', 'delete'],
        'readonly_models': [Subtitle],
    },
    'Переводчики': {
        'models': [Subtitle],
        'permissions': ['view', 'add', 'change', 'delete'],
        'readonly_models': [Anime, Episode],
    },
}


class Command(BaseCommand):
    help = 'Создаёт группы Модераторы и Переводчики с нужными разрешениями'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin',
            action='store_true',
            help='Создать суперпользователя admin/admin',
        )

    def handle(self, *args, **options):
        for group_name, config in ROLES.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана группа: {group_name}'))
            else:
                self.stdout.write(f'Группа уже существует: {group_name}')

            # Разрешения на полный доступ
            for model in config['models']:
                ct = ContentType.objects.get_for_model(model)
                for perm_code in config['permissions']:
                    codename = f'{perm_code}_{model._meta.model_name}'
                    try:
                        perm = Permission.objects.get(content_type=ct, codename=codename)
                        group.permissions.add(perm)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'  Разрешение не найдено: {codename}'))

            # Разрешения только на чтение
            for model in config.get('readonly_models', []):
                ct = ContentType.objects.get_for_model(model)
                try:
                    perm = Permission.objects.get(content_type=ct, codename=f'view_{model._meta.model_name}')
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  Разрешение не найдено: view_{model._meta.model_name}'))

            perm_count = group.permissions.count()
            self.stdout.write(f'  Назначено разрешений: {perm_count}')

        # Создание суперпользователя
        if options['admin']:
            if User.objects.filter(username='admin').exists():
                self.stdout.write('Суперпользователь admin уже существует.')
            else:
                User.objects.create_superuser('admin', 'admin@hikkidub.local', 'admin')
                self.stdout.write(self.style.SUCCESS('Создан суперпользователь: admin / admin'))

        self.stdout.write(self.style.SUCCESS('Готово! Роли настроены.'))
