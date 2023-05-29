from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import ShortenedURL, URLUser
from ..forms import ShortenedURLForm
from .common import isAjaxAndPost, objectLoadAjax
    
@login_required
def index(request):
    currentUser = URLUser.objects.get(pk=request.user.id)
    urls = currentUser.shortenedurl_set.all()
    add_url_form = ShortenedURLForm()
    return render(request, "shortener/index.html", {'urls': urls, 'add_url_form': add_url_form})

@login_required
def urlLoadAjax(request):
    def funcAssign(aDict):
        return {
                'id': aDict.id,
                'original': aDict.original,
                'shortened': aDict.shortened,
        }
    currentUser = URLUser.objects.get(pk=request.user.id)
    return objectLoadAjax(request, currentUser.shortenedurl_set.all(), funcAssign)

@login_required
def urlAddAjax(request):
    if isAjaxAndPost(request):
        form = ShortenedURLForm(request.POST)
        if form.is_valid():
            shortenedURL = ShortenedURL.create(request.POST["original"], request.user)
            shortenedURL.save()
            return JsonResponse({"success": "URL created."}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)

@login_required
def urlStatsAjax(request):
    if isAjaxAndPost(request):
        urlId = request.POST["id"]
        myUrl = get_object_or_404(ShortenedURL, pk=urlId)
        if myUrl.urlUser.id == request.user.id:
            dateAdded = myUrl.dateCreated
            timesVisited = myUrl.access_set.all().count()
            return JsonResponse({'dateAdded': dateAdded, 'timesVisited': timesVisited}, status=200)
        else:
            return JsonResponse({"error": "User does not own this URL."}, status=400)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)

@login_required
def urlDeleteAjax(request):
    if isAjaxAndPost(request):
        urlId = request.POST["id"]
        myUrl = get_object_or_404(ShortenedURL, pk=urlId)
        if myUrl.urlUser.id == request.user.id:
            myUrl.delete()
            return JsonResponse({"success": "URL deleted."}, status=200)
        else:
            return JsonResponse({"error": "User does not own this URL."}, status=400)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)
