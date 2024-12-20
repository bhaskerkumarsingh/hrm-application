from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.attendance_management.models import Attendance
from apps.leave_management.models import LeaveRequest
from apps.officer_profiles.models import Officer

class DashboardService:
    @staticmethod
    def get_attendance_summary(days=30):
        """Get attendance statistics for the last n days"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        return Attendance.objects.filter(
            date__range=[start_date, end_date]
        ).values('status').annotate(
            count=Count('id')
        )

    @staticmethod
    def get_leave_statistics():
        """Get current leave statistics"""
        return LeaveRequest.objects.filter(
            status='pending'
        ).count()

    @staticmethod
    def get_recent_activities(limit=10):
        """Get recent system activities"""
        # Combine recent attendance and leave records
        attendances = Attendance.objects.select_related('officer').order_by('-created_at')[:limit]
        leaves = LeaveRequest.objects.select_related('officer').order_by('-created_at')[:limit]
        
        activities = []
        for attendance in attendances:
            activities.append({
                'type': 'attendance',
                'officer': attendance.officer.name,
                'action': f"Marked {attendance.status}",
                'timestamp': attendance.created_at
            })
        
        for leave in leaves:
            activities.append({
                'type': 'leave',
                'officer': leave.officer.name,
                'action': f"Requested {leave.leave_type} leave",
                'timestamp': leave.created_at
            })
        
        return sorted(activities, key=lambda x: x['timestamp'], reverse=True)[:limit]