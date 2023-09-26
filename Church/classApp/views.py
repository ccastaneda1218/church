from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

from django.shortcuts import render

# ... other views

@login_required
def class_dashboard(request):
    return render(request, 'class_dashboard.html')


from django.shortcuts import render, redirect
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


from .models import Classroom, Student
from django.db.models import Count

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

from django.shortcuts import render

# ... other views ...

@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')



from .forms import AddStudentForm

# ... other views ...

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


from .models import Student

# ... other views ...

from django.db.models import Count

@login_required
def list_students(request):
    students = Student.objects.all()
    class_counts = Student.objects.values('classroom__name').annotate(total_students=Count('classroom'))

    return render(request, 'list_students.html', {'students': students, 'class_counts': class_counts})

# ... other imports ...

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

from django.contrib import messages


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


from django.db.models import Count
from django.utils import timezone

from django.shortcuts import render
from django.utils import timezone
from .models import CheckIn

from django.shortcuts import render
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


# from django.db.models import Count
# @login_required
# def your_view_function(request):
#     class_counts = Student.objects.values('classroom__name').annotate(total_students=Count('classroom')).order_by('classroom__name')

# views.py
from django.shortcuts import render

def reports_dashboard(request):
    return render(request, 'reports_dashboard.html')


