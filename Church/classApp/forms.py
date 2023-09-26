from django import forms
from .models import Classroom

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name']

from django import forms
from .models import Student, Classroom

class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['parent_full_name', 'first_name', 'last_name', 'student_id', 'classroom']
