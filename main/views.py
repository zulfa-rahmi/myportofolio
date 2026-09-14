from django.shortcuts import render

from main.models import Experience, Project


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
        "name": "Zulfa Rahmi Nasution",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    context = {
        "active_page": "projects",
        "name": "Zulfa Rahmi Nasution",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)
