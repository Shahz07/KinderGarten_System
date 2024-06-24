from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("Aboutus/", views.Aboutus, name="Aboutus"),
    path("Activities/", views.Activities, name="Activities"),


    path("Login/", views.Login, name="Login"),
    path("Signup/", views.Signup, name="Signup"),
    path("parent_profile/", views.parent_profile, name="parent_profile"),
    path("parent_activities/", views.parent_activities, name="parent_activities"),
    path("parent_complain/", views.parent_complain, name="parent_complain"),
    path("parent_register/", views.parent_register, name="parent_register"),
    path("parent_payment/", views.parent_payment, name="parent_payment"),
    path("parent_grades/", views.parent_grades, name="parent_grades"),


    path("TeacherLogin/", views.TeacherLogin, name="TeacherLogin"),
    path("Teachersignup/", views.Teachersignup, name="Teachersignup"),
    path("teacher_profile/", views.teacher_profile, name="teacher_profile"),
    path("teacher_grades/", views.teacher_grades, name="teacher_grades"),
    path("teacher_edit/", views.teacher_edit, name="teacher_edit"),



    path("AdminLogin/", views.AdminLogin, name="AdminLogin"),
    path("admin_profile/", views.admin_profile, name="admin_profile"),
    path("admin_payment/", views.admin_payment, name="admin_payment"),
    path("admin_registration/", views.admin_registration, name="admin_registration"),
    path("admin_complain/", views.admin_complain, name="admin_complain"),
    path("admin_parentinfo/", views.admin_parentinfo, name="admin_parentinfo"),
    path("admin_teacherinfo/", views.admin_teacherinfo, name="admin_teacherinfo"),
    path("Adminsignup/", views.Adminsignup, name="Adminsignup"),

]