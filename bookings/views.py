from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Booking
from .serializers import BookingSerializer
from core.permissions import IsAdminOrResourceManager


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'user']
    search_fields = ['user__email', 'user__first_name']
    ordering_fields = ['created_at', 'start_date']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'employee':
            return Booking.objects.filter(user=user).prefetch_related('items__resource')
        return Booking.objects.all().prefetch_related('items__resource')

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ['approve', 'reject']:
            return [IsAdminOrResourceManager()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.user != request.user:
            return Response(
                {'detail': 'You can only cancel your own bookings.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.status not in ['pending', 'approved']:
            return Response(
                {'detail': f'Cannot cancel a booking with status "{booking.status}".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'cancelled'
        booking.save()
        return Response({'detail': 'Booking cancelled successfully.'})

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        booking = self.get_object()

        if booking.status != 'pending':
            return Response(
                {'detail': 'Only pending bookings can be approved.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'approved'
        booking.reviewed_by = request.user
        booking.reviewed_at = timezone.now()
        booking.save()
        return Response({'detail': 'Booking approved successfully.'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        booking = self.get_object()

        if booking.status != 'pending':
            return Response(
                {'detail': 'Only pending bookings can be rejected.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reason = request.data.get('reason', '')
        if not reason:
            return Response(
                {'detail': 'A rejection reason is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'rejected'
        booking.rejection_reason = reason
        booking.reviewed_by = request.user
        booking.reviewed_at = timezone.now()
        booking.save()
        return Response({'detail': 'Booking rejected successfully.'})
