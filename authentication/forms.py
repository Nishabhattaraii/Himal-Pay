from django import forms
from authentication.enums import GenderChoices
from authentication.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["full_name", "email","mobile_number","dob","gender","username"]

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean(self):
        data=super().clean()
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError("Invalid Email or Password")
        return user

# class KYCForm(forms.Form):
#     full_name = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     mobile_number = forms.IntegerField()
#     dob = forms.DateField()
#     gender = forms.CharField(max_length=100, choices=GenderChoices.choices)
    

class KYCForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile_number = forms.IntegerField()
    dob = forms.DateField()
    gender = forms.ChoiceField(choices=GenderChoices.choices)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['full_name'].initial = user.full_name
            self.fields['email'].initial = user.email
            self.fields['mobile_number'].initial = user.mobile_number
            self.fields['dob'].initial = user.dob
            self.fields['gender'].initial = user.gender
        

class KYCPrefillForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"

