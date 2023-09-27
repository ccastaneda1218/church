from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Classroom(models.Model):
    # ... existing fields ...
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ... other imports ...
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    parent_full_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(999)])
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="students_added")
    added_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"



from django.utils import timezone

class CheckIn(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    checked_on = models.DateTimeField(default=timezone.now)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)


