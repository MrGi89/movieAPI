from datetime import date
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=128)
    year = models.CharField(max_length=64)
    rated = models.CharField(max_length=64)
    released = models.CharField(max_length=64)
    runtime = models.CharField(max_length=64)
    genre = models.CharField(max_length=64)
    director = models.CharField(max_length=64)
    writer = models.TextField()
    actors = models.TextField()
    plot = models.TextField()
    language = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    awards = models.TextField()
    poster = models.TextField()
    metascore = models.CharField(max_length=64)
    imdb_rating = models.CharField(max_length=64)
    imdb_votes = models.CharField(max_length=64)
    imdb_ID = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    dvd = models.CharField(max_length=64)
    box_office = models.CharField(max_length=64)
    production = models.CharField(max_length=64)
    website = models.TextField()
    response = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Rating(models.Model):
    source = models.CharField(max_length=64)
    value = models.CharField(max_length=64)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return '{} {}'.format(self.source, self.value)


class Comment(models.Model):
    body = models.TextField()
    create_date = models.DateField(default=date.today)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return 'Comment {} for {}'.format(self.id, self.movie.title)
