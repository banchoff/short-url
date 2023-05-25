from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Access
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from ..forms import URLUserCreationForm


def redirectTo(request, shortUrl):
    if len(shortUrl) == 32:
        myUrl = get_object_or_404(ShortenedURL, shortened = shortUrl)
        anAccess = Access.create(request.headers["User-Agent"], request.META["REMOTE_ADDR"], myUrl)     
        anAccess.save()
        return redirect(myUrl.original)


class SignUpView(CreateView):
    form_class = URLUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def help(request):
    return render(request, "shortener/help.html")

@login_required
def about(request):
    return render(request, "shortener/about.html")
