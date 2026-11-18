from rest_framework import serializers
from django.db.models import Sum
from .models import Booking, BookingItem
from resources.models import Resource
from users.serializers import UserSerializer


class BookingItemSerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)

    class Meta:
        model = BookingItem
        fields = ['id', 'resource', 'resource_name', 'quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('Quantity must be at least 1.')
        return value


class BookingSerializer(serializers.ModelSerializer):
    items = BookingItemSerializer(many=True)
    user = UserSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'status', 'start_date', 'end_date',
            'items', 'rejection_reason', 'reviewed_by', 'reviewed_at', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'rejection_reason', 'reviewed_by', 'reviewed_at', 'created_at']

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if end_date <= start_date:
            raise serializers.ValidationError('End date must be after start date.')

        items = data.get('items', [])
        if not items:
            raise serializers.ValidationError('A booking must have at least one item.')

        for item in items:
            resource = item['resource']
            quantity = item['quantity']

            if resource.status == 'inactive':
                raise serializers.ValidationError(
                    f'Resource "{resource.name}" is inactive and cannot be booked.'
                )

            already_booked = BookingItem.objects.filter(
                resource=resource,
                booking__status='approved',
                booking__start_date__lte=end_date,
                booking__end_date__gte=start_date,
            ).aggregate(total=Sum('quantity'))['total'] or 0

            available = resource.total_quantity - already_booked
            if quantity > available:
                raise serializers.ValidationError(
                    f'Only {available} unit(s) of "{resource.name}" available for the requested period.'
                )

        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        booking = Booking.objects.create(**validated_data)
        for item in items_data:
            BookingItem.objects.create(booking=booking, **item)
        return booking
