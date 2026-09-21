from django.shortcuts import render, redirect, get_object_or_404
from main.models import Project, Experience
from main.forms import ProjectForm, ExperienceForm

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

# --- PROJECTS ---

def show_projects(request):
    title_query = request.GET.get('title', '')
    if title_query:
        projects = Project.objects.filter(title__icontains=title_query)
    else:
        projects = Project.objects.all()
    
    context = {
        'project_list': projects,
        'title_query': title_query,
    }
    return render(request, 'projects.html', context)

def create_project(request):
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

def update_project(request, id):
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

def delete_project(request, id):
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        project.delete()
    return redirect('main:show_projects')


# --- EXPERIENCE ---

def show_experience(request):
    experience_list = Experience.objects.all().order_by('-started_at')
    context = {
        'experience_list': experience_list,
    }
    return render(request, 'experience.html', context)

def create_experience(request):
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

def update_experience(request, id):
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

def delete_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    if request.method == 'POST':
        experience.delete()
    return redirect('main:show_experience')