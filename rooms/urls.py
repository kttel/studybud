from django.urls import path

from rooms import views


urlpatterns = [
    path('create-room/', views.CreateRoomView.as_view(), name='create-room'),
    path('update-room/<str:pk>/', views.UpdateRoomView.as_view(),
         name='update-room'),
    path('room/<str:pk>/delete/', views.DeleteRoomView.as_view(),
         name='delete-room'),
    path('<str:pk>/', views.RoomDetailView.as_view(), name='room'),
    path('<str:pk>/message/', views.MessageView.as_view(),
         name='room-message'),
    path('<str:pk_room>/delete-message/<str:pk>/',
         views.DeleteMessageView.as_view(),
         name='delete-message'),
]
