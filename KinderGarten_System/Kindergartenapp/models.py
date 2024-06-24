from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Admin(models.Model):
    Admin_Id = models.CharField(max_length=100, primary_key=True)  
    Admin_Password = models.CharField(max_length=100)  

class Parent(models.Model):
    Parent_IC = models.CharField(max_length=100, primary_key=True)
    Parent_Password = models.CharField(max_length=100)
    Parent_Name = models.CharField(max_length=100)
    Parent_Email = models.EmailField()
    Parent_Nophone = models.CharField(max_length=20)

class Teacher(models.Model):
    Teacher_IC = models.CharField(max_length=100, primary_key=True)
    Teacher_Password = models.CharField(max_length=100)
    Teacher_Name = models.CharField(max_length=100)
    Teacher_Email = models.EmailField()
    Teacher_Nophone = models.CharField(max_length=20)

class Registration(models.Model):
    Registration_Id = models.AutoField(primary_key=True)
    Parent_IC = models.ForeignKey(Parent, on_delete=models.CASCADE)
    Child_Name = models.CharField(max_length=100)
    Child_Gender = models.CharField(max_length=10)
    Child_BirthDate = models.DateField()
    Child_ParentName = models.CharField(max_length=100)
    Parent_contact = models.CharField(max_length=20)
    Parent_email = models.EmailField()
    Child_Address = models.TextField()

class Payment(models.Model):
    Child_Name = models.CharField(max_length=100)
    Payment_Date = models.DateField()
    Payment_Details = models.FileField(upload_to='receipts/')
    Parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Child_Name} - {self.Payment_Date}"

class Complain(models.Model):
    Complain_Id = models.AutoField(primary_key=True)
    Parent_Name = models.CharField(max_length=100)
    Complain_Date = models.DateField()
    Complain_Description = models.TextField()

class Grade(models.Model):
    Grade_Id = models.AutoField(primary_key=True)
    Registration_Id= models.ForeignKey(Registration, on_delete=models.CASCADE)
    Child_Name = models.CharField(max_length=100)
    Child_Subject=models.TextField()
    Child_Grade = models.TextField()