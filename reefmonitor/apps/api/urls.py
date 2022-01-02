from django.urls import path
from .views import AquariumView, MeasurementView

urlpatterns = [
    path('aquariums/', AquariumView.as_view()),
    path('aquariums/<str:id>', AquariumView.as_view()),
    path('aquariums/<str:id>/measurements', MeasurementView.as_view())
]