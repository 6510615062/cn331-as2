from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from quota_webapp.models import Course, Student, Registration
from django.contrib.messages import get_messages


def index(request):
    return redirect('/sign-in')

@login_required(login_url="/sign-in")
def dashboard(request):
    #user, course, regristration info
    user = str(get_user(request))
    user_name = Student.objects.get(student_ID=user).student_name
    all_course = Course.objects.all()
    reg = Registration.objects.filter(student_ID=Student.objects.get(student_ID=user))

    #get filter 
    id_contains_query = request.GET.get('filter')

    #filter course
    if id_contains_query != "" and id_contains_query is not None:
        all_course = all_course.filter(course_ID__icontains=id_contains_query)

    #get massage from previous action
    messages = get_messages(request)

    return render(request, 'dashboard.html', {"all_course": all_course, "reg": reg, "user": user, "user_name": user_name})

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request, 
            username=username, 
            password=password
        )

        if user is not None:
            # Log user in
            login(request, user)
            return redirect('/dashboard')
        
        messages.error(request, 'Invalid login')
            
    return render(request, 'sign-in.html')

def sign_out(request):
    # sign user out
    logout(request)

    # Redirect to sign-in page
    return redirect('/sign-in')

def add(request, course_ID):
    #user_ID
    user = str(get_user(request))

    #get student and course object
    student = Student.objects.get(student_ID=user)
    course = Course.objects.get(course_ID=course_ID)

    #check if course full
    if course.current_registration >= course.max_capacity:
        messages.error(request, 'full')

    #check if user already register
    elif Registration.objects.filter(
        student_ID=student,
        course_ID=course
    ).count() == 0:

        reg = Registration.objects.create(
            student_ID=student,
            course_ID=course
        )
        reg.save()

        course.current_registration += 1
        course.save()

        messages.success(request, 'add success')

    else:
        messages.warning(request, 'already')
    
    return redirect("dashboard")

def delete(request, course_ID):
    #user_ID
    user = str(get_user(request))

    #get student and course object
    student = Student.objects.get(student_ID=user)
    course = Course.objects.get(course_ID=course_ID)

    reg = Registration.objects.get(
        student_ID=student,
        course_ID=course
    )
    reg.delete()

    course.current_registration -= 1
    course.save()

    messages.success(request, 'delete success')

    return redirect("dashboard")
