from django.db import models
from customer.models import Customer
from product.models import Product
# Create your models here.
class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Wishlist Item: {self.product.name}"