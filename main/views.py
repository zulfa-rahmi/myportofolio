from django.shortcuts import render

from main.models import Experience, Project

from main.forms import ProjectForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

def show_main(request):
    context = {
        "active_page": "main",
        "name": "Zulfa Rahmi Nasution",
        "npm": "2506598324",
        "study_program": "S1 Sistem Informasi",
        "based_in": "Depok, IDN",
        "bio": (
            "An Information Systems student at Universitas Indonesia passionate about "
            "Business Development, Project Management, and Tech Innovation. Experienced "
            "in leadership and project execution through various organizational roles, "
            "with a strong focus on strategic problem-solving and stakeholder management."
        ),
        "education": [
            {"program": "S1 - Sistem Informasi, Universitas Indonesia", "period": "2025 - Present"},
            {"program": "SMA Labschool Kebayoran", "period": "2022 - 2025"},
            {"program": "SMP Labschool Kebayoran", "period": "2019 - 2022"},
        ],
        "interests": ["Business Development", "Tech Innovation", "Project Management"],
        "socials": {
            "instagram": "https://www.instagram.com/zlfrahmi/",
            "github": "https://www.github.com/zulfa-rahmi",
            "linkedin": "https://www.linkedin.com/in/zulfa-rahmi-nasution-5a1600367/",
            "email": "mailto:zrahminasution@gmail.com",
        },
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "active_page": "experience",
        "name": "Zulfa Rahmi Nasution",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    json_response = get_projects_json(request)
    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]

    title_query = request.GET.get("title", "").strip()

    context = {
        "active_page": "projects",
        "name": "Zulfa Rahmi Nasution",
        "project_list": projects,
        "title_query": title_query,
    }

    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Zulfa Rahmi Nasution",
        "form": form,
        "is_edit": False,
    }
    return render(request, "projects_form.html", context)


def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Zulfa Rahmi Nasution",
        "form": form,
        "project": project,
        "is_edit": True,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")