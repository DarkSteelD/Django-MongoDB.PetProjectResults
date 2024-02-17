from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Book, Comic, Genre, UserPreferredGenre
from django.contrib.auth.decorators import login_required
from .forms import GenrePreferenceForm
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect


def home(request):
    genres = Genre.objects.all()
    genre_filter = request.GET.get('genre')

    if genre_filter:
        books = Book.objects.filter(genres__name=genre_filter)
        comics = Comic.objects.filter(genres__name=genre_filter)
    else:
        books = Book.objects.all()
        comics = Comic.objects.all()

    recommended_books = None
    recommended_comics = None
    user_preferred_genres = []

    if request.user.is_authenticated:
        user_preferred_genres = UserPreferredGenre.objects.filter(user=request.user).values_list('genre__name', flat=True)
        print("User Preferred Genres:", user_preferred_genres)  # Debug print
        all_books = Book.objects.all()
        recommended_books = [book for book in all_books if set(user_preferred_genres) & set(book.genres.values_list('name', flat=True))]
        recommended_comics = Comic.objects.filter(genres__name__in=user_preferred_genres).distinct()
        print("Recommended Books:", recommended_books)  # Debug print
        print("Recommended Comics:", recommended_comics)  # Debug print

    context = {
        'genres': genres,
        'books': books,
        'comics': comics,
        'recommended_books': recommended_books,
        'recommended_comics': recommended_comics,
        'selected_genre': genre_filter,
    }

    return render(request, 'home.html', context)

def profile(request):
    if request.method == 'POST':
        pass
    
    return render(request, 'profile.html')
def genre_preferences(request):
    if request.method == 'POST':
        form = GenrePreferenceForm(request.POST)
        if form.is_valid():
            selected_genres = form.cleaned_data['preferred_genres']
            UserPreferredGenre.objects.filter(user=request.user).delete()  # Clear existing preferences
            for genre in selected_genres:
                UserPreferredGenre.objects.create(user=request.user, genre=genre)
            return redirect('home')
    else:
        initial_genres = UserPreferredGenre.objects.filter(user=request.user).values_list('genre', flat=True)
        form = GenrePreferenceForm(initial={'preferred_genres': initial_genres})

    return render(request, 'genre_preferences.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            preferred_genres = form.cleaned_data.get('preferred_genres')
            for genre in preferred_genres:
                UserPreferredGenre.objects.create(user=user, genre=genre)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the homepage or another target page
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def book_detail(request, book_id):
    # Your logic here
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book_detail.html', {'book': book})