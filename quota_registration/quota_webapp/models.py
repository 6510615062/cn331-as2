from django.db import models

class Student(models.Model):
    student_ID = models.CharField(max_length=20)
    student_name = models.CharField(max_length=50)

class Course(models.Model):
    course_ID = models.CharField()
    course_name = models.CharField()
    max_capacity = models.IntegerField(default=0)
    current_registration = models.IntegerField(default=0)

class Professor(models.Model):
    prof_ID = models.CharField()
    prof_name = models.CharField()

class Teaches(models.Model):
    prof_ID = models.ForeignKey(Professor, on_delete=models.CASCADE)
    course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)

class Registration(models.Model):
    student_ID = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
