from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ResourceViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('', ResourceViewSet, basename='resource')

urlpatterns = [
    path('', include(router.urls)),
]
