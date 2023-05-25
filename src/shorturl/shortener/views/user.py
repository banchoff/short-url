from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models import URLUser
from django.urls import reverse_lazy
from ..forms import URLUserCreationForm, URLUserChangeForm


@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None, login_url=reverse_lazy("index"))
def userLoadAjax(request):
    count = 5
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax and request.method == "POST":
        pageNum = request.POST["pageNum"]
        nextPage = -1
        prevPage = 1
        lastPage = -1
        currentPage = 1
        usersArray = []

        users = URLUser.objects.all()
        paginator = Paginator(users, count)
        page = paginator.get_page(pageNum)

        if page.has_previous():
            prevPage = page.previous_page_number()
        if page.has_next():
            nextPage = page.next_page_number()
        lastPage = paginator.num_pages
        currentPage = page.number
        
        for aUser in page.object_list:
            usersArray.append({
                'id': aUser.id,
                'first_name': aUser.first_name,
                'last_name': aUser.last_name,
                'username': aUser.username,
                'id': aUser.id,
                'is_superuser': aUser.is_superuser,
                'email': aUser.email,})
            
        resp = {
            'next': nextPage,
            'prev': prevPage,
            'last': lastPage,
            'current': currentPage,
            'data': usersArray,
        }
        return JsonResponse(resp, status=200)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)

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
    
        # TODO: Esto no usa el id del usuario, se pierde en el request, por lo que termina creando un registro nuevo en vez de actualizar el actual.
        # form = URLUserChangeForm(request.POST) # Passes POST data to the form
        # if form.is_valid():
            
        #     form.save()
        #     return HttpResponseRedirect('/shortener/')
    return render(request, "shortener/userEdit.html", {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None, login_url=reverse_lazy("index"))
def userDeleteAjax(request):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax and request.method == "POST":
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

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == "POST":
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            return JsonResponse({"error": "Passwords do not match."}, status=400)
        userId = request.POST["id"]
        if request.user.id == userId:
            # Cambia su password. OK
            aUser = URLUser.objects.get(pk=userId)
            aUser.set_password(password1)
            aUser.save()
            return JsonResponse({"success": "Password changed."}, status=200)
        else:
            if request.user.is_superuser:
                # Es admin, puede cambiar cualquier password. OK
                aUser = URLUser.objects.get(pk=userId)
                aUser.set_password(password1)
                aUser.save()
                return JsonResponse({"success": "Password changed."}, status=200)
            else:
                # Quiere cambiar la password de otro usuario pero no es admin. ERROR
                return JsonResponse({"error": "User has no permission."}, status=400)
                pass
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)


@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None, login_url=reverse_lazy("index"))
def userList(request):
    users = URLUser.objects.all()
    add_user_form = URLUserCreationForm()

    return render(request, "shortener/userList.html", {'users': users, 'add_user_form': add_user_form})


def userLogin(request):
    return render(request, "shortener/userLogin.html")


@login_required
def userLogout(request):
    return render(request, "shortener/userLogout.html")



@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None, login_url=reverse_lazy("index"))
def userToggleAjax(request):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax and request.method == "POST":
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

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax and request.method == "POST":
        form = URLUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": "User created."}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": "Request should be Ajax POST."}, status=400)

