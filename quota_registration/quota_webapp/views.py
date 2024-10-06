from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from quota_webapp.models import Course, Student, Registration
from django.contrib.messages import get_messages
from django.shortcuts import render, redirect
from .forms import RegisterForm


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

    registed_course = []
    registed_course_id = []

    for r in reg:
        course = Course.objects.get(course_ID=r.course_ID)
        registed_course.append(course)
        registed_course_id.append(course.course_ID)

    while len(registed_course) < 7:
        course = 'empty'
        registed_course.append(course)

    context = {
        "all_course": all_course, 
        "reg": registed_course, 
        "reg_id": registed_course_id, 
        "user": user, 
        "user_name": user_name
    }

    return render(request, 'dashboard.html', context)

def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            student_id = form.cleaned_data.get('username')
            student_name = request.POST.get('first_name')
            new_student = Student.objects.create(student_ID=student_id, student_name=student_name)
            new_student.save()
            return redirect('/sign-in')
    else:
        form = RegisterForm()
        print(form)

    return render(request, 'sign-up.html', {'form': form})

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request, 
            username=username, 
            password=password
        )

        if user.is_staff == 1:
            return redirect('/admin')
        
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

    #check if register more than 7 course
    if Registration.objects.filter(
        student_ID=student
    ).count() >= 7:
        messages.error(request, 'You can not register more than 7 courses')
        
    #check if course full
    elif course.current_registration >= course.max_capacity:
        messages.error(request, f'{course} is full')

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

        messages.success(request, f'added {course}')

    else:
        messages.warning(request, f'already registered {course}')
    
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

    messages.success(request, f'deleted {course}')

    return redirect("dashboard")
