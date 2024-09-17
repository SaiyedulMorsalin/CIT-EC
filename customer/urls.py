from django.urls import path
from . import views

urlpatterns = [
    path("login", views.user_login, name="customer_login"),
    path("register", views.register, name="customer_register"),
    path("register/verify/", views.register_verify, name="customer_register_verify"),
    path("logout", views.user_logout, name="customer_logout"),
    path("activate<str:uid64>/<str:token>/", views.activate, name="customer_activate"),
]
