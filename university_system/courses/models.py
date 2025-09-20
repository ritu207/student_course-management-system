from django.db import models

# Create your models here.

from django.db import models
from django.core.exceptions import ValidationError

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    enrollment_date = models.DateField()

    def __str__(self):
        return self.name

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return self.name

    # This method will be used in the admin to show the number of courses
    def course_count(self):
        return self.course_set.count()
    course_count.short_description = 'Number of Courses' # This sets the column header in admin

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    credits = models.IntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.course_code} - {self.title}"

    # This method will be used in the admin to show the number of enrolled students
    def enrolled_student_count(self):
        return self.enrollment_set.count()
    enrolled_student_count.short_description = 'Enrolled Students'

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    grade = models.CharField(max_length=2, blank=True, null=True) # e.g., "A", "B+", "F"

    def __str__(self):
        return f"{self.student.name} - {self.course.title}"

    # This is the validation to prevent duplicate enrollments
    def clean(self):
        # Check if an enrollment with the same student and course already exists
        if Enrollment.objects.filter(student=self.student, course=self.course).exists():
            raise ValidationError('This student is already enrolled in this course.')

    # Override the save method to call `clean` before saving
    def save(self, *args, **kwargs):
        self.clean() # This will raise an error if it's a duplicate
        super().save(*args, **kwargs)

    class Meta:
        # An alternative and more robust way to enforce uniqueness at the database level
        unique_together = ('student', 'course')