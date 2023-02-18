from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from base import views

# apps: rooms, users, main
urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/',
         LogoutView.as_view(next_page=reverse_lazy('home')),
         name='logout'),
    path('register/',
         views.RegisterUserView.as_view(), name='register'),

    # users
    path('profile/<str:pk>/',
         views.ProfileView.as_view(),
         name='user-profile'),
    path('edit-user/',
         views.UpdateProfileView.as_view(), name='edit-user'),

    # main
    path('', views.HomeView.as_view(), name='home'),
    path('topics/', views.TopicsView.as_view(), name='topics'),
    path('activity/', views.ActivityView.as_view(), name='activity'),

    # rooms
    path('room/<str:pk>/', views.RoomDetailView.as_view(), name='room'),
    path('room/<str:pk>/message/',
         views.MessageView.as_view(),
         name='room-message'),
    path('room/<str:pk_room>/delete-message/<str:pk>/',
         views.DeleteMessageView.as_view(),
         name='delete-message'),
    path('create-room/',  views.CreateRoomView.as_view(), name='create-room'),
    path('update-room/<str:pk>/',
         views.UpdateRoomView.as_view(), name='update-room'),
    path('room/<str:pk>/delete/',
         views.DeleteRoomView.as_view(), name='delete-room'),
]
