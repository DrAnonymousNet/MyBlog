from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(required=True, max_length=30,
                                 widget=forms.TextInput)
    last_name = forms.CharField(required=True, max_length=30,
                                widget=forms.TextInput)
    email = forms.CharField(required=True, max_length=50,
                            widget=forms.EmailInput)

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Passweord", help_text="Enter Password Again...")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        eqs = User.objects.filter(email=email)

        if eqs.count() != 0:
            raise forms.ValidationError("This Email already exist")
        if self.cleaned_data.get("password") != self.cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords must match !")

        return super(UserRegisterForm, self).clean(*args, **kwargs)


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
                raise forms.ValidationError({password: "Incorrect password"})

        return super(UserLogin, self).clean(*args, **kwargs)


class PasswordResetForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password_1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password_2 = forms.CharField(widget=forms.PasswordInput, label="New Password 2",
                                     initial="Enter New Password Again")

    def __init__(self, user, *args, **kwargs):

        self.user = user
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        print("IN HERRRRRRR")
        password = self.cleaned_data.get("old_password")
        new_password_1 = self.cleaned_data.get("new_password_1")
        new_password_2 = self.cleaned_data.get("new_password_2")
        if self.user:

            try:
                print("NOOOOOOOO")
                user = User.objects.get(email=self.cleaned_data.get("email"))
            except:
                raise forms.ValidationError("No User with the Email")
            if self.user != user:
                raise forms.ValidationError("Your Mail does not match !")

        else:
            try:
                user = User.objects.get(email=self.cleaned_data.get("email"))
                print("YESSSSSSSSSSS")
            except:
                raise forms.ValidationError("No User with the Email")

        if not user.check_password(password):
            raise forms.ValidationError("Incorrect Old Password")
        if new_password_1 != new_password_2:
            raise forms.ValidationError("Unmatched Password")
        super(PasswordResetForm, self).clean(*args, **kwargs)


class EmailVerificationForm(forms.Form):
    verification_code = forms.IntegerField()

class ForgotPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        new_password_1 = self.cleaned_data.get("new_password")
        new_password_2 = self.cleaned_data.get("new_password_2")

        if new_password_1 != new_password_2:
            raise forms.ValidationError("Password Does Not Match !")
        super(ForgotPasswordForm, self).clean(*args, **kwargs)

class EmailForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    
    def clean(self,  *args, **kwargs):
        email = self.cleaned_data.get("email", None)
        try:
            user = User.objects.get(email=email)
        except:
            raise forms.ValidationError("No User With this Email")
        super(EmailForm, self).clean(*args, **kwargs)
