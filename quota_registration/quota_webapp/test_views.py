from django.test import TestCase, Client
from django.urls import reverse
from .models import Course, Student, Registration
from .forms import RegisterForm
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

class QuotaViewTestCase(TestCase):

    def setUp(self):
        #create Course
        course1 = Course.objects.create(
            course_ID="CN333",
            course_name="application design",
            semester=2,
            academic_year=2024,
            max_capacity=10,
            current_registration=0,
            status=1
        )

        course2 = Course.objects.create(
            course_ID="CN361",
            course_name="micro-controller",
            semester=1,
            academic_year=2024,
            max_capacity=2,
            current_registration=0,
            status=1
        )

        course3 = Course.objects.create(
            course_ID="CN399",
            course_name="Gaming",
            semester=2,
            academic_year=2024,
            max_capacity=2,
            current_registration=0,
            status=1
        )

        course4 = Course.objects.create(
            course_ID="CN101",
            course_name="Intro to programming",
            semester=2,
            academic_year=2024,
            max_capacity=2,
            current_registration=0,
            status=1
        )

        course5 = Course.objects.create(
            course_ID="TU117",
            course_name="Culture",
            semester=2,
            academic_year=2024,
            max_capacity=2,
            current_registration=0,
            status=1
        )

        course6 = Course.objects.create(
            course_ID="TU105",
            course_name="English",
            semester=2,
            academic_year=2024,
            max_capacity=2,
            current_registration=0,
            status=1
        )

        course7 = Course.objects.create(
            course_ID="TU999",
            course_name="Finance",
            semester=2,
            academic_year=2024,
            max_capacity=2,
            current_registration=0,
            status=1
        )

        course8 = Course.objects.create(
            course_ID="TU234",
            course_name="Investing",
            semester=2,
            academic_year=2024,
            max_capacity=2,
            current_registration=0,
            status=1
        )
        
                
        #create student (not from register page)
        student1 = Student.objects.create(
            student_ID="6510615120",
            student_name="Tanapat"
        )

        student2 = Student.objects.create(
            student_ID="6510615056",
            student_name="Chaisiri"
        )

        student3 = Student.objects.create(
            student_ID="6510615112",
            student_name="Teerapat"
        )

        #create user 
        user1 = RegisterForm({
            "username": "6510615120",
            "password1": "Testing12345",
            "password2": "Testing12345",
        })
        user1.save()

        #create superuser (admin)
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )


    def test_index_return_sign_in(self):
        """index is return to /sign-in"""

        c = Client()
        response = c.get("")
        self.assertEqual(response["Location"], "/sign-in")

    def test_sign_in_status_code(self):
        """sign-in's status code is OK"""

        c = Client()
        response = c.get("/sign-in")
        self.assertEqual(response.status_code, 200)

    def test_sign_in_invalid(self):
        """invalid login should get \'Invalid login\' massage"""

        c = Client()
        post_value = {
            "username": "6510615100",
            "password": "test"
        }
        response = c.post("/sign-in", data=post_value)
        message = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'Invalid login')

    def test_sign_in_valid_as_user(self):
        """valid login as user return to /dashboard and is_authenticated"""

        c = Client()
        post_value = {
            "username": "6510615120",
            "password": "Testing12345"
        }
        response = c.post("/sign-in", data=post_value, follow=True)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.request['PATH_INFO'], "/dashboard")

    # when redirect to /admin by default will redirect to /admin/login/ if not login yet
    def test_sign_in_valid_as_admin(self):
        """valid login as admin return to /admin/login/"""

        c = Client()
        post_value = {
            "username": "admin",
            "password": "adminpassword123"
        }
        response = c.post("/sign-in", data=post_value, follow=True)
        self.assertEqual(response.request['PATH_INFO'], "/admin/login/")

    def test_sign_out(self):
        """user is not authenticated and redirect to /sign-in"""

        c = Client()
        c.login(
            username='6510615120', 
            password='Testing12345'
        )
        response = c.get("/sign-out", follow=True)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.request['PATH_INFO'], "/sign-in")

    def test_sign_up_status_code(self):
        """sign-up's status code is OK"""

        c = Client()
        response = c.get("/sign-up")
        self.assertEqual(response.status_code, 200)

    def test_sign_up_context(self):
        """context is correctly set"""

        c = Client()
        response = c.get("/sign-up")
        self.assertTrue('form' in response.context)

    def test_sign_up_invalid(self):
        """invalid sign-up"""

        c = Client()
        post_value = {
            "username": "651061510a",
            "password1": "test",
            "password2": "test1",
            "first_name": "Q"
        }
        response = c.post("/sign-up", data=post_value, follow=True)
        self.assertFalse(response.context["form"].is_valid())

    def test_sign_up_valid(self):
        """valid sign-up should redirect to /sign-in"""

        c = Client()
        post_value = {
            "username": "6510615100",
            "password1": "Test12345",
            "password2": "Test12345",
            "first_name": "Parun"
        }
        #check if redirect to /sign-in
        response = c.post("/sign-up", data=post_value, follow=True)
        self.assertEqual(response.request['PATH_INFO'], "/sign-in")

        #check if database create
        student = Student.objects.filter(student_ID="6510615100")
        user = User.objects.filter(username="6510615100")
        self.assertTrue(student)
        self.assertTrue(user)

    def test_dashboard_no_authen(self):
        """"try to enter dashboard without authenticated should redirect to /sign-in"""

        c = Client()
        response = c.get("/dashboard", follow=True)
        self.assertEqual(response.request['PATH_INFO'], "/sign-in")

    def test_dashboard_filter_show_all_course(self):
        """"test default filer which is show all course filter in the dashboard page"""

        c = Client()
        c.login(
            username='6510615120', 
            password='Testing12345'
        )
        response = c.get("/dashboard", follow=True)
        self.assertEqual(response.context['all_course'].count(), 8)

    def test_dashboard_filter_show_open_course(self):
        """"test show open course filter"""

        c = Client()
        c.login(
            username='6510615120', 
            password='Testing12345'
        )
        cn399 = Course.objects.get(course_ID="CN399")
        cn399.status = 0
        cn399.save()
        response = c.get("/dashboard?filter=None&status_filter=1", follow=True)
        self.assertEqual(response.context['all_course'].count(), 7)

    def test_dashboard_filter_show_open_course(self):
        """"test if search return correct result"""

        c = Client()
        c.login(
            username='6510615120', 
            password='Testing12345'
        )
        response = c.get("/dashboard?filter=CN333&status_filter=0", follow=True)
        self.assertEqual(response.context['all_course'].count(), 1)
        self.assertEqual(response.context['all_course'][0].course_ID, 'CN333')

    def test_adding_more_than_maximum_allowed_course(self):
        """test if course are limited at 7 courses as designed"""

        c = Client()
        c.login(
            username='6510615120', 
            password='Testing12345'
        )
        courses = ['CN333', 'CN361', 'CN399', 'CN101', 'TU117', 'TU105', 'TU999']
        student = Student.objects.get(student_ID='6510615120')
        for course in courses:
            course_obj = Course.objects.get(course_ID=course)
            temp = Registration.objects.create(
                student_ID=student,
                course_ID=course_obj
            )
            temp.save()
        response = c.get("/add/TU234", follow=True)
        message = str(list(get_messages(response.wsgi_request))[0])
        self.assertEqual(message, 'You can not register more than 7 courses')
        self.assertEqual(Registration.objects.filter(student_ID=student).count() , 7)


        
        
            











    

        


        

    