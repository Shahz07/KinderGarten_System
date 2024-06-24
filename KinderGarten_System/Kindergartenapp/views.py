from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Parent, User,Registration,Teacher,Grade,Complain,Payment
from .forms import RegistrationForm  # Import your RegistrationForm
from datetime import datetime
from django.utils import timezone


# Create your views here.


#HOME

def home(request):
    return render(request, 'Home.html')

def Aboutus(request):
    return render(request, 'Aboutus.html')

def Activities(request):
    return render(request, 'Activities.html')


#PARENT 

def Login(request):
    if request.method == 'GET':
        return render(request, 'Login.html', {'message': ' '})
    else:
        Parent_IC = request.POST['ICNUM']
        Parent_Password = request.POST['PASSWORD']
        mycust = Parent.objects.filter(Parent_IC=Parent_IC, Parent_Password=Parent_Password)
        
        if mycust.exists():
            request.session['parent_ic'] = Parent_IC
            url = reverse('parent_profile')
            return HttpResponseRedirect(url)
        
    return render(request, 'Login.html', {'message': 'Your password is incorrect.'})

def Signup(request):
    if request.method == 'POST':
        Parent_IC = request.POST.get('Parent_IC')
        Parent_Password = request.POST.get('Parent_Password')
        Parent_Name = request.POST.get('Parent_Name')
        Parent_Email = request.POST.get('Parent_Email')
        Parent_Nophone = request.POST.get('Parent_Nophone')
        
        parent = Parent(
            Parent_IC=Parent_IC, 
            Parent_Password=Parent_Password, 
            Parent_Name=Parent_Name, 
            Parent_Email=Parent_Email, 
            Parent_Nophone=Parent_Nophone
        )
        parent.save()

        request.session['parent_ic'] = Parent_IC
        
        return redirect('Login')

    return render(request, 'Signup.html')

def parent_profile(request):
    # Retrieve parent's IC from session
    parent_ic = request.session.get('parent_ic')
    
    # Fetch parent's complete information from the database
    try:
        parent = Parent.objects.get(Parent_IC=parent_ic)
    except Parent.DoesNotExist:
        parent = None
    
    # Pass parent's information to the template
    return render(request, 'parent_profile.html', {'profile': parent})

def parent_activities(request):
    return render(request, 'parent_activities.html')

def parent_complain(request):
    if request.method == 'POST':
        parent_name = request.POST.get('Parent_Name')
        complain_date = request.POST.get('Complain_Date')
        complain_description = request.POST.get('Complain_Description')
        
        # Save data to Complain model
        complain = Complain(
            Parent_Name=parent_name,
            Complain_Date=complain_date,
            Complain_Description=complain_description
        )
        complain.save()
        
        # Pass a flag to indicate successful submission
        context = {'message_recorded': True}
        return render(request, 'parent_complain.html', context)
    
    # If GET request or form not submitted, just render the template
    return render(request, 'parent_complain.html')

def parent_register(request):
    if request.method == 'POST':
        parent_ic = request.session.get('parent_ic')
        if parent_ic:
            try:
                parent = Parent.objects.get(Parent_IC=parent_ic)
                child_name = request.POST.get('child_name')
                child_gender = request.POST.get('child_gender')
                child_birthdate = request.POST.get('child_birthdate')
                child_parent_name = request.POST.get('child_parent_name')
                parent_contact = request.POST.get('parent_contact')
                parent_email = request.POST.get('parent_email')
                child_address = request.POST.get('child_address')

                # Check if any required field is empty
                if not (child_name and child_gender and child_birthdate and 
                        child_parent_name and parent_contact and parent_email and child_address):
                    return render(request, 'parent_register.html', {'incomplete': True})

                registration = Registration(
                    Parent_IC=parent,
                    Child_Name=child_name,
                    Child_Gender=child_gender,
                    Child_BirthDate=child_birthdate,
                    Child_ParentName=child_parent_name,
                    Parent_contact=parent_contact,
                    Parent_email=parent_email,
                    Child_Address=child_address
                )
                registration.save()

                return render(request, 'parent_register.html', {'success': True})
            except Parent.DoesNotExist:
                return render(request, 'parent_register.html', {'message': 'Parent not found'})
        else:
            return HttpResponse("Session expired or parent IC not found.")
    else:
        return render(request, 'parent_register.html')

def parent_payment(request):
    if request.method == 'POST':
        parent_ic = request.session.get('parent_ic')
        if parent_ic:
            try:
                parent = Parent.objects.get(Parent_IC=parent_ic)
                child_name = request.POST.get('child_name')
                child_gender = request.POST.get('child_gender')
                child_birthdate = request.POST.get('child_birthdate')
                child_parent_name = request.POST.get('child_parent_name')
                parent_contact = request.POST.get('parent_contact')
                parent_email = request.POST.get('parent_email')
                child_address = request.POST.get('child_address')

                # Check if any required field is empty
                if not (child_name and child_gender and child_birthdate and 
                        child_parent_name and parent_contact and parent_email and child_address):
                    return render(request, 'parent_register.html', {'incomplete': True})

                registration = Registration(
                    Parent_IC=parent,
                    Child_Name=child_name,
                    Child_Gender=child_gender,
                    Child_BirthDate=child_birthdate,
                    Child_ParentName=child_parent_name,
                    Parent_contact=parent_contact,
                    Parent_email=parent_email,
                    Child_Address=child_address
                )
                registration.save()

                return render(request, 'parent_register.html', {'success': True})
            except Parent.DoesNotExist:
                return render(request, 'parent_register.html', {'message': 'Parent not found'})
        else:
            return HttpResponse("Session expired or parent IC not found.")
    else:
        return render(request, 'parent_register.html')

def parent_grades(request):
    if request.method == 'POST':
        child_name = request.POST.get('child_name')
        try:
            registration = Registration.objects.get(Child_Name=child_name)
            grades = Grade.objects.filter(Registration_Id=registration.Registration_Id)
            return render(request, 'parent_grades.html', {'grades': grades, 'child_name': child_name})
        except Registration.DoesNotExist:
            error_message = "Student do not exist"
            return render(request, 'parent_grades.html', {'error_message': error_message})
    return render(request, 'parent_grades.html')

#TEACHER

def TeacherLogin(request):
    if request.method == 'GET':
        return render(request, 'TeacherLogin.html', {'message': ' '})
    else:
        Teacher_IC = request.POST['ICNUM']
        Teacher_Password = request.POST['PASSWORD']
        mycust = Teacher.objects.filter(Teacher_IC=Teacher_IC, Teacher_Password=Teacher_Password)
        
        if mycust.exists():
            request.session['teacher_ic'] = Teacher_IC
            url = reverse('teacher_profile')
            return HttpResponseRedirect(url)
        
    return render(request, 'TeacherLogin.html', {'message': 'Your password is incorrect.'})
    

def Teachersignup(request):
    if request.method == 'POST':
        Teacher_IC = request.POST.get('Teacher_IC')
        Teacher_Password = request.POST.get('Teacher_Password')
        Teacher_Name = request.POST.get('Teacher_Name')
        Teacher_Email = request.POST.get('Teacher_Email')
        Teacher_Nophone = request.POST.get('Teacher_Nophone')
        
        teacher = Teacher(
            Teacher_IC=Teacher_IC, 
            Teacher_Password=Teacher_Password, 
            Teacher_Name=Teacher_Name, 
            Teacher_Email=Teacher_Email, 
            Teacher_Nophone=Teacher_Nophone
        )
        teacher.save()

        request.session['teacher_ic'] = Teacher_IC
        
        return redirect('TeacherLogin')
    return render(request, 'Teachersignup.html')

def teacher_profile(request):
   # Retrieve parent's IC from session
    teacher_ic = request.session.get('teacher_ic')
    
    # Fetch parent's complete information from the database
    try:
        teacher = Teacher.objects.get(Teacher_IC=teacher_ic)
    except Teacher.DoesNotExist:
        teacher = None
    
    # Pass parent's information to the template
    return render(request, 'teacher_profile.html', {'profile': teacher})

def teacher_grades(request):
    if request.method == 'POST':
        # Retrieve form data
        child_name = request.POST.get('name')
        math_grade = request.POST.get('math_grade')
        bahasa_malaysia_grade = request.POST.get('bahasa_malaysia_grade')
        bahasa_english_grade = request.POST.get('bahasa_english_grade')
        
        # Assuming you have some way to determine the registration_id based on the child's name
        try:
            registration = Registration.objects.get(Child_Name=child_name)
        except Registration.DoesNotExist:
            registration = None

        if registration:
            # Save grades to the Grade model
            Grade.objects.create(
                Registration_Id=registration,
                Child_Name=child_name,
                Child_Subject='Math',
                Child_Grade=math_grade,
            )
            Grade.objects.create(
                Registration_Id=registration,
                Child_Name=child_name,
                Child_Subject='Bahasa Malaysia',
                Child_Grade=bahasa_malaysia_grade,
            )
            Grade.objects.create(
                Registration_Id=registration,
                Child_Name=child_name,
                Child_Subject='Bahasa English',
                Child_Grade=bahasa_english_grade,
            )

            # Pass a success message to the template
            return render(request, 'teacher_grades.html', {'success_message': 'Student\'s grades have been submitted.'})
        else:
            # Handle case where no registration found for the provided child name
            return render(request, 'teacher_grades.html', {'error_message': 'Student name is not registered.'})

    else:
        # GET request: Render the form
        return render(request, 'teacher_grades.html')
    
def teacher_edit(request):
    grades = Grade.objects.all()
    if request.method == 'POST':
        grade_id = request.POST.get('grade_id')
        grade = get_object_or_404(Grade, Grade_Id=grade_id)

        # Check if the request is for updating a grade
        if 'update' in request.POST:
            grade.Child_Name = request.POST.get('Child_Name')
            grade.Child_Subject = request.POST.get('Child_Subject')
            grade.Child_Grade = request.POST.get('Child_Grade')
            grade.save()
            return redirect('teacher_edit')
        
        # Check if the request is for deleting a grade
        elif 'delete' in request.POST:
            grade.delete()
            return redirect('teacher_edit')
    
    return render(request, 'teacher_edit.html', {'grades': grades})
   



#ADMIN
def AdminLogin(request):
    if request.method == 'POST':
        admin_id = request.POST.get('Admin_Id')
        admin_password = request.POST.get('Admin_Password')

        # Hardcoded credentials
        if admin_id == "tadikakemasmalaysia2024" and admin_password == "12345678":
            return redirect('admin_profile')
        else:
            messages.error(request, 'Your Admin ID or Password is wrong')

    return render(request, 'AdminLogin.html')

def admin_profile(request):
    return render(request, 'admin_profile.html')

def admin_registration(request):
    if request.method == "POST":
        registration_id = request.POST.get("registration_id")
        registration = Registration.objects.get(pk=registration_id)

        if 'update' in request.POST:
            registration.Child_Name = request.POST.get("Child_Name")
            registration.Child_Gender = request.POST.get("Child_Gender")
            registration.Child_BirthDate = request.POST.get("Child_BirthDate")
            registration.Child_ParentName = request.POST.get("Child_ParentName")
            registration.Parent_contact = request.POST.get("Parent_contact")
            registration.Parent_email = request.POST.get("Parent_email")
            registration.Child_Address = request.POST.get("Child_Address")
            registration.save()
            return redirect('admin_registration')

        elif 'delete' in request.POST:
            registration.delete()
            return redirect('admin_registration')

    registrations = Registration.objects.all()
    return render(request, 'admin_registration.html', {'registrations': registrations})

def admin_parentinfo(request):
    if request.method == 'POST':
        if 'update_parent' in request.POST:
            parent_ic = request.POST.get('parent_ic')
            parent = get_object_or_404(Parent, Parent_IC=parent_ic)
            parent.Parent_Name = request.POST.get('name')
            parent.Parent_Email = request.POST.get('email')
            parent.Parent_Nophone = request.POST.get('nophone')
            parent.save()
        elif 'delete_parent' in request.POST:
            parent_ic = request.POST.get('parent_ic')
            parent = get_object_or_404(Parent, Parent_IC=parent_ic)
            parent.delete()
        return redirect('admin_parentinfo')
    parents = Parent.objects.all()
    return render(request, 'admin_parentinfo.html', {'parents': parents})



def admin_teacherinfo(request):
    if request.method == 'POST':
        if 'update_teacher' in request.POST:
            teacher_ic = request.POST.get('teacher_ic')
            teacher = get_object_or_404(Teacher, Teacher_IC=teacher_ic)
            teacher.Teacher_Name = request.POST.get('name')
            teacher.Teacher_Email = request.POST.get('email')
            teacher.Teacher_Nophone = request.POST.get('nophone')
            teacher.save()
        elif 'delete_teacher' in request.POST:
            teacher_ic = request.POST.get('teacher_ic')
            teacher = get_object_or_404(Teacher, Teacher_IC=teacher_ic)
            teacher.delete()
        return redirect('admin_teacherinfo')
    teachers = Teacher.objects.all()
    return render(request, 'admin_teacherinfo.html', {'teachers': teachers})


def admin_complain(request):
    if request.method == "POST":
        complain_id = request.POST.get("complain_id")
        complain = Complain.objects.get(pk=complain_id)

        if 'update' in request.POST:
            complain.Parent_Name = request.POST.get("Parent_Name")
            complain.Complain_Date = request.POST.get("Complain_Date")
            complain.Complain_Description = request.POST.get("Complain_Description")
            complain.save()
            return redirect('admin_complain')

        elif 'delete' in request.POST:
            complain.delete()
            return redirect('admin_complain')

    complain = Complain.objects.all()
    return render(request, 'admin_complain.html', {'complain': complain})


def admin_payment(request): 
    
    return render(request, 'admin_payment.html')

def Adminsignup(request):
    return render(request, 'Adminsignup.html')