from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name="logout"),
    path('events', views.events, name='events'),
    path('create_event', views.create_event, name='create_event'),
    path('events/<str:event_id>/', views.delete_event, name='delete_event'),
    path('events/<str:event_id>/invitations', views.event_invitations, name='event_invitations'),
    path('events/<str:event_id>/invitations/<str:user_id>', views.send_event_invite, name='send_event_invite'),
    path('invitations', views.invitations, name='invitations'),
    path('invitations/<str:invite_id>', views.accept_invite, name='accept_invite'),
    path('invitations/<str:invite_id>', views.decline_invite, name='decline_invite')
]