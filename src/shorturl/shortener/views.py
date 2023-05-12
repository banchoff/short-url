from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "shortener/index.html")

def userEdit(request):
    return render(request, "shortener/userEdit.html")

def userList(request):
    return render(request, "shortener/userList.html")

