from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('events', views.events, name='events'),
    path('create_event', views.create_event, name='create_event'),
    path('events/<str:event_id>/', views.delete_event, name='delete_event')
]