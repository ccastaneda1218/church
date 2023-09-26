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

from django import forms
from .models import Classroom, Student

class CheckInForm(forms.Form):
    def __init__(self, classroom_id, *args, **kwargs):
        super(CheckInForm, self).__init__(*args, **kwargs)
        self.fields['students'] = forms.ModelMultipleChoiceField(
            queryset=Student.objects.filter(classroom=classroom_id),
            widget=forms.CheckboxSelectMultiple
        )
