from django.urls import path
from . import views
from django.urls import path, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', RedirectView.as_view(url='/login/'), name='redirect_to_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('class-dashboard/', views.class_dashboard, name='class_dashboard'),
    path('create-classroom/', views.create_classroom, name='create_classroom'),
    path('list-classes/', views.list_classes, name='list_classes'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add-student/', views.add_student, name='add_student'),
    path('list-students/', views.list_students, name='list_students'),
    path('attendance-dashboard/', views.attendance_dashboard, name='attendance_dashboard'),
    path('check-in/', views.check_in, name='check_in'),
    path('confirm-check-in/', views.confirm_check_in, name='confirm_check_in'),
    path('attendance-dashboard/todays-checkins/', views.todays_checkins, name='todays_checkins'),
    path('reports_dashboard/', views.reports_dashboard, name='reports_dashboard'),

    path('attendance_report/', views.attendance_report, name='attendance_report'),
    path('reports_dashboard/classroom_reports/', views.classroom_reports, name='classroom_reports'),

]
