
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
# from .forms import DateRangeForm
# from django.db.models import Count


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if the user exists and if they are active
        if user is not None and user.is_active:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials or inactive account'})
    return render(request, 'login.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')



@login_required
def class_dashboard(request):
    return render(request, 'class_dashboard.html')


from .forms import ClassroomForm


@login_required
def create_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.created_by = request.user
            classroom.save()
            return redirect('class_dashboard')
    else:
        form = ClassroomForm()
    return render(request, 'create_classroom.html', {'form': form})




@login_required
def list_classes(request):
    classrooms = Classroom.objects.all()

    # Aggregating the student counts for each classroom
    class_counts = Student.objects.values('classroom__name').annotate(total_students=Count('classroom')).order_by('classroom__name')

    # Combine both querysets into one context dictionary for the template
    context = {
        'classrooms': classrooms,
        'class_counts': class_counts
    }

    return render(request, 'list_classes.html', context)



@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')



from .forms import AddStudentForm



@login_required
def add_student(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.added_by = request.user
            student.save()
            return redirect('student_dashboard')
    else:
        form = AddStudentForm()
    return render(request, 'add_student.html', {'form': form})




@login_required
def list_students(request):
    students = Student.objects.all()
    class_counts = Student.objects.values('classroom__name').annotate(total_students=Count('classroom'))

    return render(request, 'list_students.html', {'students': students, 'class_counts': class_counts})


@login_required
def attendance_dashboard(request):
    return render(request, 'attendance_dashboard.html')


from .forms import CheckInForm
from .models import Classroom, Student, CheckIn

from datetime import timedelta


@login_required
def check_in(request):
    if 'classroom_id' in request.GET:
        classroom_id = request.GET.get('classroom_id')
        form = CheckInForm(classroom_id, request.POST or None)

        # Determine which students have been checked in within the past 4 hours
        four_hours_ago = timezone.now() - timedelta(hours=4)
        recently_checked_in_students = CheckIn.objects.filter(
            student__classroom_id=classroom_id,
            checked_on__gte=four_hours_ago
        ).values_list('student_id', flat=True)

        if request.method == "POST":
            if form.is_valid():
                selected_students = form.cleaned_data['students']
                request.session['selected_students'] = [s.pk for s in selected_students]
                return redirect('confirm_check_in')
            else:
                # Handle form errors
                messages.error(request, 'There was an error with the form.')
        return render(request, 'select_students.html', {
            'form': form,
            'recently_checked_in_students': recently_checked_in_students
        })

    classrooms = Classroom.objects.all()
    return render(request, 'list_classrooms.html', {'classrooms': classrooms})



@login_required
def confirm_check_in(request):
    selected_student_ids = request.session.get('selected_students', [])
    selected_students = Student.objects.filter(pk__in=selected_student_ids)

    if request.method == "POST":
        for student in selected_students:
            CheckIn.objects.create(student=student, checked_by=request.user)
        del request.session['selected_students']
        return redirect('dashboard')  # Or wherever you'd like to send the user

    return render(request, 'confirm_check_in.html', {'students': selected_students})



from django.utils import timezone

@login_required
def todays_checkins(request):
    # Get today's check-ins
    today = timezone.localdate()
    checkins = CheckIn.objects.filter(checked_on__date=today).select_related('student')

    # Group by classroom
    classrooms = {}
    for checkin in checkins:
        classroom_name = checkin.student.classroom.name  # Assuming your Classroom model has a 'name' field
        if classroom_name not in classrooms:
            classrooms[classroom_name] = []
        classrooms[classroom_name].append(checkin.student)

    return render(request, 'todays_checkins.html', {'classrooms': classrooms})



@login_required
def reports_dashboard(request):
    return render(request, 'reports_dashboard.html')


from .models import Student, CheckIn

@login_required
def attendance_report(request):
    student_attendance_counts = Student.objects.annotate(
        total_checkins=Count('checkin')
    ).order_by('classroom', '-total_checkins')

    grouped_by_classroom = {}
    for student in student_attendance_counts:
        if student.classroom not in grouped_by_classroom:
            grouped_by_classroom[student.classroom] = []
        grouped_by_classroom[student.classroom].append(student)

    return render(request, 'attendance_report.html', {'classrooms': grouped_by_classroom})


from django.db.models import Count

@login_required
def classroom_reports(request):
    # Annotate each classroom with the number of students
    classrooms = Classroom.objects.annotate(total_students=Count('student'))

    # Calculate total check-ins for each classroom
    for classroom in classrooms:
        classroom.total_checkins = CheckIn.objects.filter(student__classroom=classroom).count()

    return render(request, 'classroom_reports.html', {'classrooms': classrooms})


from .forms import StudentForm
from .models import Student
@login_required
def search_student(request):
    if 'query' in request.GET:
        query = request.GET['query']
        students = Student.objects.filter(first_name__icontains=query) | Student.objects.filter(last_name__icontains=query)
    else:
        students = Student.objects.all()

    return render(request, 'search_student.html', {'students': students})
@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('search_student')
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form})
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


from .forms import AdminCreationForm

@login_required
def add_administrator(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # hashing password with the correct field name
            user.is_staff = True
            user.is_active = True
            user.save()
            return redirect('dashboard')
    else:
        form = AdminCreationForm()
    return render(request, 'add_administrator.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser

from django.contrib import messages
from .forms import AdminUpdateForm  # Assuming you've created a form for updating admin details

@login_required
def edit_admin(request):
    # Filter by active admins
    admins = CustomUser.objects.filter(is_staff=True, is_active=True)
    return render(request, 'edit_admin.html', {'admins': admins})

@login_required
def update_admin(request, admin_id):
    admin_instance = get_object_or_404(CustomUser, id=admin_id)


    if request.method == 'POST':
        form = AdminUpdateForm(request.POST, instance=admin_instance)

        if form.is_valid():
            # This sets the password properly using the set_password method
            user = form.save()
            messages.success(request, 'Admin details updated successfully.')
            return redirect('edit_admin')
        else:
            # Form is not valid, display error messages
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    else:
        form = AdminUpdateForm(instance=admin_instance)

    return render(request, 'update_admin.html', {'form': form})


@login_required
def delete_admin(request, admin_id):
    admin_instance = get_object_or_404(CustomUser, id=admin_id)

    if request.method == 'POST':
        admin_instance.is_active = False  # Set the admin to inactive
        admin_instance.save()
        messages.success(request, 'Admin deactivated successfully.')
        return redirect('edit_admin')

    return render(request, 'confirm_delete.html', {'admin_instance': admin_instance})


from django.shortcuts import render
from .models import CheckIn, Classroom
from .forms import CustomReportForm

def custom_report(request):
    context = {}
    if request.method == 'POST':
        form = CustomReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            classroom = form.cleaned_data['classroom']
            threshold = form.cleaned_data['threshold']

            # Filter students based on classroom
            if classroom:
                students = classroom.student_set.all()
            else:
                students = Student.objects.all()

            # Gather report data
            report_data = []
            for student in students:
                checkin_count = CheckIn.objects.filter(student=student, checked_on__range=[start_date, end_date]).count()
                data = {
                    'full_name': student.full_name,
                    'student_id': student.student_id,
                    'parent_full_name': student.parent_full_name,
                    'classroom': student.classroom.name,
                    'checkin_count': checkin_count,
                    'highlight': checkin_count < threshold
                }
                report_data.append(data)

            context['report_data'] = report_data
    else:
        form = CustomReportForm()

    context['form'] = form
    return render(request, 'report.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def update_classroom(request):
    classrooms = Classroom.objects.all()
    return render(request, 'update_classroom_list.html', {'classrooms': classrooms})


from django.db import IntegrityError

@login_required
def edit_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    if request.method == "POST":
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Classroom updated successfully!')
                return redirect('update_classroom')
            except IntegrityError:
                messages.error(request, 'A classroom with this name already exists.')
    else:
        form = ClassroomForm(instance=classroom)
    return render(request, 'edit_classroom_form.html', {'form': form})


from django.shortcuts import render
from .models import Student, CheckIn

def individual_student_report(request):
    students = Student.objects.all()
    # You can use annotate to count related objects per student
    from django.db.models import Count
    students = students.annotate(checkin_count=Count('checkin'))

    context = {
        'students': students
    }
    return render(request, 'individual_student_report.html', context)

def student_details(request, pk):
    student = Student.objects.get(pk=pk)
    check_ins = CheckIn.objects.filter(student=student).order_by('-checked_on')
    context = {
        'student': student,
        'check_ins': check_ins
    }
    return render(request, 'student_details.html', context)


from django.shortcuts import render
from django.db.models import Count
from .models import CheckIn, Classroom
from .forms import DateRangeReportForm


def date_range_report(request):
    form = DateRangeReportForm(request.GET or None)
    students_data = []
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        classroom = form.cleaned_data['classroom']
        threshold = form.cleaned_data['threshold']

        queryset = CheckIn.objects.filter(checked_on__range=[start_date, end_date])

        if classroom:
            queryset = queryset.filter(student__classroom=classroom)

        # Aggregate checkins by students
        students_data = queryset.values('student__first_name', 'student__last_name', 'student__student_id',
                                        'student__parent_full_name').annotate(total_count=Count('student')).order_by(
            'student')

    context = {
        'form': form,
        'students_data': students_data,
        'threshold': threshold if form.is_valid() else None,
    }
    return render(request, 'date_range_report.html', context)


