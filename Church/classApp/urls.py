from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('class-dashboard/', views.class_dashboard, name='class_dashboard'),
    path('create-classroom/', views.create_classroom, name='create_classroom'),
    path('list-classes/', views.list_classes, name='list_classes'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add-student/', views.add_student, name='add_student'),
    path('list-students/', views.list_students, name='list_students'),


]
