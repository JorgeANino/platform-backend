from django.db import models
from django.db import models


class Product(models.Model):
    # Choices for category field
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    FOOD = "Food"

    CATEGORY_CHOICES = (
        (ELECTRONICS, ELECTRONICS),
        (CLOTHING, CLOTHING),
        (FOOD, FOOD)
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)

    def __str__(self) -> str:
        return self.name
