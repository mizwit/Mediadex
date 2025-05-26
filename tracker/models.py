from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from PIL import Image, ImageOps


# Validators

def validate_vote_average(vote_average):
    """Ensures vote average is a valid score between 0 and 10.0"""
    if vote_average < 0 or vote_average > 10.0:
        raise ValidationError("Vote average score must be between 0 and 10.0.")


def validate_poster_path(poster_path):
    """Ensure url for poster leads to a valid image"""
    Image.init()
    valid_extensions = [ext.lower()[1:] for ext in Image.EXTENSION]
    poster_path_ext = poster_path.split(".")[-1]
    if poster_path_ext not in valid_extensions:
        raise ValidationError("Invalid image extension for poster path.")


def validate_image_size(image):
    """Ensure image is at least 100x100 pixels"""
    with Image.open(image) as img:
        width, height = img.size
        if width < 100 or height < 100:
            raise ValidationError("Image must be at least 100x100 pixels.")


# Models

class Genre(models.Model):
    """Media Genres"""
    tmdb_id = models.PositiveIntegerField(
        unique = True,
    )
    name = models.CharField(
        max_length = 150,
        unique = True,
    )

    def __str__(self):
        return self.name.capitalize()


class Movie(models.Model):
    """TMDB Movie Data"""

    tmdb_id = models.PositiveIntegerField(
        unique = True
    )
    poster_path = models.CharField(
        max_length = 150,
        null = True,
        blank = True,
        validators = [validate_poster_path],
    )
    title = models.CharField(
        max_length = 255,
    )
    original_title = models.CharField(
        max_length = 255,
        null = True,
        blank = True,
    )
    overview = models.TextField(
        blank = True,
    )
    genres = models.ManyToManyField(
        Genre,
        related_name = 'movies',
        blank = True,
    )
    release_date = models.DateField(
        null = True,
        blank = True,
    )
    runtime = models.PositiveIntegerField(
        null = True,
        blank = True,
    )
    popularity = models.FloatField(
        null = True,
        blank = True,
    )
    vote_average = models.FloatField(
        null = True,
        blank = True,
        validators = [validate_vote_average],
    )
    vote_count = models.PositiveIntegerField(
        null = True,
        blank = True,
    )

    def __str__(self):
        if self.release_date:
            return f"{self.title} ({str(self.release_date)[:4]})"
        return self.title


class Profile(models.Model):
    """User Profile - Display Name, Avatar, Watched, Watchlist, Favorites"""

    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name = 'profile',
        editable = False,
    )
    display_name = models.CharField(
        max_length = 150,
        blank = True,
    )
    avatar = models.ImageField(
        upload_to = '',
        default = 'default.jpg',
        blank = True,
        validators = [validate_image_size],
    )
    watched = models.ManyToManyField(
        Movie,
        related_name = 'watched_by',
        blank = True,
    )
    watchlist = models.ManyToManyField(
        Movie,
        related_name = 'watchlisted_by',
        blank = True,
    )
    favorites = models.ManyToManyField(
        Movie,
        related_name = 'favorited_by',
        blank = True,
    )

    def save(self, *args, **kwargs):
        if not self.display_name: 
            self.display_name = self.user.username
        super().save(*args, **kwargs)

        # Crop and save image as 100x100 pixels
        if self.avatar:
            with Image.open(self.avatar.path) as img:
                img = img.convert("RGB")
                img = ImageOps.fit(img, (100, 100))
                img.save(self.avatar.path, format='JPEG')

    def __str__(self):
        if self.display_name == self.user.username:
            return self.display_name
        return f"{self.display_name} ({self.user.username})"