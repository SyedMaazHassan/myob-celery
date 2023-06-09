from django.contrib import admin
from .models import Teacher, Student

# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'age', 'is_verified')

admin.site.register(Teacher, TeacherAdmin)



# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'age', 'is_verified')

admin.site.register(Student, StudentAdmin)