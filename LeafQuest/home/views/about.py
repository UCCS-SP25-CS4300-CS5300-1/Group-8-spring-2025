from django.shortcuts import render

def about_view(request):
    project_description = (
        "LeafQuest is an application that allows users to identify plants, "
        "save them in a Plantdex, share findings with friends, "
        "earn badges, and view a map of plant locations."
    )

    github_link = "https://github.com/UCCS-SP25-CS4300-CS5300-1/Group-8-spring-2025"

    developers = [
        {"name": "David Jones", "github": "https://github.com/wycre"},
        {"name": "Taylor Lopez", "github": "https://github.com/iAmMortos"},
        {"name": "Zach Middleton", "github": "https://github.com/zmidd520"},
        {"name": "Keegan Smith", "github": "https://github.com/keegssmith"},
        {"name": "Ethan Steiner", "github": "https://github.com/esteiner72"},
    ]

    return render(request, 'about/index.html', {
        'description': project_description,
        'github_link': github_link,
        'developers': developers,
        'version': '1.0.0',
    })
