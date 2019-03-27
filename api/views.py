from django.db.models import Count
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Comment, Movie
from api.serializers import CommentSerializer, MovieSerializer, TopSerializer


class ListMovies(APIView):

    def get(self, request):
        """

        :param request:
        :return:
        """
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """

        :param request:
        :return:
        """
        serializer = MovieSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListComments(APIView):

    def get(self, request):
        """

        :param request:
        :return:
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

        :param request:
        :return:
        """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListTop(APIView):

    def get(self, request):
        """
        
        :param request:
        :return:
        """
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        if date_from is None or date_to is None:
            return Response('No date specified', status=status.HTTP_400_BAD_REQUEST)

        movies = Movie.objects.all().values('id').annotate(total_comments=Count('comments')).order_by('-total_comments')
        rank = 1
        for count, movie in enumerate(movies):
            if count == 0 or movie['total_comments'] == movies[count - 1]['total_comments']:
                movie['rank'] = rank
            else:
                rank += 1
                movie['rank'] = rank

        serializer = TopSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

























