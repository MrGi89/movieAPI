import json
from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from api.models import Comment, Movie
from api.serializers import CommentSerializer, MovieSerializer

client = Client()


class PostMoviesTest(TestCase):
    """Test module for creating movie"""

    def test_valid_request(self):
        response = client.post(path=reverse('movies'),
                               data=json.dumps({'title': 'Forrest Gump'}),
                               content_type='application/json')

        movie = Movie.objects.get(title='Forrest Gump')
        serializer = MovieSerializer(movie)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)

    def test_invalid_title_param(self):
        response = client.post(path=reverse('movies'),
                               data=json.dumps({'aaaaaa': 'star wars'}),
                               content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_title_value(self):
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

    def test_movies_count(self):
        response = client.get(path=reverse('movies'))

        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostCommentsTest(TestCase):
    """Test module for creating comment"""

    def setUp(self):
        response = client.post(path=reverse('movies'),
                               data=json.dumps({'title': 'Forrest Gump'}),
                               content_type='application/json')
        self.movie_id = response.data.get('id')

    def test_valid_request(self):
        response = client.post(path=reverse('comments'),
                               data=json.dumps({'body': 'test test',
                                                'movie': self.movie_id}),
                               content_type='application/json')

        comment = Comment.objects.get(pk=response.data['id'])
        serializer = CommentSerializer(comment)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)

    def test_missing_param(self):
        response_one = client.post(path=reverse('comments'),
                                   data=json.dumps({'movie': self.movie_id}),
                                   content_type='application/json')

        response_two = client.post(path=reverse('comments'),
                                   data=json.dumps({'body': 'test test'}),
                                   content_type='application/json')

        response_three = client.post(path=reverse('comments'),
                                     data=json.dumps({}),
                                     content_type='application/json')

        self.assertEqual(response_one.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_two.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_three.status_code, status.HTTP_400_BAD_REQUEST)

    def test_movie_doesnt_exists(self):
        response = client.post(path=reverse('comments'),
                               data=json.dumps({'body': 'test test',
                                                'movie': 0}),
                               content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetCommentsTest(TestCase):
    """Test module for retrieving array with all comments"""

    def setUp(self):
        movie_one = client.post(path=reverse('movies'),
                                data=json.dumps({'title': 'Forrest Gump'}),
                                content_type='application/json')

        movie_two = client.post(path=reverse('movies'),
                                data=json.dumps({'title': 'Die Hard'}),
                                content_type='application/json')

        self.movie_one_id = movie_one.data.get('id')
        self.movie_two_id = movie_two.data.get('id')

        Comment.objects.create(body='test one comment',
                               movie_id=self.movie_one_id)
        Comment.objects.create(body='test two comment',
                               movie_id=self.movie_one_id)
        Comment.objects.create(body='test three comment',
                               movie_id=self.movie_two_id)

        self.all_comments = 3
        self.movie_one_comments = 2
        self.movie_two_comments = 1

    def test_comments_count(self):
        response = client.get(path=reverse('comments'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.all_comments)

    def test_movie_filter(self):
        movie_one_comments = client.get(path='{}?movie_id={}'.format(reverse('comments'), self.movie_one_id))
        movie_two_comments = client.get(path='{}?movie_id={}'.format(reverse('comments'), self.movie_two_id))

        self.assertEqual(movie_one_comments.status_code, status.HTTP_200_OK)
        self.assertEqual(movie_two_comments.status_code, status.HTTP_200_OK)
        self.assertEqual(len(movie_one_comments.data), self.movie_one_comments)
        self.assertEqual(len(movie_two_comments.data), self.movie_two_comments)


class GetTopTest(TestCase):
    """Test module for retrieving array with movie rankings based on comments date"""

    def setUp(self):
        self.movies = dict()
        for key, response in enumerate(range(4)):
            response = client.post(path=reverse('movies'),
                                   data=json.dumps({'title': 'Forrest Gump'}),
                                   content_type='application/json')
            self.movies[key + 1] = response.data
        create_date = date.today() - timedelta(days=2)
        Comment.objects.create(body='test one comment',
                               movie_id=self.movies[1]['id'])
        Comment.objects.create(body='test two comment',
                               movie_id=self.movies[1]['id'],
                               create_date=create_date)
        Comment.objects.create(body='test two comment',
                               movie_id=self.movies[1]['id'],
                               create_date=create_date)
        Comment.objects.create(body='test two comment',
                               movie_id=self.movies[2]['id'])
        Comment.objects.create(body='test three comment',
                               movie_id=self.movies[2]['id'])
        Comment.objects.create(body='test four comment',
                               movie_id=self.movies[3]['id'])

    def test_all_movies_rank(self):
        date_from = date.today() - timedelta(days=3)
        date_to = date.today() + timedelta(days=1)
        response = client.get(path='{}?date_from={}&date_to={}'.format(reverse('top'), date_from, date_to))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rank = response.data
        self.assertEqual(len(rank), len(self.movies))
        self.assertEqual(rank[0]['movie_id'], self.movies[1]['id'])
        self.assertEqual(rank[1]['movie_id'], self.movies[2]['id'])
        self.assertEqual(rank[2]['movie_id'], self.movies[3]['id'])
        self.assertEqual(rank[3]['movie_id'], self.movies[4]['id'])

    def test_filter_movies_rank(self):
        date_from = date.today() - timedelta(days=1)
        date_to = date.today() + timedelta(days=1)
        response = client.get(path='{}?date_from={}&date_to={}'.format(reverse('top'), date_from, date_to))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rank = response.data
        self.assertEqual(len(rank), len(self.movies))
        self.assertEqual(rank[0]['movie_id'], self.movies[2]['id'])
        self.assertIn(rank[1]['movie_id'], (self.movies[1]['id'], self.movies[3]['id']))
        self.assertIn(rank[2]['movie_id'], (self.movies[1]['id'], self.movies[3]['id']))
        self.assertEqual(rank[3]['movie_id'], self.movies[4]['id'])
