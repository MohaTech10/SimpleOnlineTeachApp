from django.forms import ModelForm
from .models import *

from django import forms


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'last_name']


# nums = [
#     ('teacher', 'teacher'),
#     ('student', 'student')
# ]
#
# class Choices(forms.Form):
#
#     nums_ = forms.CharField(widget=forms.RadioSelect(choices=nums))



class CourseForm(ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'
        exclude = ['students_course', 'teacher_course']



