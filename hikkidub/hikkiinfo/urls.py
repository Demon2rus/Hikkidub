from django.urls import path, register_converter
from django.contrib.auth import views as auth_views
from . import views
from . import views_panels
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")


urlpatterns = [
    # Главная
    path('', views.index, name='index'),

    # Каталог
    path('catalog/', views.catalog, name='catalog'),

    # Страница аниме
    path('anime/<str:slug>/', views.anime_detail, name='anime_detail'),

    # Просмотр эпизода
    path('anime/<str:anime_slug>/episode/<int:episode_number>/', views.episode_detail, name='episode_detail'),

    # AJAX endpoints
    path('api/switch-quality/', views.switch_quality, name='switch_quality'),
    path('api/subtitle/<int:subtitle_id>/', views.subtitle_vtt, name='subtitle_vtt'),

    # Панель модератора
    path('moderate/', views_panels.moderate_dashboard, name='moderate_dashboard'),
    path('moderate/anime/add/', views_panels.moderate_add_anime, name='moderate_add_anime'),
    path('moderate/anime/<int:anime_id>/edit/', views_panels.moderate_edit_anime, name='moderate_edit_anime'),
    path('moderate/anime/<int:anime_id>/episodes/add/', views_panels.moderate_add_episode, name='moderate_add_episode'),
    path('moderate/episode/<int:episode_id>/edit/', views_panels.moderate_edit_episode, name='moderate_edit_episode'),

    # Панель переводчика
    path('translate/', views_panels.translate_dashboard, name='translate_dashboard'),
    path('translate/episode/<int:episode_id>/<str:language>/', views_panels.translate_edit_subtitle, name='translate_edit_subtitle'),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='hikkiinfo/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Старые маршруты (перенаправление)
    path('anime/<int:anime_id>/', views.categories),
    path('player/', views.player, name='player'),
]
