from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from base import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')),
         name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('topics/', views.TopicsView.as_view(), name='topics'),
    path('activity/', views.ActivityView.as_view(), name='activity'),
]
