from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class RegisterForm(UserCreationForm):
    model = User
    fields = [
        "username",
        "password1",
        "password2",
    ]

    def password_matched(self):
        if self.data['password1'] != self.data['password2']:
            return False
        else:
            return True
        
    def username_valid(self):
        if self.data['username'].isdigit() and len(self.data['username']) == 10:
            return True
        else:
            self.errors['username'] = ', Please use student ID as username'
            return False

    def is_valid(self):
        valid = super(RegisterForm,self).is_valid()
        password_matched = self.password_matched()
        username_valid = self.username_valid()
        if valid and password_matched and username_valid:
            return True
        else:
            return False