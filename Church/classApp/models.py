from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Classroom(models.Model):
    # ... existing fields ...
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ... other imports ...
from django.contrib.auth.models import User

class Student(models.Model):
    parent_full_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(999)])
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

