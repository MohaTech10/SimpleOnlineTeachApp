from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    # a teacher has got a lot of courses

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    about = models.TextField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Student(models.Model):
    # i will use default django id pk
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_name
class Courses(models.Model):
    course_name = models.CharField(max_length=200)
    course_description = models.TextField()
    teacher_course = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    tag_belong = models.ManyToManyField(Tag)
    students_course = models.ManyToManyField(Student, null=True, blank=True)

    def __str__(self):
        return self.course_name
