from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')


def login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        request_body = {
            'email': email,
            'password': password
        }

        response = requests.post('http://authentication:8000/auth/login', json=request_body)

        if response.status_code == 200:
            token = response.json()['access_token']
            curr_reponse = JsonResponse({'message': 'Token added to the cookie'})
            curr_reponse.set_cookie('access_token', token, max_age=3600)

            return redirect('index')
        else:
            return render(request, 'login.html', {'error_msg': 'Invalid login credentials'})

    return render(request, 'login.html')


def register(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        request_body = {
            'name': name,
            'email': email,
            'password': password
        }

        response = requests.post('http://authentication:8000/auth/register', json=request_body)

        if response.status_code == 200:
            token = response.json()['access_token']
            curr_response = JsonResponse({'message': 'Token added to the cookie'})
            curr_response.set_cookie('access_token', token, max_age=3600)

            return redirect('index')
        
        elif response.status_code == 400:
            return render(request, 'register.html', {'error_msg': response.json()['detail']})
        else:
            return render(request, 'register.html', {'error_msg': 'Internal server error.'})

    return render(request, 'register.html')
