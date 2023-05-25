from django.urls import path, re_path
from .views import SignUpView
from .views import common
from .views import user
from .views import url

urlpatterns = [
    re_path(r'([a-fA-F\d]{32})', common.redirectTo, name="redirectto"),
    path("help", common.help, name="help"),
    path("about", common.about, name="about"),
    path("signup/", SignUpView.as_view(), name="signup"),

    path("", url.index, name="index"),
    path("url/add/ajax", url.urlAddAjax, name="urladdajax"),
    path("url/load/ajax", url.urlLoadAjax, name="loadurlsajax"),
    path("url/stats/ajax", url.urlStatsAjax, name="urlstatsajax"),
    path("url/delete/ajax", url.urlDeleteAjax, name="urldeleteajax"),
    path("url/add", url.urlAdd, name="urladd"),

    path("user/edit", user.userEdit, name="useredit"),
    path("user/add/ajax", user.userAddAjax, name="useraddajax"),
    path("user/load/ajax", user.userLoadAjax, name="loadusersajax"),
    path("user/login", user.userLogin, name="userlogin"),
    path("user/logout", user.userLogout, name="userlogout"),
    path("user/list", user.userList, name="userlist"),
    path("user/toggle/ajax", user.userToggleAjax, name="usertoggleajax"),
    path("user/delete/ajax", user.userDeleteAjax, name="userdeleteajax"),
    path("user/changepw/ajax", user.userChangePWAjax, name="userchangepwajax"),
]
