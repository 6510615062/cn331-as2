from django.db import models

class Student(models.Model):
    student_ID = models.CharField(max_length=20)
    student_name = models.CharField(max_length=50)

class Course(models.Model):
    course_ID = models.CharField(max_length=20)
    course_name = models.CharField(max_length=50)
    semester = models.IntegerField(default=0)
    academic_year = models.IntegerField(default=0)
    max_capacity = models.IntegerField(default=0)
    current_registration = models.IntegerField(default=0)
    status = models.BooleanField(default=1)

class Registration(models.Model):
    student_ID = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
