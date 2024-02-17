from django.contrib import admin
from .models import Book, Comic, Genre

admin.site.register(Book)
admin.site.register(Comic)
admin.site.register(Genre)

