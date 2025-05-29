from django.shortcuts import render

def home(request):
    return render(request, "home.html")  # Rendering the home.html template
