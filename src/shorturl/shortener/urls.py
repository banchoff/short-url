from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path("", views.index, name="index"),
    path("url/add", views.urlAdd, name="urladd"),
#    path("user/add", views.userAdd, name="useradd"),
#    path("user/edit", views.userEdit, name="useredit"),
    path("user/login", views.userLogin, name="userlogin"),
    path("user/logout", views.userLogout, name="userlogout"),
    path("user/list", views.userList, name="userlist"),
    path("help", views.help, name="help"),
    path("about", views.about, name="about"),
    path("signup/", SignUpView.as_view(), name="signup"),
]

