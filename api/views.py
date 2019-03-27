from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Comment, Movie
from api.serializers import CommentSerializer, MovieSerializer, TopSerializer
from django.db import connection


class ListMovies(APIView):

    def get(self, request):
        """
        This view should return list of all movies and their details stored in local database.
        """
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        This view should serialize passed data, save object instance to database and return saved data.
        """
        serializer = MovieSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListComments(APIView):

    def get(self, request):
        """
        This view should return list of movie comments(if movie ID was passed in url parameters)
        or all comments stored in database.
        """
        movie_id = request.GET.get('movie_id')
        if movie_id:
            comments = Comment.objects.filter(movie=movie_id)
        else:
            comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        This view should serialized passed data, save comment in database and return object instance.
        """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListTop(APIView):

    def get(self, request):
        """
        This view should check if date range parameter was passed in url, filter
        """
        serializer = TopSerializer(data=self.request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        movies = self.get_movies(**serializer.validated_data)
        return Response(movies, status=status.HTTP_200_OK)

    @staticmethod
    def get_movies(date_from, date_to):
        """
        Returns all movies with count of comments in specified date range with rank attribute in form of dict
        """
        cursor = connection.cursor()
        cursor.execute('''SELECT am.id AS movie_id, 
                                 COUNT(ac.id) AS total_comments, 
                                 RANK () OVER (ORDER BY COUNT(ac.id) DESC)
                          FROM api_movie am
                          LEFT JOIN api_comment ac ON am.id=ac.movie_id AND ac.create_date BETWEEN %s AND %s
                          GROUP BY am.id ORDER BY COUNT(ac.id) DESC;''', (date_from, date_to))
        row = ListTop.dictfetchall(cursor)
        return row

    @staticmethod
    def dictfetchall(cursor):
        """
        Return all rows from a cursor as a dict
        """
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
