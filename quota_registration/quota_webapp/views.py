from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from quota_webapp.models import Course, Student, Registration


def index(request):
    return redirect('/sign-in')

@login_required(login_url="/sign-in")
def dashboard(request):
    user = str(get_user(request))
    user_name = Student.objects.filter(student_ID=user)[0].student_name
    all_course = Course.objects.all()
    reg = Registration.objects.filter(student_ID=Student.objects.filter(student_ID=user)[0])

    id_contains_query = request.GET.get('filter')

    if id_contains_query != "" and id_contains_query is not None:
        all_course = all_course.filter(course_ID__icontains=id_contains_query)

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
