from rest_framework import serializers
from .models import Category, Resource


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class ResourceSerializer(serializers.ModelSerializer):
    available_quantity = serializers.ReadOnlyField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Resource
        fields = [
            'id', 'name', 'description', 'category', 'category_name',
            'total_quantity', 'available_quantity', 'location', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'available_quantity']
