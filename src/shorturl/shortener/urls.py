from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("user/edit", views.userEdit, name="useredit"),
        path("user/list", views.userList, name="userlist"),
        ]

