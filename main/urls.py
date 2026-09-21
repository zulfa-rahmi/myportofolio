from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    # Halaman Utama (Mendukung 'show_main' dan 'main:show_main')
    path("", views.show_main, name="show_main"),

    # Projects
    path("projects/", views.show_projects, name="show_projects"),
    path("projects/create/", views.create_project, name="create_project"),
    path("projects/<uuid:id>/edit/", views.update_project, name="update_project"),
    path("projects/<uuid:id>/delete/", views.delete_project, name="delete_project"),

    # Experience
    path("experience/", views.show_experience, name="show_experience"),
    path("experience/create/", views.create_experience, name="create_experience"),
    path("experience/<uuid:id>/edit/", views.update_experience, name="update_experience"),
    path("experience/<uuid:id>/delete/", views.delete_experience, name="delete_experience"),
]