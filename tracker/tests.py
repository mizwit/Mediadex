import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from .models import Genre, Movie, Profile


class TrackerTestCase(TestCase):
    """Test Case for Tracker App"""

    def setUp(self):
        """Set up dummy entries for testing"""

        # create sample genres
        self.genre1 = Genre(tmdb_id=100, name="action")
        self.genre1.save()
        self.genre2 = Genre(tmdb_id=200, name="adventure")
        self.genre2.save()
        self.genre3 = Genre(tmdb_id=300, name="comedy")
        self.genre3.save()

        # create sample movies
        self.movie1 = Movie(
            tmdb_id = 100,
            poster_path = "/abc.jpg",
            title = "Movie 1",
            release_date = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
            runtime = 100,
            popularity = 90,
            vote_average = 7.5,
            vote_count = 1000
        )
        self.movie1.save()
        self.movie1.genres.add(self.genre1, self.genre2)
        self.movie1.save()

        self.movie2 = Movie(
            tmdb_id = 200,
            poster_path = "/xyz.jpg",
            title = "Movie 2",
            release_date = datetime.datetime.strptime("2010-01-01", "%Y-%m-%d").date(),
            runtime = 150,
            popularity = 25,
            vote_average = 6.5,
            vote_count = 2000
        )
        self.movie2.save()
        self.movie2.genres.add(self.genre1, self.genre2, self.genre3)
        self.movie2.save()

        self.movie3 = Movie(
            tmdb_id = 300,
            title = "Movie 3"
        )
        self.movie3.save()

        # create user objects
        self.user1 = User.objects.create_user(username="foo", password="foo123")
        self.user2 = User.objects.create_user(username="bar", password="bar123")
        self.user3 = User.objects.create_user(username="baz", password="baz123")

        # create user profiles
        self.profile1 = Profile(user=self.user1)
        self.profile1.save()
        self.profile1.watched.add(self.movie1, self.movie2)
        self.profile1.save()

        self.profile2 = Profile(user=self.user2)
        self.profile2.save()
        self.profile2.watched.add(self.movie1, self.movie2, self.movie3)
        self.profile2.save()

        self.profile3 = Profile(user=self.user3, display_name="Bazz")
        self.profile3.save()


    def test_genre_entries(self):
        """Test if all Genre entries were created as expected"""

        self.assertTrue(Genre.objects.get(tmdb_id=100))
        self.assertTrue(Genre.objects.get(tmdb_id=200))
        self.assertTrue(Genre.objects.get(tmdb_id=300))

        def invalid_genre():
            Genre.objects.get(tmdb_id=400)
        self.assertRaises(Genre.DoesNotExist, invalid_genre)


    def test_movie_entries(self):
        """Test if all Movie entries were created as expected"""

        self.assertTrue(Movie.objects.get(tmdb_id=100))
        self.assertTrue(Movie.objects.get(tmdb_id=200))
        self.assertTrue(Movie.objects.get(tmdb_id=300))

        def invalid_movie():
            Movie.objects.get(tmdb_id=400)
        self.assertRaises(Movie.DoesNotExist, invalid_movie)


    def test_user_entries(self):
        """Test if all User entries were created as expected"""

        self.assertTrue(User.objects.get(username="foo"))
        self.assertTrue(User.objects.get(username="bar"))
        self.assertTrue(User.objects.get(username="baz"))

        def invalid_user(): 
            User.objects.get(username="zee")
        self.assertRaises(User.DoesNotExist, invalid_user)

    
    def test_profile_entries(self):
        """Test if all Profile entries were created as expected"""

        self.assertTrue(Profile.objects.get(user=self.user1))
        self.assertTrue(Profile.objects.get(user=self.user2))
        self.assertTrue(Profile.objects.get(user=self.user3))

        def invalid_profile():
            Profile.objects.get(display_name="Fooo")
        self.assertRaises(Profile.DoesNotExist, invalid_profile)

        self.assertEqual(self.profile1.display_name, self.user1.username)
        self.assertEqual(self.profile2.display_name, self.user2.username)
        self.assertNotEqual(self.profile3.display_name, self.user3.username)

    
    def test_genre_tmdb_id(self):
        """Test uniqueness of Genre tmdb_id field"""

        def non_unique_tmdb_id():
            Genre(tmdb_id=100, name="drama").save()
        self.assertRaises(IntegrityError, non_unique_tmdb_id)


    def test_genre_name_unique(self):
        """Test uniqueness of Genre name field"""

        def non_unique_name():
            Genre(tmdb_id=400, name="action").save()
        self.assertRaises(IntegrityError, non_unique_name)

    
    def test_genre_str_repr(self):
        """Test if the string representation for a Genre objects has its capitalized name"""

        self.assertEqual(str(self.genre1), "Action")
        self.assertEqual(str(self.genre2), "Adventure")
        self.assertNotEqual(str(self.genre3), "comedy")


    def test_movie_tmdb_id_unique(self):
        """Test uniqueness of Movie tmdb_id field"""

        def non_unique_tmdb_id():
            Movie(tmdb_id=100, title="Sample Movie").save()
        self.assertRaises(IntegrityError, non_unique_tmdb_id)


    def test_movie_poster_path_validate(self):
        """Test if Movie poster_path field only accepts image paths"""

        def invalid_poster_path():
            self.movie1.poster_path = "/abc.xyz"
            self.movie1.full_clean()
        self.assertRaises(ValidationError, invalid_poster_path)


    def test_movie_vote_average_validate(self):
        """Test if Movie vote_average field only accepts scores between 0 and 10.0"""

        def vote_average_too_small():
            self.movie1.vote_average = -2.5
            self.movie1.full_clean()
        self.assertRaises(ValidationError, vote_average_too_small)

        def vote_average_too_big():
            self.movie1.vote_average = 12.0
            self.movie1.full_clean()
        self.assertRaises(ValidationError, vote_average_too_big)


    def test_movie_add_genres(self):
        """Test adding and removing Genre objects to Movie genres field"""

        self.assertEqual(self.movie1.genres.count(), 2)
        self.assertEqual(self.movie2.genres.count(), 3)
        self.assertEqual(self.genre2.movies.count(), 2)

        self.assertIn(self.genre1, self.movie2.genres.all())
        self.movie2.genres.remove(self.genre1)
        self.movie2.save()
        self.assertNotIn(self.genre1, self.movie2.genres.all())


    def test_movie_str_repr(self):
        """Test if string representation of Movie object returns movie title and release date if any"""

        self.assertEqual(str(self.movie1), "Movie 1 (2020)")
        self.assertNotEqual(str(self.movie2), "Movie 2")
        self.assertEqual(str(self.movie3), "Movie 3")


    def test_profile_user_one_to_one(self):
        """Test that a user is associated with only one Profile"""

        def duplicate_user():
            self.profile1.user = self.user2
            self.profile1.full_clean()
        self.assertRaises(ValidationError, duplicate_user)


    def test_profile_add_collection(self):
        """Test adding and removing Movie objects to collections like User watched field"""

        self.assertEqual(self.profile1.watched.count(), 2)
        self.assertEqual(self.profile2.watched.count(), 3)
        self.assertEqual(self.movie2.watched_by.count(), 2)

        self.assertIn(self.movie1, self.profile2.watched.all())
        self.profile2.watched.remove(self.movie1)
        self.profile2.save()
        self.assertNotIn(self.movie1, self.profile2.watched.all())


    def test_profile_str_repr(self):
        """Test if string representation of Profile object returns username and display name if any"""

        self.assertEqual(str(self.profile1), "foo")
        self.assertEqual(str(self.profile2), "bar")
        self.assertEqual(str(self.profile3), "Bazz (baz)")