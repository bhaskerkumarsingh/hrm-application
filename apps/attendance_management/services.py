from datetime import datetime, time
from django.utils import timezone
from django.db.models import Q
from .models import Attendance, Shift

class AttendanceService:
    @staticmethod
    def mark_attendance(officer, shift, check_in_time=None):
        """Mark attendance for an officer."""
        now = timezone.now()
        today = now.date()
        
        # If check_in_time is not provided, use current time
        check_in_time = check_in_time or now
        
        # Calculate status based on shift timings
        status = AttendanceService._calculate_status(check_in_time, shift)
        
        attendance = Attendance.objects.create(
            officer=officer,
            date=today,
            shift=shift,
            status=status,
            check_in=check_in_time
        )
        return attendance

    @staticmethod
    def _calculate_status(check_in_time, shift):
        """Calculate attendance status based on check-in time and shift."""
        shift_start = datetime.combine(check_in_time.date(), shift.start_time)
        grace_period = shift.grace_period
        
        if check_in_time <= shift_start + timezone.timedelta(minutes=grace_period):
            return 'present'
        elif check_in_time <= shift_start + timezone.timedelta(hours=4):
            return 'late'
        else:
            return 'half_day'

    @staticmethod
    def get_attendance_summary(officer, start_date, end_date):
        """Get attendance summary for an officer within a date range."""
        attendances = Attendance.objects.filter(
            officer=officer,
            date__range=(start_date, end_date)
        )
        
        summary = {
            'present': attendances.filter(status='present').count(),
            'absent': attendances.filter(status='absent').count(),
            'late': attendances.filter(status='late').count(),
            'half_day': attendances.filter(status='half_day').count(),
            'on_leave': attendances.filter(status='on_leave').count(),
        }
        return summary

class AttendanceCorrectionService:
    @staticmethod
    def request_correction(attendance, new_status, reason, requested_by):
        """Request attendance correction."""
        from .models import AttendanceCorrection
        
        correction = AttendanceCorrection.objects.create(
            attendance=attendance,
            previous_status=attendance.status,
            new_status=new_status,
            reason=reason,
            requested_by=requested_by
        )
        return correction

    @staticmethod
    def approve_correction(correction, approved_by):
        """Approve attendance correction request."""
        correction.status = 'approved'
        correction.approved_by = approved_by
        correction.save()
        
        # Update the attendance record
        attendance = correction.attendance
        attendance.status = correction.new_status
        attendance.save()
        
        return correction