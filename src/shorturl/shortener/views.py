from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import ShortenedURL, URLUser
from .forms import ShortenedURLForm#, URLUserForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import URLUserCreationForm
from datetime import datetime
import hashlib


@login_required
def index(request):
#    urls = ShortenedURL.objects.all()
    currentUser = URLUser.objects.get(pk=request.user.id)
    urls = currentUser.shortenedurl_set.all()
    return render(request, "shortener/index.html", {'urls': urls})

@login_required
def userEdit(request):
    return render(request, "shortener/userEdit.html")

@login_required
def userList(request):
    users = URLUser.objects.all()
    return render(request, "shortener/userList.html", {'users': users})

def userLogin(request):
    return render(request, "shortener/userLogin.html")

@login_required
def userLogout(request):
    return render(request, "shortener/userLogout.html")

@login_required
def help(request):
    return render(request, "shortener/help.html")

@login_required
def about(request):
    return render(request, "shortener/about.html")

@login_required
def urlAdd(request):

    def getUniqueShorterURL(longUrl):
        urlHashed = hashlib.md5(longUrl.encode())
        return urlHashed.hexdigest()
    
    form = ShortenedURLForm()
    # url = SortenedURL.objects.get(pk=urlId)
    #form = ShortenedURLForm(instance = url)
    if request.method == 'POST':
        form = ShortenedURLForm(request.POST)
        if form.is_valid():
            currentDateAndTime = datetime.now()
            currentDate = currentDateAndTime.strftime("%Y-%m-%d")
            currentTime = currentDateAndTime.strftime("%H:%M:%S")
            
            myUrl = form.save(commit=False)
            myUrl.shortened = getUniqueShorterURL(myUrl.original)
            myUrl.dateCreated = currentDate
            myUrl.hourCreated = currentTime
            myUrl.urlUser = request.user
            
            myUrl.save()
            return HttpResponseRedirect('/shortener/')
    else:
        form = ShortenedURLForm()
    return render(request, "shortener/urlAdd.html", {'form': form})


# def userAdd(request):
#     form = URLUserForm()
#     # url = SortenedURL.objects.get(pk=urlId)
#     #form = ShortenedURLForm(instance = url)
#     if request.method == 'POST':
#         form = URLUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/shortener/')
#     else:
#         form = URLUserForm()
#     return render(request, "shortener/userAdd.html", {'form': form})

class SignUpView(CreateView):
    form_class = URLUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
