from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from datetime import date


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название жанра")
    slug = models.SlugField(max_length=100, unique=True, blank=True, allow_unicode=True, verbose_name="URL-адрес")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Anime(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'В процессе'),
        ('completed', 'Завершено'),
        ('planned', 'Запланировано'),
        ('on_hold', 'Приостановлено'),
        ('cancelled', 'Отменено'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название")
    title_original = models.CharField(max_length=200, blank=True, verbose_name="Оригинальное название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, allow_unicode=True, verbose_name="URL-адрес")
    description = models.TextField(verbose_name="Описание")
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, verbose_name="Постер")
    release_date = models.DateField(
        verbose_name="Год выпуска",
        validators=[MinValueValidator(date(1900, 1, 1)), MaxValueValidator(date(2100, 12, 31))]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', verbose_name="Статус")
    genres = models.ManyToManyField(Genre, related_name='anime', verbose_name="Жанры")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, 
                                validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], 
                                verbose_name="Рейтинг")
    duration_per_episode = models.IntegerField(default=24, verbose_name="Длительность эпизода (мин)")
    total_episodes = models.IntegerField(default=0, verbose_name="Всего эпизодов")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемое")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Аниме"
        verbose_name_plural = "Аниме"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        # Fallback: если slugify вернул пустую строку (например, только спецсимволы)
        if not self.slug:
            self.slug = f'anime-{self.pk or ""}'
        super().save(*args, **kwargs)
        # Если slug был основан на pk (ещё не было), обновляем после save
        if self.slug == 'anime-':
            self.slug = f'anime-{self.pk}'
            super().save(update_fields=['slug'])

    def get_absolute_url(self):
        return reverse('anime_detail', kwargs={'slug': self.slug})

    @property
    def completed_episodes_count(self):
        return self.episodes.filter(is_published=True).count()


class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes', verbose_name="Аниме")
    number = models.IntegerField(verbose_name="Номер эпизода", validators=[MinValueValidator(1)])
    title = models.CharField(max_length=200, blank=True, verbose_name="Название эпизода")
    description = models.TextField(blank=True, verbose_name="Описание")
    duration_seconds = models.IntegerField(
        default=1440,
        validators=[MinValueValidator(1)],
        verbose_name="Длительность (секунды)"
    )
    video_file = models.FileField(
        upload_to='videos/%Y/%m/',
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'mkv'])],
        verbose_name="Видеофайл"
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    release_date = models.DateField(blank=True, null=True, verbose_name="Дата выхода")
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Эпизод"
        verbose_name_plural = "Эпизоды"
        ordering = ['anime', 'number']
        unique_together = ['anime', 'number']

    def __str__(self):
        return f"{self.anime.title} - Эпизод {self.number}"

    def get_absolute_url(self):
        return reverse('episode_detail', kwargs={'anime_slug': self.anime.slug, 'episode_number': self.number})

    @property
    def duration_display(self):
        """Возвращает длительность в формате MM:SS или HH:MM:SS."""
        total = self.duration_seconds
        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"

    @property
    def active_qualities(self):
        """Возвращает только активные качества видео."""
        return self.video_qualities.filter(is_active=True)

    @property
    def has_subtitles(self):
        """Проверяет, есть ли субтитры у эпизода."""
        return self.subtitles.exists()


class VideoQuality(models.Model):
    QUALITY_CHOICES = [
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('2160p', '2160p (4K)'),
    ]

    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='video_qualities', verbose_name="Эпизод")
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, verbose_name="Качество")
    video_url = models.URLField(verbose_name="URL видео")
    file_size = models.CharField(max_length=50, blank=True, verbose_name="Размер файла")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Качество видео"
        verbose_name_plural = "Качества видео"
        ordering = ['episode', '-quality']
        unique_together = ['episode', 'quality']

    def __str__(self):
        return f"{self.episode} - {self.quality}"


class VoiceActor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    slug = models.SlugField(max_length=100, unique=True, blank=True, allow_unicode=True, verbose_name="URL-адрес")
    bio = models.TextField(blank=True, verbose_name="Биография")
    photo = models.ImageField(upload_to='voice_actors/', blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Актер озвучки"
        verbose_name_plural = "Актеры озвучки"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Character(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя персонажа")
    name_original = models.CharField(max_length=100, blank=True, verbose_name="Оригинальное имя")
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='characters', verbose_name="Аниме")
    voice_actor = models.ForeignKey(VoiceActor, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='characters', verbose_name="Актер озвучки")
    description = models.TextField(blank=True, verbose_name="Описание")
    photo = models.ImageField(upload_to='characters/', blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"
        ordering = ['anime', 'name']

    def __str__(self):
        return f"{self.name} ({self.anime.title})"


class Subtitle(models.Model):
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'English'),
    ]

    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='subtitles', verbose_name="Эпизод")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, verbose_name="Язык")
    vtt_content = models.TextField(verbose_name="VTT-содержимое")
    is_auto_generated = models.BooleanField(default=False, verbose_name="Авто-сгенерировано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Субтитры"
        verbose_name_plural = "Субтитры"
        ordering = ['episode', 'language']
        unique_together = ['episode', 'language']

    def __str__(self):
        return f"{self.episode} — {self.get_language_display()}"


class DatabaseBackup(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название бэкапа")
    file_path = models.CharField(max_length=500, verbose_name="Путь к файлу")
    file_size = models.BigIntegerField(verbose_name="Размер файла (байт)")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    created_by = models.CharField(max_length=100, blank=True, verbose_name="Создано пользователем")
    
    class Meta:
        verbose_name = "Резервная копия БД"
        verbose_name_plural = "Резервные копии БД"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"
    
    def get_file_size_display(self):
        size = self.file_size
        for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} ТБ"
