from django.contrib import admin
from quota_webapp.models import Registration, Course, Student 

# Register your models here.
admin.site.register(Registration)
admin.site.register(Course)
admin.site.register(Student)