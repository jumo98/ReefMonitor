from django.urls import path
from django.views.generic import TemplateView
from rest_framework.authtoken import views
from .views import AquariumView, MeasurementView, SwaggerView

urlpatterns = [
    # Swagger Documentation
    path('doc', TemplateView.as_view(
        template_name='api/swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='doc'),
    path('openapi-schema', SwaggerView.as_view(), name='openapi-schema'),
    # API calls
    path('aquariums/', AquariumView.as_view()),
    path('aquariums/<str:id>', AquariumView.as_view()),
    path('aquariums/<str:id>/measurements', MeasurementView.as_view()),
    # Token auth
    path('token/', views.obtain_auth_token),
    path('token', views.obtain_auth_token)
]