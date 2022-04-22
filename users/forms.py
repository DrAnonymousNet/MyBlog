from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name  = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta():
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

class UserLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError({password:"Incorrect password"})


        return super(UserLogin , self).clean(*args, **kwargs)

class PasswordResetForm(forms.Form):
    user_name = forms.CharField()
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password_1 =forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password_2 = forms.CharField(widget=forms.PasswordInput, label="New Password 2", initial="Enter New Password "
                                                                                                 "Again")


    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get("old_password")
        new_password_1 = self.cleaned_data.get("new_password_1")
        new_password_2 = self.cleaned_data.get("new_password_2")
        try:
            user = User.objects.get(username= self.cleaned_data.get("user_name"))
        except:
            raise forms.ValidationError("No User with the Username")

        if not user.check_password(password):
            raise forms.ValidationError("Incorrect Old Password")
        if new_password_1 != new_password_2:
            raise forms.ValidationError("Unmatched Password")
        super(PasswordResetForm, self).clean(*args, **kwargs)

class EmailVerificationForm(forms.Form):
    verification_code = forms.IntegerField()





