from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Resource
from .serializers import CategorySerializer, ResourceSerializer
from core.permissions import IsAdminOrResourceManager


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrResourceManager()]


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.select_related('category').all()
    serializer_class = ResourceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'location', 'status']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'total_quantity']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrResourceManager()]

    def get_queryset(self):
        queryset = Resource.objects.select_related('category').all()
        if self.request.query_params.get('available'):
            queryset = queryset.filter(status='active')
        return queryset
