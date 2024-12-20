from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import (
    AttendanceViewSet,
    AttendanceCorrectionViewSet,
    ShiftViewSet
)
from .views import (
    AttendanceListView,
    AttendanceMarkView
)

# API Router
router = DefaultRouter()
router.register(r'shifts', ShiftViewSet)
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'corrections', AttendanceCorrectionViewSet)

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Web URLs
    path('', AttendanceListView.as_view(), name='attendance_list'),
    path('mark/', AttendanceMarkView.as_view(), name='attendance_mark'),
]