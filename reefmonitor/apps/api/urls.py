from django.urls import path
from django.conf.urls import url
from .views import AquariumView, MeasurementView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('doc', schema_view),
    path('aquariums/', AquariumView.as_view()),
    path('aquariums/<str:id>', AquariumView.as_view()),
    path('aquariums/<str:id>/measurements', MeasurementView.as_view())
]