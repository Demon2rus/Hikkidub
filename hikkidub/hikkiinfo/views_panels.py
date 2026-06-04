"""Панели модератора и переводчика HikkiDub.

Доступ:
- /moderate/  — пользователи в группе "Модераторы"
- /translate/ — пользователи в группе "Переводчики"
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import AnimeForm, EpisodeForm, SubtitleForm
from .models import Anime, Episode, Subtitle, Genre


# ---------------------------------------------------------------------------
# Декораторы доступа
# ---------------------------------------------------------------------------
def moderator_required(view):
    """Доступ только для модераторов (и админов)."""
    return user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name='Модераторы').exists(),
        login_url='login'
    )(login_required(view))


def translator_required(view):
    """Доступ только для переводчиков (и админов)."""
    return user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name='Переводчики').exists(),
        login_url='login'
    )(login_required(view))


# =========================================================================
# ПАНЕЛЬ МОДЕРАТОРА
# =========================================================================

@moderator_required
def moderate_dashboard(request):
    """Дашборд модератора: список аниме, быстрые действия."""
    anime_list = Anime.objects.prefetch_related('genres').order_by('-updated_at')
    total_anime = anime_list.count()
    total_episodes = Episode.objects.count()
    pending_episodes = Episode.objects.filter(is_published=False).count()
    stats = {
        'total_anime': total_anime,
        'total_episodes': total_episodes,
        'pending_episodes': pending_episodes,
    }
    return render(request, 'hikkiinfo/moderate/dashboard.html', {
        'anime_list': anime_list,
        'stats': stats,
    })


@moderator_required
def moderate_add_anime(request):
    """Добавление нового аниме."""
    if request.method == 'POST':
        form = AnimeForm(request.POST, request.FILES)
        if form.is_valid():
            anime = form.save()
            messages.success(request, f'Аниме «{anime.title}» добавлено!')
            return redirect('moderate_dashboard')
    else:
        form = AnimeForm()
    return render(request, 'hikkiinfo/moderate/anime_form.html', {
        'form': form,
        'action': 'Добавить аниме',
    })


@moderator_required
def moderate_edit_anime(request, anime_id):
    """Редактирование аниме."""
    anime = get_object_or_404(Anime, pk=anime_id)
    if request.method == 'POST':
        form = AnimeForm(request.POST, request.FILES, instance=anime)
        if form.is_valid():
            form.save()
            messages.success(request, f'Аниме «{anime.title}» обновлено!')
            return redirect('moderate_dashboard')
    else:
        form = AnimeForm(instance=anime)
    return render(request, 'hikkiinfo/moderate/anime_form.html', {
        'form': form,
        'anime': anime,
        'action': 'Редактировать аниме',
    })


@moderator_required
def moderate_add_episode(request, anime_id):
    """Добавление эпизода к аниме."""
    anime = get_object_or_404(Anime, pk=anime_id)
    if request.method == 'POST':
        form = EpisodeForm(request.POST, request.FILES)
        if form.is_valid():
            episode = form.save(commit=False)
            episode.anime = anime
            episode.save()
            messages.success(request, f'Эпизод {episode.number} добавлен к «{anime.title}»!')
            return redirect('moderate_dashboard')
    else:
        next_number = anime.episodes.count() + 1
        form = EpisodeForm(initial={'number': next_number, 'duration_seconds': anime.duration_per_episode * 60})
    return render(request, 'hikkiinfo/moderate/episode_form.html', {
        'form': form,
        'anime': anime,
        'action': 'Добавить эпизод',
    })


@moderator_required
def moderate_edit_episode(request, episode_id):
    """Редактирование эпизода."""
    episode = get_object_or_404(Episode.objects.select_related('anime'), pk=episode_id)
    if request.method == 'POST':
        form = EpisodeForm(request.POST, request.FILES, instance=episode)
        if form.is_valid():
            form.save()
            messages.success(request, f'Эпизод обновлён!')
            return redirect('moderate_dashboard')
    else:
        form = EpisodeForm(instance=episode)
    return render(request, 'hikkiinfo/moderate/episode_form.html', {
        'form': form,
        'anime': episode.anime,
        'episode': episode,
        'action': 'Редактировать эпизод',
    })


# =========================================================================
# ПАНЕЛЬ ПЕРЕВОДЧИКА
# =========================================================================

@translator_required
def translate_dashboard(request):
    """Дашборд переводчика: список эпизодов и статус субтитров."""
    episodes = Episode.objects.select_related('anime').filter(
        is_published=True
    ).prefetch_related('subtitles').order_by('-created_at')

    episode_data = []
    for ep in episodes:
        subs = list(ep.subtitles.all())
        lang_codes = {s.language for s in subs}
        episode_data.append({
            'episode': ep,
            'subtitles': subs,
            'has_ru': 'ru' in lang_codes,
            'has_en': 'en' in lang_codes,
            'needs_ru': 'ru' not in lang_codes,
            'needs_en': 'en' not in lang_codes,
        })

    total_episodes = len(episode_data)
    missing_ru = sum(1 for d in episode_data if d['needs_ru'])
    missing_en = sum(1 for d in episode_data if d['needs_en'])

    return render(request, 'hikkiinfo/translate/dashboard.html', {
        'episode_data': episode_data,
        'stats': {
            'total_episodes': total_episodes,
            'missing_ru': missing_ru,
            'missing_en': missing_en,
        },
    })


@translator_required
def translate_edit_subtitle(request, episode_id, language):
    """Добавление или редактирование субтитров для эпизода."""
    episode = get_object_or_404(Episode.objects.select_related('anime'), pk=episode_id)
    subtitle = Subtitle.objects.filter(episode=episode, language=language).first()

    if request.method == 'POST':
        form = SubtitleForm(request.POST, instance=subtitle)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.episode = episode
            sub.language = language
            sub.save()
            lang_label = dict(Subtitle.LANGUAGE_CHOICES).get(language, language)
            messages.success(request, f'Субтитры ({lang_label}) сохранены для эпизода {episode.number}!')
            return redirect('translate_dashboard')
    else:
        form = SubtitleForm(instance=subtitle)

    return render(request, 'hikkiinfo/translate/subtitle_form.html', {
        'form': form,
        'episode': episode,
        'subtitle': subtitle,
        'language': language,
        'language_label': dict(Subtitle.LANGUAGE_CHOICES).get(language, language),
    })
