import random

from django.core.management.base import BaseCommand, CommandError

from faker import Faker

from webapp.products.models import Product


class Command(BaseCommand):
    help = "Generate random test products"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=1,
                            help="Number of products to create")

    def handle(self, *args, **options):
        count = options["count"]
        categories = [Product.ELECTRONICS, Product.CLOTHING, Product.FOOD]

        # Initialize faker
        fake = Faker()

        for _ in range(count):
            name = fake.name()
            description = fake.text()
            # random price between 10 and 1000
            price = round(random.uniform(10, 1000), 2)
            # random quantity between 1 and 100
            quantity = random.randint(1, 100)
            category = random.choice(categories)

            try:
                product = Product(name=name, description=description,
                                  price=price, quantity=quantity, category=category)
                product.save()
            except Exception as e:
                raise CommandError(f"Error creating product: {e}")

        self.stdout.write(self.style.SUCCESS(
            f"Successfully created {count} test product(s) using Faker."))
