from django.urls import path
from .views import rules_view, analyze_view

urlpatterns = [
    path('<str:aquarium_id>/rules', rules_view, name='overview'),
    path('<str:aquarium_id>/analyze', analyze_view, name='analyze'),
]