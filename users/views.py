import random
import urllib.parse

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserLogin, UserRegisterForm, PasswordResetForm, EmailVerificationForm, EmailForm, ForgotPasswordForm
from django.forms import formset_factory
from django.contrib import messages
from post.models import Author, Post
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User
from random import randint
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from urllib.parse import urlencode
from blog.settings import EMAIL_HOST_USER


# Create your views here.


def login_view(request):
    next = request.GET.get("next")
    form = UserLogin()
    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            # messages.success(request,f"Welcome {username} !")
            if next:
                return redirect(next)

            return redirect("index")
    context = {
        "form": form,
    }

    return render(request, "login.html", context)


def register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")

            user.set_password(password)
            user.save()
            author = Author.objects.create(author=user)
            author.save()
            # form.instance.is_active = False

            initial_url = reverse("email_verify")
            query_string = urllib.parse.urlencode({"email": form.instance.email})
            full_url = f"{initial_url}?{query_string}"

            return redirect(full_url)

    context = {
        "form": form
    }
    return render(request, "register.html", context)


def email_verify(request):
    random.seed(20)
    verification_code = random.randint(0, 1000)
    next = request.GET.get("next", None)
    email = request.GET.get("email", None)
    if request.method == "GET":
        validation_form = EmailVerificationForm()
        send_verification_mail(verification_code, email)
    if request.method == "POST":
        validation_form = EmailVerificationForm(request.POST)
        if validation_form.is_valid():
            input_code = validation_form.cleaned_data.get("verification_code")
            if input_code == verification_code:
                if next:
                    messages.success(request, "You can now Change Your Password !")
                    query = urllib.parse.urlencode({"email": email})
                    base_url = reverse(next)
                    full_url = f"{base_url}?{query}"
                    return redirect(full_url)
                messages.success(request, "You can now log in !")
                return redirect("login")
            else:
                messages.error(request, "Incorrect Verification Code")
    context = {
        "form": validation_form
    }
    return render(request, "email_verify.html", context)


def send_verification_mail(code, email):
    sender = "haryournifemijt@gmail.com"
    message = str(code)
    receiver = email
    subject = "Email Verification"
    send_mail(subject=subject,
              message=message,
              from_email=sender,
              recipient_list=[receiver]
              )


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


def reset_password(request):
    form = PasswordResetForm(request.user)

    if request.method == "POST":
        form = PasswordResetForm(request.user or None, request.POST)

        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data.get("email"))
            user.set_password(form.cleaned_data.get("new_password_1"))
            user.save()
            return redirect("login")

    context = {
        "form": form
    }
    return render(request, "reset_password.html", context=context)


def forgot_password(request):
    form = ForgotPasswordForm(request.POST or None)
    email = request.GET.get("email", None)
    if form.is_valid():
        password = form.cleaned_data.get("new_password_1")

        user = User.objects.get(email=email)
        user.set_password(password)
        return redirect("login")



    context = {
        "form":form
    }
    return render(request , "reset_password.html", context)



def email_view(request):

    if request.method =="POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            query = urllib.parse.urlencode({"email": email, "next": "forgot_password"})
            base_url = reverse("email_verify")
            print(base_url)
            full_url = f"{base_url}?{query}"
            print(full_url)
            return redirect(full_url)
    form = EmailForm(None)
    context = {
        "form": form
    }
    return render(request, "email_view.html", context)
