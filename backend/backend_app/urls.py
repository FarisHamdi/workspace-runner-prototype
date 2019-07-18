from django.urls import path, include
from django.views.generic import TemplateView
from backend_app.views import RegisterRunner
urlpatterns = [
    path('', TemplateView.as_view(
        template_name='index.html'), 
        name='home'),
    path('registerRunner/', RegisterRunner.as_view())
]
