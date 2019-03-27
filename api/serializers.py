import requests
from rest_framework import serializers
from .models import Comment, Movie, Rating
from movies.local_settings import OMDB_API_KEY


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ('id', 'movie')


class MovieSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def validate(self, data):
        """"""
        title = data.get('title')
        if title is None:
            raise serializers.ValidationError('Movie title was not provided')
        omdb_request = requests.get(url='http://www.omdbapi.com/',
                                    params={'t': title,
                                            'type': 'movie',
                                            'apikey': OMDB_API_KEY})

        omdb_response = omdb_request.json()
        if omdb_response.get('Response') == 'False':
            raise serializers.ValidationError('No movie with title {}'.format(title))
        return omdb_response

    def create(self, validated_data):
        movie = Movie.objects.create(title=validated_data['Title'],
                                     year=validated_data['Year'],
                                     rated=validated_data['Rated'],
                                     released=validated_data['Released'],
                                     runtime=validated_data['Runtime'],
                                     genre=validated_data['Genre'],
                                     director=validated_data['Director'],
                                     writer=validated_data['Writer'],
                                     actors=validated_data['Actors'],
                                     plot=validated_data['Plot'],
                                     language=validated_data['Language'],
                                     country=validated_data['Country'],
                                     awards=validated_data['Awards'],
                                     poster=validated_data['Poster'],
                                     metascore=validated_data['Metascore'],
                                     imdb_rating=validated_data['imdbRating'],
                                     imdb_votes=validated_data['imdbVotes'],
                                     imdb_ID=validated_data['imdbID'],
                                     type=validated_data['Type'],
                                     dvd=validated_data['DVD'],
                                     box_office=validated_data['BoxOffice'],
                                     production=validated_data['Production'],
                                     website=validated_data['Website'],
                                     response=validated_data['Response'])

        for rating in validated_data['Ratings']:
            Rating.objects.create(source=rating['Source'],
                                  value=rating['Value'],
                                  movie=movie)
        return movie


class TopSerializer(serializers.Serializer):

    movie_id = serializers.IntegerField(required=True, source='id')
    total_comments = serializers.IntegerField(required=True)
    rank = serializers.IntegerField(required=True)
