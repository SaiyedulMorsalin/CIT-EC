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
        print(first_name, last_name, username, email, password1, password2)

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords don't match.")
            return redirect("customer_register")

        # Check for empty fields
        if not (first_name and last_name and username and email and password1):
            messages.error(request, "All fields are required.")
            return redirect("customer_register")

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("customer_register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("customer_register")

        try:
            # Create user and customer profile
            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            user.set_password(password1)
            user.is_active = False  # User will be inactive until email confirmation
            user.save()

            Customer.objects.create(user=user)

            # Generate email confirmation link
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = request.build_absolute_uri(
                reverse("customer_activate", kwargs={"uid64": uid, "token": token})
            )
            email_subject = "Confirm Your Email"
            email_body = render_to_string(
                "send_mail.html", {"confirm_link": confirm_link}
            )
            print(token, uid)
            print(confirm_link)

            # Send confirmation email
            messages.success(
                request, "Registration successful! Please check your email to confirm."
            )
            email = EmailMultiAlternatives(email_subject, "", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return redirect("customer_register_verify")

        except Exception as e:
            messages.error(
                request, "An error occurred during registration. Please try again."
            )
            return redirect("customer_register")

    return render(request, "register.html")


def register_verify(request):
    return render(request, "register_verify.html")


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

                email = EmailMultiAlternatives(
                    email_subject, "", to=[request.user.email]
                )
                email.attach_alternative(email_body, "text/html")
                email.send()
            except Exception as e:
                messages.error(request, "Email Verification Failed. Please try again.")
                return redirect("home_page")

        messages.error(request, "Invalid Credintials")
        return redirect("customer_login")
    return render(request, "login.html")


@login_required(login_url="customer_login")
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
    return redirect("customer_login")


@login_required(login_url="customer_login")
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
