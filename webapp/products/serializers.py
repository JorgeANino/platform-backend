from rest_framework import serializers

from webapp.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_quantity(self, value):
        """Check that the quantity is a positive integer."""
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be a positive integer.")
        return value

    def validate_price(self, value):
        """Check that the price is a positive decimal number"""
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be a positive value.")
        return value

    def create(self, validated_data):
        """Create a Product"""
        return Product.objects.create(
            **validated_data
        )

    def update(self, instance, validated_data):
        """Update a Product"""
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        instance.save()
        return instance

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "quantity",
            "category",
            "price"
        ]
