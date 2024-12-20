from rest_framework import serializers
from ..models import Attendance, AttendanceCorrection, Shift

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    officer_name = serializers.CharField(source='officer.name', read_only=True)
    shift_name = serializers.CharField(source='shift.name', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'officer', 'officer_name', 'date', 'shift', 
            'shift_name', 'status', 'check_in', 'check_out',
            'remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class AttendanceCorrectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceCorrection
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'status']