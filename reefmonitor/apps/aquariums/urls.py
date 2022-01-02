from django.urls import path
from .views import home_view, delete_view, overview_view

urlpatterns = [
    path('', home_view, name='dashboard'),
    path('<str:aquarium_id>/delete', delete_view, name='delete'),
    path('<str:aquarium_id>/overview', overview_view, name='overview'),
]