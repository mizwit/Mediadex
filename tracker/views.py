import datetime
import json
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

import environ
import requests

from .models import Genre, Movie, Profile
from .forms import RegisterForm, ProfileForm


# Take environment variables from .env file
env = environ.Env()
environ.Env.read_env(settings.BASE_DIR / '.env')


def index(request):
    """Redirect to home at index"""
    return HttpResponseRedirect(reverse('home'))


def tmdb_api(request, endpoint):
    """API to fetch movie data using TMDB"""

    url = f"https://api.themoviedb.org/3/{endpoint}?{request.GET.urlencode()}"
    headers = {
        "Authorization": f"Bearer {env('TMDB_API')}",
        "accept": "application/json",
    }

    print(f"Fetching data from {url}...")
    response = requests.get(url, headers=headers)
    status = response.status_code
    data = response.json()
    
    print(f"Status: {status}")
    if status != 200: print(data)
    return JsonResponse(data, status=status)


def jr_to_dict(json_response):
    """Helper function to convert a JsonResponse to Python dict"""
    json_data = json_response.content
    dict_data = json.loads(json_data.decode('utf-8'))
    return dict_data


def home(request):
    """Landing page for the web app. Shows site information and movie collections"""
    if not cache.get("collections", None):
        trending = {
            "title": "Trending This Week",
            "movies": jr_to_dict(tmdb_api(request, "trending/movie/week")).get("results", [])[:12],
        }
        top_rated = {
            "title": "Top Rated of All Time",
            "movies": jr_to_dict(tmdb_api(request, "movie/top_rated")).get("results", [])[:12],
        }
        now_playing = {
            "title": "Now Playing In Theatres",
            "movies": jr_to_dict(tmdb_api(request, "movie/now_playing")).get("results", [])[:12],
        }
        upcoming = {
            "title": "Upcoming In Theatres",
            "movies": jr_to_dict(tmdb_api(request, "movie/upcoming")).get("results", [])[:12],
        }
        collections = [trending, top_rated, now_playing, upcoming]
        cache.set("collections", collections, (60 * 60 * 24))
    else:
        collections = cache.get("collections")
    return render(request, 'tracker/home.html', context={
        "collections": collections,
    })


def search(request):
    """Render search page"""
    return render(request, 'tracker/search.html')


def movie(request, movie_id):
    """Render movie page"""
    return render(request, 'tracker/movie.html', context={
        "movie_id": movie_id,
    })


def register(request):
    """Register new user"""

    if request.method == 'POST':
        print("Registering new user...")
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create and save new User object
            user = User.objects.create_user(
                username = form.cleaned_data.get('username'), 
                password = form.cleaned_data.get('password'),
            )
            # Create new Profile object for the user
            profile = Profile(
                user = user,
                display_name = form.cleaned_data.get('display_name'),
            )
            profile.save()
            print(f"User '{user.username}' Registered Successfully.")

            return HttpResponseRedirect(reverse('profile'))
        print(f"Registration Failed.")
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', context={
        'form': form,
    })


@login_required
def profile(request):
    """Display and Edit User Profile"""

    if request.method == "POST":
        print("Editing user profile...")
        form = ProfileForm(
            request.POST, request.FILES,
            initial = {"avatar": None},
            instance = request.user.profile,
        )
        if form.is_valid():
            form.save()
            print(f"Edit User '{request.user.username}' Profile Successful.")
            return HttpResponseRedirect(reverse('profile'))
        print(f"Edit User '{request.user.username}' Profile Failed.")
    else:
        form = ProfileForm(
            initial = {"avatar": None},
            instance = request.user.profile,
        )
    user_profile = request.user.profile
    return render(request, 'tracker/profile.html', context={
        'form': form,
        'watched_count': user_profile.watched.count(),
        'watchlist_count': user_profile.watchlist.count(),
        'favorites_count': user_profile.favorites.count(),
    })


@login_required
def watched(request):
    """Render 'Watched' collection page"""
    return render(request, 'tracker/collection.html', context={
        "collection": "watched",
    })


@login_required
def watchlist(request):
    """Render 'Watchlist' collection page"""
    return render(request, 'tracker/collection.html', context={
        "collection": "watchlist",
    })


@login_required
def favorites(request):
    """Render 'Favorites' collection page"""
    return render(request, 'tracker/collection.html', context={
        "collection": "favorites",
    })


@login_required
def status_movie(request, movie_id):
    """Provide movie availibility status in various user collections"""
    user_profile = request.user.profile
    data = {
        "user": request.user.username,
        "movie_id": movie_id,
        "watched": movie_id in user_profile.watched.all().values_list('tmdb_id', flat=True),
        "watchlist": movie_id in user_profile.watchlist.all().values_list('tmdb_id', flat=True),
        "favorites": movie_id in user_profile.favorites.all().values_list('tmdb_id', flat=True),
    }
    print(f"Sending movie status data... \n{data}")
    return JsonResponse(data, status=200)


def new_genre(data):
    """Helper function to create new Genre object using TMDB api data"""
    print(f"Creating new Genre object for TMDB id '{data.get('id')}'...")
    genre = Genre(
        tmdb_id = data.get('id'),
        name = data.get('name', '').strip().lower(), # Normalize genre names
    )
    genre.save()
    print(f"Success: Genre object for TMDB id '{data.get('id')}' created.")
    return genre


def new_movie(data):
    """Helper function to create new Movie object using TMDB api data"""
    
    print(f"Creating new Movie object for TMDB id '{data.get('id')}'...")
    movie = Movie(
        tmdb_id = data.get('id'),
        poster_path = data.get('poster_path', None),
        title = data.get('title', ''),
        original_title = data.get('original_title', None),
        overview = data.get('overview', '')
    )
    movie.save()

    # Add existing or new Genre objects from all genres
    for genreData in data.get('genres', []):
        try:
            genre = Genre.objects.get(tmdb_id = genreData.get('id'))
        except Genre.DoesNotExist:
            genre = new_genre(genreData)
        movie.genres.add(genre)

    # Save released_date as datetime object
    if (release_date := data.get('release_date', None)):
        movie.release_date = datetime.datetime.strptime(release_date, "%Y-%m-%d").date()
    # Save runtime as Integer
    if (runtime := data.get('runtime', None)):
        movie.runtime = int(runtime)
    # Save popularity as Float
    if (popularity := data.get('popularity', None)):
        movie.popularity = float(popularity)
    # Save vote average as Float
    if (vote_average := data.get('vote_average', None)):
        movie.vote_average = float(vote_average)
    # Save vote count as Integer
    if (vote_count := data.get('vote_count', None)):
        movie.vote_count = int(vote_count)
    
    movie.save()
    print(f"Success: Movie object for TMDB id '{data.get('id')}' created.")
    return movie


@login_required
def update_movie(request, movie_id):
    """Add or Remove movie from a user collection by changing from its current status)"""

    if request.method == "PUT":
        data = json.loads(request.body)
        print(f"Received request to update movie in collection. \n{data}")
        collection = data.get('collection', None)
        current_status = data.get('current_status', None)

        # Validate received data
        if (collection == None) or (current_status == None):
            return JsonResponse({
                "error": "Request body must include fields 'collection' and 'current_status'."
            }, status=404)
        if collection not in ['watched', 'watchlist', 'favorites']:
            return JsonResponse({
                "error": f"Invalid collection '{collection}'. Try with 'watched', 'watchlist', 'favorites'."
            }, status=404)
        if (current_status != True) and (current_status != False):
            return JsonResponse({
                "error": f"Field 'current_status' must be a Boolean value."
            }, status=404)

        # Fetch user profile and movie models
        user_profile = request.user.profile
        try:
            movie = Movie.objects.get(tmdb_id = movie_id)
        except Movie.DoesNotExist:
            # Get movie data from TMDB
            movieData = jr_to_dict(tmdb_api(request, f"movie/{movie_id}"))
            movie = new_movie(movieData)

        # Remove from collection if already present
        if current_status == True:
            print(f"Removing '{movie.title}' from {request.user.username}'s {collection} collection...")
            match collection:
                case 'watched':
                    user_profile.watched.remove(movie)
                case 'watchlist':
                    user_profile.watchlist.remove(movie)
                case 'favorites':
                    user_profile.favorites.remove(movie)

        # Add to collection if not present
        elif current_status == False:
            print(f"Adding '{movie.title}' to {request.user.username}'s {collection} collection...")
            match collection:
                case 'watched':
                    user_profile.watched.add(movie)
                case 'watchlist':
                    user_profile.watchlist.add(movie)
                case 'favorites':
                    user_profile.favorites.add(movie)

        return HttpResponse(204)
    else:
        return JsonResponse({
            "error": "Path only accessible via PUT",
        }, status=400)
    

@login_required
def collection_api(request, collection):
    """Send data of movies in a user's collection"""
    user_profile = request.user.profile
    data = {
        "user": request.user.username,
        "collection": collection,
    }

    # Order query set based on sort type
    sort_by = request.GET.get('sort', 'added-newest')
    match sort_by:
        case 'added-newest':
            sort_order = '-id'
        case 'added-oldest':
            sort_order = 'id'
        case 'released-newest':
            sort_order = '-release_date'
        case 'released-oldest':
            sort_order = 'release_date'
        case 'name-ascending':
            sort_order = 'title'
        case 'name-descending':
            sort_order = '-title'
        case 'popularity':
            sort_order = '-popularity'
        case 'vote-average':
            sort_order = '-vote_average'

    match collection:
        case 'watched':
            data["movies"] = list(user_profile.watched.values(
                'id', 'tmdb_id', 'poster_path', 'title', 'release_date', 'popularity', 'vote_average'
            ).order_by(sort_order))
            data["total_count"] = user_profile.watched.count()
            status = 200
        case 'watchlist':
            data["movies"] = list(user_profile.watchlist.values(
                'id', 'tmdb_id', 'poster_path', 'title', 'release_date', 'popularity', 'vote_average'
            ).order_by(sort_order))
            data["total_count"] = user_profile.watchlist.count()
            status = 200
        case 'favorites':
            data["movies"] = list(user_profile.favorites.values(
                'id', 'tmdb_id', 'poster_path', 'title', 'release_date', 'popularity', 'vote_average'
            ).order_by(sort_order))
            data["total_count"] = user_profile.favorites.count()
            status = 200
        case _:
            data["error"] = f"Invalid collection name '{collection}'. Try 'watched', 'watchlist', 'favorites'"
            status = 404
    print(f"Sending collection '{collection}' data for user '{request.user.username}' sorted by '{sort_order}'...")
    return JsonResponse(data, status=status)


# Access limited to admin (superuser)
@user_passes_test(lambda user: user.is_superuser)
def sandbox(request):
    """For experimental purposes"""
    # return render(request, 'tracker/sandbox.html')
    return JsonResponse({"Hello": "Admin"}, status=200)