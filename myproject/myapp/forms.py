from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Genre

class CustomUserCreationForm(UserCreationForm):
    preferred_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # Use your custom user model here
        fields = UserCreationForm.Meta.fields + ('preferred_genres',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.preferred_genres.set(self.cleaned_data['preferred_genres'])
        return user

class GenrePreferenceForm(forms.Form):
    preferred_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
