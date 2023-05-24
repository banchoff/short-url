from django.urls import path, re_path
from . import views
from .views import SignUpView

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'([a-fA-F\d]{32})', views.redirectTo, name="redirectto"),
    path("user/toggle/ajax", views.userToggleAjax, name="usertoggleajax"),
    path("user/delete/ajax", views.userDeleteAjax, name="userdeleteajax"),
    path("user/changepw/ajax", views.userChangePWAjax, name="userchangepwajax"),
    path("url/add/ajax", views.urlAddAjax, name="urladdajax"),
    path("url/load/ajax", views.urlLoadAjax, name="loadurlsajax"),
    path("user/load/ajax", views.userLoadAjax, name="loadusersajax"),
    path("url/stats/ajax", views.urlStatsAjax, name="urlstatsajax"),
    path("url/delete/ajax", views.urlDeleteAjax, name="urldeleteajax"),
    path("user/add/ajax", views.userAddAjax, name="useraddajax"),
    path("url/add", views.urlAdd, name="urladd"),
#    path("user/add", views.userAdd, name="useradd"),
    path("user/edit", views.userEdit, name="useredit"),
    path("user/login", views.userLogin, name="userlogin"),
    path("user/logout", views.userLogout, name="userlogout"),
    path("user/list", views.userList, name="userlist"),
    path("help", views.help, name="help"),
    path("about", views.about, name="about"),
    path("signup/", SignUpView.as_view(), name="signup"),
]

