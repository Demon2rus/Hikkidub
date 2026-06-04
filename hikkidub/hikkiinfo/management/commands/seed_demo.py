"""Наполнение базы демонстрационными данными для защиты диплома.

Использование:
    python manage.py seed_demo              # базовое наполнение
    python manage.py seed_demo --posters    # + генерация AI-постеров
"""
import textwrap
from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from hikkiinfo.models import Genre, Anime, Episode, VoiceActor, Character, Subtitle


# =========================================================================
# ДЕМО-ДАННЫЕ
# =========================================================================

GENRES = [
    {"name": "Сёнэн", "description": "Аниме для юношей: приключения, битвы, дружба."},
    {"name": "Драма", "description": "Эмоциональные истории с глубокими персонажами."},
    {"name": "Фэнтези", "description": "Магия, другие миры, мифические существа."},
    {"name": "Романтика", "description": "Истории о любви и отношениях."},
    {"name": "Комедия", "description": "Юмор, пародии, забавные ситуации."},
    {"name": "Приключения", "description": "Путешествия, исследования, открытия."},
    {"name": "Фантастика", "description": "Технологии будущего, роботы, космос."},
    {"name": "Психология", "description": "Внутренний мир, размышления, триллер."},
]

ANIME_DATA = [
    {
        "title": "Хроники Этериума",
        "title_original": "Etherium Chronicles",
        "description": (
            "В мире, где магия и технологии сплелись воедино, юный Кайто discovers в себе "
            "способность управлять этериумом — энергией, пронизывающей всё сущее. Вместе с "
            "командой друзей он отправляется в опасное путешествие, чтобы предотвратить войну "
            "между Гильдией Магов и Корпорацией Техномантов. Каждый эпизод раскрывает новые "
            "грани этого удивительного мира, где древние заклинания встречаются с передовыми технологиями."
        ),
        "release_date": date(2025, 9, 15),
        "status": "ongoing",
        "rating": 8.7,
        "duration_per_episode": 24,
        "is_featured": True,
        "genres": ["Фэнтези", "Приключения", "Сёнэн"],
        "episodes": [
            {"number": 1, "title": "Пробуждение", "is_published": True, "release_date": date(2025, 9, 15)},
            {"number": 2, "title": "Тени прошлого", "is_published": True, "release_date": date(2025, 9, 22)},
            {"number": 3, "title": "Испытание", "is_published": True, "release_date": date(2025, 9, 29)},
            {"number": 4, "title": "Союзники", "is_published": True, "release_date": date(2025, 10, 6)},
            {"number": 5, "title": "Битва за Этериум", "is_published": True, "release_date": date(2025, 10, 13)},
            {"number": 6, "title": "Новый рассвет", "is_published": False, "release_date": date(2025, 10, 20)},
        ],
        "characters": [
            {"name": "Кайто", "role": "Главный герой", "voice_actor": "Алексей Смирнов"},
            {"name": "Юки", "role": "Подруга детства", "voice_actor": "Мария Иванова"},
            {"name": "Мастер Року", "role": "Наставник", "voice_actor": "Владимир Петров"},
        ],
    },
    {
        "title": "Зеркальный Лабиринт",
        "title_original": "Mirror Labyrinth",
        "description": (
            "Группа студентов попадает в загадочный лабиринт, где каждое зеркало показывает "
            "альтернативную реальность. Чтобы выбраться, им нужно пройти через свои самые глубокие "
            "страхи. Психологический триллер с элементами хоррора, где каждый выбор имеет "
            "необратимые последствия. Сериал исследует темы идентичности, выбора и цены, "
            "которую мы платим за свои решения."
        ),
        "release_date": date(2025, 7, 1),
        "status": "completed",
        "rating": 9.1,
        "duration_per_episode": 22,
        "is_featured": True,
        "genres": ["Психология", "Драма", "Фантастика"],
        "episodes": [
            {"number": 1, "title": "Вход", "is_published": True, "release_date": date(2025, 7, 1)},
            {"number": 2, "title": "Первое отражение", "is_published": True, "release_date": date(2025, 7, 8)},
            {"number": 3, "title": "Голоса", "is_published": True, "release_date": date(2025, 7, 15)},
            {"number": 4, "title": "Точка невозврата", "is_published": True, "release_date": date(2025, 7, 22)},
        ],
        "characters": [
            {"name": "Рэн", "role": "Лидер группы", "voice_actor": "Дмитрий Волков"},
            {"name": "Акари", "role": "Аналитик", "voice_actor": "Анна Кузнецова"},
        ],
    },
    {
        "title": "Космический Патруль: Звёздный Путь",
        "title_original": "Space Patrol: Star Path",
        "description": (
            "2478 год. Человечество колонизировало десятки планет. Космический Патруль — "
            "элитное подразделение, охраняющее мир между колониями. Капитан Элис Хантер и её "
            "экипаж корабля «Нова» расследуют загадочные исчезновения кораблей на окраинах "
            "галактики. То, что начиналось как обычное расследование, превращается в борьбу "
            "за судьбу всей цивилизации."
        ),
        "release_date": date(2026, 2, 10),
        "status": "ongoing",
        "rating": 8.3,
        "duration_per_episode": 25,
        "is_featured": True,
        "genres": ["Фантастика", "Приключения", "Сёнэн"],
        "episodes": [
            {"number": 1, "title": "Сигнал из пустоты", "is_published": True, "release_date": date(2026, 2, 10)},
            {"number": 2, "title": "Гравитационная ловушка", "is_published": True, "release_date": date(2026, 2, 17)},
            {"number": 3, "title": "Неизвестная форма жизни", "is_published": True, "release_date": date(2026, 2, 24)},
        ],
        "characters": [
            {"name": "Элис Хантер", "role": "Капитан", "voice_actor": "Елена Соколова"},
            {"name": "Джек", "role": "Инженер", "voice_actor": "Алексей Смирнов"},
        ],
    },
    {
        "title": "Цветок Сакуры",
        "title_original": "Sakura no Hana",
        "description": (
            "Трогательная история о Миюки — девушке, которая после переезда в Токио находит "
            "старый дневник своей бабушки. Через записи она узнаёт о первой любви, войне, "
            "потерях и надежде. Параллельно разворачивается история самой Миюки, которая "
            "влюбляется в одноклассника — талантливого художника. Две любовные линии, "
            "разделённые десятилетиями, переплетаются в удивительном финале."
        ),
        "release_date": date(2025, 11, 20),
        "status": "completed",
        "rating": 9.4,
        "duration_per_episode": 23,
        "is_featured": True,
        "genres": ["Романтика", "Драма"],
        "episodes": [
            {"number": 1, "title": "Переезд", "is_published": True, "release_date": date(2025, 11, 20)},
            {"number": 2, "title": "Дневник", "is_published": True, "release_date": date(2025, 11, 27)},
            {"number": 3, "title": "Весна 1942", "is_published": True, "release_date": date(2025, 12, 4)},
            {"number": 4, "title": "Первый поцелуй", "is_published": True, "release_date": date(2025, 12, 11)},
            {"number": 5, "title": "Расставание", "is_published": True, "release_date": date(2025, 12, 18)},
            {"number": 6, "title": "Воссоединение", "is_published": True, "release_date": date(2025, 12, 25)},
        ],
        "characters": [
            {"name": "Миюки", "role": "Главная героиня", "voice_actor": "Мария Иванова"},
            {"name": "Харуто", "role": "Художник", "voice_actor": "Дмитрий Волков"},
            {"name": "Бабушка Харука", "role": "Бабушка Миюки", "voice_actor": "Татьяна Морозова"},
        ],
    },
    {
        "title": "Школа Демонов: Перерождение",
        "title_original": "Demon School: Rebirth",
        "description": (
            "Обычный школьник Такаси погибает в аварии и перерождается в младшем классе "
            "Школы Демонов — престижного учебного заведения в Подземном мире. Теперь ему "
            "нужно не только освоить демонические способности, но и скрыть тот факт, что "
            "в прошлой жизни он был человеком. Комедийное фэнтези с яркими персонажами и "
            "неожиданными поворотами сюжета."
        ),
        "release_date": date(2026, 1, 5),
        "status": "ongoing",
        "rating": 8.5,
        "duration_per_episode": 24,
        "is_featured": False,
        "genres": ["Фэнтези", "Комедия", "Сёнэн"],
        "episodes": [
            {"number": 1, "title": "Смерть и перерождение", "is_published": True, "release_date": date(2026, 1, 5)},
            {"number": 2, "title": "Первый день в аду", "is_published": True, "release_date": date(2026, 1, 12)},
            {"number": 3, "title": "Демонический экзамен", "is_published": True, "release_date": date(2026, 1, 19)},
            {"number": 4, "title": "Друзья или враги?", "is_published": True, "release_date": date(2026, 1, 26)},
            {"number": 5, "title": "Фестиваль Тьмы", "is_published": True, "release_date": date(2026, 2, 2)},
        ],
        "characters": [
            {"name": "Такаси / Рэй", "role": "Главный герой", "voice_actor": "Алексей Смирнов"},
            {"name": "Лилит", "role": "Староста класса", "voice_actor": "Анна Кузнецова"},
            {"name": "Директор Баал", "role": "Директор школы", "voice_actor": "Владимир Петров"},
        ],
    },
]

VOICE_ACTORS = [
    {"name": "Алексей Смирнов", "bio": "Ведущий актёр озвучки HikkiDub. Голос главных героев в большинстве проектов."},
    {"name": "Мария Иванова", "bio": "Актриса озвучки, специализируется на женских главных ролях. Работает в дубляже с 2019 года."},
    {"name": "Владимир Петров", "bio": "Ветеран озвучки. Голос наставников, злодеев и харизматичных персонажей."},
    {"name": "Дмитрий Волков", "bio": "Молодой актёр. Романтические герои, бунтари, сложные драматические роли."},
    {"name": "Анна Кузнецова", "bio": "Актриса широкого профиля — от комедийных до драматических ролей."},
    {"name": "Елена Соколова", "bio": "Специализируется на сильных женских персонажах."},
    {"name": "Татьяна Морозова", "bio": "Голос возрастных персонажей, рассказчиков, мудрых наставниц."},
]

SAMPLE_VTT_RU = textwrap.dedent("""\
WEBVTT

00:00:01.000 --> 00:00:05.000
Добро пожаловать в этот удивительный мир!

00:00:06.000 --> 00:00:12.000
Сегодня мы отправляемся в путешествие, полное открытий.

00:00:13.000 --> 00:00:18.000
Ты готов? Тогда поехали!

00:00:19.000 --> 00:00:25.000
Каждое решение, которое ты примешь, изменит твою судьбу.

00:00:26.000 --> 00:00:32.000
Но помни: даже в самой глубокой тьме есть луч света.

00:00:33.000 --> 00:00:40.000
Смотри внимательно. Слушай. Чувствуй.

00:00:41.000 --> 00:00:48.000
Потому что история только начинается...
""")

SAMPLE_VTT_EN = textwrap.dedent("""\
WEBVTT

00:00:01.000 --> 00:00:05.000
Welcome to this amazing world!

00:00:06.000 --> 00:00:12.000
Today we embark on a journey full of discoveries.

00:00:13.000 --> 00:00:18.000
Are you ready? Then let's go!

00:00:19.000 --> 00:00:25.000
Every decision you make will change your destiny.

00:00:26.000 --> 00:00:32.000
But remember: even in the deepest darkness, there's a ray of light.

00:00:33.000 --> 00:00:40.000
Watch carefully. Listen. Feel.

00:00:41.000 --> 00:00:48.000
Because the story is just beginning...
""")


class Command(BaseCommand):
    help = 'Наполняет базу демонстрационными данными'

    def add_arguments(self, parser):
        parser.add_argument('--posters', action='store_true', help='Генерировать AI-постеры после наполнения')

    def handle(self, *args, **options):
        self.stdout.write('=== Наполнение базы HikkiDub ===\n')

        # 1. Жанры
        self._create_genres()

        # 2. Актёры озвучки
        self._create_voice_actors()

        # 3. Аниме, эпизоды, персонажи
        self._create_anime()

        # 4. Субтитры (для первых эпизодов каждого аниме)
        self._create_subtitles()

        # 5. Пользователи
        self._create_users()

        # 6. Итоги
        self._print_summary()

        # 7. Генерация постеров
        if options.get('posters'):
            self.stdout.write('\nЗапуск генерации AI-постеров...')
            from django.core.management import call_command
            call_command('generate_posters')

    def _create_genres(self):
        for data in GENRES:
            g, created = Genre.objects.get_or_create(name=data['name'], defaults={'description': data['description']})
            if created:
                self.stdout.write(f'  + Жанр: {g.name}')
        self.stdout.write(self.style.SUCCESS(f'Жанров: {Genre.objects.count()}'))

    def _create_voice_actors(self):
        for data in VOICE_ACTORS:
            va, created = VoiceActor.objects.get_or_create(name=data['name'], defaults={'bio': data['bio']})
            if created:
                self.stdout.write(f'  + Актёр: {va.name}')
        self.stdout.write(self.style.SUCCESS(f'Актёров озвучки: {VoiceActor.objects.count()}'))

    def _create_anime(self):
        for data in ANIME_DATA:
            genre_names = data.pop('genres')
            episodes_data = data.pop('episodes')
            characters_data = data.pop('characters')

            anime, created = Anime.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                anime.genres.set(Genre.objects.filter(name__in=genre_names))
                self.stdout.write(f'  + Аниме: {anime.title}')
            else:
                self.stdout.write(f'  = Аниме уже есть: {anime.title}')

            # Эпизоды
            for ep_data in episodes_data:
                ep, ep_created = Episode.objects.get_or_create(
                    anime=anime,
                    number=ep_data['number'],
                    defaults=ep_data
                )
                if ep_created:
                    self.stdout.write(f'    + Эпизод {ep.number}: {ep.title or "(без названия)"}')

            # Персонажи
            for char_data in characters_data:
                va = VoiceActor.objects.filter(name=char_data['voice_actor']).first()
                char, char_created = Character.objects.get_or_create(
                    anime=anime,
                    name=char_data['name'],
                    defaults={'voice_actor': va, 'description': f'Роль: {char_data["role"]}'}
                )
                if char_created:
                    self.stdout.write(f'    + Персонаж: {char.name} ({char_data["role"]})')

        self.stdout.write(self.style.SUCCESS(f'Аниме: {Anime.objects.count()}, Эпизодов: {Episode.objects.count()}, Персонажей: {Character.objects.count()}'))

    def _create_subtitles(self):
        count = 0
        for anime in Anime.objects.all():
            first_ep = anime.episodes.filter(is_published=True).order_by('number').first()
            if not first_ep:
                continue

            # Русские субтитры
            sub_ru, created_ru = Subtitle.objects.get_or_create(
                episode=first_ep,
                language='ru',
                defaults={'vtt_content': SAMPLE_VTT_RU}
            )
            if created_ru:
                count += 1

            # Английские субтитры
            sub_en, created_en = Subtitle.objects.get_or_create(
                episode=first_ep,
                language='en',
                defaults={'vtt_content': SAMPLE_VTT_EN}
            )
            if created_en:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Субтитров: {Subtitle.objects.count()} (добавлено: {count})'))

    def _create_users(self):
        # Модератор
        mod_group = Group.objects.get(name='Модераторы')
        mod_user, mod_created = User.objects.get_or_create(
            username='moderator',
            defaults={'email': 'mod@hikkidub.local'}
        )
        if mod_created:
            mod_user.set_password('moderator123')
            mod_user.groups.add(mod_group)
            mod_user.save()
            self.stdout.write('  + Модератор: moderator / moderator123')

        # Переводчик
        tr_group = Group.objects.get(name='Переводчики')
        tr_user, tr_created = User.objects.get_or_create(
            username='translator',
            defaults={'email': 'tr@hikkidub.local'}
        )
        if tr_created:
            tr_user.set_password('translator123')
            tr_user.groups.add(tr_group)
            tr_user.save()
            self.stdout.write('  + Переводчик: translator / translator123')

        # Обычный пользователь
        user, u_created = User.objects.get_or_create(
            username='viewer',
            defaults={'email': 'viewer@hikkidub.local'}
        )
        if u_created:
            user.set_password('viewer123')
            user.save()
            self.stdout.write('  + Зритель: viewer / viewer123')

        self.stdout.write(self.style.SUCCESS(f'Пользователей: {User.objects.count()}'))

    def _print_summary(self):
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('НАПОЛНЕНИЕ ЗАВЕРШЕНО'))
        self.stdout.write('=' * 50)
        self.stdout.write(f'  Жанры:         {Genre.objects.count()}')
        self.stdout.write(f'  Аниме:         {Anime.objects.count()}')
        self.stdout.write(f'  Эпизоды:       {Episode.objects.count()}')
        self.stdout.write(f'  Персонажи:     {Character.objects.count()}')
        self.stdout.write(f'  Актёры озвучки: {VoiceActor.objects.count()}')
        self.stdout.write(f'  Субтитры:      {Subtitle.objects.count()}')
        self.stdout.write(f'  Пользователи:  {User.objects.count()}')
        self.stdout.write('\n  Учётные записи:')
        self.stdout.write('    admin       / admin         (администратор)')
        self.stdout.write('    moderator   / moderator123  (модератор)')
        self.stdout.write('    translator  / translator123 (переводчик)')
        self.stdout.write('    viewer      / viewer123     (зритель)')
        self.stdout.write('=' * 50 + '\n')
