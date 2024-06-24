from django import forms
from .models import Registration

class LoginForm(forms.Form):
    cusname = forms.CharField(max_length=100, required=True)
    cusemail = forms.EmailField(required=True)
    cuspassword = forms.CharField(widget=forms.PasswordInput, required=True)
    cusphonenumber = forms.CharField(max_length=15, required=True)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'  # You can specify specific fields if needed