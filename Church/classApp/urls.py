from django.urls import path
from . import views
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.urls import path

from django.urls import path
from . import views

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

    path('search_student/', views.search_student, name='search_student'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_administrator/', views.add_administrator, name='add_administrator'),
    path('edit_admin/', views.edit_admin, name='edit_admin'),
    path('update_admin/<int:admin_id>/', views.update_admin, name='update_admin'),
    path('delete_admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),
    path('reports_dashboard/date_range_report/', views.date_range_report, name='date_range_report'),

]


