from django.urls import path
from .views import *


urlpatterns = [

    path('', returnHomePage, name='home'),
    path('signup/', signUpProcess, name='signup'),
    path('login/', logPage, name='login'),
    path('teacher/', teacherPage, name='teacher'),
    path('logout/', logOutPage, name='log_out'),
    path('setting/', settingPage, name='setting'),
    path('student/', studentPage,  name='student'),
    path('create_course/<str:pk_>', createCourse, name='create_course'),

    path('course_content/<str:course_pk>', vieCourseContent, name='course_content'),

    path('pay_course/<str:pk_>', payCourse, name='pay_course'),

    path('student/courses', customerCourses, name='student_course')
    # path('r/', choice)
]