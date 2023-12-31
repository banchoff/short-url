from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import Access, ShortenedURL#, URLUser
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from ..forms import URLUserCreationForm

# Lib

def isAjax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

def isAjaxAndPost(request):
    return isAjax(request) and request.method == "POST"

def objectLoadAjax(request, objects, funcAssign):
    count = 5
    if hasattr(settings, 'TABLE_COUNT'):
        count = settings.TABLE_COUNT
    if isAjaxAndPost(request):
        pageNum = request.POST["pageNum"]
        nextPage = -1
        prevPage = 1
        lastPage = -1
        currentPage = 1
        resultsArray = []
        paginator = Paginator(objects, count)
        page = paginator.get_page(pageNum)
        if page.has_previous():
            prevPage = page.previous_page_number()
        if page.has_next():
            nextPage = page.next_page_number()
        lastPage = paginator.num_pages
        currentPage = page.number
        for anObject in page.object_list:
            resultsArray.append(funcAssign(anObject))            
        resp = {
            'next': nextPage,
            'prev': prevPage,
            'last': lastPage,
            'current': currentPage,
            'data': resultsArray,
        }
        return JsonResponse(resp, status=200)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)

# Public Views

class SignUpView(CreateView):
    form_class = URLUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def redirectTo(request, shortUrl):
    myUrl = get_object_or_404(ShortenedURL, shortened = shortUrl)
    if myUrl.urlUser.id == request.user.id:
        userAgent = "None"
        remoteAdr = "0.0.0.0"
        if "User-Agent" in request.headers:
            userAgent = request.headers["User-Agent"]
        if "REMOTE_ADDR" in request.META:
            remoteAddr = request.META["REMOTE_ADDR"]
        anAccess = Access.create(userAgent, remoteAddr, myUrl)     
        anAccess.save()
        return redirect(myUrl.original)
    else:
        return HttpResponse("Error: User does not own this URL.", status=400)

@login_required
def help(request):
    return render(request, "shortener/help.html")

@login_required
def about(request):
    return render(request, "shortener/about.html")
