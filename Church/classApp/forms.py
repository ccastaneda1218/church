from django import forms
from .models import Classroom
from django.contrib.auth.models import User

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

from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['parent_full_name', 'first_name', 'last_name', 'student_id', 'classroom']



from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AdminCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, error_messages={'required': 'First name is required.'})
    last_name = forms.CharField(max_length=30, required=True, error_messages={'required': 'Last name is required.'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

class AdminUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True, error_messages={'required': 'First name is required.'})
    last_name = forms.CharField(required=True, error_messages={'required': 'Last name is required.'})
    username = forms.CharField(required=True, error_messages={'required': 'Username is required.'})
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True, label='New Password', error_messages={'required': 'Password is required.'})
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True, label='Confirm New Password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=DateInput())
    end_date = forms.DateField(label='End Date', widget=DateInput())

