from django.shortcuts import render
from django.http import HttpResponse
from .models import Teacher, Student
from faker import Faker
from time import sleep

# Create your views here.
def sync_home_view(request):
    fake = Faker()
    for _ in range(10):
        teacher = Teacher(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            age=fake.random_int(min=20, max=60)
        )
        teacher.save()

        student = Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            age=fake.random_int(min=20, max=60)
        )
        student.save()


    teachers = Teacher.objects.all()
    return render(request, "home.html", {'teachers': teachers})
