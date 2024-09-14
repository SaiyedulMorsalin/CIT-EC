from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Customer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash



# Create your views here.
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords don't match.")
            return render(request, "register.html")

        if not (
            first_name and last_name and username and pass_key and email and password1
        ):
            messages.error(request, "All fields are required.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "register.html")

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password1)
        user.is_active = False
        user.save()

        customer_profile = Customer.objects.create(user=user)
        student_profile.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = request.build_absolute_uri(
            reverse("activate", kwargs={"uid64": uid, "token": token})
        )
        email_subject = "Confirm Your Email"
        email_body = render_to_string("send_mail.html", {"confirm_link": confirm_link})
        print(token, uid)
        print(confirm_link)

        messages.success(
            request, "Registration successful! Please check your email to confirm."
        )
        try:
            email = EmailMultiAlternatives(email_subject, "", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return render(request, "register_verify.html")
        except Exception as e:
            return messages.error(request, "Email Verification is Failed...")

    return render(request, "register.html")


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk=uid)

    except (User.DoesNotExist, ValueError, TypeError) as e:
        logger.error(f"Activation error: {e}")
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("profile")
    else:

        return redirect("profile")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        email_subject = "Security alert"
        email_body = render_to_string("login_mail.html", {"user": request.user})
        try:

            email = EmailMultiAlternatives(email_subject, "", to=[request.user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
        except Exception as e:
            messages.error(request, "Email Verification Failed. Please try again.")
            return redirect("register")
        return redirect("register")
    return render(request, "index.html")


@login_required(login_url="student_login")
def user_logout(request):

    email_subject = "Security alert"
    email_body = render_to_string("logout_mail.html", {"user": request.user})
    try:
        email = EmailMultiAlternatives(email_subject, "", to=[request.user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
    except Exception as e:
        messages.error(request, "Email Verification Failed. Please try again.")
    logout(request)
    return redirect("student_login")


@login_required(login_url="student_login")
def change_password(request):
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if len(password1) >= 8:
                user = request.user

                if user.check_password(password1):
                    messages.error(
                        request, "New password cannot be the same as the old password."
                    )
                else:
                    user.set_password(password1)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Your password was successfully updated!")
                    return redirect("student_profile")
            else:
                messages.error(request, "Password must be at least 8 characters long.")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, "change_password.html")