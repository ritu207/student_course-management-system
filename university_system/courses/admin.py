from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.utils import timezone
from .models import Student, Instructor, Course, Enrollment

# Inline for Enrollments within the Course admin
class EnrollmentInline(admin.TabularInline): # You can also use `StackedInline` for a different layout
    model = Enrollment
    extra = 1 # Number of empty forms to show for adding new enrollments

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'title', 'instructor', 'credits', 'enrolled_student_count']
    # ^ This defines which fields (and methods) appear in the list view.
    # 'enrolled_student_count' is the method we defined in the Course model.

    inlines = [EnrollmentInline]
    # ^ This allows you to add/edit enrollments directly from the Course detail page.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'department', 'enrollment_date']
    search_fields = ['name'] # Makes the name field searchable
    list_filter = ['department'] # Adds a filter sidebar for department

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'department', 'hire_date', 'course_count']
    # ^ 'course_count' is the method we defined in the Instructor model.

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'grade']
    # The `unique_together` constraint in the model will prevent duplicates in the database.
    # The `clean` method provides user-friendly error messages in the admin form.