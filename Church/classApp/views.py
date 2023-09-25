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


from .models import Classroom

# ... other views ...

@login_required
def list_classes(request):
    classrooms = Classroom.objects.all()
    return render(request, 'list_classes.html', {'classrooms': classrooms})

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