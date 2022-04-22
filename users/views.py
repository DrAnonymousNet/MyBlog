from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserLogin, UserRegisterForm, PasswordResetForm,EmailVerificationForm
from django.contrib import messages
from post.models import Author, Post
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User
from random import randint
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from urllib.parse import urlencode

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
            login(request,user)
            # messages.success(request,f"Welcome {username} !")
            if not request.user.is_active:
                email = request.user.email
                base_url = reverse(email_verify)
                query_string = urlencode({"email": email})
                full_url = f"{base_url}?{query_string}"
                return redirect(full_url)
            if next:
                return redirect(next)


            return redirect("index")
    context = {
        "form": form,
    }

    return render(request, "login.html", context)
"""
def email_verify(request):
    sent_code = randint(100, 999)
    next_ = request.GET.get("next", None)
    if request.method == "POST":
        verification_form = EmailVerificationForm(request.POST)
        if verification_form.is_valid():
            verification_code = verification_form.cleaned_data.get("verification_code")
            if verification_code == sent_code:
                messages.success(request, "Your account has been created successfully, You can now Login!")
                request.user.is_active = True
                if next_:
                    return redirect(next_)
                return redirect("login")

    email = request.GET.get("email", None)
    if not email:
        email = request.user.email
    #email = email[:email.index("%")] + "@gmail.com"
    try:
        send_mail(subject="Email Verification Code",message=f"This is your Verification Code {sent_code}",
                recipient_list=["haryourjb@gmail.com"],
                from_email="haryournifemijbt@gmail.com")
    except BadHeaderError:
        return HttpResponse('Invalid header found')
    verification_form = EmailVerificationForm()
    messages.info(request, "A Code Has Been Sent To Your Email")

    context = {
        "form":verification_form
    }
    return render(request, "email_verify.html", context)
"""

def register(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            #form.instance.is_active = False
            form.instance.save()
            """email = form.cleaned_data.get("email")
            base_url = reverse(email_verify)
            query_string = urlencode({"email":email})
            full_url = f"{base_url}?{query_string}"
            return redirect(full_url)"""

    context = {
        "form": form
    }
    return render(request, "register.html", context)


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

def reset_password(request):
    form = PasswordResetForm()

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data.get("user_name"))
            user.set_password(form.cleaned_data.get("new_password_1"))
            user.save()
            return redirect("login")
    context = {
        "form":form
    }
    return render(request, "reset_password.html", context=context)