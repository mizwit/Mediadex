from django.urls import include, path
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("sandbox/", views.sandbox, name="sandbox"),

    # Basic app urls
    path("home/", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("movie/<int:movie_id>/", views.movie, name="movie",),

    # Auth urls
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", views.register, name="register"),
    path("accounts/profile/", views.profile, name="profile"),

    # User-only app urls
    path("watched/", views.watched, name="watched"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("favorites/", views.favorites, name="favorites"),

    # Api endpoints
    path("api/tmdb/<path:endpoint>", cache_page(60 * 60 * 24)(views.tmdb_api), name="tmdb_api"), # Cache for a day
    path("api/status/movie/<int:movie_id>", views.status_movie, name="status_movie"),
    path("api/update/movie/<int:movie_id>", views.update_movie, name="update_movie"),
    path("api/collection/<str:collection>", views.collection_api, name="collection_api"),

    # Serve user uploaded media
    path('media/<str:filename>', views.serve_media, name="serve_media"),
]
