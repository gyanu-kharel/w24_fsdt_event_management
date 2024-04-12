from django.shortcuts import render



def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def register_post(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    print(name, email, password)