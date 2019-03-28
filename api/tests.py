import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from api.models import Comment, Movie, Rating
from api.serializers import MovieSerializer

client = Client()


class PostMoviesTest(TestCase):
    """Test module for creating movie"""

    def test_invalid_body_request(self):
        response = client.post(path=reverse('movies'),
                               data=json.dumps({'aaaaaa': 'star wars'}),
                               content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_body_request(self):
        response = client.post(path=reverse('movies'),
                               data=json.dumps({'title': 'Forrest Gump'}),
                               content_type='application/json')

        movie = Movie.objects.get(title='Forrest Gump')
        serializer = MovieSerializer(movie)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)

    def test_wrong_movie_title(self):
        response = client.post(path=reverse('movies'),
                               data=json.dumps({'title': 'forest gamp'}),
                               content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetMoviesTest(TestCase):
    """Test module for retrieving array with all movies"""

    def setUp(self):
        client.post(path=reverse('movies'),
                    data=json.dumps({'title': 'Forrest Gump'}),
                    content_type='application/json')
        client.post(path=reverse('movies'),
                    data=json.dumps({'title': 'Shrek'}),
                    content_type='application/json')
        client.post(path=reverse('movies'),
                    data=json.dumps({'title': 'Shrek 2'}),
                    content_type='application/json')

    def test_movies_length(self):
        response = client.get(path=reverse('movies'))

        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
