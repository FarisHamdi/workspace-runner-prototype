from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from backend_app import views

router = routers.DefaultRouter()
router.register(r'runners', views.RunnerViewSet)
router.register(r'workspaces', views.WorkspaceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', TemplateView.as_view(
        template_name='index.html'), 
        name='home'),
    path('registerRunner/', views.RegisterRunner.as_view()), 
    path('pingCoordinator/', views.CoordinatorPing.as_view()),
    path('createContainer/', views.CreateContainer.as_view()),
    # path('killContainer/')
]
