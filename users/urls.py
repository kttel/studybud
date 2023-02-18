from django.urls import path

from users import views


urlpatterns = [
    path('edit/', views.UpdateProfileView.as_view(), name='edit-user'),
    path('<str:pk>/', views.ProfileView.as_view(), name='user-profile'),
]
