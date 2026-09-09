from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Zulfa Rahmi Nasution",
        "npm": "2506598324",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "An Information Systems student at Universitas Indonesia passionate about Business Development, Project Management, and Tech Innovation. Experienced in leadership and project execution through various organizational roles, with a strong focus on strategic problem-solving and stakeholder management."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Zulfa Rahmi Nasution",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
