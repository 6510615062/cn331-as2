from django.test import TestCase
from .models import Course, Student, Registration

# Create your tests here.
class ModelTest(TestCase):

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

        student1 = Student.objects.create(
            student_ID="6510615120",
            student_name="Tanapat"
        )

        registration = Registration.objects.create(
            student_ID=student1, 
            course_ID=course1
        )

    def test_model_str(self):
        """test string display"""

        self.assertEqual(str(Course.objects.first()), "CN333")
        self.assertEqual(str(Student.objects.first()), "6510615120:Tanapat")
        self.assertEqual(str(Registration.objects.first()), "6510615120:Tanapat:CN333")
    
