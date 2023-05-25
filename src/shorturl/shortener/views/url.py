from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import ShortenedURL, URLUser
from ..forms import ShortenedURLForm
from datetime import datetime
import hashlib



@login_required
def index(request):
    currentUser = URLUser.objects.get(pk=request.user.id)
    urls = currentUser.shortenedurl_set.all()
    add_url_form = ShortenedURLForm()
    return render(request, "shortener/index.html", {'urls': urls, 'add_url_form': add_url_form})


@login_required
def urlLoadAjax(request):
    count = 5
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax and request.method == "POST":
        pageNum = request.POST["pageNum"]
        nextPage = -1
        prevPage = 1
        lastPage = -1
        currentPage = 1
        urls = []

        currentUser = URLUser.objects.get(pk=request.user.id)
        myUrls = currentUser.shortenedurl_set.all()
        paginator = Paginator(myUrls, count)
        page = paginator.get_page(pageNum)

        if page.has_previous():
            prevPage = page.previous_page_number()
        if page.has_next():
            nextPage = page.next_page_number()
        lastPage = paginator.num_pages
        currentPage = page.number
        
        for aURL in page.object_list:
            urls.append({
                'id': aURL.id,
                'original': aURL.original,
                'shortened': aURL.shortened,})
            
        resp = {
            'next': nextPage,
            'prev': prevPage,
            'last': lastPage,
            'current': currentPage,
            'data': urls,
        }
        return JsonResponse(resp, status=200)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)

@login_required
def urlAddAjax(request):

    def getUniqueShorterURL(longUrl):
        urlHashed = hashlib.md5(longUrl.encode())
        return urlHashed.hexdigest()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax and request.method == "POST":
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
            return JsonResponse({"success": "URL created."}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)



@login_required
def urlStatsAjax(request):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax and request.method == "POST":
        urlId = request.POST["id"]
        myUrl = get_object_or_404(ShortenedURL, pk=urlId)

        dateAdded = myUrl.dateCreated
        timesVisited = myUrl.access_set.all().count()
        return JsonResponse({'dateAdded': dateAdded, 'timesVisited': timesVisited}, status=200)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)



@login_required
def urlDeleteAjax(request):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax and request.method == "POST":
        urlId = request.POST["id"]
        myUrl = get_object_or_404(ShortenedURL, pk=urlId)
        if myUrl.urlUser.id == request.user.id:
            myUrl.delete()
            return JsonResponse({"success": "URL deleted."}, status=200)
        else:
            return JsonResponse({"error": "User does not own this URL."}, status=400)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)

@login_required
def urlAdd(request):
    def getUniqueShorterURL(longUrl):
        urlHashed = hashlib.md5(longUrl.encode())
        return urlHashed.hexdigest()
    # TODO: Esto esta de mas, no?
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

