from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=100, default='Unknown Genre')

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200, default='Untitled')
    author = models.CharField(max_length=100, default='Unknown Author')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    cover_image = models.ImageField(upload_to='covers/', default='default_cover.jpg')  # Default image
    description = models.TextField(default='No description available.')  # Default description
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

class Comic(models.Model):
    title = models.CharField(max_length=200, default='Untitled')
    author = models.CharField(max_length=100, default='Unknown Author')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    cover_image = models.ImageField(upload_to='covers/', default='default_cover.jpg')  # Default image
    description = models.TextField(default='No description available.')  # Default description
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

class UserPreferredGenre(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} prefers {self.genre.name}'

class CustomUser(AbstractUser):
    preferred_genres = models.ManyToManyField('Genre')  

    def __str__(self):
        return self.username