"""Представления публичной части HikkiDub."""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import RegisterForm
from .models import Anime, Episode, Genre, VideoQuality, Subtitle


# ---------------------------------------------------------------------------
# Главная
# ---------------------------------------------------------------------------
def index(request):
    featured = Anime.objects.filter(is_featured=True, status__in=['ongoing', 'completed'])[:10]
    latest = Anime.objects.filter(status__in=['ongoing', 'completed']).order_by('-created_at')[:8]
    genres = Genre.objects.annotate(anime_count=Count('anime')).order_by('name')

    context = {
        'featured': featured,
        'latest': latest,
        'genres': genres,
    }
    return render(request, 'hikkiinfo/index.html', context)


# ---------------------------------------------------------------------------
# Каталог
# ---------------------------------------------------------------------------
def catalog(request):
    anime_list = Anime.objects.select_related().prefetch_related('genres').all()

    # Фильтры
    genre_slug = request.GET.get('genre')
    status = request.GET.get('status')
    search = request.GET.get('q', '').strip()

    if genre_slug:
        anime_list = anime_list.filter(genres__slug=genre_slug)
    if status:
        anime_list = anime_list.filter(status=status)
    if search:
        anime_list = anime_list.filter(
            Q(title__icontains=search) | Q(title_original__icontains=search) | Q(description__icontains=search)
        )

    anime_list = anime_list.order_by('-created_at')

    # Пагинация
    paginator = Paginator(anime_list, 12)
    page = request.GET.get('page', 1)
    try:
        anime_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        anime_page = paginator.page(1)

    genres = Genre.objects.annotate(anime_count=Count('anime')).order_by('name')
    statuses = Anime.STATUS_CHOICES

    context = {
        'anime_list': anime_page,
        'genres': genres,
        'statuses': statuses,
        'current_genre': genre_slug,
        'current_status': status,
        'search_query': search,
        'total_count': paginator.count,
    }
    return render(request, 'hikkiinfo/catalog.html', context)


# ---------------------------------------------------------------------------
# Страница аниме
# ---------------------------------------------------------------------------
def anime_detail(request, slug):
    anime = get_object_or_404(
        Anime.objects.prefetch_related('genres', 'episodes', 'characters__voice_actor'),
        slug=slug
    )
    episodes = anime.episodes.filter(is_published=True).order_by('number')
    characters = anime.characters.select_related('voice_actor').all()

    context = {
        'anime': anime,
        'episodes': episodes,
        'characters': characters,
    }
    return render(request, 'hikkiinfo/anime_detail.html', context)


# ---------------------------------------------------------------------------
# Просмотр эпизода (плеер)
# ---------------------------------------------------------------------------
def episode_detail(request, anime_slug, episode_number):
    anime = get_object_or_404(Anime, slug=anime_slug)
    episode = get_object_or_404(
        Episode.objects.select_related('anime').prefetch_related('video_qualities', 'subtitles'),
        anime=anime, number=episode_number, is_published=True
    )
    all_episodes = anime.episodes.filter(is_published=True).order_by('number')
    qualities = episode.video_qualities.filter(is_active=True).order_by('-quality')
    subtitles = episode.subtitles.all()

    # Инкремент просмотров
    episode.views_count += 1
    episode.save(update_fields=['views_count'])

    context = {
        'anime': anime,
        'episode': episode,
        'episodes': all_episodes,
        'qualities': qualities,
        'subtitles': subtitles,
        'active_quality': qualities.first(),
    }
    return render(request, 'hikkiinfo/episode_detail.html', context)


# ---------------------------------------------------------------------------
# AJAX: переключение качества видео
# ---------------------------------------------------------------------------
@require_POST
def switch_quality(request):
    """Возвращает URL видео для выбранного качества."""
    quality_id = request.POST.get('quality_id')
    if not quality_id:
        return JsonResponse({'error': 'quality_id required'}, status=400)

    quality = get_object_or_404(VideoQuality, pk=quality_id, is_active=True)
    return JsonResponse({
        'video_url': quality.video_url,
        'quality': quality.get_quality_display(),
    })


# ---------------------------------------------------------------------------
# AJAX: получение VTT субтитров
# ---------------------------------------------------------------------------
def subtitle_vtt(request, subtitle_id):
    """Возвращает содержимое субтитров как text/vtt для <track>."""
    subtitle = get_object_or_404(Subtitle, pk=subtitle_id)
    return JsonResponse({
        'vtt': subtitle.vtt_content,
        'language': subtitle.language,
        'label': subtitle.get_language_display(),
    })


# ---------------------------------------------------------------------------
# Аутентификация
# ---------------------------------------------------------------------------
def register(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Аккаунт создан. Вы вошли в систему.")
            return redirect("profile")
        messages.error(request, "Исправьте ошибки в форме.")
    else:
        form = RegisterForm()

    return render(request, "hikkiinfo/auth/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "hikkiinfo/auth/profile.html")


# ---------------------------------------------------------------------------
# Старые заглушки (оставлены для обратной совместимости)
# ---------------------------------------------------------------------------
def categories(request, anime_id):
    return redirect('catalog')


def categories_by_slug(request, anime_slug):
    return redirect('anime_detail', slug=anime_slug)


def player(request):
    """Старый плеер — редирект на каталог."""
    return redirect('catalog')
