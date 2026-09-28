from django.shortcuts import render, redirect, get_object_or_404
from main.models import Project, Experience
from main.forms import ProjectForm, ExperienceForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.http import HttpResponse

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
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
        "last_login": last_login,
    }
    return render(request, "index.html", context)

# --- PROJECTS ---

def show_projects(request):
  title_query = request.GET.get('title', '').strip()
  json_response = get_projects_json(request)

  projects_deserialized = serializers.deserialize(
      'json',
      json_response.content.decode('utf-8'),
  )
  projects = [project.object for project in projects_deserialized]

  context = {
      "active_page": "projects",
      'name': 'Zulfa Rahmi Nasution',
      'project_list': projects,
      'title_query': title_query,
  }
  return render(request, 'projects.html', context)

@login_required(login_url="/login/")
def create_project(request):

    if not (request.user.is_superuser or request.user.groups.filter(name='Editor').exists()):
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:show_projects')
    else:
        form = ProjectForm()
    
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'projects_form.html', context)

@login_required(login_url="/login/")
def update_project(request, id):

    if not (request.user.is_superuser or request.user.groups.filter(name='Editor').exists()):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('main:show_projects')
    else:
        form = ProjectForm(instance=project)
    
    context = {
        'form': form,
        'project': project,
        'is_edit': True,
    }
    return render(request, 'projects_form.html', context)

@login_required(login_url="/login/")
def delete_project(request, id):

    if not (request.user.is_superuser or request.user.groups.filter(name='Editor').exists()):
        raise PermissionDenied
    
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        project.delete()
    return redirect('main:show_projects')

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")

# --- EXPERIENCE ---

def show_experience(request):
  title_query = request.GET.get('title', '').strip()
  json_response = get_experience_json(request)

  experiences_deserialized = serializers.deserialize(
      'json',
      json_response.content.decode('utf-8'),
  )
  experience_list = [exp.object for exp in experiences_deserialized]

  context = {
      "active_page": "experience",
      'experience_list': experience_list,
      'title_query': title_query,
  }
  return render(request, 'experience.html', context)

@login_required(login_url="/login/")
def create_experience(request):
    
    if not (request.user.is_superuser or request.user.groups.filter(name='Editor').exists()):
        raise PermissionDenied

    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:show_experience')
    else:
        form = ExperienceForm()
    
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'experience_form.html', context)

@login_required(login_url="/login/")
def update_experience(request, id):

    if not (request.user.is_superuser or request.user.groups.filter(name='Editor').exists()):
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=id)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('main:show_experience')
    else:
        form = ExperienceForm(instance=experience)
    
    context = {
        'form': form,
        'experience': experience,
        'is_edit': True,
    }
    return render(request, 'experience_form.html', context)

@login_required(login_url="/login/")
def delete_experience(request, id):

    if not (request.user.is_superuser or request.user.groups.filter(name='Editor').exists()):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=id)
    if request.method == 'POST':
        experience.delete()
    return redirect('main:show_experience')

def get_experience_json(request):
  title_query = request.GET.get('title', '').strip()
  experiences = Experience.objects.all().order_by('-started_at')

  if title_query:
    experiences = experiences.filter(title__icontains=title_query)

  experience_json = serializers.serialize('json', experiences, use_natural_foreign_keys=True)
  return HttpResponse(experience_json, content_type='application/json')

# --- LOGIN/LOGOUT FOR USER ---

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "active_page": "register",
        "name": "Zulfa Rahmi Nasution",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "active_page": "login",
        "name": "Zulfa Rahmi Nasution",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")