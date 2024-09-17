from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Cart, CartItem
from product.models import Product


# View for displaying the customer's cart
def customer_cart(request):
    user = request.user
    if user.is_authenticated:
        cart = get_object_or_404(Cart, customer__user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_total_price = sum(item.total_price for item in cart_items)
        return render(
            request, "cart.html", {"carts": cart_items, "total_price": cart_total_price}
        )
    return render(request, "cart.html")


def increase_product(request, product_id):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, "You need to be logged in to modify the cart.")
        return redirect("login")

    cart = get_object_or_404(Cart, customer__user=user)
    product = get_object_or_404(Product, id=product_id)

    # Check if the product exists in the cart
    cart_item = cart.items.filter(product=product).first()
    if cart_item:
        # Increase the quantity of the product in the cart
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Product quantity increased.")
    else:
        # Add the product to the cart if it's not already present
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        messages.success(request, "Product added to cart.")

    return redirect("customer_cart")


def decrease_product(request, product_id):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, "You need to be logged in to modify the cart.")
        return redirect("login")

    cart = get_object_or_404(Cart, customer__user=user)
    product = get_object_or_404(Product, id=product_id)

    # Check if the product exists in the cart
    cart_item = cart.items.filter(product=product).first()
    if cart_item:
        # Increase the quantity of the product in the cart
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, "Product quantity increased.")
    else:
        # Add the product to the cart if it's not already present
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        messages.success(request, "Product added to cart.")

    return redirect("customer_cart")
