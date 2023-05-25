from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models import URLUser
from django.urls import reverse_lazy
from ..forms import URLUserCreationForm, URLUserChangeForm
from .common import isAjaxAndPost, objectLoadAjax

@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None, login_url=reverse_lazy("index"))
def userLoadAjax(request):    
    def funcAssign(aDict):
        return {
            'id': aDict.id,
            'first_name': aDict.first_name,
            'last_name': aDict.last_name,
            'username': aDict.username,
            'id': aDict.id,
            'is_superuser': aDict.is_superuser,
            'email': aDict.email,
        }
    return objectLoadAjax(request, URLUser.objects.all(), funcAssign)

@login_required
def userEdit(request):
    currentUser = URLUser.objects.get(pk=request.user.id)
    form = URLUserChangeForm(instance=currentUser)  # Initial data
    if request.method == 'POST':
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        currentUser.email = email
        currentUser.first_name = first_name
        currentUser.last_name = last_name
        currentUser.save()
        return HttpResponseRedirect('/shortener/')
    return render(request, "shortener/userEdit.html", {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None, login_url=reverse_lazy("index"))
def userDeleteAjax(request):
    if isAjaxAndPost(request):
        userId = request.POST["id"]
        aUser = get_object_or_404(URLUser, pk=userId)
        if aUser.id != request.user.id:
            aUser.delete()
            return JsonResponse({"success": "User deleted."}, status=200)
        else:
            return JsonResponse({"error": "User cannot delete herself."}, status=400)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)

@login_required
def userChangePWAjax(request):
    if isAjaxAndPost(request):
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            return JsonResponse({"error": "Passwords do not match."}, status=400)
        userId = request.POST["id"]
        if request.user.id == userId:
            # Changes own password. OK
            aUser = URLUser.objects.get(pk=userId)
            aUser.set_password(password1)
            aUser.save()
            return JsonResponse({"success": "Password changed."}, status=200)
        else:
            if request.user.is_superuser:
                # Admin can change any password. OK
                aUser = URLUser.objects.get(pk=userId)
                aUser.set_password(password1)
                aUser.save()
                return JsonResponse({"success": "Password changed."}, status=200)
            else:
                # Nonadmin users cannot change other user's password. ERROR
                return JsonResponse({"error": "User has no permission."}, status=400)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)

@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None, login_url=reverse_lazy("index"))
def userList(request):
    users = URLUser.objects.all()
    add_user_form = URLUserCreationForm()
    return render(request, "shortener/userList.html", {'users': users, 'add_user_form': add_user_form})

@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None, login_url=reverse_lazy("index"))
def userToggleAjax(request):
    if isAjaxAndPost(request):
        userId = request.POST["id"]
        aUser = get_object_or_404(URLUser, pk=userId)
        userState = "NOTADMIN"
        if aUser.is_superuser:
            userState = "ADMIN"
        if aUser.id == request.user.id:
            return JsonResponse({'userState': userState, 'error': 'Cannot change your own user.'}, status=400)
        # Toggle user role
        aUser.is_superuser = not aUser.is_superuser
        userState = "NOTADMIN"
        if aUser.is_superuser:
            userState = "ADMIN"
        aUser.save()
        return JsonResponse({'userState': userState}, status=200)
    else:
        return JsonResponse({"error": "Request should be Ajax POST."}, status=400)

@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None, login_url=reverse_lazy("index"))
def userAddAjax(request):
    if isAjaxAndPost(request):
        form = URLUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": "User created."}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)

