from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/trips/', views.api_trips, name="api_trips"),
    path('api/trips/<int:pk>/', views.api_trip_detail, name='api_trip_detail'),
    path('<int:pk>/', views.trip_detail, name="detail"),
]

