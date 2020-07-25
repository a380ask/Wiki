from django.urls import path

from . import views

app_name = "tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="getEntry"),
    path("createPage", views.createPage, name="createPage"),
    path("edit/<str:entry>", views.editPage, name="editPage"),
    path("search", views.search, name="search"),
    path("random", views.randomize, name="random"),
    path("delete/<str:name>", views.delete, name="delete")
]
