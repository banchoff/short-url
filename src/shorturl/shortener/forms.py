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
        #fields = ("username", "email")
        fields = ("email",)
        

class ShortenedURLForm(forms.ModelForm):
    template_name = "shortener/shortenedURLForm.html"
    class Meta:
        model = ShortenedURL
        fields = ["original"]
        labels = {
            "original": 'URL'
        }
        
        # help_texts = {
        #     "name": _("Some useful help text."),
        # }
        # error_messages = {
        #     "name": {
        #         "max_length": _("This writer's name is too long."),
        #     },
        # }
        # widgets = {
        #     "original": Textarea(attrs={"cols": 80, "rows": 20}),
        # }

# class URLUserForm(forms.ModelForm):
#     template_name = "shortener/shortenedURLForm.html"
#     class Meta:
#         model = URLUser
#         fields = ["firstname", "lastname", "username", "email"]


    

