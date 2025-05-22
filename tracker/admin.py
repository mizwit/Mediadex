from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Genre, Movie, Profile


class ProfileInline(admin.StackedInline):
    """Inline admin descriptor for Profile model which acts like a singleton"""
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"
    filter_horizontal = ['watched', 'watchlist', 'favorites']


class NewUserAdmin(UserAdmin):
    """New user admin class including Profile model"""
    inlines = [ProfileInline]


class GenreAdmin(admin.ModelAdmin):
    """Customize Genre admin page"""
    list_display = ['tmdb_id', 'name']


class MovieAdmin(admin.ModelAdmin):
    """Customize Movie admin page"""
    list_display = ['tmdb_id', 'title', 'release_date', 'runtime', 'popularity', 'vote_average', 'vote_count']
    filter_horizontal = ['genres']


# Register models for admin site
admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)