from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.customer_cart, name="customer_cart"),
    path("product/add/<int:product_id>/", views.increase_product, name="product_add"),
    path(
        "product/remove/<int:product_id>/",
        views.increase_product,
        name="product_remove",
    ),
]
