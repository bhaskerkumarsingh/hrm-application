from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from ..models import Attendance, AttendanceCorrection, Shift
from ..services import AttendanceService, AttendanceCorrectionService
from .serializers import (
    AttendanceSerializer,
    AttendanceCorrectionSerializer,
    ShiftSerializer
)

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Attendance.objects.all()
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        # Filter by officer
        officer_id = self.request.query_params.get('officer_id')
        if officer_id:
            queryset = queryset.filter(officer_id=officer_id)
            
        return queryset

    @action(detail=False, methods=['post'])
    def mark_attendance(self, request):
        officer_id = request.data.get('officer_id')
        shift_id = request.data.get('shift_id')
        
        try:
            attendance = AttendanceService.mark_attendance(
                officer_id=officer_id,
                shift_id=shift_id
            )
            serializer = self.get_serializer(attendance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class AttendanceCorrectionViewSet(viewsets.ModelViewSet):
    queryset = AttendanceCorrection.objects.all()
    serializer_class = AttendanceCorrectionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        correction = self.get_object()
        try:
            approved_correction = AttendanceCorrectionService.approve_correction(
                correction=correction,
                approved_by=request.user
            )
            serializer = self.get_serializer(approved_correction)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )