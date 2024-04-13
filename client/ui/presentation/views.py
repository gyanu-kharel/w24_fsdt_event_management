from django.shortcuts import render, redirect
import requests


def index(request):
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return redirect('login')
    
    access_token = request.COOKIES.get('access_token')
    request_header = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    response = requests.get('http://events:8002/events/all', headers=request_header)

    return render(request, 'index.html', {'events': response.json()})


def logout(request):
    curr_response = redirect("login")
    curr_response.delete_cookie('access_token')

    return curr_response


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
            curr_reponse = redirect('index')
            curr_reponse.set_cookie('access_token', token, max_age=3600)

            return curr_reponse
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
            curr_reponse = redirect('index')
            curr_reponse.set_cookie('access_token', token, max_age=3600)

            return curr_reponse
        
        elif response.status_code == 400:
            return render(request, 'register.html', {'error_msg': response.json()['detail']})
        else:
            return render(request, 'register.html', {'error_msg': 'Internal server error.'})

    return render(request, 'register.html')



def events(request):
    access_token = request.COOKIES.get('access_token')
    request_header = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    response = requests.get('http://events:8002/events', headers=request_header)

    return render(request, 'events.html', {'events': response.json()})

def create_event(request):
    if request.method == 'POST':

        access_token = request.COOKIES.get('access_token')

        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        date = request.POST.get('date')
        capacity = request.POST.get('capacity')

        request_header = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        request_body = {
            "title": title,
            "description": description,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
            "date": date,
            "capacity": capacity
        }

        response = requests.post('http://events:8002/events', json=request_body, headers=request_header)

        if response.status_code == 200:
            return redirect('events')
        
        elif response.status_code == 400:
            error_msg = response.json['detail']
            return render(request, 'create_event.html', {'error_msg': error_msg})
        else:
            return render(request, 'create_event.html', {'error_msg': 'Internal server error'})

    return render(request, 'create_event.html')


def delete_event(request, event_id):
     access_token = request.COOKIES.get('access_token')
     request_header = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
     
     response = requests.delete(f'http://events:8002/events/{event_id}', headers=request_header)
     print(response)
     if response.status_code == 200:
        return redirect('events')
     else:
         return redirect('events')
     

def event_invitations(request, event_id):
    access_token = request.COOKIES.get('access_token')
    request_header = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    response = requests.get(f'http://authentication:8000/auth/users', headers=request_header)
    
    return render(request, 'event_invitations.html', {'users': response.json(), 'event_id': event_id})


def send_event_invite(request, event_id, user_id):
    access_token = request.COOKIES.get('access_token')
    request_header = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    request_body = {
        'user_id': user_id
    }
    
    response = requests.post(f'http://events:8002/events/{event_id}/invitations', json=request_body, headers=request_header)
    
    return redirect('event_invitations', event_id)



def invitations(request):
    access_token = request.COOKIES.get('access_token')
    request_header = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    response = requests.get(f'http://events:8002/events/invitations', headers=request_header)

    return render(request, 'invitations.html', {'invitations': response.json()})


def accept_invite(request, invite_id):
    access_token = request.COOKIES.get('access_token')
    request_header = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    request_body = {
        'confirm': True
    }
    
    response = requests.put(f'http://events:8002/events/invitations/{invite_id}',json=request_body, headers=request_header)
    return redirect('invitations')


def decline_invite(request, invite_id):
    access_token = request.COOKIES.get('access_token')
    request_header = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    request_body = {
        'confirm': False
    }
    
    response = requests.put(f'http://events:8002/events/invitations/{invite_id}',json=request_body, headers=request_header)
    return redirect('invitations')
