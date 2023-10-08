from django import forms
from .models import Classroom
from classApp.models import CustomUser

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

class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.student_id} - {obj.first_name} {obj.last_name} (Parent: {obj.parent_full_name})"

class CheckInForm(forms.Form):
    def __init__(self, classroom_id, *args, **kwargs):
        super(CheckInForm, self).__init__(*args, **kwargs)
        students = Student.objects.filter(classroom=classroom_id)
        self.fields['students'] = CustomModelMultipleChoiceField(
            queryset=students,
            widget=forms.CheckboxSelectMultiple
        )


from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['parent_full_name', 'first_name', 'last_name', 'student_id', 'classroom']



from django import forms
from classApp.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class AdminCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, error_messages={'required': 'First name is required.'})
    last_name = forms.CharField(max_length=30, required=True, error_messages={'required': 'Last name is required.'})
    admin_level = forms.ChoiceField(choices=CustomUser.ADMIN_LEVELS, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'admin_level']

class AdminUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True, error_messages={'required': 'First name is required.'})
    last_name = forms.CharField(required=True, error_messages={'required': 'Last name is required.'})
    username = forms.CharField(required=True, error_messages={'required': 'Username is required.'})
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False, label='New Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False, label='Confirm New Password')
    admin_level = forms.ChoiceField(choices=CustomUser.ADMIN_LEVELS, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'admin_level']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', 'Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user



# from django import forms
# from .models import Classroom
#
# class DateInput(forms.DateInput):
#     input_type = 'date'
#
# class DateRangeForm(forms.Form):
#     start_date = forms.DateField(label='Start Date', widget=DateInput())
#     end_date = forms.DateField(label='End Date', widget=DateInput())
#     classroom = forms.ModelChoiceField(queryset=Classroom.objects.all(), label='Classroom', required=False)
#     threshold = forms.IntegerField(min_value=1, label='Threshold')
#
#     def __init__(self, *args, **kwargs):
#         super(DateRangeForm, self).__init__(*args, **kwargs)
#         self.fields['classroom'].choices = [('', 'ALL')] + [(classroom.pk, classroom.name) for classroom in Classroom.objects.all()]


from django import forms
from .models import Classroom

class CustomReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all(), required=False)
    threshold = forms.IntegerField(min_value=1)

class UserProfileForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Confirm New Password')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password or confirm_password:
            if new_password != confirm_password:
                self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['new_password']:
            user.set_password(self.cleaned_data['new_password'])
        if commit:
            user.save()
        return user
