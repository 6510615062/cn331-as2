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

    