from django.urls import path, include

from rest_framework.routers import DefaultRouter

from base.api import views


router = DefaultRouter()
router.register('rooms', views.RoomViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('me/', views.Profile.as_view()),
]
