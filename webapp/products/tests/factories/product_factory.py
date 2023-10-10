import factory
from webapp.products.models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Test Product {n}")
    description = factory.Faker("sentence")
    price = factory.Faker("pydecimal", left_digits=3,
                          right_digits=2, positive=True)
    quantity = factory.Faker("random_int", min=1, max=100)
    category = factory.Faker("word")
