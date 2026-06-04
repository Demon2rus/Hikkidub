from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Anime, Episode, Subtitle, Genre


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Логин",
        max_length=150,
        widget=forms.TextInput(attrs={"autocomplete": "username"}),
    )
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")


class AnimeForm(forms.ModelForm):
    """Форма добавления/редактирования аниме."""

    class Meta:
        model = Anime
        fields = [
            'title', 'title_original', 'description', 'poster',
            'release_date', 'status', 'genres', 'rating',
            'duration_per_episode', 'is_featured',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'genres': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'title': 'Название',
            'title_original': 'Оригинальное название',
            'description': 'Описание',
            'poster': 'Постер',
            'release_date': 'Дата выхода',
            'status': 'Статус',
            'genres': 'Жанры',
            'rating': 'Рейтинг (0-10)',
            'duration_per_episode': 'Длительность эпизода (мин)',
            'is_featured': 'Рекомендуемое',
        }


class EpisodeForm(forms.ModelForm):
    """Форма добавления/редактирования эпизода."""

    class Meta:
        model = Episode
        fields = [
            'number', 'title', 'description', 'duration_seconds',
            'video_file', 'is_published', 'release_date',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'number': 'Номер эпизода',
            'title': 'Название эпизода',
            'description': 'Описание',
            'duration_seconds': 'Длительность (секунды)',
            'video_file': 'Видеофайл',
            'is_published': 'Опубликовать',
            'release_date': 'Дата выхода',
        }
        help_texts = {
            'duration_seconds': 'Например: 1440 = 24 минуты',
        }


class SubtitleForm(forms.ModelForm):
    """Форма добавления/редактирования субтитров (VTT)."""

    class Meta:
        model = Subtitle
        fields = ['vtt_content']
        widgets = {
            'vtt_content': forms.Textarea(attrs={
                'rows': 20,
                'placeholder': 'WEBVTT\n\n00:00:01.000 --> 00:00:05.000\nТекст субтитров...\n\n00:00:06.000 --> 00:00:10.000\nСледующая строка...',
            }),
        }
        labels = {
            'vtt_content': 'Содержимое VTT',
        }
