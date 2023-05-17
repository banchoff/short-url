from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ShortenedURL, URLUser


class URLUserCreationForm(UserCreationForm):
    class Meta:
        model = URLUser
        fields = ("username", "email")

class URLUserChangeForm(UserChangeForm):
    class Meta:
        model = URLUser
        fields = ("username", "email")
        

class ShortenedURLForm(forms.ModelForm):
    template_name = "shortener/shortenedURLForm.html"
    class Meta:
        model = ShortenedURL
        fields = ["original"]

# class URLUserForm(forms.ModelForm):
#     template_name = "shortener/shortenedURLForm.html"
#     class Meta:
#         model = URLUser
#         fields = ["firstname", "lastname", "username", "email"]


    

