from django.urls import path
from myapp.views import *
from django.contrib import admin
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('home/', home, name='home'),
    path('admin/', admin.site.urls),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('genre-preferences/', genre_preferences, name='genre_preferences'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
