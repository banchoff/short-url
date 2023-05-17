from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import URLUserCreationForm, URLUserChangeForm
from .models import URLUser

class URLUserAdmin(UserAdmin):
    add_form = URLUserCreationForm
    form = URLUserChangeForm
    model = URLUser
    list_display = ["email", "username",]

admin.site.register(URLUser, URLUserAdmin)

# Register your models here.
