from django.shortcuts import render, redirect


from django.forms import inlineformset_factory, formsets

from .decorators import *

from django.contrib import messages

from .forms import *
from django.contrib.auth.models import User, Group

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@if_admin
def returnHomePage(request):
    return render(request, 'Main.html')


@mustLoggedOut
def signUpProcess(request):

    # front-end
    form = SignUpForm()

    teacher_group = Group.objects.get(name='teachers')
    student_group = Group.objects.get(name='students')
    if request.method == "POST":
        form = SignUpForm(request.POST)

        # print(request.POST['radio-bt'])
        if form.is_valid():
            if request.POST.get('check2', False) == 'on':
                user_current = form.save()
                user_current.groups.add(teacher_group)
                Teacher.objects.create(
                    user=user_current,
                    first_name=form.cleaned_data.get('username'),
                    last_name=form.cleaned_data.get('last_name')
                )
            else:
                user_current = form.save()
                user_current.groups.add(student_group)
                Student.objects.create(
                    user=user_current,
                    first_name=form.cleaned_data.get('username'),
                    last_name=form.cleaned_data.get('last_name')
                )
        #         try:
        #             pass
        #         except Exception as e:
        #             form.save()
        #             request.user.groups.add(student_group)
            # try:
            #     print(request.POST['radio_btn'])
            #     form.save()
            #     return redirect('home')
            # except Exception as e:
            #     print(e)
    context = {
        'form': form
    }
    return render(request, 'sign_up.html', context)


# def checkGroup(request):
#
#     teacher_group = Group.objects.get(name='teachers')
#
#     print(teacher_group)
#     context = {
#         't': teacher_group
#     }
#     return render(request, 'NavBar.html', context)


@mustLoggedOut
def logPage(request):

    # print(request.user.)


    teacher_group = Group.objects.get(name='teachers')

    # print(teacher_group)
    # print(request.user.groups.name)
    username = request.POST.get('username')
    password = request.POST.get('password')

    if request.method == 'POST':
        the_user = authenticate(request, username=username, password=password)
        if the_user is not None:
            login(request, the_user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'log_in.html')


@login_required(login_url='login')
@allow_objects(in_group=['teachers'])
def teacherPage(request):

    current_teacher = request.user.teacher

    current_teach_courses = current_teacher.courses_set.all()


    context = {
        'current_teacher': current_teacher,
        'current_courses': current_teach_courses
    }
    return render(request, 'teacher_page.html', context)

def logOutPage(request):


    saving_current_user = request.user
    logout(request)

    context = {
        'current_user': saving_current_user
    }
    return render(request, 'log_out.html', context)


@login_required(login_url='login')
@allow_objects(in_group=['teachers', 'students'])
def settingPage(request):
    return render(request, 'settings.html')


@login_required(login_url='login')
def studentPage(request):

    current_student = request.user.student

    all_courses = Courses.objects.all()

    context = {
        'current_stu': current_student,
        'courses': all_courses
    }
    return render(request, 'student.html', context)

def createCourse(request, pk_):

    # this page will be basically changed because this is not what it should be !

    # ليه عشان الاوردر ماينضاف الا هذا الشخص اساسا يوزر فهمت


    # here we wanna get into the private page of the specific object/instance
    # then we will create an order/ add it ot the parent same object
    # that has the page private profile obviously !!!

    # doing that will let us able to bring the object that has the specific
    # page private
    #
    from_customer_page_we_know = Teacher.objects.get(id=pk_)
    # form = OrderForm(initial={'customer': from_customer_page_we_know})
    # here it is in from type widget that holds some input field and it will be sent to HTML using context dynamically

    # now there is a method that will let our parent add a lot of its child
    # fg which is gonna be effective

    # to create a lot forms, alright ?
    new_form = inlineformset_factory(Teacher, Courses, fields=('course_name', 'course_description', 'tag_belong'), extra=1, can_delete=False)

    # to specify these bunch of orders all belong one Object !
    # and also to fetch all multiple Orders for the private object
    # we have to let the form a bit about the private object
    # and order thing on thar matter
    form = new_form(queryset=Courses.objects.none(), instance=from_customer_page_we_know)
    if request.method == 'POST':
        form = new_form(request.POST, instance=from_customer_page_we_know)  # here if the method is POST which is True, write a new instance in the form that sent after taking the whole data from
        if form.is_valid():  # it returns either True or False
            form.save()

    context = {
        'form': form
    }

    return render(request, 'create_course.html', context)


def vieCourseContent(request, course_pk):

    # to loop through it and get all its columns value
    specific_course_chosen = Courses.objects.get(id=course_pk)
    # specific_course_chosen.teacher_course__


    tags_one_course = Tag.objects.filter(courses__course_name=specific_course_chosen.course_name)
    new_list = []
    for i in tags_one_course:
        new_list.append(i.tag_name)
        
    # print(new_list)
    new_list = ' , '.join(new_list)
    context = {
        'course_pick': specific_course_chosen,
        'one_courseTag': new_list

    }


    return render(request, 'content_course.html', context)



def payCourse(request, pk_):

    current_user = request.user.student

    the_course = Courses.objects.get(id=pk_)

    # if the_course in current_user.courses_set.all():
    #     print(True)
    # else:
    #     print(False)
    
    courses_array_of_user = []
    for i in current_user.courses_set.all():
        courses_array_of_user.append(i.course_name)

    if the_course.course_name in courses_array_of_user:
        return HttpResponse('Already Purchased this course !')

    if request.method == "POST":
        the_course.students_course.add(current_user)

    context = {
        'the_course': the_course,
        'user_courses': courses_array_of_user
    }
    return render(request, 'pay_page.html', context)



def customerCourses(request):

    the_current_user = request.user.student

    current_courses = the_current_user.courses_set.all()

    # print(current_courses)

    # for i in current_courses:
    #     print(i)

    # <QuerySet [<Tag: back-end>]>
    # <QuerySet [<Tag: Technology>, <Tag: back-end>]>
    #
    # tags_list = []
    # for course in current_courses:
    #     for j in Tag.objects.filter(courses__course_name=course.course_name):
    #         tags_list.append(j)
    #
    #     # print(tag_object[0].tag_name)
    # #
    # # print(tags_list)
    # for i in tags_list:
    #     for j in i:
    #         print(j.tag_name)
    context = {
        'your_courses': current_courses,
        # 'tag_list': tags_list
    }

    return render(request, 'customer_courses.html', context)